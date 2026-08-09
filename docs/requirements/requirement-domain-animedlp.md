**file**: docs/requirements/requirement-domain-animedlp.md  
**Status**: Active (Version 1.0.0)  
**Area**: domain  
**Key**: `requirement-domain-animedlp`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **domain surface Single Source of Truth** for AnimeDlp: which **supported sites and user-facing download/extract workflow steps** exist, what **features** the product claims, and how **help / about / messaging** must describe them.

**Operational yt-dlp download and cookie plumbing** are **not** fully owned here — they are owned by **`requirement-download-ytdlp-pipeline`**.  
**CLI entry and argparse contract** are owned by **`requirement-python-cli-interface`**.

This file remains the sole Active **`requirement-domain-*`** (four pillars).

**Legal posture:** Domain law assumes **personal / educational use** and respect for site terms of service and applicable copyright law. Product docs **MUST** keep a disclaimer. Agents **MUST NOT** expand domain into bulk commercial piracy tooling.

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Pillar A — Specialized CLI surface (workflow steps)

AnimeDlp is a **URL-argument domain CLI** (not a multi-verb Type 0 shell product). Domain surface **MUST** be expressed as the following ordered steps after entry:

| Step ID | User action | Inputs | Output / effect | Ops SSOT |
|---------|-------------|--------|-----------------|----------|
| D-01 | Supply series/episode URL | positional `url` from a **supported site** | Parse and validate host | CLI + domain |
| D-02 | Detect site | URL netloc | Route to `anime1.me` or `anime1.pw` extractor | domain |
| D-03 | Optional Cloudflare assist | `--cloudflare` / `--user-agent` when needed | Session headers/cookies for protected pages | domain + pipeline |
| D-04 | Extract episode list / media sources | page HTML + site APIs | Ordered list of `(title, source_url[, cookie_dict])` | domain extractors |
| D-05a | Extract-only mode | `--extract` / `-x` | Print title, URL, optional cookie; **no download** | domain + CLI |
| D-05b | Download mode | default (no `--extract`) | Download each item via yt-dlp | `requirement-download-ytdlp-pipeline` |
| D-06 | Report outcome | — | Per-item success/failure; completion summary | CLI + error peer |

**Routing:** Entry (`anime-dlp` / `python -m AnimeDlp` / `AnimeDlp.cli:main`) **MUST** require a positional URL (unless a future Active requirement adds a no-URL help-only mode). Unsupported hosts **MUST** fail closed.

**Supported hosts (current product law):**

| Host family | Detect | Extractor role |
|-------------|--------|----------------|
| `anime1.me` | netloc contains `anime1.me` | API path (`data-apireq`) + post to site API for source + cookies `e`/`h`/`p` |
| `anime1.pw` | netloc contains `anime1.pw` | Episode page crawl + HTML/iframe/regex video URL discovery |

**Non-goals as domain commands (unless a future requirement adds them):** arbitrary-site generic scraper, batch URL file queue, GUI, cloud sync, DRM break beyond documented cookie assist, multi-host plugin marketplace, root/system install ensure, automatic credential vault.

### 2.2 Pillar B — Specialized features (surface map)

| Feature area | Domain role | Full law |
|--------------|-------------|----------|
| Site allowlist (me / pw only) | Reject other hosts | this file + CLI |
| Series multi-episode discovery | Order episodes when multi-page | this file |
| Cloudflare assist | Optional `cf_clearance` + User-Agent | this file + CLI |
| Extract-only listing | Print sources without download | this file + CLI |
| Playback-cookie handling | Safe subset for me API cookies | pipeline peer |
| High-speed fragment download | Concurrent fragments via yt-dlp | pipeline peer |
| Verbose diagnostics | `-v` / `--verbose` | CLI + error peer |

Domain **MUST NOT** restate full yt-dlp option graphs in a second competing SSOT. Pointers and feature catalog only.

### 2.3 Pillar C — Specialized project help items

Help **MUST** be available as:

1. **`argparse` `--help`** listing domain options and required URL.  
2. **Product README** domain rows that match this catalog.  
3. Error messages that name supported sites when URL is wrong.

Help / README domain rows **MUST** include:

| Help row | Text intent |
|----------|-------------|
| Supported sites | `anime1.me` and `anime1.pw` only |
| Primary operand | Series or episode page URL |
| Extract mode | `--extract` / `-x` prints URLs without downloading |
| Cloudflare | `--cloudflare` / `-cf` with optional matching `--user-agent` / `-ua` |
| Verbose | `-v` / `--verbose` for debug detail |
| Download engine | yt-dlp (not a custom binary streamer) |
| Disclaimer | Personal/educational use; respect site ToS and local law |

### 2.4 Pillar D — Specialized project about items

Product identity / about **MUST** be able to report (via package metadata, logger banner, and/or `--help` description):

| Field / line | Content |
|--------------|---------|
| Product name | AnimeDlp |
| Version | Package version SSOT (`__version__` / `pyproject.toml`) |
| Domain summary | CLI downloader/extractor for supported anime video sites |
| Runtime tools | Python deps + yt-dlp; network access to supported hosts |
| Entry points | `anime-dlp`, `python -m AnimeDlp` |

**About is not** a remote version-check and **must not** advertise a shell `curl|sh` install channel unless a future install requirement is Active.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product / package name** | `AnimeDlp` |
| **Console script** | `anime-dlp` |
| **Domain implementation module** | `src/AnimeDlp/cli.py` (`Anime1Downloader`) |
| **VERSION (package)** | `1.1.0` (align `__init__.py` and `pyproject.toml`) |
| **Supported hosts** | `anime1.me`, `anime1.pw` |
| **anime1.me path** | Parse `entry-title` + `video-js` `data-apireq`; POST `https://v.anime1.me/api`; collect cookies `e`,`h`,`p` |
| **anime1.pw path** | Find episode links; per-page `<source>`, iframe, or m3u8/mp4 regex |
| **Extract mode flag** | `-x` / `--extract` |
| **Cloudflare flag** | `-cf` / `--cloudflare` |
| **User-Agent flag** | `-ua` / `--user-agent` |
| **Verbose flag** | `-v` / `--verbose` |
| **Output files (download)** | `{title}.%(ext)s` in **current working directory** (yt-dlp `outtmpl`) |
| **Ops SSOT** | `requirement-download-ytdlp-pipeline` |
| **CLI SSOT** | `requirement-python-cli-interface` |
| **User docs** | Root `README.md` Features / Usage / Examples / Disclaimer must match this catalog |
| **Disclaimer** | README Disclaimer section is product-user surface SSOT for legal caution |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Domain surface is explicit (four pillars) and not mixed with full download option law.  
- **Principle 5 – SSOT**: One Active domain file for feature catalog.  
- **Principle 1 – Caution**: Non-goals and legal posture listed so agents do not invent bulk/DRM/unauthorized host scope.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not invent a second yt-dlp ops SSOT in domain.  
- **Intentional:** Pillars A–D only; download details in pipeline requirement.  
- **Anti-fragile:** Clear ownership boundaries reduce drift between README and CLI.  
- **Over-protect:** Keep sole Active domain file; supersede before replace.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Duplicate full yt-dlp option law here once `requirement-download-ytdlp-pipeline` is Active.  
2. Add online install, bulk piracy queue, or root elevation as silent domain behavior without new requirements.  
3. Create a second Active `requirement-domain-*` without superseding this one.  
4. Drop support for either documented host while README still advertises it without coordinated update.  
5. Claim arbitrary-site support without updating this file, CLI validation, and peers.  
6. Remove legal disclaimer while product still downloads third-party media.  
7. Silently re-scope this product into local video editing (cut/speed/join) without domain rename / new REQs.

**Violating this rule is a critical domain regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Four pillars present (workflow steps, feature map, help framing, about fields) |
| AC-2 | Supported hosts limited to anime1.me and anime1.pw |
| AC-3 | Extract vs download modes documented |
| AC-4 | Cloudflare/User-Agent assist documented |
| AC-5 | Non-goals include arbitrary-site scraper / Type 0 shell install / elev |
| AC-6 | Registered as sole Active domain SSOT |
| AC-7 | No competing full yt-dlp ops body (defers to download-ytdlp-pipeline) |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-download-ytdlp-pipeline` | **Operational download SSOT** |
| `requirement-python-cli-interface` | Entry + argparse |
| `requirement-runtime-prerequisites` | Python deps + network |
| `requirement-python-error-handling` | Fail-closed paths |
| `requirement-class-software-dev` | Class residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-ANIMEDLP-01** | `tests/test_domain_extract.py` | **have** | Unsupported host rejects |
| **TP-ANIMEDLP-02** | `tests/test_domain_extract.py` | **have** | `--extract` prints without download |
| **TP-ANIMEDLP-03** | `tests/test_cli.py` | **have** | Missing URL → argparse error |
| **TP-ANIMEDLP-04** | `tests/test_domain_me.py` | todo | me extractor path (mocked HTTP) |
| **TP-CLI-01** | `tests/test_cli.py` | **have** | Peer: help lists domain flags |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Domain SSOT for AnimeDlp extract/download on anime1.me / anime1.pw |

---

**Last Updated**: 2026-08-09  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
