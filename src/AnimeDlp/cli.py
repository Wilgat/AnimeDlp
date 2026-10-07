#!/usr/bin/env python3
"""
AnimeDlp CLI entry — argument parse, text menu, dependency checks, exit codes.

Downloader implementation lives in ``downloader.py``.
The text menu lives in ``tui.py``.
requirement-python-cli-interface — a page URL stays on the terminal.
On a terminal with no URL, the text menu opens.
With no terminal and no URL, this module prints help and returns 0.
"""

from ChronicleLogger import ChronicleLogger
import argparse
import io
import sys
from contextlib import redirect_stdout

from . import __version__
from .about_page import AboutPage
from .check_system import CheckSystem
from .downloader import Anime1Downloader, BeautifulSoup, lxml, requests, yt_dlp
from .errors import AnimeDlpError
from .self_management import SelfManage
from .tui import Tui

# Re-export for tests that patch AnimeDlp.cli.yt_dlp / import Anime1Downloader
__all__ = ["main", "Cli", "Anime1Downloader", "AnimeDlpError", "yt_dlp"]

_VALUE_FLAGS = {
    "-cf",
    "--cloudflare",
    "-ua",
    "--user-agent",
    "-o",
    "--output-dir",
}
_SWITCHES = {
    "-v",
    "--verbose",
    "--debug",
    "-x",
    "--extract",
    "--show-cookies",
    "--force",
}


class Cli:
    """Argument contract and the door into the text menu."""

    APP_NAME = "AnimeDlp"
    CONSOLE_NAME = "anime-dlp"
    AUTHOR_NAME = "Wilgat Wong"
    LAST_UPDATE = "2026-10-07"
    HOMEPAGE = "https://github.com/Wilgat/AnimeDlp"
    BASIC_USAGE = "anime-dlp <url>"
    PRODUCT_VERBS = (
        "help",
        "version",
        "about",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
    )

    def __init__(self, logger):
        self.logger = logger
        self.version = __version__
        self.app_name = self.APP_NAME
        self.flags = None
        self.check = None
        self.about = None
        self.self_manage = None
        self.tui = None

    def _ensure_menu(self):
        """Build the text-menu stack on the first screen. A URL download does not."""
        if self.tui is not None:
            return
        logger = self.logger
        self.check = CheckSystem(
            logger=logger,
            app_name=self.APP_NAME,
            version=self.version,
            console_name=self.CONSOLE_NAME,
        )
        self.about = AboutPage(
            self.check,
            self.APP_NAME,
            self.version,
            self.AUTHOR_NAME,
            self.LAST_UPDATE,
            self.HOMEPAGE,
            "",
            self.BASIC_USAGE,
            self.CONSOLE_NAME,
            logger=logger,
        )
        self.self_manage = SelfManage(self.APP_NAME, self.version, logger=logger)
        self.tui = Tui(self, logger=logger)

    @staticmethod
    def stdout_is_tty():
        """Whether the text screen can be drawn on this stdout."""
        try:
            return sys.stdout.isatty()
        except Exception:
            return False

    @staticmethod
    def opens_text_screen(argv):
        """
        Whether this argv draws the text screen.

        The real parser has not run yet. This walk only decides is_quiet.
        Help, version, a page URL, and the pip verbs do not draw the screen.
        Empty argv and about do, when stdout is a terminal.
        --debug and the other switches, with no URL, still draw the screen.
        """
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        if not Cli.stdout_is_tty():
            return False
        if any(token in ("-h", "--help", "--version") for token in argv):
            return False
        positionals = []
        pending_value = False
        for token in argv:
            if pending_value:
                pending_value = False
                continue
            if token in _VALUE_FLAGS:
                pending_value = True
                continue
            if token in _SWITCHES:
                continue
            if token.startswith("-"):
                name = token.split("=", 1)[0]
                if name in _VALUE_FLAGS or name in _SWITCHES:
                    continue
                return False
            positionals.append(token)
        if not positionals:
            return True
        return positionals == ["about"]

    @staticmethod
    def quiet_console(argv):
        """Keep ChronicleLogger off the console when the text screen or about owns stdout."""
        if Cli.opens_text_screen(argv):
            return True
        if argv is None:
            argv = sys.argv[1:]
        positionals = []
        pending_value = False
        for token in list(argv):
            if pending_value:
                pending_value = False
                continue
            if token in _VALUE_FLAGS:
                pending_value = True
                continue
            if token in _SWITCHES or token in ("-h", "--help", "--version"):
                continue
            if token.startswith("-"):
                name = token.split("=", 1)[0]
                if name in _VALUE_FLAGS or name in _SWITCHES:
                    continue
                return False
            positionals.append(token)
        return positionals == ["about"]

    def report_error(self, message, nxt):
        """User-visible failure plus the same fact on the logger when one exists."""
        if self.logger is not None:
            self.logger.log_message(
                "{0} Next: {1}".format(message, nxt),
                level="ERROR",
                component="main",
            )
        print("ERROR: {0}".format(message), file=sys.stderr)
        print("   Next: {0}".format(nxt), file=sys.stderr)
        return 1

    def build_parser(self):
        """URL optional. No URL on a terminal opens the text menu."""
        parser = argparse.ArgumentParser(
            prog=self.CONSOLE_NAME,
            formatter_class=argparse.RawTextHelpFormatter,
            description=(
                "Clean downloader for anime1.me and anime1.pw.\n"
                "With no URL on a terminal, opens the text menu.\n"
                "With no URL and no terminal, prints this help and stops.\n"
                "A page URL downloads or extracts and does not open the menu.\n"
                "Verbs: help, version, about, self-install, version-check,\n"
                "self-update, self-uninstall. language is not a verb."
            ),
        )
        parser.add_argument(
            "target",
            nargs="?",
            default=None,
            metavar="url",
            help="Page URL from anime1.me or anime1.pw",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Enable debug output",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Same as --verbose. With no URL, still opens the text menu",
        )
        parser.add_argument(
            "-x",
            "--extract",
            action="store_true",
            help="Extract URLs only (no download)",
        )
        parser.add_argument("-cf", "--cloudflare", help="cf_clearance cookie value")
        parser.add_argument("-ua", "--user-agent", help="Custom User-Agent string")
        parser.add_argument(
            "-o",
            "--output-dir",
            default=None,
            help="Directory for downloads (default: current directory)",
        )
        parser.add_argument(
            "--show-cookies",
            action="store_true",
            help="Print full playback cookie values in --extract mode (default: redacted)",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Confirm self-uninstall. Required on the command line",
        )
        parser.add_argument(
            "--version",
            action="version",
            version="{0} {1}".format(self.APP_NAME, __version__),
        )
        return parser

    def _namespace(self, url):
        """Flags from this run, with the page URL filled in."""
        flags = self.flags
        return argparse.Namespace(
            url=url,
            verbose=bool(getattr(flags, "verbose", False) or getattr(flags, "debug", False)),
            extract=bool(getattr(flags, "extract", False)),
            cloudflare=getattr(flags, "cloudflare", None),
            user_agent=getattr(flags, "user_agent", None),
            output_dir=getattr(flags, "output_dir", None),
            show_cookies=bool(getattr(flags, "show_cookies", False)),
        )

    def _download_cli(self, url):
        """A typed page URL stays on the terminal and does not open the menu."""
        try:
            downloader = Anime1Downloader(self._namespace(url), self.logger)
            code = downloader.run()
            return int(code) if code is not None else 0
        except AnimeDlpError as exc:
            self.logger.log_message(str(exc), level="ERROR", component="main")
            return int(getattr(exc, "exit_code", 1) or 1)

    def list_page(self, url):
        """Extract one page for the stream row. Does not download."""
        downloader = Anime1Downloader(self._namespace(url), self.logger)
        return downloader.list_sources(), downloader.headers["User-Agent"]

    def download_page(self, url):
        """One menu download. stdout is kept for the result page."""
        sink = io.StringIO()
        try:
            with redirect_stdout(sink):
                downloader = Anime1Downloader(self._namespace(url), self.logger)
                code = downloader.run()
        except AnimeDlpError as exc:
            extra = sink.getvalue().strip()
            text = "ERROR: {0}".format(exc)
            if extra:
                return text + "\n\n" + extra
            return text
        body = sink.getvalue().strip()
        if code == 0:
            head = "Finished {0}".format(url)
        else:
            head = "Download failed ({0}) for {1}".format(code, url)
        if body:
            return head + "\n\n" + body
        return head

    def _dispatch(self, args):
        """One page URL, one verb, the front board, or help."""
        target = args.target
        if args.debug:
            args.verbose = True
        self.flags = args
        if args.force and target != "self-uninstall":
            return self.report_error(
                "--force is only for self-uninstall.",
                "{0} self-uninstall --force".format(self.CONSOLE_NAME),
            )
        if target == "help":
            self.build_parser().print_help()
            return 0
        if target == "version":
            print("{0} {1}".format(self.APP_NAME, self.version))
            return 0
        if target == "about":
            self._ensure_menu()
            result = self.tui.about_on_screen()
            if isinstance(result, int):
                return result
            print(result)
            return 0
        if target == "self-uninstall":
            if not args.force:
                return self.report_error(
                    "self-uninstall removes this package with pip.",
                    "{0} self-uninstall --force".format(self.CONSOLE_NAME),
                )
            self._ensure_menu()
            return self.self_manage.emit(target)
        if target in ("version-check", "self-update", "self-install"):
            self._ensure_menu()
            return self.self_manage.emit(target)
        if target:
            return self._download_cli(target)
        if not self.stdout_is_tty():
            self.build_parser().print_help()
            return 0
        self._ensure_menu()
        action = self.tui.open_text_menu()
        if action == "missing":
            return 1
        return 0

    def run(self, argv=None):
        """One job. def main already wrote ChronicleLogger(...) and passed it in."""
        if argv is None:
            argv = sys.argv[1:]
        parser = self.build_parser()
        try:
            args = parser.parse_args(list(argv))
        except SystemExit as exc:
            code = exc.code
            if code is None or code == 0:
                return 0
            return int(code) if isinstance(code, int) else 1
        return self._dispatch(args)


def _missing_module(logger, message):
    logger.log_message(message, level="FATAL", component="main")
    # The text-menu path quiets the console mirror. The missing-module line
    # still has to be visible.
    print(message, file=sys.stderr)
    return 1


def main(argv=None) -> int:
    """CLI entry. Returns process exit code (setuptools wraps with sys.exit)."""
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)

    logger = ChronicleLogger(logname="AnimeDlp", is_quiet=Cli.quiet_console(argv))
    appname = logger.logName()
    _basedir = logger.baseDir()

    if logger.isDebug():
        logger.log_message(
            f"{appname} v{__version__} ({__file__})",
            component="main",
        )
        logger.log_message(
            f"Using {ChronicleLogger.class_version()}", component="main"
        )

    if requests is None:
        return _missing_module(
            logger,
            "'requests' module is not installed. Please install it using: pip install requests",
        )
    if BeautifulSoup is None:
        return _missing_module(
            logger,
            "'beautifulsoup4' and 'lxml' modules are not installed. "
            "Please install using: pip install beautifulsoup4 lxml",
        )
    if yt_dlp is None:
        return _missing_module(
            logger,
            "'yt_dlp' module is not installed. Please install it using: pip install yt-dlp",
        )
    if lxml is None:
        return _missing_module(
            logger,
            "'lxml' module is not installed. Please install it using: pip install lxml",
        )

    app = Cli(logger)
    return app.run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
