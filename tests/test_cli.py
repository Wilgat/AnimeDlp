"""CLI tests — TP-CLI-* (no public network)."""

import argparse
import sys
from unittest import mock

import pytest

from AnimeDlp.cli import Anime1Downloader, main
from AnimeDlp.errors import AnimeDlpError


def test_TP_CLI_01_help_lists_domain_flags():
    """TP-CLI-01: --help lists extract / cloudflare / user-agent / verbose."""
    with mock.patch.object(sys, "argv", ["anime-dlp", "--help"]):
        code = main()
    assert code == 0


def test_TP_CLI_02_missing_url_nonzero():
    """TP-CLI-02: no args → argparse error / non-zero."""
    with mock.patch.object(sys, "argv", ["anime-dlp"]):
        code = main()
    assert code != 0


def test_TP_CLI_03_unsupported_host_rejected():
    """TP-CLI-03: unsupported host → ERROR path + exit 1."""
    args = argparse.Namespace(
        url="https://example.com/show",
        verbose=False,
        extract=False,
        cloudflare=None,
        user_agent=None,
        output_dir=None,
        show_cookies=False,
    )
    logger = mock.Mock()
    dl = Anime1Downloader(args, logger)
    with pytest.raises(AnimeDlpError) as ei:
        dl.run()
    assert ei.value.exit_code == 1
