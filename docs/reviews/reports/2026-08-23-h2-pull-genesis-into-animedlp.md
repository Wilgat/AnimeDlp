# Report: H2 pull genesis → AnimeDlp

**Date:** 2026-08-23  
**Mode:** H2 apply (GENESIS_SSOT → specialized PROJECT_SSOT)  
**User intent:** “sync from genesis” → confirmation map published → **confirm map**

| Role | Path |
|------|------|
| **Source** | `/dev/shm/genesis-template` (ram-drive first) |
| **Target** | `/home/leolio/prjs/AnimeDlp` (hard-disk; no `/dev/shm/AnimeDlp`) |
| **Backup** | `.h2-backup-from-ram-genesis-20260823-140307/` (local hop; global `folder-backup` grant-too-narrow) |

## Transfer (map-driven)

| Code | Count | Action |
|------|------:|--------|
| NEW | 58 | copied source → target |
| UPDATE | 175 | overwritten from source |
| SAME | 537 | no-op |
| DEST_ONLY | 3 | **kept** (`nginx-adm.md`, `pitch-desk-design-project.md`, `template-requirement-class-pitch-desk-design.md`) |
| CONFLICT | 3 | **held** (`AGENTS.md`, `docs/README.md`, `.gitignore`) |
| SKIP_PRODUCT | product classes | ship unit, 11 REQs, tests, reviews, filled CLs, housekeeping, incidents, root product docs, `pyproject.toml`, `build.sh` |

## Surfaces after apply (dest disk)

| Surface | Count |
|---------|------:|
| `docs/skills/skill-*.md` | **75** |
| `docs/terminologies` topics | **377** (genesis 375 + dest-only 2) |
| `docs/policies/policy-*.md` | **16** |
| `docs/human-intro` pages | **104** (`README` + `FORMAT` + 102 topics) |
| Law molds `template-*.md` | **120** (genesis 119 + dest-only pitch-desk) |
| Proof molds | **15** |
| Blank checklists | **45** |
| Product `requirement-*.md` | **11** (unchanged) |

## Dest-SSOT map rebind

| Field | After |
|-------|-------|
| Class | Specialized software-development |
| REQs | **11** Active — maps still recognize registry |
| Harness | skills 75 · terms 377 · policies 16 · human-intro 104 · law 120 · proof 15 · blank CL 45 |
| Maps rewritten | `AGENTS.md` live inventory · `docs/README.md` snapshot · terms/templates dest-only rows |
| Scrub | No genesis-seed workspace claim; no host SSH vault / product-brand leaks in transferred harness |

## Protected (untouched by H2)

- `src/AnimeDlp/**`, `tests/**`, `docs/requirements/**`
- Root `README.md` / `CHANGELOG.md` / `LICENSE.md` / `SECURITY.md`
- `pyproject.toml`, `build.sh`, `.gitignore`

## Backup honesty

```text
SK-USE-FOLDER-BACKUP readiness
APP_NAME: folder-backup
TARGET_USER: leolio
GLOBAL_BIN path: /usr/local/bin/folder-backup
version: 1.11.0
about trust tier: production
sudoers corroboration: /etc/sudoers.d/folder-backup-leolio exists
operate: sudo -n /usr/local/bin/folder-backup backup /home/leolio/prjs/AnimeDlp
operate exit / Verified: FAIL (password required)
Gate: FAIL
Fallback: local hop tree
```

Sudoers Cmnd is **grant-too-narrow** (exact argv is a list of dest filenames, not `backup *` / dest path). Host also has `(ALL:ALL) ALL` password sudo — **not** used from this non-TTY session. Local hop used (weaker than global deposit).

## Verdict

**Pass** — portable harness refreshed from RAM genesis; product specialization preserved; dest maps rebound.
