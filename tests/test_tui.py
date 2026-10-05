"""Text menu tests — front board, pasted URL, invalid choice. No curses screen."""

import curses

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
