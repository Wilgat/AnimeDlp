# CLI routed-verb table

**Product:** AnimeDlp
**Ship unit:** `src/AnimeDlp/cli.py` (`Cli._dispatch`)
**Scan date:** 2026-10-07
**Mode:** full (no previous table)
**Counts:** live 8, not-yet-wired 1, copied 0, re-checked 8

Inventory is the dispatcher. Help text was used only for the explain line. Handler dates come from a `Last updated:` line on that handler. A handler with no such line is `missing`.

## Live

| verb | handler | privilege | last modified date | human-readable |
|------|---------|-----------|--------------------|----------------|
| help | `Cli.build_parser` print_help | you | missing | help: Print the command summary and stop |
| version | `Cli._dispatch` version arm | you | missing | version: Print the package name and version |
| about | `Tui.about_on_screen` | you | missing | about: Show the English product page and a check of this computer |
| mpv | `Cli._stream_cli` | you | 2026-10-07 | mpv: Stream one extracted video in mpv. --id picks the video. The default is 1 |
| self-install | `SelfManage.emit` | you | missing | self-install: Install this package with pip |
| version-check | `SelfManage.emit` | you | missing | version-check: Compare this install with pip |
| self-update | `SelfManage.emit` | you | missing | self-update: Upgrade this package with pip |
| self-uninstall | `SelfManage.emit` | you | missing | self-uninstall: Remove this package with pip. Needs --force |

A page URL in the first position is a download. It is not a named verb. Empty arguments are not a verb. They open the text menu on a terminal.

## Not-yet-wired

| verb | handler | privilege | last modified date | human-readable | status |
|------|---------|-----------|--------------------|----------------|--------|
| language | — | — | — | language: Not a typed verb. Row 4 of the text menu sets the menu language | forbidden |

**Honesty:** This table was read from `Cli._dispatch`. There was no earlier table, so every live token was checked.
