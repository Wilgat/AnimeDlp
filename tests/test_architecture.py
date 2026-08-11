"""Architecture / L2 class map tests — TP-ARCH-*, TP-CLASS-*."""

import argparse
from unittest import mock

from AnimeDlp.download_service import YtDlpDownloadService
from AnimeDlp.downloader import Anime1Downloader
from AnimeDlp.extractors import Anime1MeExtractor, Anime1PwExtractor
from AnimeDlp.extractors.me import Anime1MeExtractor as MeDirect
from AnimeDlp.extractors.pw import Anime1PwExtractor as PwDirect


def _args(**kwargs):
    base = dict(
        url="https://anime1.me/x",
        verbose=False,
        extract=True,
        cloudflare=None,
        user_agent="TestAgent/1.0",
        output_dir=None,
        show_cookies=False,
    )
    base.update(kwargs)
    return argparse.Namespace(**base)


def test_TP_ARCH_01_l2_module_inventory():
    """TP-ARCH-01: L2 modules importable (cli/coordinator/extractors/download service)."""
    assert Anime1Downloader is not None
    assert Anime1MeExtractor is MeDirect
    assert Anime1PwExtractor is PwDirect
    assert YtDlpDownloadService is not None


def test_TP_CLASS_01_coordinator_composes_collaborators():
    """TP-CLASS-01: Anime1Downloader holds distinct me/pw extractors + download service."""
    dl = Anime1Downloader(_args(), mock.Mock())
    assert isinstance(dl.me_extractor, Anime1MeExtractor)
    assert isinstance(dl.pw_extractor, Anime1PwExtractor)
    assert isinstance(dl.download_service, YtDlpDownloadService)
    # not the same object doing all three jobs as one class type for extractors/download
    assert type(dl.me_extractor) is not type(dl.download_service)
    assert type(dl.pw_extractor) is not type(dl.download_service)


def test_TP_CLASS_02_me_extractor_unit_seam_without_cli():
    """TP-CLASS-02: Me extractor callable without full CLI main()."""
    session = mock.Mock()
    logger = mock.Mock()
    args = _args()
    ex = Anime1MeExtractor(session, args, logger)
    # empty paths → empty list (no CLI)
    with mock.patch.object(ex, "_extract_api_paths", return_value=[]):
        assert ex.extract("https://anime1.me/demo") == []


def test_TP_ARCH_02_download_service_unit_seam():
    """TP-ARCH-02: download service unit-testable without Anime1Downloader.run()."""
    logger = mock.Mock()
    svc = YtDlpDownloadService("UA/1", False, None, logger)
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
        ok = svc.download("Ep", "https://cdn.anime1.me/v.mp4", {"e": "1", "h": "2", "p": "3"})
    assert ok is True
    assert "e=1" in captured["opts"]["http_headers"]["Cookie"]
    assert captured["opts"]["http_headers"]["Referer"] == "https://anime1.me/"
