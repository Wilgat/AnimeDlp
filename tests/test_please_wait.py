"""TP-ANIMEDLP-05: the download line names please wait, the file, the percent, and the time until finish."""

import argparse
import io
import sys
import time
from unittest import mock

import pytest

from AnimeDlp.downloader import Anime1Downloader
from AnimeDlp.please_wait import (
    DownloadProgress,
    apply_ytdlp_event,
    flashing_wait,
    format_until_finish,
    please_wait_line,
)

PHRASES = {
    "en": "please wait",
    "zh-Hans": "请稍候",
    "zh-Hant": "請稍候",
    "es": "por favor, espere",
    "ar": "يرجى الانتظار",
    "fr": "veuillez patienter",
    "pt": "aguarde, por favor",
    "ru": "пожалуйста, подождите",
    "de": "bitte warten",
    "ja": "お待ちください",
    "ko": "잠시만 기다려 주세요",
    "nl": "even geduld",
    "el": "παρακαλώ περιμένετε",
}


@pytest.fixture(autouse=True)
def _english_wait_phrase(monkeypatch, tmp_path):
    """Do not read this login’s language leaf. English unless a test sets ANIMEDLP_LANG."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("ANIMEDLP_LANG", raising=False)


class _Tty(io.StringIO):
    def isatty(self):
        return True


def _args(**kwargs):
    base = dict(
        url="https://anime1.me/series",
        verbose=False,
        extract=False,
        cloudflare=None,
        user_agent=None,
        output_dir=None,
        show_cookies=False,
    )
    base.update(kwargs)
    return argparse.Namespace(**base)


def test_TP_ANIMEDLP_05_line_names_file_percent_and_time():
    """The line tells please wait, file current/total, percent finished, and time until finish."""
    assert please_wait_line(True, 2, 5, 40, 65) == (
        "• please wait. file 2/5, 40% finished, 1m 05s until finish"
    )
    assert please_wait_line(False, 2, 5, 40, 65) == (
        "  please wait. file 2/5, 40% finished, 1m 05s until finish"
    )
    on = please_wait_line(True, 2, 5, 40, 65, phrase="please wait")
    off = please_wait_line(False, 2, 5, 40, 65, phrase="please wait")
    assert on[1:] == off[1:]
    assert please_wait_line(True, 1, 5, 0, None) == (
        "• please wait. file 1/5, 0% finished, estimating"
    )
    assert "takes time to finish" not in please_wait_line(True, 2, 5, 40, 65)
    assert format_until_finish(5) == "5s until finish"
    assert format_until_finish(3661) == "1h 01m 01s until finish"
    assert format_until_finish(None) == "estimating"


def test_TP_ANIMEDLP_05_snapshot_percent_and_time_until_finish():
    """Percent counts finished files plus the current file. Time follows that percent."""
    progress = DownloadProgress()
    progress.begin(4)
    progress.start_file(2)
    progress.set_fraction(0.5)
    progress.started = time.monotonic() - 30
    current, total, percent, remaining = progress.snapshot()
    assert (current, total, percent) == (2, 4, 37)
    assert remaining == pytest.approx(50, abs=1)

    fresh = DownloadProgress()
    fresh.begin(4)
    fresh.start_file(1)
    fresh.set_fraction(0.0)
    assert fresh.snapshot()[2] == 0
    assert fresh.snapshot()[3] is None


def test_TP_ANIMEDLP_05_terminal_bullet_flashes_then_is_erased():
    """The bullet toggles, the time is redrawn, and the line is spaces when the job returns."""
    stream = _Tty()
    progress = DownloadProgress()
    progress.begin(1)
    progress.start_file(1)
    progress.set_fraction(0.5)
    progress.started = time.monotonic() - 30
    with flashing_wait(stream, progress):
        time.sleep(0.2)
        progress.started = time.monotonic() - 90
        time.sleep(0.9)
    text = stream.getvalue()
    assert "• please wait. file 1/1, 50% finished, 30s until finish" in text
    assert "  please wait. file 1/1, 50% finished," in text
    assert ("1m 30s until finish" in text or "1m 31s until finish" in text)
    parts = text.split("\r")
    assert parts[-1] == ""
    assert parts[-2].strip() == ""
    assert len(parts[-2]) >= len("• please wait. file 1/1, 50% finished, 30s until finish")


def test_TP_ANIMEDLP_05_quiet_stream_is_unchanged():
    stream = io.StringIO()
    progress = DownloadProgress()
    progress.begin(3)
    with flashing_wait(stream, progress):
        time.sleep(0.05)
    assert stream.getvalue() == ""


def test_TP_ANIMEDLP_05_ytdlp_event_advances_the_current_file():
    """A download event moves the percent. The next file starts again at zero fraction."""
    progress = DownloadProgress()
    progress.begin(2)
    progress.start_file(1)
    apply_ytdlp_event(progress, {
        "status": "downloading",
        "downloaded_bytes": 25,
        "total_bytes": 100,
    })
    assert progress.snapshot()[2] == 12
    apply_ytdlp_event(progress, {"status": "finished"})
    assert progress.snapshot()[2] == 50
    progress.start_file(2)
    apply_ytdlp_event(progress, {
        "status": "downloading",
        "fragment_index": 1,
        "fragment_count": 2,
    })
    assert progress.snapshot()[2] == 75


def test_TP_ANIMEDLP_05_download_installs_the_hook_on_a_terminal(monkeypatch):
    """A terminal download flashes the file line and asks yt-dlp not to draw its own bar."""
    stream = _Tty()
    monkeypatch.setattr(sys, "stderr", stream)
    dl = Anime1Downloader(_args(), mock.Mock())
    seen = []

    def _save(_title, _url, _cookie):
        seen.append(dl.download_service.progress.snapshot()[0])
        time.sleep(0.45)
        return True

    with mock.patch.object(
        dl, "extract_anime1_me", return_value=[
            ("A", "https://cdn/a.mp4", None),
            ("B", "https://cdn/b.mp4", None),
        ]
    ):
        with mock.patch.object(dl, "download_video", side_effect=_save):
            assert dl.run() == 0
    assert seen == [1, 2]
    assert dl.download_service.quiet_native_progress is True
    text = stream.getvalue()
    assert "• please wait. file 1/2, 0% finished, estimating" in text
    assert "  please wait. file 1/2, 0% finished, estimating" in text
    assert "file 2/2, 50% finished," in text
    assert "until finish" in text
    parts = text.split("\r")
    assert parts[-1] == ""
    assert parts[-2].strip() == ""


def test_TP_ANIMEDLP_05_extract_and_pipe_do_not_draw_the_line(monkeypatch):
    """Extract-only and a non-terminal leave stderr alone. yt-dlp keeps its own progress off a terminal."""
    stream = _Tty()
    monkeypatch.setattr(sys, "stderr", stream)
    dl = Anime1Downloader(_args(extract=True), mock.Mock())
    with mock.patch.object(
        dl, "extract_anime1_me", return_value=[("A", "https://cdn/a.mp4", None)]
    ):
        with mock.patch("builtins.print"):
            assert dl.run() == 0
    assert stream.getvalue() == ""

    quiet = io.StringIO()
    monkeypatch.setattr(sys, "stderr", quiet)
    plain = Anime1Downloader(_args(), mock.Mock())
    with mock.patch.object(
        plain, "extract_anime1_me", return_value=[("A", "https://cdn/a.mp4", None)]
    ):
        with mock.patch.object(plain, "download_video", return_value=True):
            assert plain.run() == 0
    assert quiet.getvalue() == ""
    assert plain.download_service.quiet_native_progress is False


def test_TP_ANIMEDLP_05_hook_is_installed_only_with_progress():
    """The byte hook and noprogress are set only when this line owns the screen."""
    dl = Anime1Downloader(_args(), mock.Mock())
    captured = {}

    class FakeYDL:
        def __init__(self, opts):
            captured["opts"] = opts

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def download(self, urls):
            captured["opts"]["progress_hooks"][0]({
                "status": "downloading",
                "downloaded_bytes": 50,
                "total_bytes": 100,
            })

    progress = DownloadProgress()
    progress.begin(2)
    progress.start_file(1)
    dl.download_service.progress = progress
    dl.download_service.quiet_native_progress = True
    with mock.patch("AnimeDlp.download_service.yt_dlp.YoutubeDL", FakeYDL):
        assert dl.download_video("Title", "https://cdn.anime1.me/a.mp4", None) is True
    assert captured["opts"]["noprogress"] is True
    assert progress.snapshot()[2] == 25

    bare = Anime1Downloader(_args(), mock.Mock())
    captured.clear()

    class QuietYDL(FakeYDL):
        def download(self, urls):
            return None

    with mock.patch("AnimeDlp.download_service.yt_dlp.YoutubeDL", QuietYDL):
        assert bare.download_video("Title", "https://cdn.anime1.me/a.mp4", None) is True
    assert "progress_hooks" not in captured["opts"]
    assert "noprogress" not in captured["opts"]


def test_TP_ANIMEDLP_05_please_wait_follows_the_saved_language(monkeypatch, tmp_path):
    """Each saved menu language supplies its own please-wait phrase. The read does not write the leaf."""
    monkeypatch.setenv("HOME", str(tmp_path))
    for code, phrase in PHRASES.items():
        monkeypatch.setenv("ANIMEDLP_LANG", code)
        assert please_wait_line(True, 2, 5, 40, 65) == (
            f"• {phrase}. file 2/5, 40% finished, 1m 05s until finish"
        )
    leaf = tmp_path / ".local" / "AnimeDlp" / "language"
    assert not leaf.exists()
