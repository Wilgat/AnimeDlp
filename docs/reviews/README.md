# Reviews

**Purpose:** Durable product/process review records for **AnimeDlp**.  
Not product law (`docs/requirements/`). Not incidents (`docs/incidents/`).

| File | Date | Scope | Status |
|------|------|-------|--------|
| `test-plan.md` | 2026-08-19 | TP map Core **have** + TP-YTDLP-04 have + TP-ANIMEDLP-04 optional | **Current** (`1.3.1` / L2) |
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
| ADLP-DOC-02 | **fixed** (2026-08-19) | Live SSOT is 1.3.1; historical reviews marked superseded |
| ADLP-SEC-01 and earlier 1.2.0/1.3.0 findings | **fixed** | Superseded by 2026-08-11 revision + L2 reports |

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
