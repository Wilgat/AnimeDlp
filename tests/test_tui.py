"""Text menu tests — front board, pasted URL, invalid choice, TP-TUI-10. No curses screen."""

import curses
import re
from pathlib import Path

from AnimeDlp.menu_model import MenuModel
from AnimeDlp.menu_painter import MenuPainter


def _painter(tmp_path):
    return MenuPainter(home=str(tmp_path))


def test_front_rows_download_and_omitted_row_2(tmp_path):
    rows = _painter(tmp_path).display_rows("front")
    numbers = [number for number, _short, _explain, _kind in rows]
    kinds = [kind for _number, _short, _explain, kind in rows]
    assert numbers == [1, 3, 4, 8, 9]
    assert kinds == ["download", "system-log", "language", "self-management", "exit"]
    assert rows[0][1] == "download"


def test_pasted_page_url_starts_download(tmp_path):
    model = MenuModel(painter=_painter(tmp_path))
    model.buffer = "https://anime1.me/watch"
    model.cursor = len(model.buffer)
    assert model._commit() == "download:https://anime1.me/watch"


def test_download_row_asks_for_a_url(tmp_path):
    model = MenuModel(painter=_painter(tmp_path))
    assert model.apply_key(10) is None
    assert model.focus == "input"
    assert model.notice == "Paste one http(s) page URL"


def test_invalid_choice_stays_on_the_board(tmp_path):
    model = MenuModel(painter=_painter(tmp_path))
    model.buffer = "nope"
    model.cursor = 4
    assert model._commit() is None
    assert model.error
    assert model.layer == "front"


def test_exit_row_leaves(tmp_path):
    model = MenuModel(painter=_painter(tmp_path))
    model.index = 4
    assert model.apply_key(curses.KEY_ENTER) == "exit"


def test_components_list_and_storyboard():
    """TP-TUI-10: the requirement prints each part, the style columns, and the capture flow."""
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs/requirements/requirement-python-tui.md").read_text(encoding="utf-8")
    section_parts = text.split("### 2.2 ", 1)[1].split("### 2.3 ", 1)[0]
    section_flow = text.split("### 2.3 ", 1)[1].split("## 3.", 1)[0]
    for name in (
        "navigation",
        "status",
        "major input",
        "major output",
        "path display",
        "system-time display",
        "time-consuming process messages",
    ):
        assert name in section_parts
    assert "Where it sits" in section_parts
    assert "Display style" in section_parts
    found = re.findall(r"screenshots/[a-z0-9.-]+\.png", section_flow)
    expected = [
        "screenshots/main-menu-en.png",
        "screenshots/language-menu.png",
        "screenshots/main-menu-zh-hans.png",
        "screenshots/main-menu-zh-hant.png",
        "screenshots/main-menu-es.png",
        "screenshots/main-menu-ar.png",
        "screenshots/main-menu-fr.png",
        "screenshots/main-menu-pt.png",
        "screenshots/main-menu-ru.png",
        "screenshots/main-menu-de.png",
        "screenshots/main-menu-ja.png",
        "screenshots/main-menu-ko.png",
        "screenshots/main-menu-nl.png",
        "screenshots/main-menu-el.png",
        "screenshots/system-log.png",
        "screenshots/self-management.png",
        "screenshots/tui-about.png",
    ]
    assert found == expected
    for name in expected:
        assert (root / name).is_file()
    assert "video.png" not in section_flow
    assert "download-progress" not in section_flow
