"""Runtime prerequisite tests — TP-PRE-* / TP-RT-*"""

import importlib
from pathlib import Path


def test_TP_PRE_02_declared_pip_deps_importable():
    """TP-PRE-02 / TP-RT-01: declared pip deps importable in test env."""
    for mod in ("requests", "bs4", "lxml", "yt_dlp", "ChronicleLogger"):
        importlib.import_module(mod)


def test_TP_PRE_01_no_product_level_ffmpeg_gate():
    """TP-PRE-01: product does not implement ensure_ffmpeg as a hard startup gate."""
    pkg = Path(__file__).resolve().parents[1] / "src" / "AnimeDlp"
    for name in ("cli.py", "downloader.py"):
        src = (pkg / name).read_text(encoding="utf-8")
        assert "def ensure_ffmpeg" not in src

