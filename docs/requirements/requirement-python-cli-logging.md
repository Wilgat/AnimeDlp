**file**: docs/requirements/requirement-python-cli-logging.md
**Status**: Active (Version 1.0.2)
**Area**: python
**Key**: `requirement-python-cli-logging`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

`def main` instantiates ChronicleLogger. The instantiation is the statement `ChronicleLogger(...)` written in that function, before the argument parser and before any product object.

AnimeDlp records system status through that one ChronicleLogger instance: process start, debug identity, menu steps, download steps, temp write, publish, discard of an unfinished temp, and failures. User-visible failure sentences stay on `requirement-python-error-handling`. The text menu stays on `requirement-python-tui`. Class homes stay on `requirement-python-oop`. The pip name and the version floor stay on `requirement-python-packaging` and `requirement-runtime-prerequisites`. Download apply stays on `requirement-download-ytdlp-pipeline`. `shutil.move` stays on `requirement-python-coding-style`.

This product creates no threads. This file does not name a thread-wait timeout. Control-C stop, an exit code for that stop, and the decision not to publish are not confirmed law in this file. Row 9 Exit returns 0 with no confirm question (`requirement-python-tui`).

The running `src/AnimeDlp/cli.py` writes `ChronicleLogger(...)` in `def main`. The allowed end state is this file.

### 1.1 Human-facing

**In one sentence:** `def main` writes `ChronicleLogger(...)`, AnimeDlp keeps a dated status file through that object, and those lines stay off the text menu.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person running `anime-dlp` | A failed download is still explained on the console, and the same fact is in the log file |
| The other role | The logger library | `ChronicleLogger(logname="AnimeDlp")` resolves the folder and the line shape |
| Not this file | How the menu is drawn, and how yt-dlp fetches the media | `requirement-python-tui`, `requirement-download-ytdlp-pipeline` |

| Includes | Excludes |
|----------|----------|
| One logger, read-back of name and folders, the debug gate, `log_message` level and component, the `instantiated` line, and the temp / publish / discard lines | Rewriting ChronicleLogger, a second logging setup, painting the menu with log lines, a copied folder ladder, a thread pool |
| `is_quiet=True` on the constructor when this run will open the text screen | A later `quiet(True)` as the only way to hide `Created directory:` |
| The daily file when the text screen is open | Mirroring identity lines onto that screen |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/AnimeDlp/cli.py` | `def main` | Writes `ChronicleLogger(...)`, then passes that one instance |
| `anime-dlp` | console script | Writes status while it runs |
| Resolved `logDir()` | daily `.log` file | History after the process exits |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start the program | `def main` writes one `ChronicleLogger(...)` with logname `AnimeDlp`, reads the resolved name and folders back, and logs status with a component tag. | `anime-dlp version` |
| Ask for the debug lines | Set `DEBUG` before the process starts. On a run that does not open the text screen, `main` displays the resolved name, the package version, `ChronicleLogger.class_version()`, and a line that says `debug mode`, before the argument parser. The text screen keeps that mirror off the console. The daily file still receives the lines. When debug mode is off, those lines stay off. | `DEBUG=1 anime-dlp version` |
| Open the menu | The constructor is quiet, so log lines do not paint over the frame. The menu is still the text screen. | `anime-dlp` |

## 2. Core Rules (Mandatory)

**Construct site.** `def main` instantiates the one ChronicleLogger. The instantiation is the statement `ChronicleLogger(...)` written in that function, before the argument parser and before any product object. Rule 5 is this law.

### 2.0 When this law applies

1. **MUST** send system-status history through ChronicleLogger.
2. **MUST NOT** add `logging.basicConfig`, a second file logger, or a hand-built folder path for those lines.
3. **MUST NOT** use this file as the law for editing the ChronicleLogger library itself.

### 2.1 One logger

4. **MUST** import `ChronicleLogger` from `ChronicleLogger` at the use site inside `def main`. **MUST NOT** import `_Suroot`. A test that freezes the clock **MUST** define its own `TimeProvider` subclass in the test module. **MUST NOT** import `FakeTimeProvider` from the package.
5. **MUST** construct **one** instance per process by writing `ChronicleLogger(...)` inside `def main`, with `logname` set to the product name `AnimeDlp`. That statement is the construct. **MUST NOT** put the construct in a function or a method. **MUST NOT** call `Cli.__new__` in order to build the logger. Helpers receive that instance. **MUST NOT** construct a second logger.
6. **MUST** read `logName()`, `baseDir()`, and `logDir()` immediately after construct, and again after any path setter, before the first `log_message`. The constructor string is not the resolved name. `AnimeDlp` resolves to `anime-dlp`.
7. **MUST NOT** re-export `ChronicleLogger` from the `AnimeDlp` package. Public exports stay `__version__` and `main` (`requirement-python-packaging`).
8. If the import fails, **MUST** fail closed on the console with the pip next step for the floor named by `requirement-python-packaging`, and **MUST** return non-zero. That line cannot go through `log_message`. Importing the `AnimeDlp` package **MUST** still succeed when ChronicleLogger is absent, because the construct is not at import time.

### 2.2 Debug

9. **MUST** ask `logger.isDebug()` for whether debug status is on. **MUST NOT** read `DEBUG` again in product code. **MUST NOT** add a `--debug` flag.
10. `isDebug()` remembers the first answer. `DEBUG` or `debug` **MUST** already be `1`, `true`, or `show` (any letter case) **before** `ChronicleLogger(...)`.
11. The startup identity lines **MUST** run only inside `if logger.isDebug():`, and `main` **MUST** run that block before the argument parser. The block is four `log_message` calls, each with `component="main"`: the resolved app name, the package version, and this file’s path; `Using` plus `ChronicleLogger.class_version()`; the `baseDir()` value; a line whose message is `debug mode`. **MUST NOT** type the library version by hand. When `isDebug()` is false, those lines **MUST NOT** be displayed.
11a. **Console mirror.** When this run will open the text screen, and that fact is known before construct, `main` **MUST** pass `is_quiet=True` into `ChronicleLogger(...)`. The runs that open the text screen are: empty argv on a terminal, and `about` on a terminal. A URL download does not open this screen. A small argv peek may decide `is_quiet` before the constructor. `ArgumentParser.parse_args` runs after the constructor and after the debug block. The library stores that flag before it resolves the name and the folders and before it creates the log directory. That constructor can print `Created directory:`. A call to `quiet(True)` after the constructor returns **MUST NOT** be the only quiet for those runs. A run that does not open the text screen **MUST** leave `is_quiet` false, so the operator sees `debug mode` on the console. The text screen **MUST** keep that mirror off the console. The same lines still go to the daily file. This product does not claim `--json`. `logger.quiet(True)` remains the setter when a screen opens later and was not known at construct.
11b. **Version string.** The identity line and the `version` verb read the same package version: the single string `__version__` in `src/AnimeDlp/__init__.py`, which matches `pyproject.toml` (`requirement-python-packaging`). The current string is `1.1.0`. **MUST NOT** add `MAJOR` / `MINOR` / `PATCH` integers. **MUST NOT** keep a second version literal for display. A suite assertion may compare the displayed string with `__version__` and with `pyproject.toml`. `main` **MUST NOT** raise because those strings differ.
11c. **Environment checks.** `CheckSystem.in_venv`, `in_pyenv`, and `in_conda` **MUST** call `inVenv()`, `inPyenv()`, and `inConda()` on the one logger. When the logger is absent, each method **MUST** return false. Those three results **MUST NOT** be printed on the about page and **MUST NOT** choose `python2 location`, `python3 location`, `conda location`, or `pyenv location`. The path reads stay on `requirement-python-about`. The proof is `TP-ABOUT-16`.

### 2.3 `log_message` level and component

12. System-status lines **MUST** call `log_message`. The component **MUST** be the keyword `component`.
13. Allowed `component` values for this product:

| Component | Status it marks |
|-----------|-----------------|
| `main` | Process start, version, missing library, top-level failure |
| `menu` | Text menu open, choice, leave, view-log, clear-log |
| `download` | Extract, yt-dlp fetch, per-title failure |
| Class name | That object was constructed, and later status recorded by that object |

The class-name components are `Cli`, `Tui`, `MenuPainter`, `MenuModel`, `MenuSession`, `MenuScreenError`, `SystemLog`, `SelfManage`, `CheckSystem`, and `AboutPage`.

### 2.3a Pass the logger into every class

13a. `main` **MUST** decide quiet and run the debug block before it constructs class `Cli`.
13b. Every product class **MUST** accept that same logger as an `__init__` parameter and store it on `self.logger`. The constructor home is `requirement-python-oop`.
13c. When the logger is present, `__init__` **MUST** call `log_message("instantiated", component="<ClassName>")` in that method. The level is INFO. The call **MUST NOT** sit inside `if logger.isDebug():`. **MUST NOT** call a module function to write that line.
13d. A class that constructs another product class **MUST** write `OtherClass(...)` at that site and pass that same logger.
13e. **MUST NOT** construct a ChronicleLogger inside a class. **MUST NOT** construct it from a method of `Cli`.
13f. A caller that has no logger may omit it. `main` has the logger and **MUST** pass it.
13g. The text screen **MUST** already be quiet, so these lines stay off that console. The daily file still receives them. A run that does not open the text screen **MUST** leave quiet off, so the operator sees each `instantiated` line.

### 2.3b Major file operations

13h. A major file operation **MUST** call `log_message` with the operation and the paths, **before** the operation. The operations are: write a temp, publish through `shutil.move`, and discard an unfinished temp. An unfinished temp is not the result.
13i. The `component` **MUST** be `download` when the line is an extract or yt-dlp step, and `menu` when the line is a menu file action. The level is `INFO`. The call **MUST NOT** sit inside `if logger.isDebug():`. **MUST NOT** use `print`. **MUST NOT** construct a second logger. Download apply stays on `requirement-download-ytdlp-pipeline`. The publish call stays on `requirement-python-coding-style`.
13j. Control-C stop, the exit code for that stop, and the decision not to publish are not confirmed law in this file. This file does not define exit 130. Row 9 Exit returns 0 with no confirm (`requirement-python-tui`). A clock redraw is not that exit.
13k. Quiet from rule 11a still applies. The daily file still receives the line.

### 2.3c Threads

13l. The running product creates no threads. **MUST NOT** add a thread, a pool, or a wait timeout in order to satisfy this file.
13m. If a later requirement adds a thread, that change **MUST** call `log_message` on the one ChronicleLogger before the call that can block or race. The operations are: create, start, join or other wait, lock acquire, lock release, and handing work to a pool. The line names the action, the thread name, and the object it waits on when there is one. The `component` is the class that performs the operation, or `main` when `main` does. Create, start, joined, acquired, and released are `INFO`. The call **MUST NOT** sit inside `if logger.isDebug():`. **MUST NOT** use `print`. **MUST NOT** construct a second logger, including one logger per thread.
13n. `log_message` **MUST NOT** run while a work lock is held. This file does not name a wait timeout.
13o. Quiet from rule 11a still applies. The daily file still receives the line. A thread join is not a substitute for a Control-C law this file does not have.

14. Allowed `level` values: `INFO`, `DEBUG`, `WARNING`, `ERROR`, `FATAL`. The library uppercases the string. `ERROR` and `FATAL` mirror to stderr. The others mirror to stdout. Omitted `level` means `INFO`.
15. A line with `level="DEBUG"` **MUST** sit inside `if logger.isDebug():`.
16. **MUST NOT** put secrets into a message. This product has none. A media URL is allowed.

### 2.4 Console, menu, and the file

17. `log_message` still tries to append the daily file when the folder is writable. An unwritable folder **MUST NOT** crash the process.
18. While the text menu is on screen, the console mirror stays off (rule 11a, or `logger.quiet(True)` when the screen was not known at construct). The file write still happens. `requirement-python-tui` still draws the screen. The screen writer is not a second logger.
19. A run that never opens the menu **MUST** leave quiet off so the operator sees the mirrored status line.
20. A user-visible failure sentence remains owned by `requirement-python-error-handling`. The same fact **MUST** also be `log_message` at `ERROR` or `FATAL` once the logger exists. While quiet is on, the logger mirror is not a substitute for that console sentence. The missing-library line in rule 8 is the exception: the logger does not exist yet.

### 2.5 Folder and line

21. **MUST** use the folders from `baseDir()` and `logDir()`. **MUST NOT** copy the library’s environment ladder into this program. **MUST NOT** hard-code `~/.app/AnimeDlp`, `/var/AnimeDlp`, or `/var/log/AnimeDlp`.
22. When the process is root and it is not under conda, pyenv, or a virtualenv, the library’s `baseDir()` is `/var/anime-dlp` and `logDir()` is `/var/anime-dlp/log`. It is not `/var/log/anime-dlp`. Product code reads those values. It does not assemble them. This sentence does not require AnimeDlp to install conda, pyenv, or a virtualenv.
23. The daily file basename **MUST** stay the library’s `{kebab-app}-{YYYYMMDD}.log` under `logDir()`. For this product the kebab name is `anime-dlp`.
24. A file line has this shape (the library writes it; this product does not format it by hand):

```text
[{YYYY-MM-DD HH:MM:SS}] pid:{PID} [{LEVEL}] @{COMPONENT} :] {MESSAGE}
```

25. Product `main` **MUST NOT** pass a hard-coded folder. A proof that needs a scratch folder may supply `basedir` and `logdir` to `main` so the test does not write the operator’s real folder. An empty value leaves resolution to the library.

### 2.6 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Library** | ChronicleLogger |
| **Floor** | Required `ChronicleLogger>=1.2.3`, owned by `requirement-python-packaging` and `requirement-runtime-prerequisites`. The live `pyproject.toml` declares that floor. |
| **Construct site** | `def main` in `src/AnimeDlp/cli.py` writes `ChronicleLogger(...)`. |
| **logname** | `AnimeDlp` (product name, not a path, not the console-script name) |
| **Resolved name** | `anime-dlp` from `logName()` |
| **Call order** | Inside `def main`: peek argv for the text screen, write `ChronicleLogger(...)` with `logname` and `is_quiet` when that screen is already known, read `logName()`, `baseDir()`, and `logDir()`, run the `isDebug()` block including `debug mode`, then parse arguments, then `Cli(logger)`. |
| **Quiet** | `is_quiet=True` for empty argv on a terminal and for `about` on a terminal. A URL download leaves it false. `quiet(True)` after return does not hide `Created directory:`. |
| **Version** | Identity and `version` use `__version__` (`1.1.0`). No second integer triple. `cli.py` reads `__version__` and does not keep a second literal. |
| **Threads** | None in the running product. No timeout is named. |
| **Control-C** | Not confirmed law here. |
| **Debug switch** | Environment `DEBUG` or `debug` already set to `1`, `true`, or `show`. No `--debug` flag. |
| **Proof** | `TP-LOG-01`, `TP-LOG-02`, `TP-LOG-03`, `TP-LOG-04`, `TP-LOG-05` stay todo. The ship unit does not pass this law. |

### Sample code

`def main` writes `ChronicleLogger(...)`, reads the resolved names back, runs the debug gate, and then writes `Cli(logger)`. `opens_text_screen` is true only for the runs in rule 11a. A non-screen run passes false.

```python
def main(argv=None, basedir="", logdir=""):
    """This function instantiates ChronicleLogger. The statement below is the construct."""
    try:
        from ChronicleLogger import ChronicleLogger
    except ImportError:
        sys.stderr.write(
            'ChronicleLogger is required. Next step: python -m pip install "ChronicleLogger>=1.2.3"\n'
        )
        return 1

    from AnimeDlp import __version__

    screen = opens_text_screen(argv)
    logger = ChronicleLogger(
        logname="AnimeDlp",
        is_quiet=screen,
        basedir=basedir,
        logdir=logdir,
    )
    appname = logger.logName()
    resolved_base = logger.baseDir()
    logger.logDir()

    if logger.isDebug():
        logger.log_message(
            "{0} v{1} ({2})".format(appname, __version__, __file__),
            component="main",
        )
        logger.log_message(
            "Using {0}".format(ChronicleLogger.class_version()),
            component="main",
        )
        logger.log_message(
            "Base {0}".format(resolved_base),
            level="DEBUG",
            component="main",
        )
        logger.log_message("debug mode", component="main")

    app = Cli(logger)
    return app.run(argv)
```

That function is `def main`. The statement `ChronicleLogger(...)` instantiates the logger there. Rule 5 keeps this statement in `def main`.

Before a temp write, a publish, or a discard:

```python
logger.log_message(
    "write temp path={0}".format(temp_path),
    level="INFO",
    component="download",
)
```

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT of output**: status history has one writer.
- **Principle 1 – Caution**: a missing library or an unwritable log folder does not wipe completed downloads or smash the menu.
- **Principle 2 – Intentional**: level and component are named on every status line.
- **Principle 12 – Traceability**: the daily file still receives lines while the text screen is quiet.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, status files stay in the folder ChronicleLogger resolves for this login. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to create the log folder or to install ChronicleLogger. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`. The next step is `python -m pip install "ChronicleLogger>=1.2.3"` as the normal user.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Quiet the console mirror before the text menu. Do not crash when the log folder is unwritable.
- **Intentional:** One instance. Components stay `main`, `menu`, `download`, and the class name.
- **Anti-fragile:** Folder choice stays inside ChronicleLogger. Product code reads `logDir()`.
- **Over-protect:** No second logger and no package re-export of ChronicleLogger.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

1. Construct ChronicleLogger outside `def main`, or construct a second logger.
2. Re-export ChronicleLogger from the AnimeDlp package.
3. Hard-code `~/.app/AnimeDlp`, `/var/AnimeDlp`, or `/var/log/AnimeDlp`, or copy the library folder ladder into product code.
4. Treat `quiet(True)` after the constructor returns as a substitute for `is_quiet=True` on a text-screen run.
5. Put the identity lines outside `logger.isDebug()`, or add a `--debug` flag.
6. Add a second version literal, or raise at import or in `main` because version strings differ.
7. Mark `TP-LOG-*` have while `src/` does not construct the logger.
8. Invent a thread, a timeout, a Control-C protocol, or exit 130 in order to satisfy this file.
9. Drop the console failure sentence because a log line exists.
10. Print `in_venv`, `in_pyenv`, or `in_conda` on the about page, or use those booleans to choose a location line.

**Violating this rule is a critical logging regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | The construct is the statement `ChronicleLogger(...)` inside `def main`, before the parser and before `Cli` |
| AC-2 | `logName()`, `baseDir()`, and `logDir()` are read before the first `log_message` |
| AC-3 | Identity lines and `debug mode` appear only inside `isDebug()`, and the text screen does not mirror them |
| AC-4 | Missing ChronicleLogger prints the pip next step and returns non-zero |
| AC-5 | Temp write, `shutil.move` publish, and discard of an unfinished temp are logged before the operation, component `download` |
| AC-6 | Floor `ChronicleLogger>=1.2.3` matches `pyproject.toml`. The package does not re-export the library |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-packaging` | Floor owner. Live manifest lags |
| `requirement-runtime-prerequisites` | Floor and the missing-import next step |
| `requirement-python-cli-interface` | When the text screen opens. Parser order |
| `requirement-python-tui` | Screen that must stay quiet |
| `requirement-python-oop` | Logger parameter on every class |
| `requirement-python-error-handling` | Console failure sentences |
| `requirement-python-coding-style` | `shutil.move` and temps |
| `requirement-download-ytdlp-pipeline` | Download steps that write those lines |
| `requirement-python-about` | Host-check path reads. `TP-ABOUT-16` proves the three logger booleans |
| `requirement-class-software-dev` | Residual pointer |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-LOG-01** | `tests/test_logging.py` | todo | One construct in `main`. `logName` / `baseDir` / `logDir` read back. Resolved name is `anime-dlp` |
| **TP-LOG-02** | `tests/test_logging.py` | todo | `DEBUG` already on shows identity lines and `debug mode` on a non-screen run. Unset shows neither. A text-screen run does not mirror those lines. The daily file still receives them |
| **TP-LOG-03** | `tests/test_logging.py` | todo | The product creates no threads. A later thread logs create, start, join, wait, lock, and pool before the blocking call, and does not call `log_message` under a work lock |
| **TP-LOG-04** | `tests/test_logging.py` | todo | Each class `__init__` logs `instantiated` at INFO, component the class name, outside `isDebug()` |
| **TP-LOG-05** | `tests/test_logging.py` | todo | Temp write, publish, and discard are logged before the operation, component `download` |
| **TP-ABOUT-16** | `tests/test_about.py` | have | `in_venv`, `in_pyenv`, and `in_conda` call the one logger and do not select location lines. Primary owner is `requirement-python-about` |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | ChronicleLogger construct for AnimeDlp. Ship unit does not construct it yet. Floor target `ChronicleLogger>=1.2.3`. Live manifest remains `ChronicleLogger>=1.2.3` |
| 2026-10-04 | Active 1.0.1 | Product version **1.1.0**. Manifest floor is `ChronicleLogger>=1.2.3`. `cli.py` reads `__version__` only |
| 2026-10-04 | Active 1.0.2 | Rule 11c: environment checks read the one logger. Current version string is **1.1.0**. `TP-LOG-*` stay todo. `TP-ABOUT-16` is have. Primary owner is `requirement-python-about` |
| 2026-10-05 | Active 1.0.3 | Specialized from the VideoJoin bootstrap. Component `join` removed. Download steps use `download`. Logger floor matches `pyproject.toml` (`ChronicleLogger>=1.2.3`) |

---

**Last Updated**: 2026-10-05
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
