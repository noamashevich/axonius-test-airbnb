import re
import urllib.parse
import difflib
from pages.base_search_page import BaseSearchPage

class AirbnbPage(BaseSearchPage):
    def __init__(self, page):
        """
        A specific page object for Airbnb's search page
        :param page: Playwright Page object.
        """
        super().__init__(page)

    @staticmethod
    def _slug(txt: str) -> str:
        """
        Simplifies a text to a slug format for URL matching.
        """
        return re.sub(r"[^a-z0-9-]+", "", txt.lower().replace(" ", "-"))

    def validate_url_contains(self, expected: dict):
        """
        Validates that the current URL contains the expected search parameters.
        Args: expected (dict): A dictionary like {"location": "Tel Aviv", "adults": 2}
        """
        url = urllib.parse.unquote(self.page.url.lower())

        if "location" in expected:
            exp = self._slug(expected["location"])
            m = re.search(r"/s/([\w~\-]+)/homes", url)
            assert m, f"Can't extract location from {url!r}"

            seg = m.group(1)  # tel-aviv~yafo--israel
            if exp not in seg:
                # Fuzzy fallback: match against each part split by ~ or --
                parts = re.split(r"[~\-]{2}|~", seg)
                assert any(
                    difflib.SequenceMatcher(None, exp, p).ratio() >= 0.8
                    for p in parts
                ), f"Location '{exp}' not found in URL segment '{seg}'"

        for k, v in expected.items():
            if k == "location":
                continue
            val = self._slug(str(v))
            assert f"{k}={val}" in url, f"Missing '{k}={val}' in URL: {url}"
