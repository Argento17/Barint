"""Shared HTTP helper for Bari integration clients.

Uses only the stdlib (urllib) so clients have zero install footprint. Provides a
single polite GET with a Bari User-Agent, timeout, simple retry/backoff on 429/5xx,
and JSON decoding. Read-only by design — there is no POST/PUT/DELETE here.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

USER_AGENT = "Bari/1.0 (+nutrition-scoring; contact tbarhaim@gmail.com)"
DEFAULT_TIMEOUT = 25


class HttpError(Exception):
    """Raised when a request fails after retries. Carries status when known."""

    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


def get(
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = 2,
    backoff: float = 1.5,
) -> bytes:
    """GET a URL with polite retry on 429/5xx. Returns raw bytes."""
    if params:
        url = f"{url}{'&' if '?' in url else '?'}{urllib.parse.urlencode(params)}"
    # Default Accept is */* — forcing application/json makes content-negotiating servers
    # (e.g. laibcatalog) reject binary .gz downloads with 406. get_json sets JSON itself.
    hdrs = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    if headers:
        hdrs.update(headers)

    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            last_exc = HttpError(f"HTTP {e.code} for {url}", status=e.code)
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(backoff * (attempt + 1))
                continue
            raise last_exc
        except urllib.error.URLError as e:
            last_exc = HttpError(f"network error for {url}: {e.reason}")
            if attempt < retries:
                time.sleep(backoff * (attempt + 1))
                continue
            raise last_exc
    raise last_exc or HttpError(f"unknown error for {url}")


def get_json(url: str, **kwargs) -> Any:
    """GET and decode JSON."""
    headers = {"Accept": "application/json", **(kwargs.pop("headers", None) or {})}
    return json.loads(get(url, headers=headers, **kwargs).decode("utf-8", errors="replace"))
