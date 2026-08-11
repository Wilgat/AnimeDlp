"""anime1.me extract path (API + playback cookies e/h/p)."""

import json
from typing import Dict, List, Optional, Tuple

from ..errors import AnimeDlpError
from ..util import redact_cookie_map

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None


class Anime1MeExtractor:
    """Extract (title, source_url, cookie_dict) from anime1.me pages."""

    def __init__(self, session, args, logger):
        self.session = session
        self.args = args
        self.logger = logger

    def extract(self, main_url: str) -> List[Tuple[str, str, Dict]]:
        """Extract videos from anime1.me."""
        self.logger.log_message(
            "Using anime1.me extractor", level="INFO", component="extractor"
        )

        videos = self._extract_api_paths(main_url)
        if not videos:
            return []

        result = []
        for title, apireq in videos:
            src, cookie = self._get_anime1_me_source(apireq)
            if src:
                full_src = "https:" + src if src.startswith("//") else src
                result.append((title, full_src, cookie or {}))
                if self.args.verbose:
                    self.logger.log_message(
                        f"Extracted: {title} → {full_src[:80]}...",
                        level="DEBUG",
                        component="extractor",
                    )

        return result

    def _extract_api_paths(self, url: str) -> List[Tuple[str, str]]:
        """Extract titles and data-apireq from anime1.me page."""
        if BeautifulSoup is None:
            raise AnimeDlpError(
                "'beautifulsoup4' is required for anime1.me extraction"
            )
        try:
            if self.args.user_agent and self.args.cloudflare:
                resp = self.session.get(url)
            elif self.args.user_agent or self.args.cloudflare:
                raise AnimeDlpError(
                    "Provide both --user-agent and --cloudflare or neither"
                )
            else:
                self.logger.log_message(
                    "Missing user-agent/cf_clearance, Cloudflare may block",
                    level="WARN",
                    component="extractor",
                )
                resp = self.session.get(url)

            if resp.status_code == 403:
                raise AnimeDlpError("Blocked by Cloudflare")

            soup = BeautifulSoup(resp.text, "lxml")

            titles = [t.get_text().strip() for t in soup.find_all(class_="entry-title")]
            videos = [v.get("data-apireq") for v in soup.find_all(class_="video-js")]

            if not videos or not videos[0]:
                raise AnimeDlpError("Could not find data-apireq")
            if not titles or not titles[0]:
                raise AnimeDlpError("Could not find titles")
            if len(titles) != len(videos):
                raise AnimeDlpError(
                    f"Title/video count mismatch: {len(titles)} titles vs {len(videos)} videos"
                )

            return list(zip(titles, videos))

        except AnimeDlpError:
            raise
        except Exception as e:
            self.logger.log_message(
                f"Failed to extract API paths: {e}",
                level="ERROR",
                component="extractor",
            )
            return []

    def _get_anime1_me_source(
        self, apireq: str
    ) -> Tuple[Optional[str], Optional[Dict]]:
        """Call anime1.me API to get video source and relevant cookies."""
        try:
            data = f"d={apireq}"
            response = self.session.post(
                "https://v.anime1.me/api",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            result = json.loads(response.content.decode("utf-8"))
            src = result["s"][0]["src"]

            cookie_dict = {}
            for cookie in self.session.cookies:
                if cookie.name in ("e", "h", "p"):
                    cookie_dict[cookie.name] = cookie.value

            if self.args.verbose:
                self.logger.log_message(
                    f"API Response src: https:{src}",
                    level="DEBUG",
                    component="api",
                )
                self.logger.log_message(
                    f"Relevant cookies (redacted): {redact_cookie_map(cookie_dict)}",
                    level="DEBUG",
                    component="api",
                )

            return src, cookie_dict

        except Exception as e:
            self.logger.log_message(
                f"anime1.me API call failed: {e}", level="ERROR", component="api"
            )
            return None, None
