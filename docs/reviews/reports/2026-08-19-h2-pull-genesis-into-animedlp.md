# Report: H2 pull genesis → AnimeDlp

**Date:** 2026-08-19  
**Mode:** H2 apply (GENESIS_SSOT → specialized PROJECT_SSOT)  
**User intent:** “sync from genesis” → confirmation map published → **confirm map**

| Role | Path |
|------|------|
| **Source** | `/dev/shm/genesis-template` (ram-drive first) |
| **Target** | `/home/leolio/prjs/AnimeDlp` (hard-disk; no `/dev/shm/AnimeDlp`) |
| **Backup** | `.h2-backup-from-ram-genesis-20260819-065639/` (local hop; global `folder-backup` verify failed) |

## Transfer (map-driven)

| Code | Count | Action |
|------|------:|--------|
| NEW | 160 | copied source → target |
| UPDATE | 144 | overwritten from source |
| SAME | 403 | no-op |
| DEST_ONLY | 3 | **kept** (`nginx-adm.md`, `pitch-desk-design-project.md`, `template-requirement-class-pitch-desk-design.md`) |
| CONFLICT | 2 | **held** (`AGENTS.md`, `docs/README.md`) |
| SKIP_PRODUCT | product classes | ship unit, 11 REQs, tests, reviews, filled CLs, housekeeping, incidents, root product docs, `pyproject.toml`, `build.sh` |

## Surfaces after apply (dest disk)

| Surface | Count |
|---------|------:|
| `docs/skills/skill-*.md` | **72** |
| `docs/terminologies` topics | **348** (genesis 346 + dest-only 2) |
| `docs/policies/policy-*.md` | **16** |
| `docs/human-intro` pages | **80** |
| Law molds `template-*.md` | **119** (genesis 118 + dest-only pitch-desk) |
| Proof molds | **14** |
| Blank checklists | **45** |
| Product `requirement-*.md` | **11** (unchanged) |

## Dest-SSOT map rebind

| Field | After |
|-------|-------|
| Class | Specialized software-development |
| REQs | **11** Active — maps still recognize registry |
| Harness | skills 72 · terms 348 · policies 16 · human-intro 80 · law 119 · proof 14 · blank CL 45 |
| Maps rewritten | `AGENTS.md` live inventory · `docs/README.md` snapshot · terms/templates dest-only rows |
| Scrub | No genesis-seed workspace claim; no host SSH vault / product-brand leaks in transferred harness |

## Protected (untouched)

- `src/AnimeDlp/**`, `tests/**`, `docs/requirements/**`
- Root `README.md` / `CHANGELOG.md` / `LICENSE.md` / `SECURITY.md`
- `pyproject.toml`, `build.sh`

## Backup honesty

Global `folder-backup` 1.9.0 at `/usr/local/bin/folder-backup`; sudoers `/etc/sudoers.d/folder-backup-leolio` present. Operate `backup` failed verify (`840 != 836`); no deposit written. Fallback local hop tree used.

## Verdict

**Pass** — portable harness refreshed from RAM genesis; product specialization preserved; dest maps rebound.
