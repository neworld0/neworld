import logging
from dataclasses import dataclass
from typing import Mapping, Optional
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logger = logging.getLogger("neworld.crawler")


class WolClientError(Exception):
    pass


class WolNetworkError(WolClientError):
    pass


class WolTimeoutError(WolNetworkError):
    pass


class WolHttpStatusError(WolClientError):
    pass


class WolEmptyResponseError(WolClientError):
    pass


class WolUnexpectedContentTypeError(WolClientError):
    pass


class WolRedirectError(WolClientError):
    pass


class WolParseError(WolClientError):
    pass


class WolValidationError(WolClientError):
    pass


@dataclass(frozen=True)
class WolResponse:
    url: str
    text: str
    status_code: int
    headers: Mapping[str, str]


class WolClient:
    def __init__(self, session=None, timeout=(5, 15), max_bytes=2_000_000):
        self.session = session or self._session()
        self.timeout = timeout
        self.max_bytes = max_bytes

    @staticmethod
    def _session():
        session = requests.Session()
        retry = Retry(
            total=2,
            connect=2,
            read=1,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(("GET",)),
            respect_retry_after_header=True,
        )
        session.mount("https://", HTTPAdapter(max_retries=retry))
        return session

    def get_html(self, url: str) -> WolResponse:
        logger.info("event=WOL_FETCH_START url=%s", url)
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
        except requests.Timeout as exc:
            self._fail(url, "timeout")
            raise WolTimeoutError("WOL request timed out") from exc
        except requests.RequestException as exc:
            self._fail(url, "network_error")
            raise WolNetworkError("WOL request failed") from exc

        final = urlparse(response.url)
        if final.hostname != "wol.jw.org":
            self._fail(url, "unexpected_redirect", response.status_code)
            raise WolRedirectError("WOL redirected to an unexpected host")
        if response.status_code != 200:
            self._fail(url, "http_status", response.status_code)
            raise WolHttpStatusError("Unexpected WOL status: %s" % response.status_code)
        content_type = response.headers.get("Content-Type", "").lower()
        if "html" not in content_type:
            self._fail(url, "unexpected_content_type", response.status_code)
            raise WolUnexpectedContentTypeError("WOL response is not HTML")
        body = response.content
        if not body or not body.strip():
            self._fail(url, "empty_response", response.status_code)
            raise WolEmptyResponseError("WOL returned an empty response")
        if len(body) > self.max_bytes:
            self._fail(url, "response_too_large", response.status_code)
            raise WolValidationError("WOL response exceeds the safe size limit")
        response.encoding = response.encoding or "utf-8"
        logger.info("event=WOL_FETCH_OK url=%s status=%s response_bytes=%s", url, response.status_code, len(body))
        return WolResponse(response.url, response.text, response.status_code, response.headers)

    @staticmethod
    def _fail(url: str, reason: str, status: Optional[int] = None):
        logger.warning("event=WOL_FETCH_FAIL url=%s status=%s reason=%s", url, status or "none", reason)

