**file**: docs/requirements/requirement-domain-animedlp.md  
**Status**: Active (Version 1.2.0)  
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

**Download progress:** This file owns the shape of the wait line. The please-wait phrase follows the saved menu language. The thirteen phrases stay on `requirement-python-cli-language`. While videos are being saved on a terminal, the operator sees one line. The bullet is `•`. It flashes. One moment the bullet is drawn. The next moment that cell is a space, so the rest of the line does not jump. Each flash rebuilds the line.

The line is `{phrase}. file {current}/{total}, {percent}% finished, {time} until finish`, with the bullet in front. `{phrase}` is the saved-language words for `please wait`. English is `please wait`. `{current}` is the video being saved, starting at 1. `{total}` is how many videos the page yielded. `{percent}` is how much of that list is finished, counting the bytes of the current video. A finished video counts in full, so the next video starts at that share. `{time}` is the time until finish, estimated from the time already spent and that percent. Under one percent the time word is `estimating`. A minute is `1m 05s`. An hour is `1h 01m 01s`. Under a minute the line says `45s until finish`. The words `file`, `finished`, `until finish`, and `estimating` stay English.

A worked English line is `• please wait. file 2/5, 40% finished, 1m 05s until finish`. The next flash may be `  please wait. file 2/5, 46% finished, 58s until finish`. With the menu language Traditional Chinese the same moment is `• 請稍候. file 2/5, 40% finished, 1m 05s until finish`.

When the downloads return, the line is erased before later text. A stream that is not a terminal does not show the line, and yt-dlp keeps its own progress. `--extract` does not save videos and does not show the line. On a terminal, yt-dlp's own bar is turned off so it does not overwrite this line. The bytes still move the percent through yt-dlp's progress hook.

This product does not print `{choice} has been selected. {process} takes time to finish.`

The line is drawn by `src/AnimeDlp/please_wait.py`. The phrase is read once when the line starts, from `MenuLanguage`, and that read does not write the language leaf. `Anime1Downloader.run` counts the files. `YtDlpDownloadService` reports the bytes. Do not store the line in a module-level constant.

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
| Download progress line | Flashing bullet, saved-language please wait, file count, percent finished, time until finish | this file + `requirement-python-cli-language` |

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
| **Domain implementation** | `src/AnimeDlp/extractors/me.py`, `extractors/pw.py` (coordinator: `downloader.py`) |
| **CLI entry** | `src/AnimeDlp/cli.py` (thin) |
| **L2 classes peer** | `requirement-python-classes` |
| **VERSION (package)** | `1.5.2` (align `__init__.py` and `pyproject.toml`) |
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
| **Architecture / classes peers** | `requirement-python-system-architecture`, `requirement-python-classes` |
| **User docs** | Root `README.md` Features / Usage / Examples / Disclaimer must match this catalog |
| **Disclaimer** | README Disclaimer section is product-user surface SSOT for legal caution |
| **Download progress** | `• please wait. file 2/5, 40% finished, 1m 05s until finish` on a terminal when the menu language is English. The bullet flashes. The phrase follows the saved menu language. The time is redrawn. The line is erased when the downloads return. Drawn by `src/AnimeDlp/please_wait.py` |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Domain surface is explicit (four pillars) and not mixed with full download option law.  
- **Principle 5 – SSOT**: One Active domain file for feature catalog.  
- **Principle 1 – Caution**: Non-goals and legal posture listed so agents do not invent bulk/DRM/unauthorized host scope. A download on a terminal shows a flashing bullet, the saved-language please-wait phrase, the file count, the percent finished, and a time until finish that moves on each flash. That line is removed when the downloads return.

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
8. Leave the progress line on the screen after the downloads have returned.  
9. Omit the please-wait phrase, print that phrase in a language other than the saved menu language, print `{choice} has been selected. {process} takes time to finish.`, or freeze the time until finish so a later flash shows a stale clock.

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
| AC-8 | A terminal download shows a flashing bullet, the saved-language please-wait phrase, `file current/total`, the percent finished, and a time until finish that changes when the flash redraws. The line is gone when the downloads return. Extract-only and a non-terminal do not show it |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-download-ytdlp-pipeline` | **Operational download SSOT** |
| `requirement-python-cli-interface` | Entry + argparse |
| `requirement-runtime-prerequisites` | Python deps + network |
| `requirement-python-error-handling` | Fail-closed paths |
| `requirement-class-software-dev` | Class residual |
| `requirement-python-cli-language` | The thirteen please-wait phrases |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-ANIMEDLP-01** | `tests/test_domain.py` | **have** | Unsupported host rejects |
| **TP-ANIMEDLP-02** | `tests/test_domain.py` | **have** | `--extract` prints without download |
| **TP-ANIMEDLP-03** | `tests/test_domain.py` | **have** | anime1.pw routes to pw extractor |
| **TP-ANIMEDLP-04** | `tests/test_live_network.py` | **optional** | Live HTTP extract; opt-in `ANIMEDLP_LIVE_NET=1` |
| **TP-CLI-01** | `tests/test_cli.py` | **have** | Peer: help lists domain flags |
| **TP-ANIMEDLP-05** | `tests/test_please_wait.py` | **have** | The bullet flashes beside the saved-language please-wait phrase, `file current/total`, the percent finished, and the time until finish. The line is absent when the job returns |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Domain SSOT for AnimeDlp extract/download on anime1.me / anime1.pw |
| 2026-08-11 | Active 1.0.0 | Implementation Notes: downloader module + 1.2.0 + L2 peers |
| 2026-08-19 | Active 1.0.0 | DTV aligned to disk; TP-ANIMEDLP-04 optional live extract |
| 2026-10-05 | Active 1.1.0 | A terminal download shows `file current/total`, the percent finished, and the time until finish. Each flash redraws that time. Package **1.4.0**. `TP-ANIMEDLP-05` has |
| 2026-10-05 | Active 1.1.0 | Package **1.5.0**. The text menu is on a terminal with no page URL |
| 2026-10-06 | Active 1.2.0 | The wait line starts with a flashing bullet and the saved-language words for please wait. The file count, the percent, and the time until finish stay. Package **1.5.1** |
| 2026-10-07 | Active 1.2.0 | Product version cell aligned to **1.5.2** |

---

**Last Updated**: 2026-10-07  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
