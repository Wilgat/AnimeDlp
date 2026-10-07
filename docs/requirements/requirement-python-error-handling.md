**file**: docs/requirements/requirement-python-error-handling.md  
**Status**: Active (Version 1.0.1)  
**Area**: python  
**Key**: `requirement-python-error-handling`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define how AnimeDlp **detects, reports, and recovers from errors** during dependency checks, extraction, and downloads without claiming false success.

---

## 2. Core Rules (Mandatory)

### 2.1 Fail-closed principles

1. **MUST NOT** silently ignore a failed extract or download when the product claims success.  
2. **MUST NOT** treat invalid URLs / unsupported hosts as success.  
3. **MUST** prefer clear human-readable messages (via logger and/or console) over stack-only failures for expected user mistakes.  
4. **MUST NOT** delete user files outside product-created download outputs as “cleanup.”

### 2.2 Required error categories

| Category | Detection | Required action |
|----------|-----------|-----------------|
| Missing Python dependency | Import gate fails | FATAL message with install hint; non-zero exit |
| Missing positional URL | argparse | Usage error; non-zero exit |
| Unsupported host | netloc not anime1.me / anime1.pw | ERROR message; exit 1 |
| Cloudflare block (403) | HTTP 403 on protected fetch | ERROR; exit 1; hint `--cloudflare` / User-Agent |
| Partial Cloudflare assist | UA xor cf only when ship unit requires both | ERROR; exit 1 with clear pairing message |
| No titles / no apireq | parse failure | ERROR; exit 1 |
| Title/video count mismatch | list lengths differ | ERROR; exit 1 |
| Empty extract result | zero videos | INFO/WARN + no success claim; exit non-zero **SHOULD** when nothing found |
| mpv missing or not mplayer2 | `mpv` verb and the player check fails | ERROR; exit 1; do not extract and do not play |
| `mpv` without a page URL | verb `mpv` and no URL | ERROR; exit 1; do not open the menu |
| `--id` without `mpv` | the switch is set and the verb is not `mpv` | ERROR; exit 1; do not open the menu and do not download |
| mpv id out of range | `--id` is below 1 or greater than the extract count | ERROR; exit 1; do not start mpv |
| HTTP fetch failure | non-200 / exception | WARN/ERROR; skip item or abort path per site logic |
| API parse failure | me API exception | ERROR for item; continue or stop per current ship unit (log clearly) |
| Download failure | yt-dlp exception | ERROR for that title; **MUST NOT** claim that title succeeded |
| Cookie-related errors | jar / header issues | ERROR with guidance; keep cookie subset fix intact |

### 2.3 Exit codes

5. Expected failures **MUST** exit non-zero (`sys.exit(1)` or argparse default).  
6. Successful full run after downloads **MAY** exit 0 even if individual items failed only when law documents partial success — **current honest default:** prefer clear per-item errors; agents **MUST NOT** invent “all green” when errors were logged.

### 2.4 Logging

7. **SHOULD** use ChronicleLogger for durable diagnostics.  
8. **MUST** still emit user-visible failure reasons (logger levels FATAL/ERROR/WARN).  
9. **MUST NOT** log secrets other than optional session cookies under explicit verbose mode.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Import gates** | requests / BeautifulSoup / yt_dlp / lxml → FATAL + exit 1 |
| **Unsupported host** | `sys.exit(1)` after ERROR log |
| **Cloudflare 403** | ERROR + exit 1 |
| **UA/cf pairing** | ERROR + exit 1 when only one of the two provided in me path |
| **Parse mismatches** | ERROR + exit 1 |
| **Download exceptions** | ERROR log in `download_video`; continues loop to next item (honest: no global abort unless later law changes) |
| **Extract mode** | prints blocks; returns without download |
| **ChronicleLogger levels** | DEBUG/INFO/WARN/ERROR/FATAL as used in ship unit |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Fail closed on blocks and bad hosts.  
- **Principle 12 – Traceability**: User-visible failure reasons.  
- **Principle 5 – SSOT**: Error category table is product law.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Unsupported hosts never reach download.  
- **Intentional:** Category table is product law.  
- **Anti-fragile:** Per-item download errors do not wipe completed files.  
- **Over-protect:** No silent success.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Swallow Cloudflare/host errors without user-visible failure.  
2. Claim success after total extract failure.  
3. Replace clear messages with silent `pass`.  
4. Log credentials or permanent tokens (none should exist).  
5. Delete unrelated user files as cleanup.

**Violating this rule is a critical safety regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Missing deps → FATAL + non-zero |
| AC-2 | Unsupported host → ERROR + non-zero |
| AC-3 | Cloudflare 403 → ERROR + guidance |
| AC-4 | Download failure logs ERROR for title |
| AC-5 | No secret logging requirement |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-cli-interface` | Argparse / gates |
| `requirement-domain-animedlp` | Host validation |
| `requirement-download-ytdlp-pipeline` | Download exceptions |
| `requirement-runtime-prerequisites` | Dep presence |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-ERR-01** | `tests/test_errors.py` | **have** | unsupported host |
| **TP-ERR-02** | `tests/test_errors.py` | **have** | missing dependency gate (mocked) |
| **TP-CLI-06** | `tests/test_cli.py` | **have** | Peer: mpv missing, bad `--id`, and `mpv` without a URL exit 1 with a next command |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Error categories for AnimeDlp |
| 2026-10-07 | Active 1.0.1 | The `mpv` verb fails closed when the player is missing, the page URL is missing, or `--id` is out of range |

---

**Last Updated**: 2026-10-07  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
