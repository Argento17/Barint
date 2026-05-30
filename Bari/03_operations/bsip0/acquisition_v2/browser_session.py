"""
Playwright session manager for BSIP0 acquisition v2.

Manages persistent browser contexts (for cookie/session reuse), network
interception for XHR/fetch product API capture, popup dismissal, and
screenshot-on-failure evidence collection.
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Callable

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    Request,
    Response,
    sync_playwright,
)

SESSIONS_DIR = Path(__file__).parent / "sessions"
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots" / "failure_states"

SESSIONS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_HEADERS = {
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

POPUP_SELECTORS = [
    # Generic cookie/consent banners
    "button[data-testid*='accept']",
    "button[id*='accept-cookie']",
    "button[class*='accept-cookie']",
    "button[class*='cookie-accept']",
    "[aria-label*='Accept']",
    "[aria-label*='agree']",
    # Location / delivery area prompts
    "button[data-testid*='close']",
    "button[aria-label*='Close']",
    "button[aria-label*='סגור']",
    "[data-testid='modal-close-button']",
    # Common dialog close patterns
    ".modal-close",
    ".popup-close",
    ".dialog-close",
    "button.close",
]


class CapturedRequest:
    def __init__(self, url: str, method: str, timestamp: str):
        self.url = url
        self.method = method
        self.timestamp = timestamp
        self.response_status: int | None = None
        self.response_body: bytes | None = None
        self.response_headers: dict = {}

    def to_dict(self) -> dict:
        body_text = None
        if self.response_body:
            try:
                body_text = self.response_body.decode("utf-8")
            except Exception:
                body_text = f"<binary {len(self.response_body)} bytes>"
        return {
            "url": self.url,
            "method": self.method,
            "timestamp": self.timestamp,
            "response_status": self.response_status,
            "response_body_preview": body_text[:2000] if body_text else None,
            "response_body_length": len(self.response_body) if self.response_body else 0,
        }


class BrowserSession:
    """
    Wraps a Playwright persistent context.

    Args:
        retailer_id: short string used for session dir naming and screenshots
        headless: run browser without visible window (default True)
        capture_patterns: list of URL substrings — matching XHR responses are captured
        slow_mo: milliseconds to slow down each Playwright action (0 = off)
    """

    def __init__(
        self,
        retailer_id: str,
        headless: bool = True,
        capture_patterns: list[str] | None = None,
        slow_mo: int = 0,
    ):
        self.retailer_id = retailer_id
        self.headless = headless
        self.capture_patterns = capture_patterns or []
        self.slow_mo = slow_mo

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self.page: Page | None = None

        self.captured: list[CapturedRequest] = []
        self._session_dir = SESSIONS_DIR / retailer_id

    # ------------------------------------------------------------------
    # Context manager

    def __enter__(self) -> "BrowserSession":
        self._playwright = sync_playwright().start()
        self._session_dir.mkdir(exist_ok=True)
        self._context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(self._session_dir),
            headless=self.headless,
            slow_mo=self.slow_mo,
            locale="he-IL",
            timezone_id="Asia/Jerusalem",
            viewport={"width": 1280, "height": 900},
            extra_http_headers=DEFAULT_HEADERS,
            args=["--disable-blink-features=AutomationControlled"],
        )
        self.page = self._context.new_page()
        self.page.on("response", self._on_response)
        return self

    def __exit__(self, *_) -> None:
        try:
            if self._context:
                self._context.close()
            if self._playwright:
                self._playwright.stop()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Network capture

    def _on_response(self, response: Response) -> None:
        if not self.capture_patterns:
            return
        url = response.url
        if not any(pat in url for pat in self.capture_patterns):
            return
        cr = CapturedRequest(
            url=url,
            method=response.request.method,
            timestamp=datetime.utcnow().isoformat(),
        )
        cr.response_status = response.status
        try:
            cr.response_headers = dict(response.headers)
            cr.response_body = response.body()
        except Exception:
            pass
        self.captured.append(cr)

    # ------------------------------------------------------------------
    # Navigation helpers

    def goto(self, url: str, wait_until: str = "domcontentloaded", timeout: int = 30_000) -> bool:
        """Navigate; return True if page loaded without exception."""
        try:
            self.page.goto(url, wait_until=wait_until, timeout=timeout)
            return True
        except Exception as exc:
            self.screenshot(f"nav_fail_{self.retailer_id}")
            print(f"[BrowserSession] goto failed: {exc}")
            return False

    def wait_networkidle(self, timeout: int = 15_000) -> None:
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Popup dismissal

    def dismiss_popups(self, attempts: int = 3, pause_ms: int = 800) -> list[str]:
        """
        Try to click known popup/modal close or accept buttons.
        Returns list of selectors that successfully fired.
        """
        dismissed = []
        for _ in range(attempts):
            clicked_any = False
            for sel in POPUP_SELECTORS:
                try:
                    locator = self.page.locator(sel).first
                    if locator.is_visible(timeout=400):
                        locator.click(timeout=600)
                        dismissed.append(sel)
                        clicked_any = True
                        self.page.wait_for_timeout(pause_ms)
                        break
                except Exception:
                    continue
            if not clicked_any:
                break
        return dismissed

    # ------------------------------------------------------------------
    # Screenshot

    @staticmethod
    def _safe_label(label: str) -> str:
        invalid = r'\/:*?"<>|%'
        for ch in invalid:
            label = label.replace(ch, "_")
        return label[:60]

    def screenshot(self, label: str) -> Path:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        safe = self._safe_label(label)
        path = SCREENSHOTS_DIR / f"{self.retailer_id}_{safe}_{ts}.png"
        try:
            self.page.screenshot(path=str(path), full_page=True)
        except Exception as exc:
            print(f"[BrowserSession] screenshot failed: {exc}")
        return path

    # ------------------------------------------------------------------
    # Content helpers

    def html(self) -> str:
        try:
            return self.page.content()
        except Exception:
            return ""

    def current_url(self) -> str:
        try:
            return self.page.url
        except Exception:
            return ""

    def title(self) -> str:
        try:
            return self.page.title()
        except Exception:
            return ""

    def eval_js(self, expression: str):
        try:
            return self.page.evaluate(expression)
        except Exception:
            return None

    def get_cookies(self) -> list[dict]:
        try:
            return self._context.cookies()
        except Exception:
            return []

    def save_captured(self, out_path: Path) -> None:
        data = [c.to_dict() for c in self.captured]
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # ------------------------------------------------------------------
    # Blocking check

    def is_blocked(self) -> bool:
        """Return True if current page indicates access block."""
        try:
            status_el = self.page.locator("h1").first.text_content(timeout=1000)
        except Exception:
            status_el = ""
        url = self.current_url()
        html = self.html()[:3000].lower()
        block_signals = ["403", "forbidden", "access denied", "blocked", "captcha"]
        return any(sig in html for sig in block_signals)

    def is_maintenance(self) -> bool:
        html = self.html()[:3000].lower()
        return "maintenance" in html and len(self.html()) < 5000

    def is_js_shell(self) -> bool:
        html = self.html()[:5000]
        signals = ["ng-version=", "ng-cont", "angularjs.org", "<app-root", "data-reactroot"]
        return any(s.lower() in html.lower() for s in signals)
