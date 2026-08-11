"""Error-handling tests — TP-ERR-* (mocked; no public network)."""

import argparse
from unittest import mock

import pytest

from AnimeDlp.cli import Anime1Downloader
from AnimeDlp.errors import AnimeDlpError


def _ns(**kwargs):
    base = dict(
        url="https://anime1.me/x",
        verbose=False,
        extract=False,
        cloudflare=None,
        user_agent=None,
        output_dir=None,
        show_cookies=False,
    )
    base.update(kwargs)
    return argparse.Namespace(**base)


def test_TP_ERR_01_unsupported_host():
    """TP-ERR-01: unsupported host → AnimeDlpError (main maps to exit 1)."""
    with pytest.raises(AnimeDlpError) as ei:
        Anime1Downloader(_ns(url="https://evil.example/"), mock.Mock()).run()
    assert ei.value.exit_code == 1
    assert "anime1" in str(ei.value).lower()


def test_TP_ERR_02_download_failure_logs_error():
    """TP-ERR-02: yt-dlp exception logs ERROR for title (no claim of success)."""
    logger = mock.Mock()
    dl = Anime1Downloader(_ns(), logger)

    class BoomYDL:
        def __init__(self, opts):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def download(self, urls):
            raise RuntimeError("network boom")

    with mock.patch("AnimeDlp.download_service.yt_dlp.YoutubeDL", BoomYDL):
        ok = dl.download_video("EpX", "https://cdn/v.mp4", None)
    assert ok is False
    levels = [c.kwargs.get("level") for c in logger.log_message.call_args_list]
    assert "ERROR" in levels


def test_TP_ERR_03_empty_extract_non_zero():
    """TP-ERR-03: empty extract list → AnimeDlpError (fail closed)."""
    args = _ns(url="https://anime1.me/series/demo", extract=True)
    dl = Anime1Downloader(args, mock.Mock())
    with mock.patch.object(dl, "extract_anime1_me", return_value=[]):
        with pytest.raises(AnimeDlpError) as ei:
            dl.run()
    assert ei.value.exit_code == 1
    assert "no videos" in str(ei.value).lower()


def test_TP_ERR_04_download_failure_run_exits_nonzero():
    """TP-ERR-04: download failure in run() returns exit code 1."""
    args = _ns(url="https://anime1.me/series/demo", extract=False)
    logger = mock.Mock()
    dl = Anime1Downloader(args, logger)
    with mock.patch.object(
        dl, "extract_anime1_me", return_value=[("T", "https://cdn/v.mp4", None)]
    ):
        with mock.patch.object(dl, "download_video", return_value=False):
            code = dl.run()
    assert code == 1
    # must not claim all completed
    msgs = " ".join(str(c) for c in logger.log_message.call_args_list)
    assert "All downloads completed" not in msgs
