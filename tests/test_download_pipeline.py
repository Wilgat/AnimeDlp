"""Download pipeline tests — TP-YTDLP-* (mocked; no public network)."""

import argparse
from unittest import mock

from AnimeDlp.cli import Anime1Downloader
from AnimeDlp.util import sanitize_filename


def _dl(**kwargs):
    args = argparse.Namespace(
        url="https://anime1.me/x",
        verbose=False,
        extract=False,
        cloudflare=None,
        user_agent="TestAgent/1.0",
        output_dir=None,
        show_cookies=False,
        **kwargs,
    )
    return Anime1Downloader(args, mock.Mock())


def test_TP_YTDLP_01_cookie_string_only_ehp():
    """TP-YTDLP-01: Cookie header builds only e/h/p keys in stable order."""
    dl = _dl()
    captured = {}

    class FakeYDL:
        def __init__(self, opts):
            captured["opts"] = opts

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def download(self, urls):
            captured["urls"] = urls

    with mock.patch("AnimeDlp.download_service.yt_dlp.YoutubeDL", FakeYDL):
        ok = dl.download_video(
            "Title", "https://v.example/a.mp4", {"e": "E", "h": "H", "p": "P", "extra": "X"}
        )
    assert ok is True
    cookie = captured["opts"]["http_headers"].get("Cookie", "")
    assert "e=E" in cookie and "h=H" in cookie and "p=P" in cookie
    assert "extra" not in cookie


def test_TP_YTDLP_02_extract_mode_never_calls_youtube_dl():
    """TP-YTDLP-02: extract mode never constructs YoutubeDL."""
    args = argparse.Namespace(
        url="https://anime1.me/series/demo",
        verbose=False,
        extract=True,
        cloudflare=None,
        user_agent=None,
        output_dir=None,
        show_cookies=False,
    )
    dl = Anime1Downloader(args, mock.Mock())
    with mock.patch.object(
        dl, "extract_anime1_me", return_value=[("T", "https://cdn/v.mp4", None)]
    ):
        with mock.patch("AnimeDlp.download_service.yt_dlp.YoutubeDL") as YDL:
            with mock.patch("builtins.print"):
                dl.run()
            YDL.assert_not_called()


def test_TP_YTDLP_03_referer_selection_me_vs_pw():
    """TP-YTDLP-03: Referer selects anime1.me vs anime1.pw by media URL."""
    dl = _dl()
    captured = {}

    class FakeYDL:
        def __init__(self, opts):
            captured.setdefault("opts", []).append(opts)

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def download(self, urls):
            pass

    with mock.patch("AnimeDlp.download_service.yt_dlp.YoutubeDL", FakeYDL):
        dl.download_video("A", "https://cdn.anime1.me/v.mp4", None)
        dl.download_video("B", "https://cdn.anime1.pw/v.m3u8", None)
    assert captured["opts"][0]["http_headers"]["Referer"] == "https://anime1.me/"
    assert captured["opts"][1]["http_headers"]["Referer"] == "https://anime1.pw/"


def test_TP_YTDLP_05_unsafe_title_sanitized_in_outtmpl():
    """TP-YTDLP-05: path separators in title sanitized in outtmpl."""
    dl = _dl()
    captured = {}

    class FakeYDL:
        def __init__(self, opts):
            captured["opts"] = opts

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def download(self, urls):
            pass

    dirty = "../evil/name/with spaces"
    with mock.patch("AnimeDlp.download_service.yt_dlp.YoutubeDL", FakeYDL):
        dl.download_video(dirty, "https://cdn/v.mp4", None)
    outtmpl = captured["opts"]["outtmpl"]
    assert ".." not in outtmpl
    assert "/" not in outtmpl.replace("%(ext)s", "mp4")
    assert sanitize_filename(dirty) in outtmpl
