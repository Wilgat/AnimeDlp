**file**: docs/requirements/requirement-python-project-structure.md  
**Status**: Active (Version 1.0.3)  
**Area**: python  
**Key**: `requirement-python-project-structure`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the **repository layout** and package structure for AnimeDlp as a Python package project: where source, packaging, and requirements law live.

---

## 2. Core Rules (Mandatory)

### 2.1 Source package layout

1. **MUST** keep the installable package under **`src/AnimeDlp/`**.  
2. **MUST** include `__init__.py` (version export), `__main__.py` (module entry), and thin `cli.py` (argparse + dep gates + exit map).  
3. **MUST** keep download/extract implementation outside a fat `cli.py` (`downloader.py` coordinator, `download_service.py`, `extractors/`).  
4. **MUST NOT** scatter a second installable package name that contradicts packaging SSOT without an explicit rename plan.

### 2.2 Project root layout

5. **MUST** keep `pyproject.toml` at repository root.  
6. **MUST** keep product user docs at root **`README.md`**.  
7. **MUST** keep specialized product law under **`docs/requirements/`** with `requirement-` prefix and registry `index.md`.  
8. Product design notes **MAY** live under `docs/` without becoming requirement law unless registered.

### 2.3 Generated / non-source

9. **MUST NOT** commit `build/` or `dist/` artifacts as product source of truth.  
10. Egg-info / `__pycache__` / compiled artifacts **MUST** remain ignore-friendly (gitignore).  
11. Optional Cython/`build.sh` tooling **MAY** exist as maintainer tooling; it **MUST NOT** replace `src/AnimeDlp` as runtime package SSOT.

### 2.4 Requirements surface discipline

12. All product-law files **MUST** use basename prefix `requirement-`.  
13. **MUST** register every Active requirement in `docs/requirements/index.md`.  
14. Product source comments that cite law **MUST** cite live `requirement-*.md` keys only — never templates or skills as behavioral authority.

### 2.5 Implementation Notes (this project)

| Path | Role |
|------|------|
| `src/AnimeDlp/` | Installable package |
| `src/AnimeDlp/cli.py` | Thin CLI entry (argparse, dep gates, exit map) |
| `src/AnimeDlp/downloader.py` | L2 coordinator (`Anime1Downloader`) |
| `src/AnimeDlp/download_service.py` | `YtDlpDownloadService` |
| `src/AnimeDlp/extractors/me.py` | `Anime1MeExtractor` |
| `src/AnimeDlp/extractors/pw.py` | `Anime1PwExtractor` |
| `src/AnimeDlp/errors.py` | `AnimeDlpError` |
| `src/AnimeDlp/util.py` | Pure helpers (sanitize, redaction) |
| `src/AnimeDlp/please_wait.py` | Download line: flashing bullet, saved-language please wait, file count, percent finished, time until finish |
| `src/AnimeDlp/mpv_stream.py` | `MpvStream`: mplayer2 detection and one media URL played by mpv, with no saved file |
| `src/AnimeDlp/tui.py` | Text menu session (`Tui`) |
| `src/AnimeDlp/menu_painter.py` | Menu frame (`MenuPainter`) |
| `src/AnimeDlp/menu_model.py` | Keystroke state (`MenuModel`) |
| `src/AnimeDlp/menu_session.py` | Menu loop (`MenuSession`) |
| `src/AnimeDlp/menu_language.py` | Menu language (`MenuLanguage`) |
| `src/AnimeDlp/system_log.py` | Log folder actions (`SystemLog`) |
| `src/AnimeDlp/self_management.py` | Pip lifecycle (`SelfManage`) |
| `src/AnimeDlp/about_page.py` | About page (`AboutPage`) |
| `src/AnimeDlp/check_system.py` | Host check for the about page (`CheckSystem`) |
| `src/AnimeDlp/__init__.py` | `__version__` + public `main` |
| `src/AnimeDlp/__main__.py` | Module entry |
| `pyproject.toml` | Packaging SSOT |
| `build.sh` | Maintainer build/release helper |
| `cy-master` / `cy-master.ini` | Optional Cython/maintainer tooling (not runtime SSOT) |
| `docs/requirements/` | Product law |
| `README.md` | User documentation |
| `tests/` | Executable suites (proof; not law) |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Layout is explicit.  
- **Principle 5 – SSOT**: One package path, one requirements registry.  
- **Principle 17 – Storage**: Generated dirs not confused with source.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not invent parallel packages.  
- **Intentional:** `src/` layout for packaging.  
- **Anti-fragile:** Clear ignore of build debris.  
- **Over-protect:** Requirements registry discipline.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Move the installable package out of `src/AnimeDlp/` without packaging update.  
2. Delete `docs/requirements/index.md` discipline.  
3. Commit secrets under `src/` or `docs/requirements/`.  
4. Cite templates/skills from product source as product law.  
5. Treat maintainer Cython binaries as the only runtime ship unit for end users.

**Violating this rule is a critical structure regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Package at `src/AnimeDlp/` |
| AC-2 | `cli.py`, `__init__.py`, `__main__.py` present |
| AC-3 | `docs/requirements/index.md` registry exists |
| AC-4 | Root `pyproject.toml` + `README.md` present |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-packaging` | Manifest |
| `requirement-python-cli-interface` | Entry modules |
| `requirement-python-system-architecture` | Architecture boundaries |
| `requirement-python-classes` | Module/class map |
| `requirement-class-software-dev` | Class residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-STRUCT-01** | path inventory | **have** | expected package files exist |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Layout law for AnimeDlp |
| 2026-08-11 | Active 1.0.0 | Thin cli + downloader/helpers; L2 target modules |
| 2026-08-11 | Active 1.0.0 | L2 modules on disk; product **1.3.0** |
| 2026-10-05 | Active 1.0.1 | `please_wait.py` draws the file count, the percent finished, and the time until finish |
| 2026-10-07 | Active 1.0.3 | `mpv_stream.py` plays one extracted media URL in mpv and does not save a file |
| 2026-10-06 | Active 1.0.2 | That line also draws the saved-language please-wait phrase |

---

**Last Updated**: 2026-10-07  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
