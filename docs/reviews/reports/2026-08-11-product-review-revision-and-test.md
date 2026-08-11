# Report: product review for revision and test — AnimeDlp 1.1.0

**Date:** 2026-08-11  
**Mode:** full product review (revision + test focus)  
**Status:** **Pass (fixed in 1.2.0 implement)** — residuals closed; Core **25 passed**  
**Method:** load prior reviews + law registry + ship unit + test-plan/RTM; implement + re-run `python3 -m pytest -q tests/`  
**Baseline proof:** **25 passed** (offline mocks; 2026-08-11 post-fix)

---

## Summary

AnimeDlp remains a coherent **pip CLI** for **anime1.me / anime1.pw** extract+download via site parsers and **yt-dlp**. Release **1.1.0** Core gates (packaging, domain reject, extract-vs-download, cookie subset, structure) still pass.

Prior **P2** packaging/export/version issues from `2026-08-09-product-review.md` stay **fixed**. This review prioritizes **what to change next** and **what to prove with tests**, not reopening closed 1.1.0 gates.

**Verdict: Revise** (not Block): ship is usable with Core green; next revision should fix exit-code honesty, reduce cookie exposure, tighten version SSOT, and optionally add offline unit cases for empty-result / download-failure paths before any live-network optional suite.

---

## Prior lessons re-check

| Prior ID | Topic | Re-check 2026-08-11 |
|----------|--------|---------------------|
| ADLP-DOC-01 | Packaging description wrong product | **Still fixed** — pyproject anime-focused |
| ADLP-PKG-01 | Phantom `ChronicleLogger` export | **Still fixed** — `__all__` = version + main |
| ADLP-VER-01 | Version surface drift | **Still fixed** at 1.1.0; residual **triple version constants** (see ADLP-VER-02) |
| ADLP-NET-01 | No live-network tests | **Still deferred** (optional) |
| ADLP-SEC-01 | Verbose cookie logging | **Still open** — verbose logs + extract prints cookies |

---

## Test execution

```text
python3 -m pytest -q tests/
# 20 passed in ~0.4s (2026-08-11)
```

| Family | Status |
|--------|--------|
| TP-STRUCT / TP-PKG / TP-PRE / TP-CLI / TP-ANIMEDLP / TP-YTDLP / TP-ERR / TP-STYLE | **have** (Core green) |
| TP-ANIMEDLP-04 / TP-YTDLP-04 | **todo optional** (live network) |

---

## Findings (revision backlog)

### ADLP-EXIT-01 — Severity: **P2** (medium) — **open** · revision candidate

| Field | Value |
|-------|--------|
| **Area** | error handling / UX honesty |
| **Location** | `src/AnimeDlp/cli.py` `run()` ~312–327 |
| **Description** | When **zero** videos are extracted, process still exits **0** and, in download mode, logs **"All downloads completed!"**. Download failures in `download_video` log ERROR but the loop continues and still claims completion. |
| **Impact** | CI/scripts cannot trust exit status; operators may think success on total failure. |
| **Suggestion** | Fail closed: non-zero exit if `all_videos` empty or if any download fails; distinguish partial success if product wants soft continue (document either way). |
| **Test** | **TP-ERR-03** (todo) empty extract → non-zero; **TP-ERR-04** (todo) download exception → non-zero or partial policy |
| **Requirement** | `requirement-python-error-handling` |

### ADLP-ERR-02 — Severity: **P2** (medium) — **open** · revision candidate

| Field | Value |
|-------|--------|
| **Area** | structure / testability |
| **Location** | `cli.py` extractors (`sys.exit(1)` inside `_extract_api_paths`, Cloudflare 403, etc.) |
| **Description** | Hard `sys.exit` from deep methods aborts process; harder to unit-test and mixes control flow with library-style methods. |
| **Impact** | Extractor failures cannot be asserted cleanly without process isolation; inconsistent with raise/return patterns. |
| **Suggestion** | Raise domain exceptions or return error results; let `main`/`run` map to exit codes once. |
| **Test** | Prefer unit tests once exit is centralized (TP-ERR-*) |

### ADLP-SEC-01 — Severity: **P3** (low) — **open** (accepted residual; tighten in revision)

| Field | Value |
|-------|--------|
| **Area** | security / privacy |
| **Location** | `cli.py` verbose API cookie log; extract mode `print(f"Cookie: {cookie}")` |
| **Description** | Playback cookies and `cf_clearance` path can appear in logs/stdout. SECURITY already warns; still operator footgun. |
| **Impact** | Session tokens in log files / shell history if verbose/extract misused. |
| **Suggestion** | Redact cookie values in logs by default; extract mode optionally `--show-cookies`; never log full `cf_clearance`. |
| **Test** | **TP-SEC-01** (todo optional): verbose path does not emit full cookie values when redaction enabled |

### ADLP-VER-02 — Severity: **P3** (low) — **open** · revision candidate

| Field | Value |
|-------|--------|
| **Area** | version SSOT |
| **Location** | `Anime1Downloader.MAJOR/MINOR/PATCH`, `main()` triple, `__version__`, `pyproject` |
| **Description** | Version expressed in **three** code places + packaging (aligned today at 1.1.0 but drift-prone). |
| **Impact** | Future bump forgets CLI constants → debug banner lies. |
| **Suggestion** | Single SSOT: read `__version__` (or packaging metadata) for banners; delete class-level triples. |
| **Test** | Extend **TP-PKG-02** to assert CLI banner path uses `__version__` if refactored |

### ADLP-ARCH-01 — Severity: **P3** (low) — **open** · revision candidate

| Field | Value |
|-------|--------|
| **Area** | maintainability |
| **Location** | single `cli.py` (~388 lines): me + pw + download + main |
| **Description** | Monolith slows targeted tests and site-drift fixes. |
| **Impact** | Higher cost to patch one host without risking the other. |
| **Suggestion** | Split extractors / download / CLI entry under `src/AnimeDlp/` in a later revision (keep public `main`). |
| **Test** | Keep existing TP-IDs green after split |

### ADLP-NET-01 — Severity: **P3** (low) — **deferred optional**

| Field | Value |
|-------|--------|
| **Area** | live coverage |
| **Description** | No scheduled live extract/download against real hosts. |
| **Suggestion** | Optional CI job with secrets for CF only; keep Core offline. |
| **Test** | TP-ANIMEDLP-04 / TP-YTDLP-04 remain optional |

### ADLP-IO-01 — Severity: **P3** (low) — **open** · revision candidate

| Field | Value |
|-------|--------|
| **Area** | download filesystem |
| **Location** | `download_video` `outtmpl`: `f"{title}.%(ext)s"` |
| **Description** | Episode titles may contain path separators / unsafe characters; cwd-only writes with no output dir flag. |
| **Impact** | Odd filenames or path traversal-ish titles depending on yt-dlp sanitization. |
| **Suggestion** | Sanitize title for filesystem; optional `-o` / output directory flag. |
| **Test** | **TP-YTDLP-05** (todo): title with `/` or `..` sanitized in opts |

---

## Non-findings (still OK)

| Check | Result |
|-------|--------|
| Core suite 20/20 | Pass |
| Host allowlist / unsupported host exit 1 | Pass (TP-CLI-03 / TP-ANIMEDLP-01) |
| Extract does not call yt-dlp | Pass (TP-YTDLP-02) |
| Cookie header only e/h/p | Pass (TP-YTDLP-01) |
| No Type 1 elev / shell Type O | Absent by design |
| Packaging description honesty | Pass (TP-PKG-03) |
| Secrets committed in tree | None found |

---

## Priority remediation order (revision plan)

| Priority | Item | Effort | Tests to land |
|----------|------|--------|----------------|
| **1** | **ADLP-EXIT-01** fail-closed empty extract / download failure exit policy | S | TP-ERR-03, TP-ERR-04 |
| **2** | **ADLP-ERR-02** centralize exit / reduce deep `sys.exit` | M | unit-friendly extractors |
| **3** | **ADLP-SEC-01** redact cookies in verbose logs | S | TP-SEC-01 optional |
| **4** | **ADLP-VER-02** single version SSOT in code | S | strengthen TP-PKG-02 |
| **5** | **ADLP-IO-01** sanitize titles / output dir | S–M | TP-YTDLP-05 |
| **6** | **ADLP-ARCH-01** split modules | M | re-run full Core |
| **7** | **ADLP-NET-01** optional live smoke | M | TP-ANIMEDLP-04 / TP-YTDLP-04 |

---

## Test plan deltas (recommended)

| TP-ID | Intent | Core | Status after this review |
|-------|--------|------|---------------------------|
| **TP-ERR-03** | Empty extract → non-zero exit | Core (once EXIT-01 fixed) | **todo** |
| **TP-ERR-04** | Download failure → non-zero or documented partial | Core (once EXIT-01 fixed) | **todo** |
| **TP-SEC-01** | Verbose does not log full cookie secrets when redaction on | Optional | **todo** |
| **TP-YTDLP-05** | Unsafe title sanitized in outtmpl | Core after IO-01 | **todo** |
| TP-ANIMEDLP-04 / TP-YTDLP-04 | Live network | Optional | **todo** (unchanged) |

Do **not** flip todo→have until suite asserts + map + law notes updated same change.

---

## Verdict

| Gate | Result |
|------|--------|
| Core automated tests | **Pass** (20) |
| Prior P2 packaging/version | **Still fixed** |
| Ready for unreviewed 1.2 without EXIT-01 | **Revise recommended** |
| Block release of current Core packaging | **No** |

**Overall (post-implement 1.2.0):** **Pass** — ADLP-EXIT/ERR/SEC/VER/IO/ARCH closed in code + Core tests; only optional live-network TP-ANIMEDLP-04 / TP-YTDLP-04 remain deferred.

---

## Related

| Artifact | Role |
|----------|------|
| `docs/reviews/2026-08-09-product-review.md` | Prior full review |
| `docs/reviews/test-plan.md` | TP map |
| `docs/reviews/requirement-test-matrix.md` | RTM |
| `docs/requirements/index.md` | Law registry |
| `tests/` | Executable proof |

**Written by:** multi-agent council (product review)  
**Lessons loaded:** prior product review findings table  
