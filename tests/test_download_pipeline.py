"""Download pipeline tests — TP-YTDLP-* (mocked; no public network)."""

import argparse
from unittest import mock

from AnimeDlp.cli import Anime1Downloader


def _dl(**kwargs):
    args = argparse.Namespace(
        url="https://anime1.me/x",
        verbose=False,
        extract=False,
        cloudflare=None,
        user_agent="TestAgent/1.0",
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

    with mock.patch("AnimeDlp.cli.yt_dlp.YoutubeDL", FakeYDL):
        dl.download_video("Title", "https://v.example/a.mp4", {"e": "E", "h": "H", "p": "P", "extra": "X"})
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
    )
    dl = Anime1Downloader(args, mock.Mock())
    with mock.patch.object(
        dl, "extract_anime1_me", return_value=[("T", "https://cdn/v.mp4", None)]
    ):
        with mock.patch("AnimeDlp.cli.yt_dlp.YoutubeDL") as YDL:
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

    with mock.patch("AnimeDlp.cli.yt_dlp.YoutubeDL", FakeYDL):
        dl.download_video("A", "https://cdn.anime1.me/x.mp4", None)
        dl.download_video("B", "https://cdn.other/x.mp4", None)
    assert captured["opts"][0]["http_headers"]["Referer"] == "https://anime1.me/"
    assert captured["opts"][1]["http_headers"]["Referer"] == "https://anime1.pw/"
