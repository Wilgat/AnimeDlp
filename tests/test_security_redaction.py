"""Security / privacy — TP-SEC-* (mocked; no public network)."""

import argparse
from unittest import mock

from AnimeDlp.cli import Anime1Downloader
from AnimeDlp.util import redact_cookie_map


def test_TP_SEC_01_verbose_api_logs_redacted_cookies():
    """TP-SEC-01: verbose API path logs redacted cookies, not full values."""
    args = argparse.Namespace(
        url="https://anime1.me/x",
        verbose=True,
        extract=False,
        cloudflare=None,
        user_agent=None,
        output_dir=None,
        show_cookies=False,
    )
    logger = mock.Mock()
    dl = Anime1Downloader(args, logger)

    class FakeResp:
        content = b'{"s":[{"src":"//cdn/v.mp4"}]}'

    class FakeCookie:
        def __init__(self, name, value):
            self.name = name
            self.value = value

    session = mock.Mock()
    session.post.return_value = FakeResp()
    session.cookies = [
        FakeCookie("e", "supersecrettoken"),
        FakeCookie("h", "hhhhhhhh"),
        FakeCookie("p", "pppppppp"),
    ]
    dl.session = session
    dl.me_extractor.session = session

    src, cookie = dl.me_extractor._get_anime1_me_source("apireq")
    assert src
    assert cookie["e"] == "supersecrettoken"  # returned for download use
    joined = " ".join(str(c) for c in logger.log_message.call_args_list)
    assert "supersecrettoken" not in joined
    assert "redacted" in joined.lower() or "…" in joined or "len=" in joined


def test_redact_cookie_map_helper():
    red = redact_cookie_map({"e": "abcdef"})
    assert red["e"] != "abcdef"
    assert "len=" in red["e"] or "…" in red["e"] or red["e"] == "****"
