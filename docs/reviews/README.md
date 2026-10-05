# Reviews

**Purpose:** Durable product/process review records for **AnimeDlp**.  
Not product law (`docs/requirements/`). Not incidents (`docs/incidents/`).

| File | Date | Scope | Status |
|------|------|-------|--------|
| `2026-10-05-download-progress-review.md` | 2026-10-05 | Wait line: file count, percent finished, time until finish | **Current** (`1.4.0`) |
| `test-plan.md` | 2026-10-05 | TP map Core **have**, including TP-ANIMEDLP-05 | **Current** (`1.4.0` / L2) |
| `requirement-test-matrix.md` | 2026-08-19 | REQ ↔ TP RTM (incl. live/integration rows) | **Current** |
| `2026-08-09-product-review.md` | 2026-08-09 | Full product + requirements + tests | Prior |
| `2026-08-09-requirements-review.md` | 2026-08-09 | Requirements set quality | Closed (Active set) |
| `reports/2026-08-11-product-review-revision-and-test.md` | 2026-08-11 | EXIT/ERR/SEC/VER/IO; **1.2.0** | Pass (fixed) |
| `reports/2026-08-11-product-review-l2-oop-1.3.0.md` | 2026-08-11 | **L2 OOP + version 1.3.0** re-review | **Pass** |
| `reports/2026-08-11-h2-sync-from-ram-genesis.md` | 2026-08-11 | Harness H2 (not product law) | Pass |
| `reports/2026-08-11-h2-pull-genesis-into-animedlp.md` | 2026-08-11 | H2 pull genesis → AnimeDlp (housekeeping phase 1) | Pass |
| `reports/2026-08-13-h2-pull-genesis-into-animedlp.md` | 2026-08-13 | H2 pull hard-disk genesis → AnimeDlp (housekeeping phase 1) | Pass |
| `reports/2026-08-19-h2-pull-genesis-into-animedlp.md` | 2026-08-19 | H2 pull RAM genesis → AnimeDlp (confirm map) | Pass |
| `reports/2026-08-23-h2-pull-genesis-into-animedlp.md` | 2026-08-23 | H2 pull RAM genesis → AnimeDlp (confirm map) | Pass |
| `reports/2026-08-24-h2-pull-genesis-into-animedlp.md` | 2026-08-24 | H2 pull RAM genesis → AnimeDlp (confirm map) | Pass |
| `reports/2026-08-19-product-review-open-residuals.md` | 2026-08-19 | Close ADLP-NET-01 + ADLP-DOC-02; **1.3.1** | **Pass** |

## Residuals (honesty)

| ID | Status | Notes |
|----|--------|-------|
| ADLP-NET-01 | **fixed** (2026-08-19) | TP-ANIMEDLP-04 optional live extract; TP-YTDLP-04 loopback HTTP **have** |
| ADLP-DOC-02 | **fixed** (2026-08-19) | Live SSOT was aligned to 1.3.1; **1.4.0** realigns the version cells |
| ADLP-SEC-01 and earlier 1.2.0/1.3.0 findings | **fixed** | Superseded by 2026-08-11 revision + L2 reports |
| ADLP-WAIT-02 | **fixed** (2026-10-05) | A terminal download shows the file line and turns off yt-dlp's own bar |
| ADLP-WAIT-03 | **open** | Five unregistered requirement files stay out of the registry |

## Conventions

| Element | Rule |
|---------|------|
| Path | `docs/reviews/YYYY-MM-DD-<scope>-review.md` |
| Findings IDs | `ADLP-<AREA>-NN` |
| Severity | P0 · P1 · P2 · P3 |
| Status | open · fixed · deferred · wontfix |

## Related

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Product law registry |
| `tests/` | Executable proof |
