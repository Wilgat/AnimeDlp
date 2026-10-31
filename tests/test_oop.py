"""Class-map proofs. TP-OOP-01 through TP-OOP-04."""

import inspect
from pathlib import Path

from AnimeDlp import __version__
from AnimeDlp.about_page import AboutPage
from AnimeDlp.check_system import CheckSystem
from AnimeDlp.cli import Cli, main
from AnimeDlp.menu_language import MenuLanguage
from AnimeDlp.menu_model import MenuModel
from AnimeDlp.menu_painter import MenuPainter
from AnimeDlp.menu_session import MenuSession
from AnimeDlp.self_management import SelfManage
from AnimeDlp.system_log import SystemLog
from AnimeDlp.tui import MenuScreenError, Tui

_ROOT = Path(__file__).resolve().parents[1]
_CLI = (_ROOT / "src" / "AnimeDlp" / "cli.py").read_text(encoding="utf-8")


class _Log:
    def __init__(self):
        self.lines = []

    def log_message(self, message, level="INFO", component=""):
        self.lines.append((message, level, component))

    def isDebug(self):
        return False


def _saw(logger, component):
    return any(
        message == "instantiated" and comp == component
        for message, _level, comp in logger.lines
    )


def test_TP_OOP_01_one_class_in_cli_and_main_stays_there():
    """The mapped class files exist. cli.py defines Cli and main only."""
    package = _ROOT / "src" / "AnimeDlp"
    names = [
        "cli.py",
        "tui.py",
        "menu_painter.py",
        "menu_language.py",
        "menu_model.py",
        "menu_session.py",
        "system_log.py",
        "self_management.py",
        "check_system.py",
        "about_page.py",
    ]
    for name in names:
        assert (package / name).is_file()
    assert _CLI.count("\nclass ") == 1
    assert "class Cli" in _CLI
    assert "def main(" in _CLI
    assert inspect.signature(main).parameters.keys() >= {"argv", "basedir", "logdir"}


def test_TP_OOP_02_each_mapped_class_logs_instantiated():
    """Every mapped __init__ takes the logger, stores it, and logs instantiated."""
    logger = _Log()
    classes = {
        "Cli": Cli(logger),
        "Tui": Tui(logger=logger),
        "MenuPainter": MenuPainter(logger=logger),
        "MenuLanguage": MenuLanguage(logger=logger),
        "MenuModel": MenuModel(logger=logger),
        "SystemLog": SystemLog(logger=logger),
        "SelfManage": SelfManage("AnimeDlp", __version__, logger=logger),
        "CheckSystem": CheckSystem(logger=logger),
        "MenuScreenError": MenuScreenError("screen", logger=logger),
    }
    painter = classes["MenuPainter"]
    classes["MenuSession"] = MenuSession(
        "AnimeDlp",
        __version__,
        on_version=lambda: __version__,
        on_about=lambda: "about",
        logger=logger,
        painter=painter,
    )
    classes["AboutPage"] = AboutPage(
        classes["CheckSystem"],
        "AnimeDlp",
        __version__,
        "Wilgat Wong",
        "2026-10-31",
        "https://github.com/Wilgat/AnimeDlp",
        "",
        "anime-dlp <url>",
        "anime-dlp",
        logger=logger,
    )
    for name, obj in classes.items():
        assert obj.logger is logger
        assert _saw(logger, name)


def test_TP_OOP_03_painter_owns_the_frame():
    """Frame glyphs and row tuples live on MenuPainter, not in cli.py."""
    assert MenuPainter.FRAME_TOP_LEFT == "╭"
    assert MenuPainter.MENU_ROWS
    assert MenuPainter.SELF_ROWS
    assert MenuPainter.LOG_ROWS
    assert "FRAME_TOP_LEFT" not in _CLI
    assert "MENU_ROWS" not in _CLI
    assert "SELF_ROWS" not in _CLI
    assert "LOG_ROWS" not in _CLI


def test_TP_OOP_04_identity_constants_live_on_cli():
    """Identity and verb lists are attributes of Cli. Display version is __version__."""
    for name in (
        "APP_NAME",
        "CONSOLE_NAME",
        "PRODUCT_VERBS",
        "LIFECYCLE_VERBS",
        "AUTHOR_NAME",
        "AUTHOR_EMAIL",
        "HOMEPAGE",
        "LAST_UPDATE",
        "DOWNLOAD_URL",
        "BASIC_USAGE",
    ):
        assert hasattr(Cli, name)
    assert Cli.APP_NAME == "AnimeDlp"
    assert Cli.CONSOLE_NAME == "anime-dlp"
    assert "MAJOR" not in _CLI
    assert "MINOR" not in _CLI
    assert "PATCH" not in _CLI
    assert 'fallback "1.1.0"' not in _CLI
    assert __version__
