# Review: download progress line

**Date:** 2026-10-05  
**Aligned:** 2026-10-06  
**Product:** AnimeDlp 1.5.1  
**Scope:** On a terminal download, replace yt-dlp's own bar with a flashing bullet, the saved-language words for please wait, the file being saved, the file total, the percent finished, and a time until finish that updates on each flash.  
**Law:** `requirement-domain-animedlp` 1.2.0. Phrases: `requirement-python-cli-language` 1.0.5. Layout peer: `requirement-python-project-structure` 1.0.2 (`please_wait.py`).  
**Checklist:** `docs/checklists/2026-10-05-checklist-download-progress.md`  
**Base:** origin/main `ddb9d3d` (AnimeDlp 1.3.1, L2). The 1.4.0 tree had a positional URL and no text menu. Package 1.5.0 opened the text menu. This line stays on the download path.

## What a person sees

`anime-dlp` with a page URL on a terminal draws one line while the videos are saved. A worked English line is `• please wait. file 2/5, 40% finished, 1m 05s until finish`. The next flash, 0.4 seconds later, draws a space where the bullet was and reads the progress again, so the percent and the time move. When the downloads return, the line is erased. The phrase is the saved menu language. English is `please wait`. `file`, `finished`, `until finish`, and `estimating` stay English.

The percent is `((current - 1) + current-file byte fraction) / total`, truncated. Starting file 2 of 2, before any bytes of that file, is already 50% of the job. Under one percent of the whole job the time word is `estimating`. After that, the time until finish is elapsed × (1 − overall) / overall. A minute is `1m 05s`. An hour is `1h 01m 01s`. Under a minute the line says `45s until finish`.

`--extract` prints sources and does not show the line. A pipe or other non-terminal does not show the line, and yt-dlp keeps its own progress. On a terminal, yt-dlp's bar is turned off (`noprogress`) so it does not overwrite this line. The bytes still arrive through yt-dlp's progress hook.

The line does not print `{choice} has been selected. {process} takes time to finish.`

## Cases

| Case | Result | Proof |
|------|--------|-------|
| Line shape | Saved-language please wait, `file current/total`, percent finished, time until finish. Bullet toggles. The rest of the line does not jump | `test_TP_ANIMEDLP_05_line_names_file_percent_and_time` |
| Phrase | Thirteen saved-language sentences. The read does not write the language leaf | `test_TP_ANIMEDLP_05_please_wait_follows_the_saved_language` |
| Percent and time | File 2 of 4 at half the file is 37%. Thirty seconds elapsed leaves about 50 seconds. File 1 at fraction 0 has no time yet | `test_TP_ANIMEDLP_05_snapshot_percent_and_time_until_finish` |
| Flash then erase | Terminal redraws 30s, then about 1m 30s, then clears the line | `test_TP_ANIMEDLP_05_terminal_bullet_flashes_then_is_erased` |
| Not a terminal | No characters written | `test_TP_ANIMEDLP_05_quiet_stream_is_unchanged` |
| yt-dlp bytes | File 1 at 25/100 of 2 files is 12%. Finished moves that file to 50%. File 2, fragment 1/2, is 75% | `test_TP_ANIMEDLP_05_ytdlp_event_advances_the_current_file` |
| Terminal download | Files are counted 1 then 2. File 1 at 0% says `estimating` with the bullet on and off. File 2 of 2 at 50% says `until finish`. Native progress is quiet. The line is erased | `test_TP_ANIMEDLP_05_download_installs_the_hook_on_a_terminal` |
| Extract and pipe | Extract on a terminal writes nothing. A non-terminal writes nothing and leaves native progress on | `test_TP_ANIMEDLP_05_extract_and_pipe_do_not_draw_the_line` |
| Hook | The progress hook and `noprogress` are set only when this line owns the screen | `test_TP_ANIMEDLP_05_hook_is_installed_only_with_progress` |
| Suite | 38 passed, 1 skipped | `PYTHONPATH=src python3 -m pytest -q tests/` on 2026-10-05. The skip is optional live extract `TP-ANIMEDLP-04` |
| Suite | 48 passed, 1 skipped | `PYTHONPATH=src python3 -m pytest -q tests/` on 2026-10-06. The skip is optional live extract `TP-ANIMEDLP-04` |

## Sample frames

`screenshots/download-progress-file-1.png`, `download-progress-file-2.png`, and `download-progress-file-3.png` are one three-file download. Each wait line is the string from `please_wait_line` with the English phrase:

| Frame | Line |
|-------|------|
| File 1 | `• please wait. file 1/3, 18% finished, 2m 10s until finish` |
| File 2 | `  please wait. file 2/3, 54% finished, 48s until finish` |
| File 3 | `• please wait. file 3/3, 91% finished, 6s until finish` |

File 1 shows the command. Files 2 and 3 do not. The window title is `anime-dlp 1.5.1 — sample download`. The root `README.md` describes each frame. The picture destinations are absolute `https://github.com/Wilgat/AnimeDlp/raw/main/screenshots/…` URLs because the README is also the package description.

## Findings

| ID | Severity | Status | Finding |
|----|----------|--------|---------|
| ADLP-WAIT-02 | P3 | fixed | An earlier port left a positional page URL on yt-dlp's own bar. On 1.4.0 that URL, on a terminal, shows this line and sets `noprogress`. Off a terminal, yt-dlp keeps its bar. |
| ADLP-WAIT-03 | P2 | open | `requirement-python-about`, `requirement-python-cli-language`, `requirement-python-cli-logging`, `requirement-python-oop`, and `requirement-python-readme` are on disk and are not in `docs/requirements/index.md`. This change does not register them. |

There is no pip row and no `update-yt-dlp` verb on this tree, so a pip line that stays at `estimating` is not a finding here.

## Verdict

The wait line matches `requirement-domain-animedlp` 1.2.0. `TP-ANIMEDLP-05` is have. The package string is **1.5.1** in `pyproject.toml` and `src/AnimeDlp/__init__.py`. The frame titles follow **1.5.1**.

**Written:** 2026-10-05  
**Aligned:** 2026-10-06  
**Review status:** Pass, with ADLP-WAIT-03 left open and out of this change.
