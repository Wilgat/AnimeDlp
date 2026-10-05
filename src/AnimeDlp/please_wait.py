"""A flashing bullet while videos are being saved.

Each flash redraws one line: the file now being saved, the file total,
the percent finished, and the time until finish. The line is removed
when the downloads return. A stream that is not a terminal is left alone.
"""

import sys
import threading
import time


class DownloadProgress:
    """File counts and byte fraction for the wait line. Safe to update from the downloader thread."""

    def __init__(self):
        self._lock = threading.Lock()
        self.total = 0
        self.current = 0
        self.fraction = 0.0
        self.started = None

    def begin(self, total):
        """Start a job of `total` files. The first file is current. The clock starts now."""
        with self._lock:
            self.total = max(0, int(total))
            self.current = 1 if self.total else 0
            self.fraction = 0.0
            self.started = time.monotonic()

    def start_file(self, index):
        """Move to a 1-based file. The byte fraction of that file starts at zero."""
        with self._lock:
            self.current = max(1, int(index))
            self.fraction = 0.0
            if self.started is None:
                self.started = time.monotonic()

    def set_fraction(self, fraction):
        """How much of the current file is saved, from 0 to 1."""
        with self._lock:
            self.fraction = max(0.0, min(1.0, float(fraction)))

    def note_bytes(self, done, total_bytes):
        """Set the current-file fraction from a byte or fragment count."""
        if not total_bytes:
            return
        self.set_fraction(float(done) / float(total_bytes))

    def snapshot(self):
        """Return current, total, percent finished, and seconds until finish.

        Seconds are None until at least one percent of the whole job is done.
        """
        with self._lock:
            total = self.total
            current = self.current
            fraction = self.fraction
            started = self.started
        if total <= 0:
            return 0, 0, 0, None
        if current <= 0:
            current = 1
        if current > total:
            current = total
        overall = ((current - 1) + fraction) / float(total)
        overall = max(0.0, min(1.0, overall))
        percent = int(overall * 100)
        remaining = None
        if started is not None and overall >= 0.01:
            elapsed = time.monotonic() - started
            remaining = elapsed * (1.0 - overall) / overall
        return current, total, percent, remaining


def apply_ytdlp_event(progress, event):
    """Copy one yt-dlp progress event onto `progress`."""
    status = event.get("status")
    if status == "downloading":
        total = event.get("total_bytes") or event.get("total_bytes_estimate") or 0
        done = event.get("downloaded_bytes") or 0
        if total:
            progress.note_bytes(done, total)
            return
        count = event.get("fragment_count") or 0
        index = event.get("fragment_index") or 0
        if count:
            progress.note_bytes(index, count)
    elif status == "finished":
        progress.set_fraction(1.0)


def format_until_finish(seconds):
    """Time until finish, or `estimating` when the time is not known yet."""
    if seconds is None:
        return "estimating"
    whole = int(round(float(seconds)))
    if whole < 0:
        whole = 0
    minutes, secs = divmod(whole, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes:02d}m {secs:02d}s until finish"
    if minutes:
        return f"{minutes}m {secs:02d}s until finish"
    return f"{secs}s until finish"


def please_wait_line(bullet_on, current=0, total=0, percent=0, remaining_seconds=None):
    """One line. The bullet is drawn, or a space of the same width.

    With a file total the line names `file current/total`, the percent
    finished, and the time until finish. Without a total it names the
    percent and the time only.
    """
    bullet = "•" if bullet_on else " "
    percent = max(0, min(100, int(percent)))
    clock = format_until_finish(remaining_seconds)
    if int(total) > 0:
        shown = max(1, min(int(current), int(total)))
        return f"{bullet} file {shown}/{int(total)}, {percent}% finished, {clock}"
    return f"{bullet} {percent}% finished, {clock}"


class flashing_wait:
    """Rewrite one terminal line until the block ends, then erase it."""

    def __init__(self, stream=None, progress=None):
        self.stream = sys.stderr if stream is None else stream
        self.progress = progress
        self._stop = threading.Event()
        self._thread = None
        self._active = False
        self._width = 0

    def __enter__(self):
        isatty = getattr(self.stream, "isatty", None)
        if not callable(isatty) or not isatty():
            return self
        self._active = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._stop.set()
        if self._thread is not None:
            self._thread.join()
        if self._active:
            self.stream.write("\r" + (" " * self._width) + "\r")
            self.stream.flush()
        return False

    def _line(self, bullet_on):
        if self.progress is None:
            return please_wait_line(bullet_on)
        current, total, percent, remaining = self.progress.snapshot()
        return please_wait_line(bullet_on, current, total, percent, remaining)

    def _loop(self):
        on = True
        while not self._stop.is_set():
            line = self._line(on)
            self._width = max(self._width, len(line))
            padded = line + (" " * (self._width - len(line)))
            self.stream.write("\r" + padded)
            self.stream.flush()
            on = not on
            if self._stop.wait(0.4):
                break
