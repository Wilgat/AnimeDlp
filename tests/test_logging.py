"""Logging proofs for the process entry. TP-LOG-01 and TP-LOG-02."""

import os
from pathlib import Path

from AnimeDlp.cli import main


def _quiet_env(monkeypatch):
    monkeypatch.delenv("DEBUG", raising=False)
    monkeypatch.delenv("debug", raising=False)


def _log_text(logdir: Path) -> str:
    files = sorted(logdir.glob("anime-dlp-*.log"))
    assert files, "daily log was not written"
    return files[-1].read_text(encoding="utf-8", errors="replace")


def test_TP_LOG_01_main_constructs_logger_in_the_scratch_folder(tmp_path, capsys, monkeypatch):
    """TP-LOG-01: one construct in main. Names read back. Resolved name is anime-dlp."""
    _quiet_env(monkeypatch)
    base = tmp_path / "base"
    logs = tmp_path / "logs"
    code = main(["--version"], basedir=str(base), logdir=str(logs))
    assert code == 0
    names = sorted(logs.glob("anime-dlp-*.log"))
    assert names, "daily log was not written under the supplied logdir"
    text = names[-1].read_text(encoding="utf-8", errors="replace")
    assert "instantiated" in text
    assert "@Cli" in text or "Cli" in text
    captured = capsys.readouterr()
    assert "debug mode" not in captured.out
    assert "debug mode" not in text


def test_TP_LOG_02_debug_lines_on_a_non_screen_run(tmp_path, capsys, monkeypatch):
    """TP-LOG-02: DEBUG already on shows the identity lines and debug mode."""
    _quiet_env(monkeypatch)
    monkeypatch.setenv("DEBUG", "1")
    logs = tmp_path / "logs"
    code = main(["--version"], basedir=str(tmp_path / "base"), logdir=str(logs))
    assert code == 0
    captured = capsys.readouterr()
    text = _log_text(logs)
    for line in ("debug mode", "Using ", "Base "):
        assert line in captured.out
        assert line in text


def test_TP_LOG_02_text_screen_keeps_debug_off_the_console(tmp_path, capsys, monkeypatch):
    """A text-screen run does not mirror debug mode. The daily file still receives it."""
    _quiet_env(monkeypatch)
    monkeypatch.setenv("DEBUG", "show")
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    monkeypatch.setattr("AnimeDlp.cli.Tui.open_text_menu", lambda self: None)
    logs = tmp_path / "logs"
    code = main([], basedir=str(tmp_path / "base"), logdir=str(logs))
    assert code == 0
    captured = capsys.readouterr()
    text = _log_text(logs)
    assert "debug mode" not in captured.out
    assert "debug mode" in text
    assert os.environ["DEBUG"] == "show"
