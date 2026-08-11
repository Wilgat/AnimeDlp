# Reviews

**Purpose:** Durable product/process review records for **AnimeDlp**.  
Not product law (`docs/requirements/`). Not incidents (`docs/incidents/`).

| File | Date | Scope | Status |
|------|------|-------|--------|
| `test-plan.md` | 2026-08-11 | TP map Core **have** (29) + optional live net todos | **Current** (`1.3.0` / L2) |
| `requirement-test-matrix.md` | 2026-08-11 | REQ ↔ TP RTM (incl. architecture + classes) | **Current** |
| `2026-08-09-product-review.md` | 2026-08-09 | Full product + requirements + tests | Prior |
| `2026-08-09-requirements-review.md` | 2026-08-09 | Requirements set quality | Closed (Active set) |
| `reports/2026-08-11-product-review-revision-and-test.md` | 2026-08-11 | EXIT/ERR/SEC/VER/IO; **1.2.0** | Pass (fixed) |
| `reports/2026-08-11-product-review-l2-oop-1.3.0.md` | 2026-08-11 | **L2 OOP + version 1.3.0** re-review | **Pass** |
| `reports/2026-08-11-h2-sync-from-ram-genesis.md` | 2026-08-11 | Harness H2 (not product law) | Pass |

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
