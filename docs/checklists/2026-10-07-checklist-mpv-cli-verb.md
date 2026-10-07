# Checklist: mpv command

**ID:** CL-MPV-CLI-VERB
**Scope:** The typed verb `anime-dlp mpv <url>` and `--id`. Law is `requirement-python-cli-interface` 1.2.0. The player is `MpvStream`. The extract is `Anime1Downloader.list_sources`.
**Date:** 2026-10-07
**Product:** 1.5.3
**Review:** `docs/reviews/2026-10-07-mpv-cli-verb-review.md`

## 1. What the verb does

- [x] `anime-dlp mpv <url>` stays on the terminal and does not open the text menu.
- [x] The verb checks that `mpv` is on PATH and that `mpv --version` contains `mplayer2` before it parses the page.
- [x] When that check fails, the process exits 1, names the next command, and does not extract.
- [x] A page with one video streams that video when `--id` is omitted.
- [x] A page with more than one video streams the video numbered by `--id`. Numbers start at 1.
- [x] When `--id` is omitted, the number is 1.
- [x] An id below 1, or above the extracted count, exits 1 and does not start mpv.
- [x] `--id` without the `mpv` verb exits 1 and does not open the menu.
- [x] `mpv` without a page URL exits 1 and does not open the menu.
- [x] The verb does not save a media file and does not call the download run.

## 2. Where it does not apply

- [x] A page URL with no verb still downloads or extracts.
- [x] Bare `anime-dlp` on a terminal still opens the menu.
- [x] Menu row 2 still shows a title list when the page has several videos.
- [x] `mpv` is not installed by this package.

## 3. Proof

- [x] `TP-CLI-06` in `tests/test_cli.py` locks the default id, `--id 2`, one video, a missing player, a high id, `--id 0`, `--id` alone, a missing URL, and an unsupported host.
- [x] `PYTHONPATH=src python3 -m pytest -q tests/` — 73 passed, 1 skipped on 2026-10-07. The skip is optional live extract `TP-ANIMEDLP-04`.

## 4. Out of this change

- [x] Menu pictures stay the 1.5.2 captures.
- [x] No PyPI upload in this change.
- [x] No second domain file.
