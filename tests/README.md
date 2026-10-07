# Tests — AnimeDlp

Executable proof for product law. **Design map:** `docs/reviews/test-plan.md`.  
**RTM:** `docs/reviews/requirement-test-matrix.md`.

## Status (2026-10-07, product 1.5.3)

| Item | State |
|------|--------|
| Design TP map | present under `docs/reviews/test-plan.md` |
| Automated suites | implemented under `tests/` |
| Runner | `PYTHONPATH=src python3 -m pytest -q tests/` |
| Live extract | optional; `ANIMEDLP_LIVE_NET=1` + `ANIMEDLP_LIVE_URL` |

## Layout

| File | TP families |
|------|-------------|
| `test_structure.py` | TP-STRUCT |
| `test_packaging.py` | TP-PKG |
| `test_prerequisites.py` | TP-PRE |
| `test_cli.py` | TP-CLI, including TP-CLI-06 for the `mpv` verb |
| `test_mpv_stream.py` | mplayer2 detection and one media URL |
| `test_tui.py` | menu door and rows; **TP-TUI-10** |
| `test_domain.py` | TP-ANIMEDLP-01..03 |
| `test_please_wait.py` | TP-ANIMEDLP-05 |
| `test_download_pipeline.py` | TP-YTDLP-01..03, TP-YTDLP-05 |
| `test_live_network.py` | TP-ANIMEDLP-04, TP-YTDLP-04 |
| `test_errors.py` | TP-ERR |
| `test_exports.py` | TP-STYLE |
| `test_security_redaction.py` | TP-SEC |
| `test_architecture.py` | TP-ARCH, TP-CLASS |

## Rules

1. Assert messages / test names **MUST** include the **TP-ID**.  
2. Core cases **MUST NOT** require public network (use mocks or loopback).  
3. Flip `todo` → `have` in maps only after green runs.  
4. Do not place executable tests under `docs/templates/`.  
5. Live extract (**TP-ANIMEDLP-04**) stays opt-in.

## Run

```bash
pip3 install -e .
pip3 install pytest
PYTHONPATH=src python3 -m pytest -q tests/

# Optional live extract (real host; may skip on Cloudflare):
ANIMEDLP_LIVE_NET=1 ANIMEDLP_LIVE_URL='https://anime1.me/…' \
  PYTHONPATH=src python3 -m pytest -q tests/test_live_network.py
```
