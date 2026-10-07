"""mpv stream row: mplayer2 detection, one video, and a title list."""

import argparse
from unittest import mock

from AnimeDlp.downloader import Anime1Downloader
from AnimeDlp.mpv_stream import MpvStream
from AnimeDlp.tui import Tui


class _Completed:
    def __init__(self, stdout="", stderr="", code=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = code


def _args(**kwargs):
    base = dict(
        url="https://anime1.me/series/demo",
        verbose=False,
        extract=False,
        cloudflare=None,
        user_agent=None,
        output_dir=None,
        show_cookies=False,
    )
    base.update(kwargs)
    return argparse.Namespace(**base)


def test_version_text_must_name_mplayer2():
    def runner(cmd, **_kwargs):
        return _Completed(
            stdout="mpv 0.37.0 Copyright © 2000-2023 mpv/MPlayer/mplayer2 projects\n"
        )

    player = MpvStream(which=lambda _name: "/usr/bin/mpv", runner=runner)
    assert player.available() is True
    assert player._binary == "/usr/bin/mpv"


def test_missing_mpv_is_not_offered():
    player = MpvStream(which=lambda _name: None, runner=lambda *_a, **_k: None)
    assert player.available() is False


def test_version_without_mplayer2_is_not_offered():
    def runner(cmd, **_kwargs):
        return _Completed(stdout="mpv 0.1.0 custom build\n")

    player = MpvStream(which=lambda _name: "/usr/bin/mpv", runner=runner)
    assert player.available() is False


def test_command_passes_the_media_url_and_does_not_save_a_file():
    player = MpvStream(available=True)
    player._binary = "/usr/bin/mpv"
    cmd = player.command(
        "https://cdn.example/a.mp4",
        "Ep 1",
        "https://anime1.me/watch",
        "UA/1",
        {"e": "1", "h": "2", "p": "3", "other": "no"},
    )
    assert cmd[0] == "/usr/bin/mpv"
    assert cmd[-1] == "https://cdn.example/a.mp4"
    assert "--no-ytdl" in cmd
    assert "--referrer=https://anime1.me/" in cmd
    assert "--user-agent=UA/1" in cmd
    cookie = [part for part in cmd if part.startswith("--http-header-fields=")]
    assert len(cookie) == 1
    assert cookie[0] == "--http-header-fields=Cookie: e=1; h=2; p=3"
    assert not any(
        part == "-o" or part.startswith("--o") or "stream-record" in part or "%(ext)s" in part
        for part in cmd
    )


def test_pw_page_uses_the_pw_referer_and_no_cookie():
    player = MpvStream(available=True)
    cmd = player.command(
        "https://cdn.example/a.m3u8",
        "T",
        "https://anime1.pw/1",
        "UA",
        None,
    )
    assert "--referrer=https://anime1.pw/" in cmd
    assert not any(part.startswith("--http-header-fields=") for part in cmd)


def test_play_runs_mpv_on_the_media_url():
    seen = {}

    def runner(cmd):
        seen["cmd"] = list(cmd)
        return _Completed(code=0)

    player = MpvStream(available=True, runner=runner)
    player._binary = "/usr/bin/mpv"
    ok, message = player.play(
        "https://cdn.example/a.mp4",
        "Ep",
        "https://anime1.me/x",
        "UA",
        None,
    )
    assert ok is True
    assert message == "Played Ep"
    assert seen["cmd"][-1] == "https://cdn.example/a.mp4"
    assert "--no-ytdl" in seen["cmd"]


def test_play_refuses_when_mpv_is_not_mplayer2():
    player = MpvStream(available=False)
    ok, message = player.play(
        "https://cdn.example/a.mp4", "T", "https://anime1.me/x", "UA"
    )
    assert ok is False
    assert "mplayer2" in message


def test_list_sources_does_not_download():
    downloader = Anime1Downloader(_args(), mock.Mock())
    items = [
        ("Ep 1", "https://cdn.example/a.mp4", {"e": "1"}),
        ("Ep 2", "https://cdn.example/b.mp4", None),
    ]
    with mock.patch.object(downloader, "extract_anime1_me", return_value=items):
        with mock.patch.object(downloader, "download_video") as download:
            found = downloader.list_sources()
    download.assert_not_called()
    assert found == items


def test_one_video_plays_without_a_title_list(monkeypatch):
    import curses

    monkeypatch.setattr(curses, "endwin", lambda: None)
    monkeypatch.setattr(curses, "reset_prog_mode", lambda: None)
    monkeypatch.setattr(curses, "doupdate", lambda: None)
    app = mock.Mock()
    app.list_page.return_value = (
        [("Only", "https://cdn.example/only.mp4", {"e": "1", "h": "2"})],
        "UA",
    )
    player = mock.Mock()
    player.available.return_value = True
    player.play.return_value = (True, "Played Only")
    tui = Tui(app=app, player=player)
    text = tui.stream_result("https://anime1.me/one", None, None)
    assert text == "Played Only"
    player.play.assert_called_once_with(
        "https://cdn.example/only.mp4",
        "Only",
        "https://anime1.me/one",
        "UA",
        {"e": "1", "h": "2"},
    )


def test_several_videos_play_the_chosen_title(monkeypatch):
    import curses

    monkeypatch.setattr(curses, "endwin", lambda: None)
    monkeypatch.setattr(curses, "reset_prog_mode", lambda: None)
    monkeypatch.setattr(curses, "doupdate", lambda: None)
    app = mock.Mock()
    app.list_page.return_value = (
        [
            ("First", "https://cdn.example/1.mp4", None),
            ("Second", "https://cdn.example/2.mp4", {"p": "9"}),
        ],
        "UA",
    )
    player = mock.Mock()
    player.available.return_value = True
    player.play.return_value = (True, "Played Second")
    tui = Tui(app=app, player=player)
    tui._read_index = lambda screen, model, lines, count, title="stream": 1
    text = tui.stream_result("https://anime1.pw/show", object(), object())
    assert text == "Played Second"
    media, title, page, agent, cookie = player.play.call_args[0]
    assert media == "https://cdn.example/2.mp4"
    assert title == "Second"
    assert page == "https://anime1.pw/show"
    assert agent == "UA"
    assert cookie == {"p": "9"}


def test_leaving_the_title_list_does_not_play(monkeypatch):
    import curses

    monkeypatch.setattr(curses, "endwin", lambda: None)
    monkeypatch.setattr(curses, "reset_prog_mode", lambda: None)
    monkeypatch.setattr(curses, "doupdate", lambda: None)
    app = mock.Mock()
    app.list_page.return_value = (
        [("A", "https://cdn/a.mp4", None), ("B", "https://cdn/b.mp4", None)],
        "UA",
    )
    player = mock.Mock()
    player.available.return_value = True
    tui = Tui(app=app, player=player)
    tui._read_index = lambda *args, **kwargs: None
    assert tui.stream_result("https://anime1.me/show", object(), object()) is None
    player.play.assert_not_called()
