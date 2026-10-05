# AnimeDlp — product test plan (TP map)

**Product:** AnimeDlp `1.4.0`  
**Updated:** 2026-10-05  
**Install mode:** pip / local package (`anime-dlp`) — **not** shell Type O  
**Suite root:** `tests/`  
**Architecture:** **L2** multi-class SRP (`requirement-python-system-architecture`, `requirement-python-classes`)  
**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Review:** `docs/reviews/reports/2026-08-11-product-review-l2-oop-1.3.0.md`

## Status legend

| Status | Meaning |
|--------|---------|
| **have** | Executable proof green |
| **todo** | Designed; not yet proven |
| **optional** | Nice-to-have; not release-blocking |
| **n/a** | Not in product scope |

## Intentionally n/a families

| Family | Reason |
|--------|--------|
| TP-LC / TP-CURL / TP-CSUM | No shell online install / self-update / companion checksum channel |
| TP-FFMPEG / TP-VIDEOJOIN | Not a local video editor product |
| TP-DOMAIN-* | Deprecated alias — use **TP-ANIMEDLP-*** |

---

## Core map

| TP-ID | Intent | Core | Suite | Primary requirement(s) | Status |
|-------|--------|------|-------|------------------------|--------|
| **TP-STRUCT-01** | Package under `src/AnimeDlp/` with L2 modules | Core | `tests/test_structure.py` | `requirement-python-project-structure` | **have** |
| **TP-PKG-01** | Console script + `main` export | Core | `tests/test_packaging.py` | `requirement-python-packaging`, `requirement-python-cli-interface` | **have** |
| **TP-PKG-02** | `pyproject` version == `__version__` | Core | `tests/test_packaging.py` | `requirement-python-packaging` | **have** |
| **TP-PKG-03** | Packaging description honest (anime downloader) | Core | `tests/test_packaging.py` | `requirement-python-packaging` | **have** |
| **TP-PRE-01** | No product-level `ensure_ffmpeg` gate | Core | `tests/test_prerequisites.py` | `requirement-runtime-prerequisites` | **have** |
| **TP-PRE-02** | Declared pip deps importable | Core | `tests/test_prerequisites.py` | `requirement-runtime-prerequisites` | **have** |
| **TP-CLI-01** | `--help` exits 0 (lists domain surface) | Core | `tests/test_cli.py` | `requirement-python-cli-interface` | **have** |
| **TP-CLI-02** | Missing URL → non-zero | Core | `tests/test_cli.py` | `requirement-python-cli-interface` | **have** |
| **TP-CLI-03** | Unsupported host → exit 1 | Core | `tests/test_cli.py` | `requirement-python-cli-interface`, `requirement-domain-animedlp` | **have** |
| **TP-ANIMEDLP-01** | Unsupported host domain reject | Core | `tests/test_domain.py` | `requirement-domain-animedlp` | **have** |
| **TP-ANIMEDLP-02** | Extract mode prints without download | Core | `tests/test_domain.py` | `requirement-domain-animedlp`, `requirement-download-ytdlp-pipeline` | **have** |
| **TP-ANIMEDLP-03** | anime1.pw routes to pw extractor | Core | `tests/test_domain.py` | `requirement-domain-animedlp` | **have** |
| **TP-ANIMEDLP-05** | The wait line names the file count, the percent finished, and the time until finish. The bullet flashes. The line is gone when the job returns | Core | `tests/test_please_wait.py` | `requirement-domain-animedlp` | **have** |
| **TP-YTDLP-01** | Cookie header only e/h/p | Core | `tests/test_download_pipeline.py` | `requirement-download-ytdlp-pipeline` | **have** |
| **TP-YTDLP-02** | Extract never builds YoutubeDL | Core | `tests/test_download_pipeline.py` | `requirement-download-ytdlp-pipeline` | **have** |
| **TP-YTDLP-03** | Referer me vs pw selection | Core | `tests/test_download_pipeline.py` | `requirement-download-ytdlp-pipeline` | **have** |
| **TP-YTDLP-05** | Unsafe title sanitized in outtmpl | Core | `tests/test_download_pipeline.py` | `requirement-download-ytdlp-pipeline` | **have** |
| **TP-ERR-01** | Unsupported host error path | Core | `tests/test_errors.py` | `requirement-python-error-handling` | **have** |
| **TP-ERR-02** | Download exception logs ERROR | Core | `tests/test_errors.py` | `requirement-python-error-handling` | **have** |
| **TP-ERR-03** | Empty extract → non-zero / AnimeDlpError | Core | `tests/test_errors.py` | `requirement-python-error-handling` | **have** |
| **TP-ERR-04** | Download failure in run → exit 1 | Core | `tests/test_errors.py` | `requirement-python-error-handling` | **have** |
| **TP-STYLE-01** | Package exports only real symbols | Core | `tests/test_exports.py` | `requirement-python-coding-style` | **have** |
| **TP-SEC-01** | Verbose API logs redacted cookies | Core | `tests/test_security_redaction.py` | `requirement-python-coding-style` / SECURITY | **have** |
| **TP-ARCH-01** | L2 modules importable | Core | `tests/test_architecture.py` | `requirement-python-system-architecture` | **have** |
| **TP-ARCH-02** | Download service unit seam (no full run) | Core | `tests/test_architecture.py` | `requirement-python-system-architecture` | **have** |
| **TP-CLASS-01** | Coordinator composes extractors + download service | Core | `tests/test_architecture.py` | `requirement-python-classes` | **have** |
| **TP-CLASS-02** | Me extractor unit seam without CLI main | Core | `tests/test_architecture.py` | `requirement-python-classes` | **have** |

## Optional map

| TP-ID | Intent | Core | Suite | Primary requirement(s) | Status |
|-------|--------|------|-------|------------------------|--------|
| **TP-ANIMEDLP-04** | Live HTTP extract against real host | Optional | `tests/test_live_network.py` | `requirement-domain-animedlp` | **optional** (opt-in `ANIMEDLP_LIVE_NET=1`) |
| **TP-YTDLP-04** | Integration download of a short HTTP fixture | Optional | `tests/test_live_network.py` | `requirement-download-ytdlp-pipeline` | **have** (loopback; no public net) |

## DoD for flipping `todo` → `have`

1. Suite assert label includes the **TP-ID**.  
2. Case is green without public network for Core.  
3. Primary requirement DTV row updated same change when law changes.  
4. This map row updated same change.

## Last verification

```text
PYTHONPATH=src python3 -m pytest -q tests/
# 38 passed, 1 skipped (2026-10-05) — product 1.4.0 / L2
# skip = TP-ANIMEDLP-04 optional live extract (ANIMEDLP_LIVE_NET not set)
```

**Reviews:**  
- `docs/reviews/reports/2026-08-11-product-review-revision-and-test.md` — 1.2.0 residual close  
- `docs/reviews/reports/2026-08-11-product-review-l2-oop-1.3.0.md` — L2 OOP re-review  
- `docs/reviews/reports/2026-08-19-product-review-open-residuals.md` — ADLP-NET-01 / ADLP-DOC-02 close  

---

**Last Updated:** 2026-08-19  
**Owner:** project maintainers
