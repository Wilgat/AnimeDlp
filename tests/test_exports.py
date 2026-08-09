"""Package export honesty — TP-STYLE-01"""

import AnimeDlp


def test_TP_STYLE_01_exports_only_real_symbols():
    """TP-STYLE-01: __all__ symbols exist; no phantom ChronicleLogger re-export."""
    assert "__version__" in AnimeDlp.__all__
    assert "main" in AnimeDlp.__all__
    assert "ChronicleLogger" not in AnimeDlp.__all__
    assert not hasattr(AnimeDlp, "ChronicleLogger") or "ChronicleLogger" not in dir(AnimeDlp)
    from AnimeDlp import main, __version__
    assert callable(main)
    assert isinstance(__version__, str) and __version__
