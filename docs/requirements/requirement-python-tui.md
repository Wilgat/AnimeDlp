**file**: docs/requirements/requirement-python-tui.md  
**Status**: Active (Version 1.0.0)  
**Area**: python  
**Key**: `requirement-python-tui`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

The text menu for AnimeDlp. On a terminal with no page URL, `anime-dlp` opens this menu. A page URL on the command line downloads or extracts and does not open it.

The argument contract stays on `requirement-python-cli-interface`. Download apply stays on `requirement-domain-animedlp`.

### 1.1 Human-facing

**In one sentence:** Run `anime-dlp` with no URL and the text menu opens so you can paste a page URL.

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open the menu | Front rows are download (**1**), system-log (**3**), language (**4**), self-management (**8**), and Exit (**9**). Row 2 is omitted | `anime-dlp` |
| Download | Paste one `http://` or `https://` page URL in the bottom box | the page URL, then Enter |
| Leave | The program returns 0. There is no confirm question | `9` or `Exit` |
| No terminal | Help is printed and the process returns 0. The menu is not drawn | `anime-dlp` with stdout redirected |

## 2. Core Rules (Mandatory)

1. **Door.** No positional URL on a terminal **MUST** open this menu, including when the only extra tokens are `--debug` or `--verbose`. `--help` and `--version` **MUST NOT** open it. A page URL **MUST NOT** open it.  
2. **No terminal.** No URL and no terminal **MUST** print help and return 0. The menu **MUST NOT** wait on stdin.  
3. **Front rows.** The front board **MUST** list **1** `download`, **3** `system-log`, **4** `language`, **8** `self-management`, and **9** `Exit`. Row **2** **MUST** stay omitted.  
4. **Download.** Choosing download focuses the bottom box. A token that starts with `http://` or `https://` on the front board **MUST** run that page through `Anime1Downloader` and then show the result on the result page. The menu **MUST NOT** start a download by itself.  
5. **Children.** System-log children are **31** view-log, **32** clear-log, **33** log-folder, and **0** Back. Language children are **41** through **53**, then **0** Back. Self-management children are **82** version, **83** about, **84** version-check, **85** self-update, **86** self-uninstall, **87** self-install, and **0** Back.  
6. **Frame.** The front board, system-log, language, and self-management show the current directory on the left of row 0 and a local `HH:MM:SS` clock on the right when the row has room. The status line shows the product name and version. The input box is the bottom three rows.  
7. **Invalid choice.** A number or word that is not on the current board **MUST** stay on that board. It **MUST NOT** exit the process.  
8. **Exit.** Row 9 Exit returns 0.  
9. **After a leaf.** A finished leaf redisplays the front board.

### 2.1 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Session** | `src/AnimeDlp/tui.py` class `Tui` |
| **Frame** | `src/AnimeDlp/menu_painter.py` class `MenuPainter` |
| **Keys** | `src/AnimeDlp/menu_model.py` class `MenuModel` |
| **Loop** | `src/AnimeDlp/menu_session.py` class `MenuSession` |
| **Proof** | `tests/test_tui.py`, `tests/test_cli.py` TP-CLI-02, TP-CLI-04, TP-CLI-05 |

## 3. Protection Rule (Sacred)

**Future AI assistants MUST NOT**:

1. Require a page URL before this menu can open on a terminal.  
2. Open this menu when a page URL was given.  
3. Put row 2 back, or put install on the front board.  
4. Hang when stdout is not a terminal.

## 4. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | No URL on a terminal opens the menu |
| AC-2 | No URL and no terminal prints help and returns 0 |
| AC-3 | Front numbers are 1, 3, 4, 8, 9 |
| AC-4 | A pasted `http(s)` URL is a download |
| AC-5 | An unknown choice stays on the board |

## 5. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-cli-interface` | Who opens this menu |
| `requirement-domain-animedlp` | Page download |
| `docs/requirements/index.md` | Registry |

## 6. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-05 | Active 1.0.0 | Text menu for a bare `anime-dlp` |
