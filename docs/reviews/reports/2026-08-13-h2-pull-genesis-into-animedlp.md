# Report: H2 pull genesis → AnimeDlp (housekeeping phase 1)

**Date:** 2026-08-13  
**Mode:** H2 apply (GENESIS_SSOT → specialized PROJECT_SSOT)  
**User intent:** housekeeping → map option **1** (confirm NEW+UPDATE; hold CONFLICT)

| Role | Path |
|------|------|
| **Source** | `/home/leolio/prjs/genesis-template` (hard-disk; no `/dev/shm/genesis-template`) |
| **Target** | `/home/leolio/prjs/AnimeDlp` (hard-disk; no `/dev/shm/AnimeDlp`) |
| **Backup** | `.h2-backup-from-disk-genesis-20260813-014426/` |

## Transfer (map-driven)

| Code | Count | Action |
|------|------:|--------|
| NEW | 68 | copied source → target |
| UPDATE | 39 | overwritten from source |
| SAME | 446 | no-op |
| DEST_ONLY | 0 | — |
| CONFLICT | 2 | **held** (`AGENTS.md`, `docs/README.md`) |
| SKIP_PRODUCT | 11 classes | ship unit, 11 REQs, tests, reviews, filled CLs, root product docs, `pyproject.toml` |

## Surfaces after apply (dest disk)

| Surface | Count |
|---------|------:|
| `docs/skills/skill-*.md` | **66** |
| `docs/terminologies` topics | **272** |
| `docs/policies/policy-*.md` | **15** |
| `docs/human-intro` pages | **32** |
| Law molds `template-*.md` | **102** |
| Proof molds | **10** |
| Blank checklists | **37** |
| Product `requirement-*.md` | **11** (unchanged) |

## Dest-SSOT map rebind

| Field | After |
|-------|-------|
| Class | Specialized software-development |
| REQs | **11** Active — maps still recognize registry |
| Harness | skills 66 · terms 272 · policies 15 |
| Maps rewritten | `AGENTS.md` live inventory · `docs/README.md` snapshot · skills/terms/templates/human-intro indexes |
| Scrub | 4 nginx skills: “This workspace = Genesis seed” → dest specialized / nginx unbound |

## Protected (untouched)

- `src/AnimeDlp/**`, `tests/**`, `docs/requirements/**`
- Root `README.md` / `CHANGELOG.md` / `LICENSE.md` / `SECURITY.md`
- `pyproject.toml`

## Verdict

**Pass** — portable harness refreshed from hard-disk genesis; product specialization preserved; dest maps rebound.
