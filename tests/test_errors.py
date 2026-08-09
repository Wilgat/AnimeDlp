"""Error-handling tests — TP-ERR-* (mocked; no public network)."""

import argparse
from unittest import mock

import pytest

from AnimeDlp.cli import Anime1Downloader


def test_TP_ERR_01_unsupported_host():
    """TP-ERR-01: unsupported host → non-zero exit."""
    args = argparse.Namespace(
        url="https://evil.example/",
        verbose=False,
        extract=False,
        cloudflare=None,
        user_agent=None,
    )
    with pytest.raises(SystemExit) as ei:
        Anime1Downloader(args, mock.Mock()).run()
    assert ei.value.code == 1


def test_TP_ERR_02_download_failure_logs_error():
    """TP-ERR-02: yt-dlp exception logs ERROR for title (no claim of success)."""
    args = argparse.Namespace(
        url="https://anime1.me/x",
        verbose=False,
        extract=False,
        cloudflare=None,
        user_agent=None,
    )
    logger = mock.Mock()
    dl = Anime1Downloader(args, logger)

    class BoomYDL:
        def __init__(self, opts):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def download(self, urls):
            raise RuntimeError("network boom")

    with mock.patch("AnimeDlp.cli.yt_dlp.YoutubeDL", BoomYDL):
        dl.download_video("EpX", "https://cdn/v.mp4", None)
    # at least one ERROR-level log
    levels = [c.kwargs.get("level") for c in logger.log_message.call_args_list]
    assert "ERROR" in levels
