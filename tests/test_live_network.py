"""Optional live / HTTP integration — TP-ANIMEDLP-04, TP-YTDLP-04.

Core stays offline. TP-ANIMEDLP-04 is opt-in public HTTP (ANIMEDLP_LIVE_NET=1).
TP-YTDLP-04 proves the download service over loopback HTTP (no public network).
"""

from __future__ import annotations

import argparse
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

import pytest

from AnimeDlp.cli import Anime1Downloader
from AnimeDlp.errors import AnimeDlpError

# Minimal ISO-BMFF so yt-dlp generic HTTP can save a clip.
_MINI_MP4 = (
    b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom"
    b"\x00\x00\x00\x08free"
    b"\x00\x00\x00\x08mdat"
)


def _args(**kwargs):
    base = dict(
        url="https://anime1.me/series/demo",
        verbose=False,
        extract=True,
        cloudflare=None,
        user_agent="AnimeDlp-live-test/1.5.2",
        output_dir=None,
        show_cookies=False,
    )
    base.update(kwargs)
    return argparse.Namespace(**base)


class _ClipHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?", 1)[0] != "/clip.mp4":
            self.send_error(404)
            return
        body = _MINI_MP4
        self.send_response(200)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        return


def test_TP_ANIMEDLP_04_live_http_extract():
    """TP-ANIMEDLP-04: live HTTP extract against a real supported host (opt-in)."""
    if os.environ.get("ANIMEDLP_LIVE_NET") != "1":
        pytest.skip("optional live network; set ANIMEDLP_LIVE_NET=1")
    url = (os.environ.get("ANIMEDLP_LIVE_URL") or "").strip()
    if not url:
        pytest.skip("set ANIMEDLP_LIVE_URL to an anime1.me or anime1.pw URL")

    args = _args(url=url, extract=True)
    logger = mock.Mock()
    dl = Anime1Downloader(args, logger)
    try:
        if "anime1.me" in url.lower():
            items = dl.extract_anime1_me(url)
        elif "anime1.pw" in url.lower():
            items = dl.extract_anime1_pw(url)
        else:
            pytest.fail("ANIMEDLP_LIVE_URL must be anime1.me or anime1.pw")
    except AnimeDlpError as exc:
        if "Cloudflare" in str(exc):
            pytest.skip(f"live host blocked: {exc}")
        raise

    assert items, "live extract returned no videos"
    title, src = items[0][0], items[0][1]
    assert title
    assert src.startswith("http")


def test_TP_YTDLP_04_integration_download_http_fixture(tmp_path):
    """TP-YTDLP-04: integration download of a short HTTP fixture (loopback)."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), _ClipHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address
        media = f"http://{host}:{port}/clip.mp4"
        args = _args(url="https://anime1.me/x", extract=False, output_dir=str(tmp_path))
        dl = Anime1Downloader(args, mock.Mock())
        ok = dl.download_video("live-fixture", media, None)
        assert ok is True
        written = list(Path(tmp_path).glob("live-fixture.*"))
        assert written, "download wrote no file"
        assert written[0].stat().st_size > 0
    finally:
        server.shutdown()
        server.server_close()
