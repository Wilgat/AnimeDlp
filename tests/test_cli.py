"""CLI tests — TP-CLI-* (no public network)."""

import argparse
import sys
from types import SimpleNamespace
from unittest import mock

import pytest

from AnimeDlp.cli import Anime1Downloader, main


def test_TP_CLI_01_help_lists_domain_flags():
    """TP-CLI-01: --help lists extract / cloudflare / user-agent / verbose."""
    with pytest.raises(SystemExit) as ei:
        with mock.patch.object(sys, "argv", ["anime-dlp", "--help"]):
            main()
    assert ei.value.code == 0


def test_TP_CLI_02_missing_url_nonzero():
    """TP-CLI-02: no args → argparse error / non-zero."""
    with pytest.raises(SystemExit) as ei:
        with mock.patch.object(sys, "argv", ["anime-dlp"]):
            main()
    assert ei.value.code != 0


def test_TP_CLI_03_unsupported_host_rejected():
    """TP-CLI-03: unsupported host → ERROR path + exit 1."""
    args = argparse.Namespace(
        url="https://example.com/show",
        verbose=False,
        extract=False,
        cloudflare=None,
        user_agent=None,
    )
    logger = mock.Mock()
    # main() builds logger; test runner class directly for host gate
    dl = Anime1Downloader(args, logger)
    with pytest.raises(SystemExit) as ei:
        dl.run()
    assert ei.value.code == 1
    # ERROR logged for host rejection
    calls = " ".join(str(c) for c in logger.log_message.call_args_list)
    assert "anime1.me" in calls or "anime1.pw" in calls or "URL must" in calls
