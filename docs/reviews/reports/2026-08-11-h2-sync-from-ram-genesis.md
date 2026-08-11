# Report: H2 harness sync from RAM genesis — AnimeDlp

**Date:** 2026-08-11  
**Mode:** H2 apply (genesis knowledge → software-dev target)  
**Status:** applied · product protected  
**User confirm:** “confirm map”

## Source / target

| Role | Path |
|------|------|
| **Source (GENESIS_SSOT)** | `/dev/shm/genesis-template` (ram-drive first) |
| **Target (PROJECT_SSOT)** | `/var/www/grok.dr-sense.com/prjs/AnimeDlp` |

## Pre-flight

PASS (roots exist, hop H2-style, ship unit + 9 product REQs + reviews/tests SKIP_PRODUCT, no secrets plan).

## Confirmation map totals (applied)

| Code | Count | Action |
|------|------:|--------|
| NEW | 468 | copied |
| UPDATE | 1 | `AGENTS.md` overwritten from genesis |
| SAME | 0 | — |
| DEST_ONLY | 0 | — |
| CONFLICT / keep | 1 | `.gitignore` kept (product-tuned AnimeDlp) |
| SKIP_PRODUCT | ship unit, REQs, tests, reviews, product README/… | not transferred |

## Surfaces transferred

| Surface | Files on dest |
|---------|--------------:|
| `docs/skills` | 57 |
| `docs/terminologies` | 229 |
| `docs/templates` | 140 |
| `docs/policies` | 15 |
| `docs/human-intro` | 15 |
| `docs/whitelists` | 10 |
| `docs/incidents` | 1 (README shell) |
| `docs/README.md` | yes |
| `AGENTS.md` | updated (backup: `AGENTS.md.bak-before-h2-sync-*`) |

## Excluded (not transferred)

- `docs/requirements/**` (product law preserved — class + domain + Python REQs intact)
- `docs/checklists/` (filled genesis audit trails)
- `docs/reviews/**` (product proof)
- Ship unit, tests, product user markdown, pyproject, build.sh, cy-master
- `.gitignore` (kept dest product version by confirmed map)

## Integrity

- Ship unit `src/AnimeDlp` present  
- 9 product `requirement-*.md` including class + domain  
- `reviews/` and `tests/` untouched  
- Residual rsync dry-run on transferred surfaces: empty  
- `.gitignore` still product-labeled AnimeDlp  

## Honesty residual

**Closed 2026-08-11:** Dest-SSOT map rebind rule added to H1/H2 skills + terms; AnimeDlp `AGENTS.md` + `docs/README.md` now recognize **9** Active REQs (software-dev). See `docs/checklists/2026-08-11-checklist-dest-ssot-map-rebind-rule.md`.

## Verdict

**Pass** — portable harness knowledge pulled from RAM genesis; product specialization preserved.
