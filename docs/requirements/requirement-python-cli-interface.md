**file**: docs/requirements/requirement-python-cli-interface.md  
**Status**: Active (Version 1.1.0)  
**Area**: python  
**Key**: `requirement-python-cli-interface`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the official **command-line entry points**, **argument contract**, and **startup gates** for the AnimeDlp Python package.

Domain catalog is owned by **`requirement-domain-animedlp`**. Download ops are owned by **`requirement-download-ytdlp-pipeline`**.

---

## 2. Core Rules (Mandatory)

### 2.1 Entry points

1. **MUST** expose a console script entry named **`anime-dlp`** pointing at `AnimeDlp.cli:main` (declared in packaging SSOT).  
2. **MUST** support module execution: **`python -m AnimeDlp`**.  
3. **MUST** keep `main()` as the single runtime entry for argument parse + downloader run (thin package surface).  
4. **MUST NOT** require root or sudo to run the CLI.

### 2.2 Empty argv / missing URL (Type N)

5. **MUST** treat bare invocation with no URL as the text menu when stdout is a terminal, and as usage help with exit 0 when stdout is not a terminal. That path is not Type O online install-ensure.  
6. **MUST NOT** default empty argv to shell channel install or self-update.  
7. `--debug` and `--verbose` with no URL **MUST** still open the text menu on a terminal. A page URL **MUST** download or extract and **MUST NOT** open the text menu. `--help` and `--version` **MUST NOT** open the text menu.

### 2.3 Required and optional arguments

| Arg | Form | Required | Behavior |
|-----|------|----------|----------|
| URL | positional `url` | no | Source page from a supported host. Omit it to open the text menu on a terminal |
| Verbose | `-v` / `--verbose` | no | Debug logging + yt-dlp verbose |
| Extract only | `-x` / `--extract` | no | Print sources; no download |
| Cloudflare | `-cf` / `--cloudflare` | no | `cf_clearance` cookie value |
| User-Agent | `-ua` / `--user-agent` | no | Custom User-Agent string |

8. **MUST** document that for Cloudflare-protected pages, providing **both** custom User-Agent and `cf_clearance` together (or neither) is the supported assist pattern when the ship unit enforces that pairing.  
9. **MUST** fail closed when the host is not a supported anime1 host (domain peer).

### 2.4 Startup dependency gates

10. Before running the downloader, **MUST** fail closed with actionable messages if required Python modules are missing: `requests`, `beautifulsoup4`/`bs4`, `lxml`, `yt_dlp`.  
11. **MUST** initialize product logging via **ChronicleLogger** when that dependency is the declared logging path.  
12. **MUST NOT** continue into network extract when critical import gates failed.

### 2.5 Output behavior

13. Extract mode **MUST** print human-readable title/URL/(cookie) blocks.  
14. Download mode **MUST** emit progress via logger for each title.  
15. **MUST NOT** mix machine-only JSON mode into normal runs unless a `--json` mode is explicitly implemented and documented.

### 2.6 Non-interactive environments

16. With a page URL, the CLI does not prompt. It is suitable for scripts. With no URL and no terminal, it prints help and returns 0. It does not wait for stdin.  
17. Network failures **MUST** surface via logger/exit rather than hanging on stdin prompts. The text menu is the interactive path and is owned with `requirement-python-tui`.

### 2.7 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Console script** | `anime-dlp = AnimeDlp.cli:main` |
| **Module entry** | `src/AnimeDlp/__main__.py` → `main()` |
| **CLI module** | `src/AnimeDlp/cli.py` |
| **Empty argv** | Terminal: text menu. No terminal: help, exit 0 |
| **Argparse** | implemented (`ArgumentParser`) |
| **Quiet/JSON flags** | not implemented today |
| **Privilege** | user-level only |
| **Ship CLI SSOT** | `src/AnimeDlp/cli.py` |
| **Startup gates** | import checks for requests, BeautifulSoup, lxml, yt_dlp → FATAL + exit 1 |
| **Logger** | `ChronicleLogger(logname='AnimeDlp')` |
| **Class runner** | `Anime1Downloader(args, logger).run()` |
| **User docs** | Root `README.md` Usage / Options / Examples must match this contract |
| **Product version** | package **1.5.2** |

### 2.8 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Entry and argument surface are explicit.  
- **Principle 16 – Interactive awareness**: Non-prompt CLI; argparse owns missing args.  
- **Principle 5 – SSOT**: One CLI surface for entry contract.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Missing deps and unsupported hosts fail closed.  
- **Intentional:** Positional URL + documented flags.  
- **Anti-fragile:** Module + console script dual entry.  
- **Over-protect:** No install-ensure on empty argv.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Change empty argv to Type O online install without explicit user order and new install requirements.  
2. Remove console script or module entry without packaging + docs update.  
3. Bypass domain/pipeline peers by reimplementing download only in a second ad-hoc script as the “real” product.  
4. Require root to run normal extract/download.  
5. Drop the page-URL download without a documented replacement. The replacement for a missing URL is the text menu on a terminal and help (exit 0) with no terminal.

**Violating this rule is a critical CLI regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `anime-dlp` entry declared in packaging |
| AC-2 | `python -m AnimeDlp` works |
| AC-3 | Missing URL on a terminal → text menu. Missing URL with no terminal → help, exit 0. Not install-ensure |
| AC-4 | Flags: verbose, extract, cloudflare, user-agent |
| AC-5 | Missing Python deps → actionable FATAL messages |
| AC-6 | Unsupported host → clear error |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-domain-animedlp` | Domain workflow |
| `requirement-download-ytdlp-pipeline` | Download path |
| `requirement-python-packaging` | Console script declaration |
| `requirement-python-error-handling` | Fail-closed messaging |
| `requirement-runtime-prerequisites` | Dep modules |
| `requirement-python-tui` | Text menu opened when no URL is given on a terminal |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-CLI-01** | `tests/test_cli.py` | **have** | `--help` lists flags |
| **TP-CLI-02** | `tests/test_cli.py` | **have** | no URL and no terminal → help, exit 0 |
| **TP-CLI-04** | `tests/test_cli.py` | **have** | no URL on a terminal, and `--debug` with no URL, open the text menu |
| **TP-CLI-05** | `tests/test_cli.py` | **have** | a page URL does not open the text menu |
| **TP-CLI-03** | `tests/test_cli.py` | **have** | unsupported host rejected |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | CLI entry + argparse for AnimeDlp |
| 2026-10-05 | Active 1.0.0 | Product version cell aligned to **1.4.0** |
| 2026-10-05 | Active 1.0.0 | Product version cell aligned to **1.5.0** |
| 2026-10-05 | Active 1.1.0 | No URL on a terminal opens the text menu. No terminal prints help and returns 0 |
| 2026-10-06 | Active 1.1.0 | Product version cell aligned to **1.5.1** |
| 2026-10-07 | Active 1.1.0 | Product version cell aligned to **1.5.2** |

---

**Last Updated**: 2026-10-07  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
