**file**: docs/requirements/requirement-download-ytdlp-pipeline.md  
**Status**: Active (Version 1.0.0)  
**Area**: download  
**Key**: `requirement-download-ytdlp-pipeline`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the **operational download pipeline** for AnimeDlp: how extracted media sources are fetched with **yt-dlp**, how **HTTP headers and playback cookies** are applied, and how retries / concurrency are configured — without owning domain site catalog or CLI argparse tables.

Domain catalog is owned by **`requirement-domain-animedlp`**.  
CLI flags that enable extract-only mode are owned by **`requirement-python-cli-interface`**.

---

## 2. Core Rules (Mandatory)

### 2.1 Engine

1. **MUST** use **yt-dlp** (`yt_dlp.YoutubeDL`) as the download engine for non-extract runs.  
2. **MUST NOT** replace yt-dlp with an undocumented custom HTTP streamer as the default download path without updating this requirement.  
3. **MUST** treat yt-dlp as a **pip dependency** (not a system binary prerequisite separate from the package) unless a future REQ declares dual install surfaces.

### 2.2 Per-item download contract

4. For each extracted item `(title, video_url, special_cookie?)`, **MUST** invoke download with a clear progress log line.  
5. **MUST** set output template to include the **episode/title** stem (current law: `"{title}.%(ext)s"`).  
6. **MUST** set a **Referer** appropriate to the source family when known (`anime1.me` vs `anime1.pw`).  
7. **MUST** pass the same **User-Agent** used for extraction session headers into yt-dlp HTTP headers.  
8. When `special_cookie` is present (anime1.me API cookies), **MUST** pass only the **needed cookie names** as a Cookie header string — do not dump the entire session jar blindly in a way that reintroduces duplicate-name conflicts.

### 2.3 Cookie safety (sacred)

9. **MUST** extract only the documented playback cookie names for anime1.me (`e`, `h`, `p` as currently used).  
10. **MUST** build cookie header strings without relying on multi-value CookieJar entries that collide under the same name when a single header string is required.  
11. **MUST NOT** log full cookie values at INFO level in non-verbose mode; verbose/debug **MAY** log for diagnostics but **MUST NOT** write secrets unrelated to session cookies (no passwords/tokens).  
12. Cloudflare `cf_clearance` when supplied **MUST** be applied to the extraction **session**, not invented as a permanent vaulted secret.

### 2.4 Resilience options

13. **SHOULD** enable concurrent fragment downloads for faster media fetch when the engine supports it (current product: `concurrent_fragment_downloads: 16`).  
14. **SHOULD** set non-zero retries for transient network failures (current product: `retries: 10`).  
15. Verbose flag **MUST** control yt-dlp verbose mode when wired.

### 2.5 Extract-only boundary

16. When extract-only mode is active, **MUST NOT** call the download pipeline.  
17. Download failures **MUST NOT** be reported as successful completions (error peer).

### 2.6 Privilege and network

18. **MUST** run as the invoking user (Type 0) — no sudo for downloads.  
19. Network egress is **inherent** to this product’s purpose; **MUST** limit default host contact to supported sites + CDN/media hosts returned by those sites (no open proxy/TOR product claim unless separately lawed).  
20. **MUST NOT** require Type 1 elevation for download write paths (writes to cwd by default).

### 2.7 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Implementation** | `YtDlpDownloadService` in `src/AnimeDlp/download_service.py` (coordinator facade: `Anime1Downloader.download_video`) |
| **Classes peer** | `requirement-python-classes` |
| **Engine** | `yt_dlp.YoutubeDL` |
| **outtmpl** | `"{title}.%(ext)s"` (cwd relative) |
| **concurrent_fragment_downloads** | `16` |
| **retries** | `10` |
| **Referer me** | `https://anime1.me/` when URL path indicates me media |
| **Referer pw** | `https://anime1.pw/` otherwise |
| **Cookie header keys** | `e`, `h`, `p` only when present in `special_cookie` dict |
| **API endpoint (me)** | POST `https://v.anime1.me/api` with form `d=<apireq>` |
| **Session HTTP timeout (fetch_html)** | 25 seconds |
| **Cloudflare cookie name** | `cf_clearance` via session cookies when `--cloudflare` set |
| **Extract-only** | skips this pipeline entirely |
| **User docs** | README How It Works / Troubleshooting must mention yt-dlp and Cloudflare cookie refresh |

### 2.8 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT**: One home for download options and cookie plumbing.  
- **Principle 1 – Caution**: Cookie jar collisions and Cloudflare blocks are designed around.  
- **Principle 10 – Least privilege**: User-level download only.  
- **Principle 12 – Traceability**: Failures logged per title.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Cookie subset only; fail loudly on API/download errors.  
- **Intentional:** yt-dlp is the named engine.  
- **Anti-fragile:** Retries and concurrent fragments.  
- **Over-protect:** No elev; no silent success on download failure.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Drop cookie-collision safeguards when anime1.me still needs `e`/`h`/`p`.  
2. Replace yt-dlp silently without updating this REQ and packaging deps.  
3. Write downloads under system directories that require root.  
4. Log passwords or permanent secrets (none should exist).  
5. Download in extract-only mode.  
6. Expand cookie dump to entire jar without law update if that reintroduces name conflicts.

**Violating this rule is a critical download regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | yt-dlp is the download engine |
| AC-2 | Cookie header limited to documented names |
| AC-3 | Referer/User-Agent applied |
| AC-4 | Extract-only does not call download |
| AC-5 | No Type 1 elev for download |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-domain-animedlp` | Domain catalog + extractors |
| `requirement-python-cli-interface` | Flags including extract |
| `requirement-python-error-handling` | Download failure reporting |
| `requirement-runtime-prerequisites` | yt-dlp pip dep |
| `requirement-python-coding-style` | General Python style |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-YTDLP-01** | `tests/test_download_pipeline.py` | **have** | Cookie string builds only e/h/p |
| **TP-YTDLP-02** | `tests/test_download_pipeline.py` | **have** | Extract mode never calls YoutubeDL |
| **TP-YTDLP-03** | `tests/test_download_pipeline.py` | **have** | Referer selection me vs pw |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | yt-dlp + cookie-safe pipeline for AnimeDlp |
| 2026-08-11 | Active 1.0.0 | Implementation path: `downloader.py`; L2 service target |

---

**Last Updated**: 2026-08-11  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
