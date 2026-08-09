# Product review: AnimeDlp (full product)

**Date:** 2026-08-09  
**Reviewer:** multi-agent council (Explore/Plan/Implement/Review/Security)  
**Product:** AnimeDlp `VERSION=1.1.0`  
**Ship unit:** `src/AnimeDlp/` (console script `anime-dlp`)  
**Scope:** requirements set, packaging honesty, CLI/domain/download path, automated tests, user docs  
**Method:** disk read + `python3 -m pytest -q tests/` (20 passed)  
**Baseline:** **PASS** — 20 Core tests green (mocked; no public network)

## Summary

AnimeDlp is a specialized Python pip package that extracts and downloads media from **anime1.me** and **anime1.pw** using site parsers plus **yt-dlp**. Release **1.1.0** introduces a full Active requirements set, automated Core proof, packaging/export honesty fixes, and aligned version SSOTs. Residual risks are operational (site/Cloudflare drift) and incomplete live-network optional coverage—not Core gate failures.

## Strengths

| Area | Notes |
|------|--------|
| Domain clarity | Host allowlist + extract/download modes explicit in law and CLI |
| Cookie safety | Playback cookies limited to `e`/`h`/`p`; covered by TP-YTDLP-01 |
| Fail-closed hosts | Unsupported hosts exit non-zero without download |
| Packaging SSOT | Version dual-write aligned at 1.1.0; console script declared |
| Test isolation | Core suite mocks HTTP/yt-dlp; no live network required |
| Privilege | User-level only; no Type 1 elev surface |

## Findings

### ADLP-DOC-01 — Severity: P2 (medium)
- **Area:** docs / metadata residual  
- **Status:** fixed  
- **Location:** `pyproject.toml` description/keywords (pre-1.1.0)  
- **Description:** Packaging described an unrelated video-editing tool.  
- **Impact:** PyPI/metadata honesty failure.  
- **Suggestion:** Keep description aligned with anime downloader purpose (done in 1.1.0).  
- **Cross-ref:** `requirement-python-packaging`

### ADLP-PKG-01 — Severity: P2 (medium)
- **Area:** package exports  
- **Status:** fixed  
- **Location:** `src/AnimeDlp/__init__.py`  
- **Description:** Re-exported undefined `ChronicleLogger` from `.cli`.  
- **Impact:** Broken public import surface / confusion.  
- **Suggestion:** Export only `__version__` and `main` (done; TP-STYLE-01).  

### ADLP-VER-01 — Severity: P2 (medium)
- **Area:** version align  
- **Status:** fixed  
- **Location:** pyproject / `__init__` / CLI constants / README badge  
- **Description:** Surfaces disagreed (1.0.0 / 1.0.1 / 1.1.0).  
- **Impact:** Release confusion vs PyPI 1.0.1.  
- **Suggestion:** Align all local surfaces to **1.1.0** (done).  

### ADLP-NET-01 — Severity: P3 (low)
- **Area:** test coverage  
- **Status:** deferred  
- **Location:** optional TP-ANIMEDLP-04 / TP-YTDLP-04  
- **Description:** No live-network integration tests against real hosts.  
- **Impact:** Site HTML/API drift may break extractors without CI signal.  
- **Suggestion:** Optional scheduled integration job; keep Core offline.  

### ADLP-SEC-01 — Severity: P3 (low)
- **Area:** security / ops  
- **Status:** open (accepted residual)  
- **Location:** CLI `--cloudflare` value handling  
- **Description:** Session cookies may appear in verbose logs.  
- **Impact:** Local log exposure of short-lived site cookies.  
- **Suggestion:** Keep verbose-only; never commit cookies; document in SECURITY.  

## Non-findings (explicitly OK)

| Check | Result |
|-------|--------|
| Type 1 elev / sudoers | Absent by design |
| Shell Type O install | Absent by design |
| Unsupported host download | Rejected before extract |
| Extract mode downloads | Does not call yt-dlp (TP-YTDLP-02) |
| Requirements git-surface harness paths | Clean |
| Secrets in tree | None found |

## Priority remediation order

1. ~~Fix packaging description / exports / version align~~ **done (1.1.0)**  
2. Optional: live-network extractor smoke (deferred)  
3. Optional: reduce verbose cookie logging further  

## Related

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Law registry |
| `docs/reviews/test-plan.md` | TP map |
| `docs/reviews/requirement-test-matrix.md` | RTM |
| `tests/` | Suites (20 passed) |
| `README.md` / `CHANGELOG.md` / `SECURITY.md` | User surfaces |

**Written by:** multi-agent council  
**Review status:** Residual P3 only; release Core gates green  

---

**Last Updated:** 2026-08-09
