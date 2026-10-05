**file**: docs/requirements/requirement-python-oop.md
**Status**: Active (Version 1.1.3)
**Area**: python
**Key**: `requirement-python-oop`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define when AnimeDlp uses a class, and name the file that holds each class. One class lives in one module. `def main` stays in `src/AnimeDlp/cli.py`. Every class in the map accepts the one status logger as an `__init__` parameter so that class can log. The line text stays on `requirement-python-cli-logging`.

The menu picture stays on `requirement-python-tui`. The about page stays on `requirement-python-about`. The domain sentence stays on `requirement-domain-animedlp`. Download apply stays on `requirement-download-ytdlp-pipeline`. `shutil.move` stays on `requirement-python-coding-style`. This file decides the class and the file. It does not invent a second picture, a second about page, or a join/concat class.

The target is an ordinary multi-class split. A StateLogic + `Attr` rewrite stays unordered. This file does not claim that rewrite. The notes still record the older three-module gap. `CheckSystem` and `AboutPage` are named in the map. They are not in the running tree. `TP-OOP-*` stay todo.

### 1.1 Human-facing

**In one sentence:** Each class lives in its own file, `main` stays in `cli.py`, and each class receives the logger in `__init__`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer adding a prompt or a log action | Put it on the class that already owns that job |
| The other role | The menu picture, the about facts, and the download steps | Their own requirements |
| Not this file | A StateLogic rewrite of `main` | `requirement-python-coding-style` leaves that rewrite unordered |

| Includes | Excludes |
|----------|----------|
| One class per file. The class is the only public surface of that module. Constants that `Cli` owns live on class `Cli` | A second class in the same file, a module-level function beside the class, or a module-level assignment of `Cli`'s identity or verb lists |
| `def main` in `src/AnimeDlp/cli.py` | Moving `main` to another module |
| Ordinary classes named in the map below | One class per function. A StateLogic rewrite |
| The one logger passed into `__init__`. `ClassName(...)` at the site that needs the object | A setter, a module global, a second logger built inside the class, or a factory |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/AnimeDlp/cli.py` | `def main` and class `Cli` | Entry. Builds the other objects and runs one job |
| `src/AnimeDlp/tui.py` | class `Tui` | Text-menu session |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Add a menu prompt | It is a method on `Tui`. The frame is `MenuPainter`. | Edit the class file this requirement names |
| Start the program | The console script calls `AnimeDlp.cli:main`. | `anime-dlp` |
| Name a constant the program uses | It is an attribute of the class that owns it. `Cli` owns identity and the verb lists. | `Cli.APP_NAME` |

## 2. Core Rules (Mandatory)

### 2.1 Use a class when the functions share one job

1. When a set of functions shares one job, product Python **MUST** make them methods of one class and put that class in its own module under `src/AnimeDlp/`.
2. **MUST NOT** make a class whose only method is a single function that nothing else in the file shares.
3. The class **MUST** be the only public surface of its module. A module-level `def` beside that class is a second home. **MUST NOT** add one.
4. That module **MUST** define one class. One exception type raised by that class **MAY** share the file. `MenuScreenError` shares `tui.py` with `Tui`.
5. The file name **MUST** be the class job in snake case (`MenuPainter` → `menu_painter.py`, `AboutPage` → `about_page.py`, `SelfManage` → `self_management.py`).
6. A full StateLogic + `Attr` rewrite of `main` stays unordered (`requirement-python-coding-style`). This file does not order that rewrite. The classes in the map are ordinary classes. The allowed end state is this map. **MUST NOT** collapse the end state back to a single procedural module. The running three-module tree remains legal until an implement order lands the files named here.

### 2.2 Entry: `main` stays in `cli.py`

7. `src/AnimeDlp/cli.py` **MUST** define class `Cli` and **MUST NOT** define another class.
8. `def main` **MUST** stay in `src/AnimeDlp/cli.py`. The signature stays `main(argv=None, basedir="", logdir="")`. `main` writes `ChronicleLogger(...)` (`requirement-python-cli-logging`), builds `Cli`, and runs one job. Empty `basedir` and `logdir` leave folder resolution to the library.
9. The console script **MUST** stay `anime-dlp = AnimeDlp.cli:main`. `src/AnimeDlp/__main__.py` **MUST** keep `from .cli import main`.
10. `cli.py` **MUST NOT** define another class's methods. `Cli` owns `build_parser`, `dispatch`, `opens_text_screen`, `verb_help`, `verb_version`, `verb_about`, `verb_hello`, `verb_lifecycle`, `unknown_verb`, `stdin_is_tty`, and `stdout_is_tty`. `Cli` does not own the ChronicleLogger construct. Pip argument lists stay on `SelfManage`. The about body stays on `AboutPage`. Download and extract stay on `Anime1Downloader` in `cli.py` until a later class split. There is no `Join` class and no `verb_join`. The frame stays on `MenuPainter`.
11. `Cli` constructs the other classes and calls them. Each class receives its collaborators through its constructor.
11f. A constant or variable that class `Cli` or `def main` owns is an attribute of class `Cli`, or a name assigned inside `main()`. It is not a module-level assignment in `cli.py`. That set is `APP_NAME` (`AnimeDlp`), `CONSOLE_NAME` (`anime-dlp`), `PRODUCT_VERBS`, `LIFECYCLE_VERBS`, `AUTHOR_NAME`, `AUTHOR_EMAIL`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, and `BASIC_USAGE`. The about page prints the author name, the homepage, the box date, and the usage line. It does not print the email. The email stays on `Cli`. `Cli` reads the package version from `__version__` only and **MUST NOT** keep a second literal, including a fallback `"1.1.0"`. `Cli` **MUST NOT** keep `MAJOR`, `MINOR`, or `PATCH` integers. `Cli` passes the values other classes print. Those classes do not import the names from the `cli` module.
11g. Another class keeps its own constants. The frame glyphs, `MENU_ROWS`, `SELF_ROWS`, `LOG_ROWS`, `PATH_LABEL_EN`, and `PATH_LABEL_ZH_HANT` stay on `MenuPainter`. `Cli` does not own those names.

### 2.2a The logger arrives through `__init__`

11a. Every class in the map, and `MenuScreenError`, **MUST** accept the one ChronicleLogger as a parameter of `__init__`.
11b. `__init__` **MUST** store that object on `self.logger`. A class that constructs another class in the map **MUST** pass that same object into that constructor.
11c. `def main` writes `ChronicleLogger(...)` before `Cli` (`requirement-python-cli-logging`) and **MUST** pass that object into `Cli(...)`. `main` **MUST NOT** call `Cli.__new__` to build the logger. The parameter **MAY** default to absent so a caller that has no logger can omit it. `main` has the logger and **MUST NOT** omit it.
11d. **MUST NOT** construct a ChronicleLogger inside a class or from a method. **MUST NOT** attach the logger through a setter or a module global after `__init__` returns. **MUST NOT** call a module function to write the instantiation line. `__init__` calls `log_message` itself.
11e. The instantiation line, its level, and quiet stay on `requirement-python-cli-logging`. This file owns only that the logger arrives through `__init__`.
11h. The site that needs an object **MUST** write `ClassName(...)`. A factory is a function or a method whose job is to instantiate a class. This map does not include a factory. The class can be created without one. The ban on that factory also lives on `requirement-python-coding-style`.

### 2.3 Text menu

12. `src/AnimeDlp/tui.py` **MUST** define class `Tui` and the exception `MenuScreenError`. No other class. `Tui` owns `open_text_menu`, `front_lines`, `self_lines`, `log_lines`, `language_lines`, `about_on_screen`, `help_on_screen`, `read_key`, and `notice`.
13. Class `MenuPainter` in `src/AnimeDlp/menu_painter.py` owns `paint`, `paint_prompt`, `path_label`, `path_line`, `clock_text`, `format_rows`, `display_rows`, `screen_can_hold`, `display_width`, `clip_columns`, and `clip_columns_right`. The frame glyphs, `MENU_ROWS`, `SELF_ROWS`, `LOG_ROWS`, `PATH_LABEL_EN`, and `PATH_LABEL_ZH_HANT` live on that class. `display_width`, `clip_columns`, and `clip_columns_right` are methods of that class. The module does not define them beside the class. Wide and Fullwidth count as two. Ambiguous stays one. The column rule stays on `requirement-python-tui`. `FRAME_TOP_LEFT` **MUST NOT** appear in `cli.py`. `path_label`, `clock_text`, and `path_line` draw the first row of the front board, of the self-management board, of the system-log board, and of the language board. The clock shape, shortening the path from the left, and when the clock is omitted stay on `requirement-python-tui` rule 13. The selected word stays on `requirement-python-cli-language`. `path_label` returns that word. It does not read `LANG` or `LC_ALL`, and it does not invent a second line. `MenuPainter.__init__` writes `MenuLanguage(...)`.
14. Class `MenuModel` in `src/AnimeDlp/menu_model.py` owns `apply_key`, `edge_keys`, `highlighted_row`, and `buffer_text`.
15. Class `MenuSession` in `src/AnimeDlp/menu_session.py` owns `run`, `take_action`, `wait_key`, and `leave_to_front`. `wait_key` is the one-second clock wait from `requirement-python-tui` rule 13, including the language board. It does not start a thread. `run` loops until row 9 Exit. A leaf action returns to the front board. A language pick saves through the shared `MenuLanguage` and returns to the front board. `MenuSession` dispatches system-log, language, self-management, and exit. It does not paint the frame.
15a. Class `MenuLanguage` in `src/AnimeDlp/menu_language.py` owns the thirteen codes, the language leaf, and the menu words. One class. No second class in that file. The logger arrives through `__init__`. The codes and the leaf stay on `requirement-python-cli-language`.
16. The menu picture stays on `requirement-python-tui`. These classes implement that picture. They do not invent a second layout.
17. Until an implement order lands this split, `cli.py` still holds the prompt session. After the split, `cli.py` **MUST NOT** hold `Tui`, `MenuPainter`, `MenuModel`, or `MenuSession` methods.

### 2.4 About page

18. Class `AboutPage` in `src/AnimeDlp/about_page.py` owns `framework_about`, `about_box_lines`, `install_kind`, `install_sentence`, and `_is_source_checkout`. `framework_about` composes the page in `requirement-python-about`. The domain sentence stays on `requirement-domain-animedlp`. `install_sentence` names GLOBAL, LOCAL, or UNINSTALLED. It **MUST NOT** name `python -m pip install AnimeDlp` and **MUST NOT** name a downloaded-script installer. Class `CheckSystem` in `src/AnimeDlp/check_system.py` owns the host-check reads, including the pyenv and conda paths. `Cli` writes `CheckSystem(...)` and then `AboutPage(...)`. `AboutPage` calls that object. It **MUST NOT** construct `CheckSystem`. Row 83 and the `about` verb call `framework_about`.
### 2.5 The other jobs

20. Class `SystemLog` in `src/AnimeDlp/system_log.py` owns `log_dir`, `log_files`, `read_log`, `clear_log`, and `folder_text`. The menu rows and the result-page words stay on `requirement-python-tui`. `Tui` writes `SystemLog(...)` at the site that needs it and passes the same logger. `cli.py` **MUST NOT** list the log files, read one, or empty one.
21. Class `SelfManage` in `src/AnimeDlp/self_management.py` owns `local_version`, `argv_for`, `run_pip`, and `emit`. `local_version` reads `__version__` and does not call pip. `argv_for` builds the pip argument lists for `version-check`, `self-update`, `self-install`, and `self-uninstall`. The verb names and the command strings stay on `requirement-python-cli-interface` and `requirement-python-tui`. `cli.py` **MUST NOT** build those pip argument lists. The about body is not this class.
22. Version display stays the single string `__version__` in `src/AnimeDlp/__init__.py`. **MUST NOT** add a second integer triple.

### 2.6 Implementation Notes (this project)

| Class | File | Owns |
|-------|------|------|
| `Cli` | `src/AnimeDlp/cli.py` | Parser, dispatch, verbs, tty checks. Identity constants and verb lists (rule 11f). `def main` stays in this file |
| `Tui` | `src/AnimeDlp/tui.py` | Text-menu session (rule 12). Shares the file with `MenuScreenError` |
| `MenuPainter` | `src/AnimeDlp/menu_painter.py` | Frame, glyphs, `MENU_ROWS`, `SELF_ROWS`, `LOG_ROWS`, `PATH_LABEL_EN`, `PATH_LABEL_ZH_HANT`, `paint`, `path_label`, `path_line`, `clock_text`, `display_width`, `clip_columns`, `clip_columns_right`. Writes `MenuLanguage(...)` |
| `MenuLanguage` | `src/AnimeDlp/menu_language.py` | Thirteen codes, the language leaf, and the menu words |
| `MenuModel` | `src/AnimeDlp/menu_model.py` | Keystroke state. Shares the painter’s language object |
| `MenuSession` | `src/AnimeDlp/menu_session.py` | `run`, `take_action`, `wait_key`, `leave_to_front` |
| `SystemLog` | `src/AnimeDlp/system_log.py` | Log folder, file list, read, empty |
| `SelfManage` | `src/AnimeDlp/self_management.py` | Local version and the pip commands for rows 84–87 |
| `CheckSystem` | `src/AnimeDlp/check_system.py` | Host-check reads for the about page. Does not draw the star box |
| `AboutPage` | `src/AnimeDlp/about_page.py` | `framework_about`, the star box, and the install kind. Calls `CheckSystem` |

| Item | Value |
|------|--------|
| **Console script** | `anime-dlp = AnimeDlp.cli:main` |
| **Module entry** | `src/AnimeDlp/__main__.py` imports `main` from `.cli` |
| **Running tree** | `src/AnimeDlp/__init__.py`, `__main__.py`, `cli.py`, `tui.py`, and `menu_painter.py`. Class `Anime1Downloader` lives in `cli.py`. Class `Tui` and class `MenuPainter` draw the text menu. That tree is not the full map below |
| **Landed** | `Tui` and `MenuPainter` are in the tree for the download menu. `Cli`, `MenuLanguage`, `MenuModel`, `MenuSession`, `SystemLog`, `SelfManage`, `CheckSystem`, and `AboutPage` are named in the map and are not in the tree. `TP-OOP-01` through `TP-OOP-04` stay todo |
| **Logger** | Every class `__init__` in the map accepts `logger` and stores it. `def main` writes `ChronicleLogger(...)` and then `Cli(logger)`. Collaborators are `OtherClass(...)` at the site that needs them |
| **Not this split** | Menu rows, about line facts, download steps, version string, the wording of the instantiation line |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Each job has one class and one file. That class receives the logger in `__init__`.
- **Principle 5 – SSOT**: `cli.py` does not keep a second copy of another class's methods. `main` has one home.
- **Principle 1 – Caution**: The picture, the about facts, and the download steps stay where their requirements already put them. The running tree is not declared illegal before the split lands.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, each class still receives the logger through `__init__` at this login. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to construct a class or to pass the logger. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## Sample code

StateLogic stays unordered. The site writes the class name. This sample is the allowed end state. The running `cli.py` does not look like this yet.

```python
def main(argv=None, basedir="", logdir=""):
    logger = ChronicleLogger(logname="AnimeDlp", is_quiet=opens_text_screen(argv))
    app = Cli(logger)
    return app.run(argv)

class Cli:
    APP_NAME = "AnimeDlp"
    CONSOLE_NAME = "anime-dlp"

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Cli")
        self.tui = Tui(logger)
```

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not treat `Tui` and `MenuPainter` as the full map, and do not pretend the unlanded class files are already on disk.
- **Intentional:** One job, one class, one file. Download stays on `Anime1Downloader` until a later split. There is no encoder class.
- **Anti-fragile:** `def main` and the console script keep their addresses.
- **Over-protect:** No factory, no second logger, no StateLogic rewrite hidden inside this map.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

1. Move `def main` out of `src/AnimeDlp/cli.py`.
2. Put two classes in one module, except `MenuScreenError` beside `Tui`.
3. Leave a class that has only one method.
4. Construct ChronicleLogger inside a class.
5. Add a factory whose job is to instantiate a class in this map.
6. Put `MENU_ROWS`, `SELF_ROWS`, `LOG_ROWS`, or frame glyphs on `Cli`.
7. Keep a second version literal on `Cli`.
8. Add an encoder class or a file-stage class for this product.
9. Order a StateLogic + `Attr` rewrite from this file.
10. Mark `TP-OOP-*` have before the class files exist and the proofs pass.
11. Delete the running `cli.py` behavior in a requirement-only edit.

**Violating this rule is a critical structure regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | The map names `Cli`, `Tui`, `MenuPainter`, `MenuLanguage`, `MenuModel`, `MenuSession`, `SystemLog`, `SelfManage`, `CheckSystem`, and `AboutPage`, each in its own file |
| AC-2 | `def main` stays in `cli.py`. The console script stays `AnimeDlp.cli:main` |
| AC-3 | Every class `__init__` accepts the logger. The site writes `ClassName(...)` |
| AC-4 | `Cli` owns the identity constants. `MenuPainter` owns the row tuples and the glyphs |
| AC-5 | `AboutPage` composes the about page. `CheckSystem` owns the host check. Download and extract stay on `Anime1Downloader` until a later class split |
| AC-6 | `tui.py` and `menu_painter.py` are in the tree. The rest of the map is not. Proofs stay todo |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-cli-logging` | Construct, `instantiated` line, quiet |
| `requirement-python-tui` | Picture the classes draw |
| `requirement-python-cli-interface` | Verb names `Cli` dispatches |
| `requirement-python-about` | About page line text. This file names `AboutPage` and `CheckSystem` |
| `requirement-domain-animedlp` | Domain sentence. This file does not own extract or download steps |
| `requirement-download-ytdlp-pipeline` | yt-dlp download steps |
| `requirement-python-coding-style` | `shutil.move`. StateLogic stays unordered. Factory ban |
| `requirement-python-project-structure` | Running tree versus this map |
| `requirement-python-packaging` | Console script and `__version__` |
| `requirement-class-software-dev` | Residual pointer |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-OOP-01** | `tests/test_oop.py` | todo | The class files in the map exist. `cli.py` defines `Cli` and `def main` and does not define another class's methods |
| **TP-OOP-02** | `tests/test_oop.py` | todo | Every class `__init__` takes the logger, stores it, and logs `instantiated` |
| **TP-OOP-03** | `tests/test_oop.py` | todo | `MenuPainter` owns the frame glyphs and `MENU_ROWS` / `SELF_ROWS` / `LOG_ROWS`. Those names are absent from `cli.py` |
| **TP-OOP-04** | `tests/test_oop.py` | todo | `APP_NAME`, `CONSOLE_NAME`, `PRODUCT_VERBS`, `LIFECYCLE_VERBS`, identity constants are attributes of `Cli`. Display version is `__version__` only |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | L2 class map for AnimeDlp. Running tree remains three modules. StateLogic unordered. Proofs todo |
| 2026-10-04 | Active 1.0.1 | `MenuPainter` owns `path_label`, `PATH_LABEL_EN`, and `PATH_LABEL_ZH_HANT`. Those methods do not detect a language. `TP-OOP-*` stay todo |
| 2026-10-04 | Active 1.0.2 | Class `MenuLanguage` is the language home. `MenuPainter` writes `MenuLanguage(...)`. `TP-OOP-*` stay todo |
| 2026-10-04 | Active 1.0.3 | `display_width`, `clip_columns`, and `clip_columns_right` are methods of `MenuPainter`. `TP-OOP-*` stay todo |
| 2026-10-04 | Active 1.1.0 | `CheckSystem` owns the host check. `AboutPage` owns `framework_about`. No second version triple. `TP-OOP-*` stay todo |
| 2026-10-05 | Active 1.1.1 | Specialized from the VideoJoin bootstrap. Class `Join`, concat, and video suffix sets removed |
| 2026-10-05 | Active 1.1.2 | Acceptance rows no longer name class `Join`. Video suffix sets stay off `Cli`. The map is not claimed to be on disk |
| 2026-10-05 | Active 1.1.3 | `Tui` and `MenuPainter` are in the running tree. The rest of the map stays todo |

---

**Last Updated**: 2026-10-05
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
