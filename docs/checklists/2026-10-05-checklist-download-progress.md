# Checklist: download progress line

**ID:** CL-DOWNLOAD-PROGRESS  
**Scope:** The long-job line on a terminal download. Law is `requirement-domain-animedlp` 1.1.0. The coordinator is `Anime1Downloader.run`. The bytes come from `YtDlpDownloadService`.  
**Date:** 2026-10-05  
**Product:** 1.4.0  
**Review:** `docs/reviews/2026-10-05-download-progress-review.md`

## 1. What the line says

- [x] A terminal download shows `file {current}/{total}`, the percent finished, and the time until finish. Worked line: `• file 2/5, 40% finished, 1m 05s until finish`.
- [x] The bullet is `•`. The next paint puts a space in that cell. The numbers do not jump.
- [x] Each paint reads the progress again. The time until finish changes when the elapsed time or the percent changes.
- [x] Under one percent the time word is `estimating`.
- [x] The percent counts finished files plus the byte fraction of the current file. Starting file 2 of 2 is already 50%.
- [x] A minute is `1m 05s`. An hour is `1h 01m 01s`. Under a minute the line says `45s until finish`.
- [x] The line is removed when the downloads return.
- [x] The words `please wait` are not painted.
- [x] The sentence `{choice} has been selected. {process} takes time to finish.` is not printed.
- [x] The line is not stored in a module-level constant.

## 2. Where it shows

- [x] A page URL on a terminal shows the line while the videos are saved.
- [x] On that terminal, yt-dlp's own bar is off so it does not overwrite this line. The progress hook still moves the percent.
- [x] `--extract` does not save videos and does not show the line.
- [x] A stream that is not a terminal does not show the line. yt-dlp keeps its own progress there.
- [x] This release has no text menu and no `update-yt-dlp` path. The line is the download path only.
- [x] An empty extract raises before the line is drawn.

## 3. Proof

- [x] `TP-ANIMEDLP-05` in `tests/test_please_wait.py` locks the sentence, the percent math, the yt-dlp hook, the file counter, the terminal flash, the erase, extract, and the quiet stream.
- [x] `PYTHONPATH=src python3 -m pytest -q tests/` — 38 passed, 1 skipped on 2026-10-05. The skip is optional live extract `TP-ANIMEDLP-04`.
- [x] Sample frames under `screenshots/` are drawn from `please_wait_line` and described in the root `README.md`.

## 4. Out of this change

- [x] No second domain file. This line stays on `requirement-domain-animedlp`.
- [x] No timeout seconds were invented.
- [x] No `sudo` and no downloaded install script.
- [x] The five unregistered requirement files stay unregistered.
