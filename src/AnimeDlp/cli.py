#!/usr/bin/env python3
"""
AnimeDlp CLI entry — argument parse, dependency checks, exit-code mapping.
Downloader implementation lives in ``downloader.py``.
"""

from ChronicleLogger import ChronicleLogger
import argparse
import sys

from . import __version__
from .downloader import Anime1Downloader, BeautifulSoup, lxml, requests, yt_dlp
from .errors import AnimeDlpError

# Re-export for tests that patch AnimeDlp.cli.yt_dlp / import Anime1Downloader
__all__ = ["main", "Anime1Downloader", "AnimeDlpError", "yt_dlp"]


def main(argv=None) -> int:
    """CLI entry. Returns process exit code (setuptools wraps with sys.exit)."""
    appname = "AnimeDlp"

    logger = ChronicleLogger(logname=appname)
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
        logger.log_message(
            "'requests' module is not installed. Please install it using: pip install requests",
            level="FATAL",
            component="main",
        )
        return 1

    if BeautifulSoup is None:
        logger.log_message(
            "'beautifulsoup4' and 'lxml' modules are not installed. "
            "Please install using: pip install beautifulsoup4 lxml",
            level="FATAL",
            component="main",
        )
        return 1

    if yt_dlp is None:
        logger.log_message(
            "'yt_dlp' module is not installed. Please install it using: pip install yt-dlp",
            level="FATAL",
            component="main",
        )
        return 1

    if lxml is None:
        logger.log_message(
            "'lxml' module is not installed. Please install it using: pip install lxml",
            level="FATAL",
            component="main",
        )
        return 1

    parser = argparse.ArgumentParser(
        appname,
        formatter_class=argparse.RawTextHelpFormatter,
        description="Clean downloader for anime1.me and anime1.pw",
    )
    parser.add_argument("url", help="URL from anime1.me or anime1.pw")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug output"
    )
    parser.add_argument(
        "-x", "--extract", action="store_true", help="Extract URLs only (no download)"
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

    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        code = e.code
        if code is None:
            return 0
        return int(code) if isinstance(code, int) else 1

    try:
        downloader = Anime1Downloader(args, logger)
        code = downloader.run()
        return int(code) if code is not None else 0
    except AnimeDlpError as e:
        logger.log_message(str(e), level="ERROR", component="main")
        return int(getattr(e, "exit_code", 1) or 1)


if __name__ == "__main__":
    raise SystemExit(main())
