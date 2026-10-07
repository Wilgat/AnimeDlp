# Product review: AnimeDlp (mpv command)

**Date:** 2026-10-07
**Reviewer:** implementation pass for the typed `mpv` verb
**Product:** AnimeDlp `1.5.3`
**Ship unit:** `src/AnimeDlp/cli.py`
**Scope:** The typed verb `anime-dlp mpv <url>` and `--id` (default 1). Menu row 2 is unchanged.
**Method:** Disk read of the dispatcher, `MpvStream`, and the CLI requirement. Suite run below.
**Baseline:** `PYTHONPATH=src python3 -m pytest -q tests` — 73 passed, 1 skipped. The skip is optional live extract `TP-ANIMEDLP-04`.

## Summary

`anime-dlp mpv <url>` stays on the terminal. It checks that `mpv` is on PATH and that `mpv --version` contains `mplayer2`, then extracts the page and plays one video. `--id` selects that video. When the switch is omitted, the number is 1. The verb does not save a file and does not open the text menu. The suite that locks this path is green.

## Strengths

| Area | Notes |
|------|--------|
| Same player | Menu row 2 and the verb both call `MpvStream`. One media URL, no output path |
| Fail closed | A missing player does not extract. A bad id does not start mpv. `--id` on another command does not open the menu |
| Numbering | Video numbers start at 1, the same order as the menu title list |
| Proof | `TP-CLI-06` in `tests/test_cli.py` covers the default, `--id 2`, one video, a missing player, a high id, `--id 0`, `--id` alone, a missing URL, and an unsupported host |

## Findings

No open findings in this scope.

### ADLP-MPV-01 — Severity: P2 (medium)
- **Area:** CLI
- **Status:** fixed
- **Location:** `src/AnimeDlp/cli.py` `Cli._stream_cli`
- **Description:** The text menu could stream, and the command line could not.
- **Impact:** A script could not pick one video from a page that has several.
- **Suggestion:** Shipped as `anime-dlp mpv <url> [--id N]` with default 1.
- **Cross-ref:** `requirement-python-cli-interface` Active 1.2.0

## Non-findings (explicitly OK)

| Check | Result |
|-------|--------|
| Menu row 2 still asks for a title when several videos are extracted | Unchanged. The verb does not open that list |
| A page URL with no verb still downloads | `TP-CLI-05` still green |
| Bare `anime-dlp` on a terminal still opens the menu | `TP-CLI-04` still green |
| Operator-readable errors | Each new failure prints `ERROR:` and `Next:` with a command to type. Machine exit code is 1 |
| ChronicleLogger construction | Not in this change. `main` still writes one logger and passes it in |
| Menu pictures | Left as the 1.5.2 captures. The layout did not change |

## Priority remediation order

1. None. ADLP-MPV-01 is fixed in this tree.

## Related

| Artifact | Role |
|----------|------|
| `docs/requirements/requirement-python-cli-interface.md` | Verb and `--id` law |
| `docs/checklists/2026-10-07-checklist-mpv-cli-verb.md` | Filled checklist |
| `docs/reviews/cli-routed-verb-table.md` | Live verb inventory |
| `tests/test_cli.py` | `TP-CLI-06` |

**Written by:** implementation pass, 2026-10-07
**Review status:** closed
