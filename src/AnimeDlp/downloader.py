"""
Anime1 coordinator (L2) — session setup, host route, extract→download orchestration.

Site extractors: ``extractors.me`` / ``extractors.pw``.
Download ops: ``download_service.YtDlpDownloadService``.
"""

from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

from .download_service import YtDlpDownloadService, yt_dlp
from .errors import AnimeDlpError
from .extractors import Anime1MeExtractor, Anime1PwExtractor
from .util import redact_cookie_map

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

try:
    import lxml  # noqa: F401
except ImportError:  # pragma: no cover
    lxml = None

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None


class Anime1Downloader:
    """Thin coordinator: route host, run extractors, download or list sources."""

    CLASSNAME = "Anime1Downloader"

    def __init__(self, args, logger):
        if requests is None:
            raise AnimeDlpError(
                "'requests' module is not installed. Please install it using: pip install requests"
            )
        self.args = args
        self.session = requests.Session()
        self.logger = logger

        self.headers = {
            "User-Agent": args.user_agent
            or (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
            )
        }

        self.cookies = {}
        if getattr(args, "cloudflare", None):
            self.cookies["cf_clearance"] = args.cloudflare

        self.session.headers.update(self.headers)
        if self.cookies:
            self.session.cookies.update(self.cookies)

        self.output_dir = getattr(args, "output_dir", None) or None
        self.show_cookies = bool(getattr(args, "show_cookies", False))

        self.me_extractor = Anime1MeExtractor(self.session, args, logger)
        self.pw_extractor = Anime1PwExtractor(self.session, args, logger)
        self.download_service = YtDlpDownloadService(
            user_agent=self.headers["User-Agent"],
            verbose=bool(args.verbose),
            output_dir=self.output_dir,
            logger=logger,
        )

    # ---- Facade methods (tests + thin API; logic lives in collaborators) ----

    def extract_anime1_me(self, main_url: str) -> List[Tuple[str, str, Dict]]:
        """Delegate to Anime1MeExtractor."""
        return self.me_extractor.extract(main_url)

    def extract_anime1_pw(self, main_url: str) -> List[Tuple[str, str]]:
        """Delegate to Anime1PwExtractor."""
        return self.pw_extractor.extract(main_url)

    def download_video(
        self, title: str, video_url: str, special_cookie: Optional[Dict] = None
    ) -> bool:
        """Delegate to YtDlpDownloadService."""
        return self.download_service.download(title, video_url, special_cookie)

    def run(self) -> int:
        """
        Run extract or download pipeline.
        Returns process exit code (0 success, 1 failure). Does not call sys.exit.
        """
        url = self.args.url.strip().rstrip("/")
        self.logger.log_message(f"Processing: {url}", level="INFO", component="main")

        domain = urlparse(url).netloc.lower()
        is_anime1_me = "anime1.me" in domain
        is_anime1_pw = "anime1.pw" in domain

        if not (is_anime1_me or is_anime1_pw):
            raise AnimeDlpError("URL must be from anime1.me or anime1.pw")

        self.logger.log_message(
            f"Detected site: {'anime1.me' if is_anime1_me else 'anime1.pw'}",
            level="INFO",
            component="main",
        )

        all_videos = []

        if is_anime1_me:
            items = self.extract_anime1_me(url)
            for title, src, cookie in items:
                all_videos.append((title, src, cookie))
        else:
            items = self.extract_anime1_pw(url)
            for title, src in items:
                all_videos.append((title, src, None))

        self.logger.log_message(
            f"Total videos found: {len(all_videos)}",
            level="INFO",
            component="main",
        )

        if not all_videos:
            raise AnimeDlpError("No videos extracted")

        if self.args.extract:
            for title, src, cookie in all_videos:
                print(f"Title : {title}")
                print(f"URL   : {src}")
                if cookie:
                    if self.show_cookies:
                        print(f"Cookie: {cookie}")
                    else:
                        print(
                            f"Cookie: {redact_cookie_map(cookie)} "
                            f"(use --show-cookies for values)"
                        )
                print("-" * 70)
            return 0

        failures = 0
        for title, video_url, special_cookie in all_videos:
            ok = self.download_video(title, video_url, special_cookie)
            if not ok:
                failures += 1

        if failures:
            self.logger.log_message(
                f"Completed with {failures} download failure(s) of {len(all_videos)}",
                level="ERROR",
                component="main",
            )
            return 1

        self.logger.log_message(
            "All downloads completed!", level="INFO", component="main"
        )
        return 0
