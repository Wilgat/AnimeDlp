"""Structure tests — TP-STRUCT-*"""

from pathlib import Path

import AnimeDlp


ROOT = Path(__file__).resolve().parents[1]


def test_TP_STRUCT_01_package_layout():
    """TP-STRUCT-01: installable package under src/AnimeDlp with init/main/cli + modules."""
    pkg = ROOT / "src" / "AnimeDlp"
    assert pkg.is_dir(), "TP-STRUCT-01 expected src/AnimeDlp/"
    for name in (
        "__init__.py",
        "__main__.py",
        "cli.py",
        "downloader.py",
        "download_service.py",
        "errors.py",
        "util.py",
        "extractors/__init__.py",
        "extractors/me.py",
        "extractors/pw.py",
    ):
        assert (pkg / name).is_file(), f"TP-STRUCT-01 missing {name}"


def test_TP_STRUCT_01_importable_package():
    """TP-STRUCT-01: package import path is AnimeDlp."""
    assert AnimeDlp.__name__ == "AnimeDlp"
    assert hasattr(AnimeDlp, "__version__")
