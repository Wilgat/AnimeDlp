**file**: docs/requirements/requirement-python-tui.md  
**Status**: Active (Version 1.2.2)  
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
| Open the menu | Front rows are download (**1**), system-log (**3**), language (**4**), self-management (**8**), and Exit (**9**). Row **2** `stream to mpv player` is shown only when `mpv` is on PATH and `mpv --version` contains `mplayer2`. Otherwise row 2 is omitted | `anime-dlp` |
| Download | Paste one `http://` or `https://` page URL in the bottom box | the page URL, then Enter |
| Leave | The program returns 0. There is no confirm question | `9` or `Exit` |
| No terminal | Help is printed and the process returns 0. The menu is not drawn | `anime-dlp` with stdout redirected |

## 2. Core Rules (Mandatory)

1. **Door.** No positional URL on a terminal **MUST** open this menu, including when the only extra tokens are `--debug` or `--verbose`. `--help` and `--version` **MUST NOT** open it. A page URL **MUST NOT** open it.  
2. **No terminal.** No URL and no terminal **MUST** print help and return 0. The menu **MUST NOT** wait on stdin.  
3. **Front rows.** The front board **MUST** list **1** `download`, **3** `system-log`, **4** `language`, **8** `self-management`, and **9** `Exit`. Row **2** **MUST** be `stream to mpv player` only when `mpv` is on PATH and the text of `mpv --version` contains `mplayer2`. Otherwise row **2** **MUST** stay omitted.  
4. **Download.** Choosing download focuses the bottom box. A token that starts with `http://` or `https://` on the front board, while row 2 is not the chosen row, **MUST** run that page through `Anime1Downloader` and then show the result on the result page. The menu **MUST NOT** start a download by itself.  
4a. **Stream.** Choosing row 2 focuses the bottom box for one page URL. The program **MUST** extract that page and **MUST NOT** save a media file. One extracted video **MUST** be played by executing `mpv` with that media URL. More than one extracted video **MUST** show a numbered list of titles, and the chosen title **MUST** be the media URL passed to `mpv`. Esc on that list **MUST** return to the front board and **MUST NOT** start mpv. A pasted URL while another front row is chosen **MUST** stay a download.  
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

### 2.2 Components list and style guide

This menu names each part, where that part sits, and the display style.

| Part | What it is | Where it sits | Display style |
|------|------------|---------------|---------------|
| navigation | The numbered rows you pick | Under the path line and above the bottom input box, on the front board and on each child board | Each row is a number, a short name, and an explain sentence. The front board is **1** download, **3** system-log, **4** language, **8** self-management, and **9** Exit. Row **2** `stream to mpv player` is shown only when `mpv --version` contains `mplayer2`. Otherwise it stays omitted. Child boards stay rule 5: system-log **31**–**33**, language **41**–**53**, self-management **82**–**87**, and each child board ends with **0** Back |
| status | The product name, the version, the board title, and the key hint | The line under the bottom input box. It is the last row of a choice board | Plain text: two spaces, the product name, one space, the version, two spaces, `│`, two spaces, the board title, two spaces, `│`, two spaces, `Up/Down  •  Enter`. A result page does not draw this line. When the about page is longer than the window, its footer is `Up/Down scrolls this page.` The return line is `Press a key to return to the main menu.` |
| major input | The box where you type a row number or a page URL | The bottom three rows of a board that takes a choice: a top border, one typing line, and a bottom border | The typing line starts with `> `. The corners are `╭` `╮` `╰` `╯`. The horizontal stroke is `─`. The vertical stroke is `│`. A focused box shows the typed text and a block caret `█`. A result page has no input box |
| major output | The board the screen writer draws | The whole terminal | `MenuPainter` in `src/AnimeDlp/menu_painter.py` is the writer. One paint replaces the screen. A result page scrolls with Up and Down and does not draw the path or the clock |
| path display | The folder you are standing in | The left side of row 0 on the front board, system-log, language, and self-management | `<label>: <absolute current directory>` with one space after the colon. The English label is `Path`. Other languages use the path word `requirement-python-cli-language` names. Traditional Chinese is `路徑`. The directory is not translated. When the row is too narrow, the directory shortens from the left |
| system-time display | The local time of this machine | The right side of that same row 0, when the row has room, on the front board, system-log, language, and self-management | `HH:MM:SS`, 24-hour, zero-padded, eight characters. No date, no timezone, and no label. At least two spaces sit before the clock. A row that cannot hold both keeps the path and omits the clock. A result page and a question do not draw the clock. The clock is drawn again at most once a second, with no thread. The clock is not translated |
| time-consuming process messages | The sentence shown while videos are being saved | One line on the terminal’s error stream, while that download runs. It is not a row of this menu | A flashing bullet, then the saved-language words for `please wait`, then the file count, the percent finished, and the time until finish. The bullet cell flashes. The phrase and the numbers stay put. The thirteen phrases stay on `requirement-python-cli-language`. The line shape stays on `requirement-domain-animedlp`. This menu does not download an AI model and does not convert images, and it does not print `{choice} has been selected. {process} takes time to finish.` |

### 2.3 Storyboard

These captures are already on disk. The order is the operator flow. Each row names the action that opens that file. Caption sentences stay on `requirement-python-readme`. Exit has no capture. A page URL does not open this menu, so a download picture is not a step of this menu.

| Order | Action | Capture |
|------|--------|---------|
| 1 | Open `anime-dlp` with no page URL on a terminal | `screenshots/main-menu-en.png` |
| 2 | Choose **4** language | `screenshots/language-menu.png` |
| 3 | Save 简体中文 and return to the front board | `screenshots/main-menu-zh-hans.png` |
| 4 | Save 繁體中文 and return to the front board | `screenshots/main-menu-zh-hant.png` |
| 5 | Save Español and return to the front board | `screenshots/main-menu-es.png` |
| 6 | Save العربية and return to the front board | `screenshots/main-menu-ar.png` |
| 7 | Save Français and return to the front board | `screenshots/main-menu-fr.png` |
| 8 | Save Português and return to the front board | `screenshots/main-menu-pt.png` |
| 9 | Save Русский and return to the front board | `screenshots/main-menu-ru.png` |
| 10 | Save Deutsch and return to the front board | `screenshots/main-menu-de.png` |
| 11 | Save 日本語 and return to the front board | `screenshots/main-menu-ja.png` |
| 12 | Save 한국어 and return to the front board | `screenshots/main-menu-ko.png` |
| 13 | Save Nederlands and return to the front board | `screenshots/main-menu-nl.png` |
| 14 | Save Ελληνικά and return to the front board | `screenshots/main-menu-el.png` |
| 15 | Choose **3** system-log | `screenshots/system-log.png` |
| 16 | Back, then choose **8** self-management | `screenshots/self-management.png` |
| 17 | Choose **83** about. This result page has no clock and no input box | `screenshots/tui-about.png` |

## 3. Protection Rule (Sacred)

**Future AI assistants MUST NOT**:

1. Require a page URL before this menu can open on a terminal.  
2. Open this menu when a page URL was given.  
3. Show row 2 when `mpv` is absent or its version text does not contain `mplayer2`. Put install on the front board. Save a streamed video to disk.  
4. Hang when stdout is not a terminal.  
5. Drop a part, its place, or its display style from the components list.  
6. Name a storyboard capture that is not a file under `screenshots/`, or describe a download-progress frame as a step of this menu.  
7. Invent a capture, or recapture pictures from this requirement.

## 4. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | No URL on a terminal opens the menu |
| AC-2 | No URL and no terminal prints help and returns 0 |
| AC-3 | Front numbers are 1, 3, 4, 8, 9 when mpv is not an mplayer2 build, and 1, 2, 3, 4, 8, 9 when it is |
| AC-4 | A pasted `http(s)` URL on a row other than stream is a download. Row 2 plays the extracted media URL in mpv and does not save a file |
| AC-5 | An unknown choice stays on the board |
| AC-6 | The components list names each part with where it sits and the display style, and the storyboard names the captured menu files in operator order |

### 4.1 Design-time verification

| TP-ID | Suite | Status |
|-------|-------|--------|
| **TP-TUI-10** | `tests/test_tui.py` | have |

**Map:** `docs/reviews/test-plan.md`

## 5. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-cli-interface` | Who opens this menu |
| `requirement-domain-animedlp` | Page download, and the download wait line |
| `requirement-python-readme` | Caption cells for the captures this storyboard names |
| `requirement-python-cli-language` | The path word for each saved language |
| `docs/requirements/index.md` | Registry |

## 6. Terminologies

### default-tui-style

**Definition:** Default TUI style is the full-screen look of this text menu. One screen writer draws two regions on a choice board: a menu region and a bottom input box pinned to the bottom of the screen. The first row of the menu region is the path line: a label, a colon, one space, and the absolute current directory. That directory is not translated. The product name and the version are not on that row. They stay on the status line under the box, as plain text, with a space between the name and the version. When the row has room, a local clock `HH:MM:SS` is on the right: 24-hour, zero-padded, eight characters, no date, no timezone name, no label, and not translated. At least two spaces separate the path from the clock. A row that cannot hold both keeps the path, shortened from the left, and omits the clock. Numbered rows follow the path line. The box is a rounded frame exactly three terminal rows high, and the status row under it is the last row of the screen. While a choice board is showing, the session waits at most one second for the next key. No key redraws the clock and stays on the board. A typed key is still delivered. No thread. A result page and a question do not draw the clock and do not use that wait.

**Human daily-life explanation:** The chalkboard fills the window. The top line names the folder you are standing in, and a small clock of the local time sits on the right of that same line and moves once a second. The rows sit under that line, and a rounded writing tray is fixed to the bottom edge. The product name and the version sit on the thin strip under the tray, not on the top line.

**Daily-life example:** On the AnimeDlp front board the top line reads `Path: ` and then the folder you are standing in, and the clock `14:05:09` ends at the right edge. A second later the clock shows the new local time and the rows have not moved. You type the row number in the bottom box. The about page does not show the clock.

### major-tui-entry-point

**Definition:** The major entry of this text menu is interactive mode with no positional page URL. Flags that are not a command, such as `--debug` or `--verbose` with no URL, stay on that entry. `--help` and `--version` do not open the menu. A page URL does not open the menu. A verb opens this menu only when this requirement names that verb.

**Human daily-life explanation:** You see the walk-up board when you name no dish. Naming a page sends you to the download counter. A light switch that is not a dish, such as `--debug`, still leaves you at the walk-up board.

**Daily-life example:** You run `anime-dlp` and name no page. The menu opens. You add only `--debug`. The menu still opens. You pass a page URL. That download is not this door.

### well-known-time-consuming-process

**Definition:** A well-known time-consuming process is a closed catalog of operator work that is known to take long enough that the selected choice must show one sentence before that work starts. The catalog is downloading an AI model and converting images. The sentence names the choice and says that the process takes time to finish. The process words are `Downloading the AI model` or `Converting images`. The sentence is shown only when that process is about to start. A choice that only opens a submenu does not announce. An empty input, a missing path, a rejected format, a failure to create the output directory, language, Exit, version, about, and a package-manager lifecycle do not announce. Do not say the model is downloading when the weights file is already a file. On a terminal the sentence is printed and flushed before the blocking call. On a text screen it is painted and refreshed and does not wait for a key. A caller that also prints returned text must not print the sentence a second time.

**Human daily-life explanation:** It is a dish the kitchen already knows will take a while. The waiter says the dish you picked and that it takes time, then goes to the kitchen. Opening the menu book is not that dish. A glass of water that is already on the table is not announced as still being filled.

**Daily-life example:** This AnimeDlp menu does not download an AI model and does not convert images, so it does not say that sentence. A video download shows a flashing bullet and the saved-language words for please wait, then the file count, the percent, and the time until finish. That line stays on `requirement-domain-animedlp` and is erased when the downloads return.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-07 | Active 1.2.2 | Row 2 streams to mpv when `mpv --version` contains `mplayer2`. One video plays immediately. Several videos show a numbered title list. No file is saved |
| 2026-10-07 | Active 1.2.1 | `video.png` is not a step of this menu |
| 2026-10-06 | Active 1.2.0 | The time-consuming row is the download wait line: a flashing bullet and the saved-language words for please wait |
| 2026-10-06 | Active 1.1.0 | Components list, style guide, and storyboard of captures already on disk |
| 2026-10-05 | Active 1.0.0 | Text menu for a bare `anime-dlp` |
