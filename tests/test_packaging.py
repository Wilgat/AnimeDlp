"""Packaging tests — TP-PKG-*"""

import re
from pathlib import Path

import AnimeDlp
from AnimeDlp import __version__


ROOT = Path(__file__).resolve().parents[1]


def _pyproject_version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'(?m)^version\s*=\s*"([^"]+)"', text)
    assert m, "TP-PKG-02: version not found in pyproject.toml"
    return m.group(1)


def test_TP_PKG_01_console_script_declared():
    """TP-PKG-01: console script anime-dlp → AnimeDlp.cli:main."""
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'anime-dlp = "AnimeDlp.cli:main"' in text, "TP-PKG-01 missing console script"


def test_TP_PKG_01_main_export():
    """TP-PKG-01: package exports main entry."""
    from AnimeDlp import main

    assert callable(main)


def test_TP_PKG_02_version_align():
    """TP-PKG-02: pyproject version == __version__; CLI uses package SSOT (no triple)."""
    assert _pyproject_version() == AnimeDlp.__version__, (
        f"TP-PKG-02 mismatch: pyproject={_pyproject_version()!r} "
        f"__version__={AnimeDlp.__version__!r}"
    )
    # ADLP-VER-02: no parallel MAJOR/MINOR/PATCH constants on downloader
    from AnimeDlp.downloader import Anime1Downloader
    from AnimeDlp import cli as cli_mod

    assert not hasattr(Anime1Downloader, "MAJOR_VERSION")
    assert not hasattr(cli_mod, "MAJOR_VERSION")
    # main source references __version__
    cli_src = (ROOT / "src" / "AnimeDlp" / "cli.py").read_text(encoding="utf-8")
    assert "__version__" in cli_src
    assert "MAJOR_VERSION" not in cli_src


def test_TP_PKG_03_description_honest():
    """TP-PKG-03: packaging description describes anime downloader (not unrelated editor)."""
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "boomerang" not in text.lower()
    assert "anime" in text.lower() or "downloader" in text.lower()
