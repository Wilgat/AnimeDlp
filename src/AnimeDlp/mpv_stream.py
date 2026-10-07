"""Play one extracted media URL in mpv. This path does not save a file."""

from __future__ import annotations

import shutil
import subprocess


class MpvStream:
    """Detect an mplayer2-lineage mpv and hand it one media URL.

    Detection runs ``mpv --version`` once. The row is offered only when that
    text contains ``mplayer2``. Playback passes the extracted URL, the same
    referer, user agent, and ``e``/``h``/``p`` cookie subset the downloader
    uses. There is no output template and no YoutubeDL call.
    """

    def __init__(self, logger=None, available=None, runner=None, which=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="MpvStream")
        self._runner = runner
        self._which = which
        self._binary = None
        self._available = available

    def available(self) -> bool:
        """True when ``mpv`` is on PATH and its version text names mplayer2."""
        if self._available is None:
            self._available = self._probe()
        return bool(self._available)

    def _probe(self) -> bool:
        finder = self._which or shutil.which
        path = finder("mpv")
        if not path:
            return False
        runner = self._runner or subprocess.run
        try:
            completed = runner(
                [path, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        text = ""
        if completed is not None:
            text = "{0}\n{1}".format(
                getattr(completed, "stdout", "") or "",
                getattr(completed, "stderr", "") or "",
            )
        if "mplayer2" not in text.lower():
            return False
        self._binary = path
        return True

    @staticmethod
    def referer_for(page_url: str) -> str:
        """Page-family referer. A CDN host is not the page host."""
        if page_url and "anime1.pw" in page_url and "anime1.me" not in page_url:
            return "https://anime1.pw/"
        return "https://anime1.me/"

    @staticmethod
    def cookie_header(cookie) -> str:
        """Playback names only. The rest of the jar stays out of the header."""
        if not isinstance(cookie, dict):
            return ""
        parts = []
        for key in ("e", "h", "p"):
            value = cookie.get(key)
            if value is None or value == "":
                continue
            parts.append("{0}={1}".format(key, value))
        return "; ".join(parts)

    def command(self, media_url, title, page_url, user_agent, cookie=None) -> list:
        """argv for one stream. No output path, so mpv does not save a file."""
        binary = self._binary or "mpv"
        safe_title = (title or "video").replace("\n", " ").replace("\r", " ").strip()
        if not safe_title:
            safe_title = "video"
        cmd = [
            binary,
            "--no-ytdl",
            "--force-media-title={0}".format(safe_title),
            "--title={0}".format(safe_title),
            "--referrer={0}".format(self.referer_for(page_url)),
        ]
        if user_agent:
            cmd.append("--user-agent={0}".format(user_agent))
        header = self.cookie_header(cookie)
        if header:
            cmd.append("--http-header-fields=Cookie: {0}".format(header))
        cmd.append(media_url)
        return cmd

    def play(self, media_url, title, page_url, user_agent, cookie=None):
        """Block until mpv exits. Returns (ok, message). Does not write a file."""
        if not self.available():
            return False, "mpv is not an mplayer2 build"
        if not self._binary:
            finder = self._which or shutil.which
            self._binary = finder("mpv") or "mpv"
        cmd = self.command(media_url, title, page_url, user_agent, cookie)
        if self.logger is not None:
            self.logger.log_message(
                "Streaming → {0}".format(title),
                level="INFO",
                component="menu",
            )
        runner = self._runner or subprocess.run
        try:
            if runner is subprocess.run:
                completed = runner(cmd, check=False)
            else:
                completed = runner(cmd)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, "mpv could not start: {0}".format(exc)
        code = getattr(completed, "returncode", 0)
        if code not in (0, None):
            return False, "mpv exited {0} for {1}".format(code, title)
        return True, "Played {0}".format(title)
