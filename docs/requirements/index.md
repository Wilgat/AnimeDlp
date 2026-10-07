# Requirements index

**Product:** AnimeDlp (Python CLI — extract/download from supported anime video sites)  
**Workspace state:** Specialized product law (left genesis); **software-development** class; **pip/local package** install (not shell online Type 0).  
**Product version:** **1.5.2** (align `pyproject.toml`, `__init__.__version__`, root `README.md` Version badge)  
**Updated:** 2026-10-07

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + residual stack (Python, setuptools) | class | Active | `requirement-class-software-dev.md` | 2026-10-07 |
| requirement-domain-animedlp | Domain surface SSOT (four pillars). A terminal download flashes a bullet, the saved-language words for please wait, the file count, the percent finished, and the time until finish | domain | Active | `requirement-domain-animedlp.md` | 2026-10-07 |
| requirement-download-ytdlp-pipeline | yt-dlp download ops SSOT (cookies, headers, retries, extract boundary). Menu stream is mpv and does not save a file | download | Active | `requirement-download-ytdlp-pipeline.md` | 2026-10-07 |
| requirement-python-cli-interface | CLI entry points + argparse surface. No URL on a terminal opens the text menu | python | Active | `requirement-python-cli-interface.md` | 2026-10-07 |
| requirement-python-tui | Text menu: download, stream to mpv when mplayer2 is detected, system-log, language, self-management, Exit | python | Active | `requirement-python-tui.md` | 2026-10-07 |
| requirement-python-coding-style | Python style; exports honesty; cookie/I/O conventions; L2 shape | python | Active | `requirement-python-coding-style.md` | 2026-08-11 |
| requirement-python-packaging | `pyproject.toml` / version / console script packaging | python | Active | `requirement-python-packaging.md` | 2026-10-07 |
| requirement-python-project-structure | Repository and `src/AnimeDlp` L2 layout, including `please_wait.py` and `mpv_stream.py` | python | Active | `requirement-python-project-structure.md` | 2026-10-07 |
| requirement-python-error-handling | Fail-closed errors; host/dep/download failures | python | Active | `requirement-python-error-handling.md` | 2026-08-09 |
| requirement-python-system-architecture | PyPI execution shape; L2 architecture (implemented) | python | Active | `requirement-python-system-architecture.md` | 2026-10-07 |
| requirement-python-classes | L2 multi-class SRP map (implemented), including `MpvStream` | python | Active | `requirement-python-classes.md` | 2026-10-07 |
| requirement-runtime-prerequisites | Pip deps + network; no root auto-install claim | runtime | Active | `requirement-runtime-prerequisites.md` | 2026-10-07 |

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
