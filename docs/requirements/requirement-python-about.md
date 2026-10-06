**file**: docs/requirements/requirement-python-about.md
**Status**: Active (Version 1.0.2)
**Area**: python
**Key**: `requirement-python-about`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the about page for AnimeDlp. Menu action **about** returns one text page: the product identity lines, a host check, and a star-bordered box. This file names every line and the read that fills it.

The screen that shows the page stays on `requirement-python-tui`. The domain sentence stays on `requirement-domain-animedlp`. The version string stays the single `__version__` on `requirement-python-packaging`. `--version` stays a one-line human string on `requirement-python-cli-interface`. This product does not claim `--json`. This file does not open the menu, download a file, or write a JSON object.

Pyenv and conda path reads for this page stay in this file. This product does not add `requirement-python-pyenv` or `requirement-python-conda`.

### 1.1 Human-facing

**In one sentence:** On the text menu, choose **about** and the page names this build, this computer, and where the program is running from.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person reading the about page | Menu row **83 about**, under **8** self-management |
| The other role | The text-menu result page | `requirement-python-tui` draws it and scrolls it |
| Not this file | The download, the pip rows, and a JSON object | Domain, CLI, and the absent JSON requirement |

| Includes | Excludes |
|----------|----------|
| Identity lines, the host-check lines, and the star box | A second about layout, a remote version lookup |
| How each value is read on this machine | Running `python2` or `python3` to ask their version |
| Install kind: global, local, or uninstalled | An install command while this product has no download URL |
| Pyenv and conda path reads used by the location lines | A separate pyenv or conda requirement |

| Surface | What you open | What for |
|---------|---------------|----------|
| `anime-dlp` | text menu on a terminal | Choose **8**, then **83**, or type `about` |
| `anime-dlp about` | the same page, no front-board pick | No folder prompt and no file prompt |
| `src/AnimeDlp/about_page.py` | class `AboutPage` | The page text. It calls `CheckSystem` for the host check |
| `src/AnimeDlp/check_system.py` | class `CheckSystem` | Host-check reads, including pyenv and conda paths |
| `tests/test_about.py` | suite | The lines and the reads |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open about | The menu stays in the result page. The page starts with the product name and the domain sentence, then the host check, then the star box. Up and Down scroll when the page is longer than the screen. Any other key returns to the menu. | `anime-dlp`, then `8`, then `83` |
| Read the install sentence | A checkout under `src/AnimeDlp` with `pyproject.toml` above it says UNINSTALLED. A copy under your home directory says LOCAL INSTALLED. A copy under `/usr`, `/opt`, or `/bin` says GLOBAL INSTALLED. | Same page |
| Read the pyenv lines | When this login has pyenv and is not under conda, `python2 location` and `python3 location` are paths inside that root. `pyenv location` is `bin/pyenv`, not `libexec/pyenv`. | `anime-dlp about` |
| Read the conda lines | When this login has conda, `python2 location` and `python3 location` are paths inside the conda prefix. `conda location` is `bin/conda`, not `condabin/conda`. An active prefix does not borrow the base interpreter. | `anime-dlp about` |
| Read the run lines | After `Location`, the check names this process id, the cache folder in use and its three candidates, the persistence directory, and whether stdout is a terminal. | Same page |

## 2. Core Rules (Mandatory)

1. **One page.** Menu action **about** and the verb `anime-dlp about` **MUST** show one result page whose body is this file. The verb **MUST NOT** ask for a folder or a file. The page **MUST** be three blocks in this order: identity, host check, star box. A blank line **MUST** separate the blocks. The page **MUST NOT** be `--version`. Without a terminal, that page **MUST** be the whole of standard output. This product does not claim `--json`. The page **MUST NOT** gain a JSON stream.
2. **Identity block.** The first four lines **MUST** be, in order: `{APP_NAME} {version}`, `Domain: CLI downloader/extractor for supported anime video sites`, `Runtime tools: Python deps + yt-dlp`, `Entry points: anime-dlp, python -m AnimeDlp`. `{version}` **MUST** be the package version string `__version__`. The domain sentence **MUST** stay the sentence on `requirement-domain-animedlp`. The runtime-tools line is static. It **MUST NOT** be a live `ffmpeg` or `yt-dlp` probe. The page **MUST NOT** name `py-tui`. It **MUST NOT** print `python -m pip install` or an author email.
3. **Host-check header.** The check **MUST** start with `{local stamp} {APP_NAME}(v{version})  [CHECK SYSTEM]:` and the next line **MUST** be two spaces then `Now checking your operation system!`. The stamp **MUST** be local time `YYYY-MM-DD HH:MM:SS.ffffff` from `datetime.datetime.now()`. There are two spaces before `[CHECK SYSTEM]:`.
4. **Host-check fields.** After the header, the page **MUST** print these labels in this order, each starting with four spaces, then the label, a colon, a space, and the value. A missing value **MUST** leave the line in place. The check **MUST NOT** spawn `python2`, `python3`, `conda`, `pyenv`, or `id`.

| Label | Read |
|-------|------|
| `Python` | `platform.python_version()`. When `sys.version` contains `[PyPy ` and `with`, append ` (` plus the text after `[` and before `with`, stripped, plus `)`. |
| `C Library` | Compiler token from `sys.version`, brackets removed. See rule 5. |
| `Operation System` | `platform.freedesktop_os_release()["PRETTY_NAME"]` when that call works and the name is non-empty. Otherwise `platform.platform()`. |
| `Architecture` | See rule 6. |
| `Current User` | Environment `USER`, else `USERNAME`, else `getpass.getuser()`. On failure, empty. |
| `Shell` | Environment `SHELL`, else empty. |
| `Python Executable` | Basename of `sys.executable`. Split on `/` or `\`. Empty when `sys.executable` is empty. |
| `python2 location` | Rule 15, then rule 16, otherwise `shutil.which("python2")`, else empty. |
| `python3 location` | Rule 15, then rule 16, otherwise `shutil.which("python3")`, else empty. |
| `conda location` | When the check is under conda, `{root}/bin/conda` from rule 15. Otherwise `shutil.which("conda")`, else empty. |
| `pyenv location` | When the check is under pyenv and not forced onto conda for that name, `{root}/bin/pyenv` from rule 16. Otherwise `shutil.which("pyenv")`, else empty. |
| `Inside docker container` | `True` when `/.dockerenv` exists, otherwise `False`. Python’s `True` / `False` spelling. No other container probe. |
| `Cython String` | `sysconfig.get_config_var("SOABI")`, else empty. The label stays `Cython String`. |
| `Binary Type` | `{arch}-{libc}` when both are non-empty. `{arch}-` when libc is empty. Empty when arch is empty. |
| `Location` | The program path from rule 8. The same path **MUST** be the indented path inside the star box. |
| `PID` | `os.getpid()` as decimal text. |
| `Cache folder used` | Rule 17. The page **MUST NOT** create the cache directories. |
| `Cache folder (preferred)` | Rule 17. |
| `Cache folder (1st fallback)` | Rule 17. |
| `Cache folder (2nd fallback)` | Rule 17. The leaf has no username. |
| `Persistence storage` | Rule 17. Durable data. Not the user bin. Not the cache. The language leaf lives under this directory. This read **MUST NOT** create it. |
| `TTY / Interactive` | `yes` when `sys.stdout.isatty()` is true, otherwise `no`. This line does not measure stdin and does not choose the menu. |

5. **C Library parse.** Start from `sys.version`. If it contains a newline, keep the second line. Otherwise, if it contains `[` and `]`, keep the text between the first `[` and the first `]`. If that text is exactly `GCC`, use `[GCC]`. If it contains ` (Red Hat`, cut at that phrase and append `]`. If the probe (the extracted text when it still contains `[PyPy `, otherwise the original `sys.version`) contains `[PyPy ` and `with`, the compiler text is `[` plus the text after `with `. Strip one pair of surrounding `[` `]` before display.
6. **Architecture.** If `sys.version` contains `AMD64`, the arch is `amd64`. Else if it contains `AMD32`, the arch is `x86`. Else map `platform.machine()` ignoring case: `x86_64` and `amd64` → `amd64`; `aarch64` and `arm64` → `arm64`; `i386`, `i686`, and `x86` → `x86`. Any other machine name is kept as `platform.machine()` returned it.
7. **Libc token.** Read `platform.libc_ver()[0]`, or `unknown` when that call fails. If `sys.version` contains `AMD64` or `AMD32` and also `MSC`, the token is `msc`. If `sys.version` contains `clang` in any letter case, the token is `clang`. If the token is still empty and `SHELL` is `/bin/ash`, the token is `muslc`.
8. **Program path.** If `sys.argv[0]` is an existing file and its basename is the console script or `AnimeDlp`, use its real path. If it is an existing file in the same directory as `cli.py` and the basename is `cli.py` or `__main__.py`, use that real path. Otherwise use the real path of `cli.py`.
9. **Install kind.** Classify that real path in this order. A path under `site-packages` or `dist-packages` is packaged.
   - Not packaged, the path contains `{sep}src{sep}AnimeDlp{sep}`, and a parent within eight levels has `pyproject.toml`: **uninstalled**.
   - Under the home directory, and packaged or the basename is the console script or `AnimeDlp`: **local**.
   - Starts with `/usr/`, `/opt/`, or `/bin/`: **global**.
   - Packaged and not under the home directory: **global**.
   - Otherwise: **uninstalled**.
10. **Star box sentences.** **global** **MUST** say `You are using the GLOBAL INSTALLED version, location:`. **local** **MUST** say `You are using the LOCAL INSTALLED version, location:`. **uninstalled** **MUST** say `You are using an UNINSTALLED version, location:`.
11. **Star box lines.** Inside the border, in order: the title `{APP_NAME} ({version}) by {author} on {date}`; a blank line; the install sentence; four spaces and the program path; a blank line; `Basic Usage:`; four spaces and the usage line; a blank line; `Please visit our homepage: `; four spaces, a double quote, the homepage, and a double quote; then the trailing blanks from rule 12. `{version}` **MUST** be the package version string. **MUST NOT** split it into `MAJOR`, `MINOR`, and `PATCH` integers. Author, date, homepage, and usage are the constants in Implementation Notes.
12. **Border.** Take the lines of rule 11. When the download URL is empty and the homepage is non-empty, print the first twelve of those source lines (through the second blank after the homepage). When both are empty, print the first eleven. When the download URL is non-empty, the source list uses `Installation command:` and `    curl -fsSL {url} | {python basename}` in place of the extra blanks, and the print stops before the final blank. Pad every printed line on the right to the longest printed line. The top and bottom borders are that width plus four asterisks. Each body row is `* `, the padded line, ` *`. One all-space body row sits under the top border and one sits above the bottom border.
13. **No install channel on this page.** The product download URL **MUST** stay empty while no Active install requirement names a channel. The live about page **MUST NOT** contain `curl -fsSL`. The box **MAY** render that install line only when a caller passes a non-empty URL. This product’s about caller **MUST NOT** pass one. Pip install stays on rows 84–87. It is not a line of this page.
14. **No privilege and no network.** Building the page **MUST NOT** call `sudo`, wrap `apt` or `dnf`, create an account, open a socket, or recommend `sudo pip` or `sudo curl | sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`.
15. **Conda paths.** Under conda means `conda_root()` is non-empty. A non-empty `CONDA_EXE` is the only candidate: its parent directory name **MUST** be `bin` or `condabin`, and `{root}/bin/conda` **MUST** exist (`lexists`, a symlink counts). Otherwise a non-empty `CONDA_PREFIX`: the prefix itself when it has `bin/conda`, otherwise `{root}` when the prefix is `{root}/envs/{name}` and that root has `bin/conda`. Otherwise the first of `~/miniconda3`, `~/anaconda3`, `~/miniforge3`, and `~/mambaforge` that has `bin/conda`. `conda location` **MUST** be `{root}/bin/conda`, not `condabin/conda`. The active prefix is `CONDA_PREFIX` when that path is the root or `{root}/envs/{name}`. Otherwise the prefix is the root. `python2` and `python3` are `{prefix}/bin/{name}` when that file exists. A missing interpreter stays empty. The active prefix **MUST NOT** borrow the base interpreter. Conda wins over pyenv for `python2`, `python3`, and `conda`.
16. **Pyenv paths.** Under pyenv means `pyenv_root()` is non-empty and the name was not taken by rule 15. A non-empty `PYENV_ROOT` is the only candidate and **MUST** contain `bin/pyenv`. Otherwise `~/.pyenv` when that directory contains `bin/pyenv`. Otherwise not under pyenv. `pyenv location` **MUST** be `{root}/bin/pyenv`, not `libexec/pyenv`. Selected versions come from `PYENV_VERSION` when it is non-empty, split on `:`, otherwise the lines of `{root}/version`. Skip blank, `system`, `.`, `..`, and any token that contains `/` or `\`. `python2` and `python3` are `{root}/versions/{version}/bin/{name}` for the first selected version where that file exists. Otherwise `{root}/shims/{name}` when that shim exists. Otherwise empty.
17. **Run lines.** The username segment is the `Current User` value. The pid segment is the `PID` value. `{APP_NAME}` is `AnimeDlp`.
    - **Home.** Environment `HOME` when it is set and non-blank. Otherwise `os.path.expanduser("~")` when that result is an absolute path. Otherwise there is no home.
    - **Preferred leaf.** When the username is non-empty, `cache-{APP_NAME}-{username}-{pid}`. When it is empty, `cache-{APP_NAME}-{pid}`.
    - **Preferred path.** `/dev/shm/cache/` plus the preferred leaf.
    - **1st fallback.** `/tmp/cache/` plus the preferred leaf.
    - **2nd fallback.** `{home}/.cache/cache-{APP_NAME}-{pid}` when home exists. No username in that leaf. Empty when home does not exist. The line stays.
    - **Used.** The preferred path when `/dev/shm` is a directory. Otherwise the 1st fallback when `/tmp` is a directory. Otherwise the 2nd fallback. Building the page **MUST NOT** call `os.mkdir` or `os.makedirs`.
    - **Persistence storage.** `{home}/.local/{APP_NAME}` when home exists. Empty when it does not. The line stays.
18. **Environment booleans.** `in_venv`, `in_pyenv`, and `in_conda` **MUST** call `inVenv()`, `inPyenv()`, and `inConda()` on the one logger (`requirement-python-cli-logging`). When the logger is absent, each **MUST** return false. Those three results **MUST NOT** be printed on this page and **MUST NOT** choose a location line.
19. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`.
20. Dest fence conditions: **considered — none**. Do not invent one.
21. The host-check methods named in `requirement-python-oop` **MUST** be methods of class `CheckSystem` in `src/AnimeDlp/check_system.py`. This file still owns the line text. Class `AboutPage` in `src/AnimeDlp/about_page.py` is the about composer. It **MUST** call `CheckSystem` for the check block and for `self_location`. `Cli` writes `CheckSystem(...)` and then `AboutPage(...)`. `AboutPage` **MUST NOT** construct `CheckSystem`.

### 2.1 Sample shape

Values in angle brackets are the live read. They are not a frozen login or home path.

```text
AnimeDlp 1.1.0
Domain: CLI downloader/extractor for supported anime video sites
Runtime tools: Python deps + yt-dlp
Entry points: anime-dlp, python -m AnimeDlp

2026-10-04 11:16:23.700590 AnimeDlp(v1.1.0)  [CHECK SYSTEM]:
  Now checking your operation system!
    Python: 3.12.3
    C Library: GCC 13.3.0
    Operation System: Ubuntu 24.04 LTS
    Architecture: amd64
    Current User: <login>
    Shell: /bin/bash
    Python Executable: python3
    python2 location: <python2 inside conda or pyenv, or empty>
    python3 location: <python3 inside conda or pyenv, or empty>
    conda location: <conda root>/bin/conda
    pyenv location: <pyenv root>/bin/pyenv
    Inside docker container: False
    Cython String: cpython-312-x86_64-linux-gnu
    Binary Type: amd64-glibc
    Location: <program path>
    PID: <pid>
    Cache folder used: /dev/shm/cache/cache-AnimeDlp-<login>-<pid>
    Cache folder (preferred): /dev/shm/cache/cache-AnimeDlp-<login>-<pid>
    Cache folder (1st fallback): /tmp/cache/cache-AnimeDlp-<login>-<pid>
    Cache folder (2nd fallback): <home>/.cache/cache-AnimeDlp-<pid>
    Persistence storage: <home>/.local/AnimeDlp
    TTY / Interactive: <yes or no>

***************************************************
*                                                 *
* AnimeDlp (1.1.0) by Wilgat Wong on 2026-10-04  *
*                                                 *
* You are using an UNINSTALLED version, location: *
*     <program path>                              *
*                                                 *
* Basic Usage:                                    *
*     anime-dlp <url>                            *
*                                                 *
* Please visit our homepage:                      *
*     "https://github.com/Wilgat/AnimeDlp"       *
*                                                 *
*                                                 *
*                                                 *
***************************************************
```

The version string in the sample is the package version at the time of writing. A later package version **MUST** appear instead. The stamp **MUST** be the clock at the moment the page is built. `<login>`, `<pid>`, `<home>`, and `<yes or no>` are the live reads. They are not a frozen login or home path. When `/dev/shm` is not a directory, `Cache folder used` is the 1st fallback or the 2nd fallback under rule 17. The sample shows the case where used equals preferred.

Invocation: `anime-dlp` on a terminal, then `8`, then `83`. The same page is `anime-dlp about` with no terminal.

### 2.2 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Page builder** | Class `AboutPage` in `src/AnimeDlp/about_page.py` (`framework_about`) |
| **Host check** | Class `CheckSystem` in `src/AnimeDlp/check_system.py` |
| **Pyenv paths** | Rule 16. Not a separate requirement |
| **Conda paths** | Rule 15. Not a separate requirement |
| **Star box** | `AboutPage.about_box_lines` calls `CheckSystem` for `self_location` and the Python executable name |
| **Menu hook** | Row 83 and `anime-dlp about` use `AboutPage.framework_about` |
| **APP_NAME** | `AnimeDlp` |
| **Console script** | `anime-dlp` |
| **Author** | `Wilgat Wong` |
| **Homepage** | `https://github.com/Wilgat/AnimeDlp` |
| **About date** | `2026-10-06` (`Cli.LAST_UPDATE`). This is the box date, not the host-check stamp |
| **Usage line** | `anime-dlp <url>` (`Cli.BASIC_USAGE`) |
| **Download URL** | empty (`Cli.DOWNLOAD_URL`) |
| **Docker marker** | `/.dockerenv` only |
| **PID** | `os.getpid()` |
| **Cache folders** | Preferred `/dev/shm/cache/…`, 1st `/tmp/cache/…`, 2nd `{home}/.cache/…` with no username. Used follows rule 17. The page does not create them |
| **Persistence storage** | `{home}/.local/AnimeDlp` |
| **TTY / Interactive** | `yes` or `no` from `sys.stdout.isatty()` |
| **JSON** | Not claimed. No `--json` stream |
| **Privilege** | normal user privilege |
| **Product version** | `1.1.0` |

### 2.3 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): one page owns the about lines and the reads that fill them.
- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): each label names one read. The install kind is three named sentences.
- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): missing tools stay blank. The page does not run interpreters or open the network.
- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): a person opens the page from the menu. `--version` stays the short line.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** building the about page **MUST NOT** call `sudo`, wrap `apt` / `dnf`, create a dedicated account, or recommend `sudo pip` or `sudo curl \| sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`. The page only reads the local interpreter, environment, and files.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A missing `python2`, `conda`, or `pyenv` is an empty location, not an error.
- **Intentional:** Field order and the three install sentences are named.
- **Anti-fragile:** A source checkout, a home install, and a `/usr` install each get a sentence from the same path rules.
- **Over-protect (Principle 20):** Do not add a second about page, and do not print a `curl | sh` line while the download URL is empty.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

- Drop a host-check label or change its order.
- Replace `shutil.which` with a subprocess that runs `python2`, `python3`, `conda`, or `pyenv`.
- Report `{root}/libexec/pyenv` as `pyenv location` when `{root}/bin/pyenv` exists.
- Report `{root}/condabin/conda` as `conda location` when `{root}/bin/conda` exists.
- Let an active conda prefix borrow a base `python2` or `python3`.
- Probe containers by anything other than `/.dockerenv`.
- Show GLOBAL, LOCAL, or UNINSTALLED for a path the rules in this file classify differently.
- Put `curl -fsSL` on the live about page while the download URL is empty.
- Put `python -m pip install` or a live `ffmpeg` or `yt-dlp` PATH probe on this page.
- Turn this page into `--version` or into a JSON object.
- Add `--json` for this page.
- Split the package version into `MAJOR`, `MINOR`, and `PATCH` for the star-box title.
- Emit the `[CHECK SYSTEM]:` block through ChronicleLogger.
- Print `in_venv`, `in_pyenv`, or `in_conda`, or use those booleans to choose a location line.
- Name `py-tui` on the page.
- Freeze a Unix login or a `/home/<login>/…` path into this requirement.
- Drop `PID`, the four cache-folder lines, `Persistence storage`, or `TTY / Interactive`, or print them before `Location`.
- Create the cache directories or the persistence directory while building this page.
- Run `id` to fill `Current User` or a cache leaf.
- Construct `CheckSystem` inside `AboutPage`.

## 5. Design-time verification

| ID | Suite | Status |
|----|-------|--------|
| TP-ABOUT-01 | `tests/test_about.py` | have |
| TP-ABOUT-02 | `tests/test_about.py` | have |
| TP-ABOUT-03 | `tests/test_about.py` | have |
| TP-ABOUT-04 | `tests/test_about.py` | have |
| TP-ABOUT-05 | `tests/test_about.py` | have |
| TP-ABOUT-06 | `tests/test_about.py` | have |
| TP-ABOUT-07 | `tests/test_about.py` | have |
| TP-ABOUT-08 | `tests/test_about.py` | have |
| TP-ABOUT-09 | `tests/test_about.py` | have |
| TP-ABOUT-10 | `tests/test_about.py` | have |
| TP-ABOUT-11 | `tests/test_about.py` | have |
| TP-ABOUT-12 | `tests/test_about.py` | have |
| TP-ABOUT-13 | `tests/test_about.py` | have |
| TP-ABOUT-14 | `tests/test_about.py` | have |
| TP-ABOUT-16 | `tests/test_about.py` | have |

There is no TP-ABOUT-15. This product does not claim `--json`.

TP-ABOUT-01 asserts the identity line, every host-check label, the star-box title, `anime-dlp <url>`, and that the live page has no `curl -fsSL`, no `py-tui`, no `ffmpeg is on PATH`, and no `python -m pip install`. TP-ABOUT-02 asserts the stamp `YYYY-MM-DD HH:MM:SS.ffffff`, the `[CHECK SYSTEM]:` header, and the field order. TP-ABOUT-03 asserts the star box is one rectangle and that a global path uses the GLOBAL sentence. TP-ABOUT-04 asserts an explicit download URL renders the install line, and that the product URL stays empty. TP-ABOUT-05 asserts the GCC token, the PyPy token, the arch map, `msc`, `clang`, `muslc`, and `amd64-glibc`. TP-ABOUT-06 asserts checkout = uninstalled, a home copy = local, and `/usr` = global. TP-ABOUT-07 asserts the docker marker file and a missing `which` result. TP-ABOUT-08 asserts a long about page scrolls to `Basic Usage:` and a one-line result still closes on Down. TP-ABOUT-09 and TP-ABOUT-10 assert the pyenv paths in rule 16. TP-ABOUT-11 and TP-ABOUT-12 assert the conda paths in rule 15. TP-ABOUT-13 asserts `PID`, the four cache lines, persistence, and `TTY / Interactive` on the page, and that building the check does not create those directories. TP-ABOUT-14 asserts used follows `/dev/shm`, then `/tmp`, then the 2nd fallback, and that the 2nd leaf has no username. TP-ABOUT-16 asserts `in_venv`, `in_pyenv`, and `in_conda` call the logger and do not select location lines.

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`.

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-domain-animedlp.md` | Domain sentence on the identity block |
| `docs/requirements/requirement-python-tui.md` | Result page; scroll; row 83 |
| `docs/requirements/requirement-python-oop.md` | Class `CheckSystem` owns the host-check reads. Class `AboutPage` owns the composer |
| `docs/requirements/requirement-python-cli-logging.md` | `in_venv`, `in_pyenv`, and `in_conda` read the one logger. They are not printed |
| `docs/requirements/requirement-python-cli-interface.md` | `--version` stays the short human line. The verb `about` is named there |
| `docs/requirements/requirement-python-cli-language.md` | The about page stays English. The leaf short `about` stays English |
| `docs/requirements/requirement-python-packaging.md` | The version string in the title and the stamp |
| `docs/requirements/requirement-runtime-prerequisites.md` | Pip dependencies. This page does not probe ffmpeg |
| `docs/requirements/requirement-class-software-dev.md` | Approver none; no dest fence |
| `src/AnimeDlp/about_page.py` | Class `AboutPage`. `framework_about` |
| `src/AnimeDlp/check_system.py` | Class `CheckSystem` |
| `pyproject.toml` | Homepage URL and the version string |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | About page: identity, host check, star box. Pyenv and conda reads stay here. No `--json`. Product version **1.1.0**. `./tests/run.sh` — 23 tests, OK. `TP-ABOUT-01` through `TP-ABOUT-14` and `TP-ABOUT-16` are have. There is no `TP-ABOUT-15` |
| 2026-10-05 | Active 1.0.1 | Specialized from the VideoJoin bootstrap. Domain line is the anime downloader. The page does not probe ffmpeg |
| 2026-10-06 | Active 1.0.2 | The about box date is `2026-10-06`. The host-check stamp is the time of the capture |

**Last Updated**: 2026-10-06
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
