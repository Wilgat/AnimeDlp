**file**: docs/requirements/requirement-python-cli-language.md
**Status**: Active (Version 1.0.6)
**Area**: python
**Key**: `requirement-python-cli-language`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file owns the menu language for AnimeDlp. The text menu can show its boards in one of thirteen languages. English is the default. The person picks a language on front row **4**. The pick is saved for the next run. The picture of the menu stays on `requirement-python-tui`. Typed verbs stay on `requirement-python-cli-interface`. `language` is not one of those verbs.

Class `MenuLanguage` in `src/AnimeDlp/menu_language.py` holds the codes, the saved leaf, and the words. Class `MenuPainter` writes `MenuLanguage(...)` in its constructor and asks that object for the path word and the row text. A factory does not create it.

### 1.1 Human-facing

**In one sentence:** On the AnimeDlp menu, you type **4** to pick the language the menu uses, and the next time you open the menu it still uses that language.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person at the keyboard | `anime-dlp`, then `4` |
| The other role | The menu language object | class `MenuLanguage` in `menu_language.py` |
| Not this file | Download messages other than the please-wait phrase, pip output, help, and the about page | Those stay English in this version |

| Includes | Excludes |
|----------|----------|
| Front row 4, the language board, the saved file, and the words on the menu boards | A `language` argument on the command line |
| English as the default when the file is missing or not a known code | Reading `LANG` or `LC_ALL` to pick the menu language |
| The path word, board titles, category names, Back, Exit, and the choice warning | Translating the folder path, the clock, or a leaf command token such as `view-log` |

| Surface | What you open | What for |
|---------|---------------|----------|
| `anime-dlp` on a terminal | Front board | Row **4** is language. Row **3** is system-log |
| `~/.local/AnimeDlp/language` | One-line file in this login’s home | The code saved from the menu |
| `ANIMEDLP_LANG` | Environment value for this process | Wins over the file and does not write it |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open the language board | The board lists thirteen language names in their own script, numbered 41 through 53, then Back. Numbers 40 and 54 through 59 are not printed. | `4` |
| Save Traditional Chinese | The file stores `zh-Hant`. The front board comes back in Traditional Chinese, and the line above the box says the menu language is Traditional Chinese. | `43` |
| Go back | The file is not written. The front board stays in the language you already had. | `0`, or Esc |
| Start with no saved language | The menu is English. A Traditional Chinese locale does not switch it. | `anime-dlp` |

## 2. Core Rules (Mandatory)

1. **One owner.** This file selects the menu language and owns the words the menu boards print. `requirement-python-tui` draws the path line and the rows. It does not detect a language. `language` **MUST NOT** be an argv verb. `requirement-python-cli-interface` states the same ban.
2. **Default.** The code **MUST** be `en` when the leaf is missing, when the first line is empty, or when that line is not one of the thirteen codes. An invalid first line **MUST NOT** be rewritten. `LANG`, `LANGUAGE`, `LC_ALL`, and `LC_MESSAGES` **MUST NOT** select a code. This file does not use gettext.
3. **Process override.** When `ANIMEDLP_LANG` is one of the thirteen codes, that code **MUST** win at process start. That start **MUST NOT** write the leaf. Any other value of `ANIMEDLP_LANG` is ignored and the leaf is read.
4. **Leaf.** The leaf is `${HOME}/.local/AnimeDlp/language`. The program reads only the first line, ignores a trailing carriage return, and ignores later lines. A menu pick **MUST** write the code, one newline, and nothing else. The directory **MUST** be mode `0700`. The file **MUST** be mode `0600`. The program creates that directory only when a pick is saved. A missing home, or a write that fails, **MUST** keep the code this process already had and **MUST** show the failed-write line in that previous language. The front board **MUST** still return.
5. **Front row 4.** On every host, including Termux, Git Bash, and Windows cmd, the front board **MUST** print row **4** `language`. That row **MUST** open the language board. It **MUST NOT** run a command and **MUST NOT** leave the program. Row **1** is `download`. Row **2** is `stream to mpv player` only when `mpv` is on PATH and `mpv --version` contains `mplayer2`; otherwise row **2** stays omitted. That short stays English. Rows **8** and **9** stay self-management and Exit. **MUST NOT** put `join` on row 1. System-log is front row **3**. Its children are **31** view-log, **32** clear-log, and **33** log-folder. Those numbers are the picture on `requirement-python-tui`. The leaf short `download` stays English.
6. **Language block.** The language board uses the twenty numbers **40** through **59**. Assigned rows are **41** through **53**, in the order below. **40** and **54** through **59** are reserved. They **MUST NOT** be printed. Typing a reserved number **MUST** show the unknown-choice line and **MUST NOT** write the leaf. **0**, an empty Enter on Back, and Esc **MUST** return to the front board and **MUST NOT** write the leaf.
7. **Names on the language board.** Each assigned row **MUST** show that language’s endonym as the short. This build prints the English explain `use this language for this menu` on every language row. The per-language sentence in the table below is the saved-language line. A translated explain for every UI language stays with `TP-LANG-01`.
8. **What follows the code.** This build applies the path word, the saved-language sentence, and the please-wait phrase for the selected code. Board titles, category shorts, Back, Exit, the unknown-choice line, and the failed-write line stay English. Full translation of those strings is `TP-LANG-01` and stays todo. Leaf shorts stay the English tokens `download`, `view-log`, `clear-log`, `log-folder`, `version`, `about`, `version-check`, `self-update`, `self-uninstall`, and `self-install`. `join` is not a leaf.
9. **What stays English.** Extract messages, download messages other than the please-wait phrase, command output, pip lifecycle output, the argv `version` line, host and download fail-closed sentences, the help body, and the about page stay English in this version. On the download line, `file`, `finished`, `until finish`, and `estimating` stay English. The key hint `Up/Down  •  Enter` stays English. The folder path and the clock `HH:MM:SS` are not translated. The product name and the version stay on the status line. The please-wait phrase is the one download phrase this build translates. It is not `TP-LANG-01`.
10. **After a successful pick.** The session **MUST** show the saved-language line and **MUST** return to the front board with the new path word. That line sits above the box. It is not the error line. It stays until the next key. A failed write uses the same place. This build shows the English line `Could not save the menu language`.
11. **Unknown choice.** A number or a word that is not on the current board **MUST** stay on that board and show the unknown-choice line in the selected language. It **MUST NOT** exit the process and **MUST NOT** write the leaf. The English line is `That choice is not on this list. Pick a listed number.`
12. **Clock.** The language board is a clock board. The one-second wait from `requirement-python-tui` rule 13 includes it. A language pick does not open a result page.
13. **Construct.** `MenuPainter.__init__` writes `MenuLanguage(...)`. The session and the model share that painter, so a save updates the rows the next paint reads. The site does not call a factory. `def main` stays in `src/AnimeDlp/cli.py`.
14. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`. This file does **not** add an actor requirement.
15. Dest fence conditions: **considered — none**. Do not invent one.

### 2.1 Implementation Notes (this project)

| Code | Endonym | Row | Path label | Saved line | Failed-write line |
|------|---------|-----|------------|------------|-------------------|
| `en` | English | 41 | Path | Menu language is English | Could not save the menu language |
| `zh-Hans` | 简体中文 | 42 | 路径 | 菜单语言是简体中文 | 无法保存菜单语言 |
| `zh-Hant` | 繁體中文 | 43 | 路徑 | 選單語言是繁體中文 | 無法儲存選單語言 |
| `es` | Español | 44 | Ruta | El idioma del menú es español | No se pudo guardar el idioma del menú |
| `ar` | العربية | 45 | المسار | لغة القائمة هي العربية | تعذر حفظ لغة القائمة |
| `fr` | Français | 46 | Chemin | La langue du menu est le français | Impossible d'enregistrer la langue du menu |
| `pt` | Português | 47 | Caminho | O idioma do menu é português | Não foi possível guardar o idioma do menu |
| `ru` | Русский | 48 | Путь | Язык меню — русский | Не удалось сохранить язык меню |
| `de` | Deutsch | 49 | Pfad | Die Menüsprache ist Deutsch | Die Menüsprache konnte nicht gespeichert werden |
| `ja` | 日本語 | 50 | パス | メニューの言語は日本語 | メニューの言語を保存できませんでした |
| `ko` | 한국어 | 51 | 경로 | 메뉴 언어는 한국어 | 메뉴 언어를 저장하지 못했습니다 |
| `nl` | Nederlands | 52 | Pad | De menutaal is Nederlands | De menutaal kon niet worden opgeslagen |
| `el` | Ελληνικά | 53 | Διαδρομή | Η γλώσσα του μενού είναι ελληνικά | Δεν ήταν δυνατή η αποθήκευση της γλώσσας του μενού |

The download line’s please-wait phrase. `requirement-domain-animedlp` owns where that phrase sits. This file owns the thirteen sentences. English is `please wait`.

| Code | Phrase |
|------|--------|
| `en` | please wait |
| `zh-Hans` | 请稍候 |
| `zh-Hant` | 請稍候 |
| `es` | por favor, espere |
| `ar` | يرجى الانتظار |
| `fr` | veuillez patienter |
| `pt` | aguarde, por favor |
| `ru` | пожалуйста, подождите |
| `de` | bitte warten |
| `ja` | お待ちください |
| `ko` | 잠시만 기다려 주세요 |
| `nl` | even geduld |
| `el` | παρακαλώ περιμένετε |

| Item | Value |
|------|--------|
| **Class** | This build stores the thirteen codes on `Tui` in `src/AnimeDlp/tui.py`. Class `MenuLanguage` remains the named end state and is not in the tree |
| **Painter site** | `Tui` supplies the path word. A pick writes the leaf. The next start reads it. `ANIMEDLP_LANG` wins and does not write |
| **Front row** | **4** language. Children **41**–**53**. Reserved and not printed: **40**, **54**–**59** |
| **System-log** | Front **3**. Children **31** view-log, **32** clear-log, **33** log-folder |
| **Leaf** | `${HOME}/.local/AnimeDlp/language`. Directory mode `0700`. File mode `0600`. Not the cache folder. Not `/var/AnimeDlp` |
| **Override** | `ANIMEDLP_LANG` at process start. Does not write |
| **Back / Exit shorts** | en Back / Exit. zh-Hans 返回 / 离开. zh-Hant 返回 / 離開. es Atrás / Salir. ar رجوع / خروج. fr Retour / Quitter. pt Voltar / Sair. ru Назад / Выход. de Zurück / Beenden. ja 戻る / 終了. ko 뒤로 / 종료. nl Terug / Afsluiten. el Πίσω / Έξοδος |
| **Category shorts** | language: language, 语言, 語言, idioma, لغة, langue, язык, Sprache, 言語, 언어, taal, γλώσσα. Spanish and Portuguese both use idioma. system-log and self-management shorts are the words in `MenuLanguage` for that code. The English tokens stay `system-log` and `self-management` |
| **Language-board tokens** | 41 `english` / `en` / `English`. 42 `simplified-chinese` / `zh-hans` / `zh-Hans` / `简体中文`. 43 `traditional-chinese` / `zh-hant` / `zh-Hant` / `繁體中文`. 44 `spanish` / `es` / `Español` / `español`. 45 `arabic` / `ar` / `العربية` / `عربي`. 46 `french` / `fr` / `Français` / `français`. 47 `portuguese` / `pt` / `Português` / `português` / `portugues`. 48 `russian` / `ru` / `Русский` / `русский`. 49 `german` / `de` / `Deutsch` / `deutsch`. 50 `japanese` / `ja` / `日本語`. 51 `korean` / `ko` / `한국어`. 52 `dutch` / `nl` / `Nederlands` / `nederlands`. 53 `greek` / `el` / `Ελληνικά` / `ελληνικά` |
| **About leaf long (en)** | `version, yt-dlp, and this computer`. The other twelve codes say that fact in that language. The about page stays English and is `requirement-python-about` |
| **Not a verb** | `language` is absent from `Cli.PRODUCT_VERBS` |
| **Proof** | `TP-TUI-09` has for the path word, the leaf, and `ANIMEDLP_LANG`. `TP-LANG-01` stays todo: full translation of every explain, and class `MenuLanguage`, are not this build |

Worked leaf, this login, after choosing Traditional Chinese:

```text
zh-Hant
```

The file is `~/.local/AnimeDlp/language`. The line ends with a newline. A test passes its own home directory into `MenuLanguage(...)` and does not read the developer’s leaf.

Invocation sample for the row this file owns. There is no `anime-dlp language` command. On the open menu:

```text
anime-dlp
4
43
```

That sequence opens the menu, opens the language board, and saves `zh-Hant`.

### 2.2 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): One class owns the codes and the words. The menu picture does not keep a second catalog.
- **CIAO Principle 2 – Intentional**: English is the default. A locale variable does not change the menu.
- **CIAO Principle 21 – Dual Policies**: `language` is named here and on the CLI interface as not a verb.
- **CIAO Principle 22 – File modes**: The leaf is `0600` and its directory is `0700`.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the person runs `anime-dlp` as the normal user. **This requirement:** saving the language file is this login’s home. Do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to write it. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`. Row 4 is numbered on those hosts the same way it is numbered on Linux.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** An invalid file stays English and is not rewritten. A failed write keeps the previous code.
- **Intentional:** Thirteen codes, a block of twenty numbers, and one leaf.
- **Anti-fragile:** `ANIMEDLP_LANG` can force a code for one process without touching the file.
- **Over-protect:** Reserved numbers warn and do not write. Back does not write.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Add `language` as an argv verb.
- Read `LANG` or `LC_ALL` to select the menu language, or restore gettext for this menu.
- Print reserved numbers 40 or 54–59, or write the leaf when one of those numbers is typed.
- Write the leaf on Back, on an empty Enter of Back, or on Esc.
- Translate the folder path, the clock, or a leaf short such as `view-log`.
- Put the language file in the cache folder or under `/var/AnimeDlp`.
- Renumber row 4, or move system-log back onto row 4, to make room.
- Mark `TP-OOP-*` or `TP-TUI-01` through `TP-TUI-08` have from this file.

**Violating this rule is a critical menu-language regression.**

## 5. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry SSOT |
| `docs/requirements/requirement-python-tui.md` | Menu picture. Points here for the selected language |
| `docs/requirements/requirement-python-cli-interface.md` | `language` is not an argv verb |
| `docs/requirements/requirement-python-oop.md` | Class home for `MenuLanguage` |
| `docs/requirements/requirement-class-software-dev.md` | Residual pointer |
| `src/AnimeDlp/menu_language.py` | Codes, leaf, and words |
| `src/AnimeDlp/menu_painter.py` | Writes `MenuLanguage(...)` and paints the rows |

## 6. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Front row 4 opens the language board. Rows 41–53 show the endonyms. 40 and 54–59 are not printed |
| AC-2 | System-log is front row 3. Its children are 31, 32, and 33 |
| AC-3 | A pick writes `${HOME}/.local/AnimeDlp/language` mode `0600` and switches this process |
| AC-4 | Back, Esc, and a reserved number do not write. A failed write keeps the previous code |
| AC-5 | A missing or invalid leaf is English and is not rewritten. `LANG` does not select a code. `ANIMEDLP_LANG` wins and does not write |
| AC-6 | `language` is not an argv verb. Leaf shorts stay English |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-LANG-01** | `tests/test_language.py` | todo | Full board translation and class `MenuLanguage`. Not this build |
| **TP-TUI-09** | `tests/test_tui.py` | **have** | No leaf keeps `Path`. `LANG` does not switch it. A pick saves `zh-Hant` and `路徑`. `ANIMEDLP_LANG` wins and does not write. An invalid leaf is not rewritten |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | Menu language for AnimeDlp. Front row 4. Thirteen codes. Leaf under this login’s home. `TP-LANG-01` has |
| 2026-10-04 | Active 1.0.1 | English about explain is `version, FFmpeg, and this computer`. The about page stays English |
| 2026-10-05 | Active 1.0.2 | Specialized from the VideoJoin bootstrap. About explain no longer names FFmpeg. Product is AnimeDlp |
| 2026-10-05 | Active 1.0.3 | Specialized from the VideoJoin bootstrap. Row 1 is omitted. `join` is not a leaf. The process override is `ANIMEDLP_LANG` |
| 2026-10-05 | Active 1.0.4 | Row 1 is `download`. Row 2 stays omitted. The running session stores the codes on `Tui`. `TP-LANG-01` stays todo |
| 2026-10-07 | Active 1.0.6 | Row 2 `stream to mpv player` is English and appears only when `mpv --version` contains `mplayer2` |
| 2026-10-06 | Active 1.0.5 | The download line’s please-wait phrase follows the saved code. The rest of that line stays English. `TP-LANG-01` stays todo |

---

**Last Updated**: 2026-10-07
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
