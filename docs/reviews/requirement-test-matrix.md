# AnimeDlp — requirement ↔ test matrix (RTM)

**Product:** AnimeDlp `1.1.0`  
**Updated:** 2026-08-09  
**Map:** `docs/reviews/test-plan.md`  
**Law registry:** `docs/requirements/index.md`

## Matrix

| Requirement key | Area | TP families | Core TP-IDs (minimum) | Coverage status |
|-----------------|------|-------------|------------------------|-----------------|
| `requirement-class-software-dev` | class | (document + packaging smoke) | TP-PKG-*, TP-STRUCT-01 | **have** (via peers) |
| `requirement-domain-animedlp` | domain | **TP-ANIMEDLP**, TP-CLI | TP-ANIMEDLP-01..03, TP-CLI-03 | **have** |
| `requirement-download-ytdlp-pipeline` | download | **TP-YTDLP** | TP-YTDLP-01..03 | **have** |
| `requirement-python-cli-interface` | python | **TP-CLI**, TP-PKG | TP-CLI-01..03, TP-PKG-01 | **have** |
| `requirement-python-packaging` | python | **TP-PKG** | TP-PKG-01..03 | **have** |
| `requirement-python-project-structure` | python | **TP-STRUCT** | TP-STRUCT-01 | **have** |
| `requirement-python-coding-style` | python | **TP-STYLE** | TP-STYLE-01 | **have** |
| `requirement-python-error-handling` | python | **TP-ERR** | TP-ERR-01..02 | **have** |
| `requirement-runtime-prerequisites` | runtime | **TP-PRE** | TP-PRE-01..02 | **have** |

## Ownership rules

1. Each Core TP-ID has exactly one **primary** requirement in `test-plan.md` (peers may be secondary).  
2. Domain subject family is **`TP-ANIMEDLP-*`** only (not `TP-DOMAIN-*`).  
3. Class residual covered by packaging/structure smoke.  
4. Do not mark requirement “verified” while its Core TP-IDs remain `todo`.

## Out of scope

| Topic | Reason |
|-------|--------|
| Online install / self-update | Intentionally absent product mode |
| Type 1 sudoers elev | Intentionally absent |
| FFmpeg product encode gate | Not this product |

---

**Last Updated:** 2026-08-09  
**Owner:** project maintainers
