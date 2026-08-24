# Report: close last-review open residuals — AnimeDlp 1.3.1

**Date:** 2026-08-19  
**Mode:** residual close from `reports/2026-08-11-product-review-l2-oop-1.3.0.md`  
**Status:** **Pass**  
**User intent:** “fix all still open”

## Scope

Close the two leftover findings from the 2026-08-11 L2 / 1.3.0 re-review:

| ID | Was | Now |
|----|-----|-----|
| **ADLP-NET-01** | P3 deferred optional — no live/integration suite | **fixed** |
| **ADLP-DOC-02** | P3 accepted residual — live docs still read as 1.1.0/1.2.0 | **fixed** |

No P0/P1/P2 were open.

## ADLP-NET-01

| Field | Value |
|-------|--------|
| **TP-ANIMEDLP-04** | Suite `tests/test_live_network.py`; **optional**; skip unless `ANIMEDLP_LIVE_NET=1` + `ANIMEDLP_LIVE_URL` |
| **TP-YTDLP-04** | Same suite; **have** via loopback HTTP fixture (no public network) |
| **Core** | Still offline (add-tests rule) |
| **DTV** | Domain + download REQs updated; stale `test_domain_extract.py` / wrong ANIMEDLP-03 note corrected |

## ADLP-DOC-02

| Surface | Action |
|---------|--------|
| `tests/README.md` | Was live “product 1.1.0”; now **1.3.1** |
| Historical reviews | Supersession banners; 1.1.0/1.2.0 **history kept** |
| Version SSOT | `pyproject.toml`, `__version__`, README badge, CHANGELOG, SECURITY, requirements index → **1.3.1** |

CHANGELOG `[1.2.0]` / `[1.1.0]` sections stay as history (not a leak of live SSOT).

## Proof

```text
PYTHONPATH=src python3 -m pytest -q tests/
# 30 passed, 1 skipped (2026-08-19) — 1.3.1
# skip = TP-ANIMEDLP-04 (set ANIMEDLP_LIVE_NET=1 to run)
```

## Verdict

**Pass** — both still-open last-review findings closed; product **1.3.1**.

**Last Updated:** 2026-08-19
