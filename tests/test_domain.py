"""Domain tests — TP-ANIMEDLP-* (mocked; no public network)."""

import argparse
from unittest import mock

import pytest

from AnimeDlp.cli import Anime1Downloader


def _args(**kwargs):
    base = dict(
        url="https://anime1.me/series/demo",
        verbose=False,
        extract=True,
        cloudflare=None,
        user_agent=None,
    )
    base.update(kwargs)
    return argparse.Namespace(**base)


def test_TP_ANIMEDLP_01_unsupported_host_message():
    """TP-ANIMEDLP-01: unsupported host rejects."""
    args = _args(url="https://not-supported.example/x")
    logger = mock.Mock()
    with pytest.raises(SystemExit) as ei:
        Anime1Downloader(args, logger).run()
    assert ei.value.code == 1


def test_TP_ANIMEDLP_02_extract_mode_skips_download():
    """TP-ANIMEDLP-02: --extract prints without calling download_video."""
    args = _args(url="https://anime1.me/series/demo", extract=True)
    logger = mock.Mock()
    dl = Anime1Downloader(args, logger)
    fake_items = [("Ep 1", "https://cdn.example/v.mp4", {"e": "1", "h": "2", "p": "3"})]
    with mock.patch.object(dl, "extract_anime1_me", return_value=fake_items):
        with mock.patch.object(dl, "download_video") as dl_dl:
            with mock.patch("builtins.print") as pr:
                dl.run()
            dl_dl.assert_not_called()
            printed = " ".join(str(c) for c in pr.call_args_list)
            assert "Ep 1" in printed
            assert "https://cdn.example/v.mp4" in printed


def test_TP_ANIMEDLP_03_detects_anime1_pw_route():
    """TP-ANIMEDLP-03: anime1.pw URL routes to pw extractor."""
    args = _args(url="https://anime1.pw/123", extract=True)
    logger = mock.Mock()
    dl = Anime1Downloader(args, logger)
    with mock.patch.object(dl, "extract_anime1_pw", return_value=[("T", "https://x/v.m3u8")]) as ex:
        with mock.patch.object(dl, "download_video") as dl_dl:
            with mock.patch("builtins.print"):
                dl.run()
            ex.assert_called_once()
            dl_dl.assert_not_called()
