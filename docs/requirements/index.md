# Requirements index

**Product:** AnimeDlp (Python CLI — extract/download from supported anime video sites)  
**Workspace state:** Specialized product law (left genesis); **software-development** class; **pip/local package** install (not shell online Type 0).  
**Product version:** **1.1.0** (align `pyproject.toml`, `__init__.__version__`, root `README.md` Version badge)  
**Updated:** 2026-08-09

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + residual stack (Python, setuptools) | class | Active | `requirement-class-software-dev.md` | 2026-08-09 |
| requirement-domain-animedlp | Domain surface SSOT (four pillars: workflow, features, help, about) | domain | Active | `requirement-domain-animedlp.md` | 2026-08-09 |
| requirement-download-ytdlp-pipeline | yt-dlp download ops SSOT (cookies, headers, retries, extract boundary) | download | Active | `requirement-download-ytdlp-pipeline.md` | 2026-08-09 |
| requirement-python-cli-interface | CLI entry points + argparse surface | python | Active | `requirement-python-cli-interface.md` | 2026-08-09 |
| requirement-python-coding-style | Python style; exports honesty; cookie/I/O conventions | python | Active | `requirement-python-coding-style.md` | 2026-08-09 |
| requirement-python-packaging | `pyproject.toml` / version / console script packaging | python | Active | `requirement-python-packaging.md` | 2026-08-09 |
| requirement-python-project-structure | Repository and `src/AnimeDlp` layout | python | Active | `requirement-python-project-structure.md` | 2026-08-09 |
| requirement-python-error-handling | Fail-closed errors; host/dep/download failures | python | Active | `requirement-python-error-handling.md` | 2026-08-09 |
| requirement-runtime-prerequisites | Pip deps + network; no root auto-install claim | runtime | Active | `requirement-runtime-prerequisites.md` | 2026-08-09 |

## Intentionally absent (by design)

| Surface | Status on AnimeDlp |
|---------|----------------------|
| Shell online install / `SCRIPT_URL` / Type O empty-argv install-ensure | **Absent** |
| Shell local `install` / `uninstall` / self-update Type 0 package | **Absent** (pip package product) |
| Type 1 sudoers / root elevation allowlist | **Absent** |
| Automatic companion `.sha256` channel integrity law | **Absent** |
| FFmpeg product-level encode pipeline | **Absent** (download product; not VideoJoin/VideoSpeed) |
| Second Active `requirement-domain-*` | **Forbidden** while domain-animedlp is Active |

**Install mode:** **pip / local package** (`anime-dlp` console script). Not dual-mode shell+pip install-ensure.

**Rules for agents:**

1. Treat rows above as the **live product-law inventory** for AnimeDlp.  
2. **Do not invent** additional `requirement-*.md` paths — verify on disk and add a registry row in the same change when creating one.  
3. Product source comments cite **only** these live requirement files — never templates/skills as behavioral authority.  
4. This versioned surface lists **requirement rows only** — do not dump templates / skills / terminologies / incidents path inventories here.  
5. Keep Status and Path in sync with each file’s header when status changes.  
6. **Class gate:** software-development requires exactly one Active `requirement-class-software-dev.md` (this registry includes it).  
7. **Domain SSOT:** exactly one Active domain file (`requirement-domain-animedlp`).  
8. **Do not introduce** online shell install or Type 1 elevation without explicit user order and registry update.  
9. Keep legal disclaimer honesty: personal/educational use; respect site ToS and applicable law.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status in sync with the file header.
