# Tests — AnimeDlp

Executable proof for product law. **Design map:** `docs/reviews/test-plan.md`.  
**RTM:** `docs/reviews/requirement-test-matrix.md`.

## Status (2026-08-09, product 1.1.0)

| Item | State |
|------|--------|
| Design TP map | present under `docs/reviews/test-plan.md` |
| Automated suites | implemented under `tests/` |
| Runner | `pytest -q tests/` |

## Layout

| File | TP families |
|------|-------------|
| `test_structure.py` | TP-STRUCT |
| `test_packaging.py` | TP-PKG |
| `test_prerequisites.py` | TP-PRE |
| `test_cli.py` | TP-CLI |
| `test_domain.py` | TP-ANIMEDLP |
| `test_download_pipeline.py` | TP-YTDLP |
| `test_errors.py` | TP-ERR |
| `test_exports.py` | TP-STYLE |

## Rules

1. Assert messages / test names **MUST** include the **TP-ID**.  
2. Core cases **MUST NOT** require public network (use mocks).  
3. Flip `todo` → `have` in maps only after green runs.  
4. Do not place executable tests under `docs/templates/`.

## Run

```bash
pip3 install -e ".[ ]" 2>/dev/null || pip3 install -e .
pip3 install pytest
pytest -q tests/
```
