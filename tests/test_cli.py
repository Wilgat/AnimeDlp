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


def test_TP_CLI_02_missing_url_help_when_not_a_terminal(capsys):
    """TP-CLI-02: no URL and no terminal → help, exit 0. Not install-ensure."""
    with mock.patch.object(sys.stdout, "isatty", return_value=False):
        code = main([])
    assert code == 0
    captured = capsys.readouterr()
    assert "text menu" in captured.out
    assert "url" in captured.out


def test_TP_CLI_04_bare_terminal_opens_menu():
    """A terminal with no URL opens the text menu and does not require a URL."""
    with mock.patch.object(sys.stdout, "isatty", return_value=True), mock.patch(
        "AnimeDlp.cli.Tui.open_text_menu", return_value=None
    ) as open_menu:
        code = main([])
    assert code == 0
    open_menu.assert_called_once()


def test_TP_CLI_04_debug_without_url_opens_menu():
    """--debug with no URL still opens the text menu."""
    with mock.patch.object(sys.stdout, "isatty", return_value=True), mock.patch(
        "AnimeDlp.cli.Tui.open_text_menu", return_value=None
    ) as open_menu:
        code = main(["--debug"])
    assert code == 0
    open_menu.assert_called_once()


def test_TP_CLI_05_url_does_not_open_menu():
    """A page URL stays on the terminal downloader."""
    with mock.patch.object(sys.stdout, "isatty", return_value=True), mock.patch(
        "AnimeDlp.cli.Tui.open_text_menu"
    ) as open_menu, mock.patch("AnimeDlp.cli.Anime1Downloader") as downloader:
        downloader.return_value.run.return_value = 0
        code = main(["https://anime1.me/x"])
    assert code == 0
    open_menu.assert_not_called()
    downloader.assert_called_once()


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
