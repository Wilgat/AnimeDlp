# Requirements

Authoritative specialized product law for **AnimeDlp** lives here.

**Current state (2026-08-09):** Specialized **software-development** product. Left genesis. Registry is populated — see `index.md`.

## Product identity (summary)

| Field | Value |
|-------|--------|
| Product / package | `AnimeDlp` |
| Version SSOT | **`1.5.2`** (`pyproject.toml` + `src/AnimeDlp/__init__.py`) |
| Product README SSOT | Root `README.md` (app-name, short description, version badge) |
| Ship surface | Python package; console script **`anime-dlp`**; module `python -m AnimeDlp` |
| Install mode | **pip / local package** — not shell Type O |
| Domain surface | `requirement-domain-animedlp` — four pillars (anime1.me / anime1.pw extract+download). A terminal download flashes a bullet, the saved-language words for please wait, the file count, the percent finished, and the time until finish |
| Download ops | `requirement-download-ytdlp-pipeline` — yt-dlp; cookie-safe headers; extract boundary |
| Coding style | `requirement-python-coding-style` — exports honesty; fail-closed messaging |
| Runtime tools | Pip deps (requests, bs4, lxml, yt-dlp, ChronicleLogger); network egress |

## Class requirement gate

| Class | Required class file |
|-------|---------------------|
| software-development | `requirement-class-software-dev.md` (**Active**) |
| genesis-template | N/A — this workspace is no longer genesis for product law |

## Purpose

- **Plan** designs work by reading and updating these docs.  
- **Implement** delivers code that **traces** to these requirements.  
- **Review** verifies delivery against requirements and CIAO checklists.  
- Product **README** must stay honest with this law (install, features, version, disclaimer).

## Layout

| Path | Role |
|------|------|
| `docs/requirements/index.md` | Registry of all requirements — keep in sync |
| `docs/requirements/requirement-*.md` | CIAO-style project requirements |

## Status values

Typical: `draft` · `Active` · `approved` · `in-progress` · `done` · `deprecated` · `superseded`

## Rules

1. Never invent paths — verify on disk.  
2. Class files only via class process; non-class via create-specific process.  
3. Never dump harness inventories into this versioned surface.  
4. Online shell install and Type 1 elevation stay **absent** unless product mode is explicitly changed.  
5. Sole domain SSOT: `requirement-domain-animedlp.md`.  
6. When changing extract/download behavior: update domain + pipeline + CLI REQs **and** root `README.md` in the same change.  
7. Version dual SSOT + README Version badge must match when a release is claimed.  
8. Keep packaging description honest (anime downloader, not unrelated video-editing copy).
