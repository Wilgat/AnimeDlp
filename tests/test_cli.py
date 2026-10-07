"""CLI tests — TP-CLI-* (no public network)."""

import argparse
import sys
from unittest import mock

import pytest

from AnimeDlp.cli import Anime1Downloader, main
from AnimeDlp.errors import AnimeDlpError


def test_TP_CLI_01_help_lists_domain_flags(capsys):
    """TP-CLI-01: --help lists extract / cloudflare / user-agent / verbose / mpv / --id."""
    with mock.patch.object(sys, "argv", ["anime-dlp", "--help"]):
        code = main()
    assert code == 0
    captured = capsys.readouterr()
    assert "mpv" in captured.out
    assert "--id" in captured.out
    assert "--extract" in captured.out


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


def _mpv_main(argv, items, available=True, play_result=(True, "Played First")):
    """Run the mpv verb with a stand-in player and a stand-in extract."""
    player = mock.Mock()
    player.available.return_value = available
    player.play.return_value = play_result
    downloader = mock.Mock()
    downloader.list_sources.return_value = items
    downloader.headers = {"User-Agent": "UA"}
    downloader.run.return_value = 0
    with mock.patch.object(sys.stdout, "isatty", return_value=True), mock.patch(
        "AnimeDlp.cli.Tui.open_text_menu"
    ) as menu, mock.patch(
        "AnimeDlp.cli.MpvStream", return_value=player
    ), mock.patch(
        "AnimeDlp.cli.Anime1Downloader", return_value=downloader
    ):
        code = main(argv)
    return code, menu, player, downloader


_TWO = [
    ("First", "https://cdn.example/1.mp4", None),
    ("Second", "https://cdn.example/2.mp4", {"p": "9"}),
]


def test_TP_CLI_06_mpv_default_id_plays_the_first_video(capsys):
    """TP-CLI-06: omitted --id is 1. Several videos stream that one. No menu, no file."""
    code, menu, player, downloader = _mpv_main(
        ["mpv", "https://anime1.me/show"], _TWO
    )
    assert code == 0
    menu.assert_not_called()
    downloader.run.assert_not_called()
    player.play.assert_called_once_with(
        "https://cdn.example/1.mp4",
        "First",
        "https://anime1.me/show",
        "UA",
        None,
    )
    assert "Played First" in capsys.readouterr().out


def test_TP_CLI_06_mpv_id_selects_that_video():
    """TP-CLI-06: --id 2 streams the second extracted video."""
    code, menu, player, downloader = _mpv_main(
        ["mpv", "https://anime1.pw/show", "--id", "2"],
        _TWO,
        play_result=(True, "Played Second"),
    )
    assert code == 0
    menu.assert_not_called()
    downloader.run.assert_not_called()
    media, title, page, agent, cookie = player.play.call_args[0]
    assert media == "https://cdn.example/2.mp4"
    assert title == "Second"
    assert page == "https://anime1.pw/show"
    assert agent == "UA"
    assert cookie == {"p": "9"}


def test_TP_CLI_06_one_video_uses_id_1():
    """One video and no --id streams that video."""
    only = [("Only", "https://cdn.example/only.mp4", {"e": "1"})]
    code, _menu, player, downloader = _mpv_main(
        ["mpv", "https://anime1.me/one"], only, play_result=(True, "Played Only")
    )
    assert code == 0
    downloader.run.assert_not_called()
    player.play.assert_called_once_with(
        "https://cdn.example/only.mp4",
        "Only",
        "https://anime1.me/one",
        "UA",
        {"e": "1"},
    )


def test_TP_CLI_06_missing_mpv_does_not_parse(capsys):
    """mpv must exist and name mplayer2 before the page is parsed."""
    code, menu, player, downloader = _mpv_main(
        ["mpv", "https://anime1.me/show"], _TWO, available=False
    )
    assert code == 1
    menu.assert_not_called()
    downloader.list_sources.assert_not_called()
    player.play.assert_not_called()
    err = capsys.readouterr().err
    assert "mplayer2" in err
    assert "Next:" in err


def test_TP_CLI_06_id_past_the_list_does_not_play(capsys):
    """--id beyond the extracted list exits 1 and does not start mpv."""
    code, _menu, player, downloader = _mpv_main(
        ["mpv", "--id", "3", "https://anime1.me/show"], _TWO
    )
    assert code == 1
    downloader.run.assert_not_called()
    player.play.assert_not_called()
    err = capsys.readouterr().err
    assert "Video 3" in err
    assert "Next:" in err


def test_TP_CLI_06_id_below_one(capsys):
    """--id 0 is rejected before extract."""
    code, _menu, player, downloader = _mpv_main(
        ["mpv", "https://anime1.me/show", "--id", "0"], _TWO
    )
    assert code == 1
    downloader.list_sources.assert_not_called()
    player.play.assert_not_called()
    assert "--id must be 1 or greater" in capsys.readouterr().err


def test_TP_CLI_06_id_without_the_verb_does_not_open_the_menu(capsys):
    """--id is only for mpv. It does not open the menu and does not download."""
    with mock.patch.object(sys.stdout, "isatty", return_value=True), mock.patch(
        "AnimeDlp.cli.Tui.open_text_menu"
    ) as menu, mock.patch("AnimeDlp.cli.Anime1Downloader") as downloader:
        code = main(["--id", "1"])
    assert code == 1
    menu.assert_not_called()
    downloader.assert_not_called()
    assert "--id is only for mpv" in capsys.readouterr().err


def test_TP_CLI_06_mpv_without_a_url(capsys):
    """The mpv verb needs a page URL and does not open the menu."""
    with mock.patch.object(sys.stdout, "isatty", return_value=True), mock.patch(
        "AnimeDlp.cli.Tui.open_text_menu"
    ) as menu, mock.patch("AnimeDlp.cli.MpvStream") as player:
        code = main(["mpv"])
    assert code == 1
    menu.assert_not_called()
    player.assert_not_called()
    assert "mpv needs a page URL" in capsys.readouterr().err


def test_TP_CLI_06_unsupported_host_on_the_verb(capsys):
    """A host outside anime1.me and anime1.pw fails closed and does not play."""
    player = mock.Mock()
    player.available.return_value = True
    downloader = mock.Mock()
    downloader.list_sources.side_effect = AnimeDlpError(
        "URL must be from anime1.me or anime1.pw"
    )
    downloader.headers = {"User-Agent": "UA"}
    with mock.patch.object(sys.stdout, "isatty", return_value=False), mock.patch(
        "AnimeDlp.cli.MpvStream", return_value=player
    ), mock.patch("AnimeDlp.cli.Anime1Downloader", return_value=downloader):
        code = main(["mpv", "https://example.com/show"])
    assert code == 1
    player.play.assert_not_called()
    downloader.run.assert_not_called()
    assert "anime1.me" in capsys.readouterr().err


def test_TP_CLI_06_explicit_id_before_the_url():
    """--id=1 before the page URL still selects the first video."""
    code, _menu, player, _downloader = _mpv_main(
        ["mpv", "--id=1", "https://anime1.me/show"], _TWO
    )
    assert code == 0
    assert player.play.call_args[0][1] == "First"
