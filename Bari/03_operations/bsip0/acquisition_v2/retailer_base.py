"""
Abstract base class for all retailer probes in BSIP0 acquisition v2.

Every probe returns a RetailProbeResult which feeds into acquisition_audit_v2.py.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class RawProduct:
    """
    A single product as extracted by a retailer probe.
    All text fields are stored verbatim from the source.
    """
    retailer_id: str
    retailer_name: str
    source_url: str
    scraped_at: str

    # Identity
    name_he: str = ""
    name_en: str = ""
    brand: str = ""
    barcode: str = ""

    # Category
    category_raw: str = ""
    subcategory_raw: str = ""

    # Nutrition (per 100g, raw strings from label)
    energy_kcal_raw: str = ""
    protein_raw: str = ""
    carbs_raw: str = ""
    fat_raw: str = ""
    fiber_raw: str = ""
    sodium_raw: str = ""
    sugar_raw: str = ""

    # Ingredients
    ingredients_raw: str = ""
    ingredients_language: str = ""

    # Images
    image_urls: list[str] = field(default_factory=list)

    # Internal provenance
    extraction_method: str = ""   # "ssr_json" | "xhr_capture" | "dom_parse" | "api_direct"
    extraction_confidence: str = ""  # "high" | "medium" | "low"
    raw_source_json: dict = field(default_factory=dict)

    def has_nutrition(self) -> bool:
        return bool(self.energy_kcal_raw or self.carbs_raw or self.fat_raw or self.protein_raw)

    def has_ingredients(self) -> bool:
        return bool(self.ingredients_raw and len(self.ingredients_raw) > 10)

    def to_dict(self) -> dict:
        return {
            "retailer_id": self.retailer_id,
            "retailer_name": self.retailer_name,
            "source_url": self.source_url,
            "scraped_at": self.scraped_at,
            "name_he": self.name_he,
            "name_en": self.name_en,
            "brand": self.brand,
            "barcode": self.barcode,
            "category_raw": self.category_raw,
            "subcategory_raw": self.subcategory_raw,
            "nutrition": {
                "energy_kcal_raw": self.energy_kcal_raw,
                "protein_raw": self.protein_raw,
                "carbs_raw": self.carbs_raw,
                "fat_raw": self.fat_raw,
                "fiber_raw": self.fiber_raw,
                "sodium_raw": self.sodium_raw,
                "sugar_raw": self.sugar_raw,
            },
            "ingredients_raw": self.ingredients_raw,
            "ingredients_language": self.ingredients_language,
            "image_urls": self.image_urls,
            "extraction_method": self.extraction_method,
            "extraction_confidence": self.extraction_confidence,
        }


@dataclass
class RetailProbeResult:
    """Output from a single retailer probe run."""
    retailer_id: str
    retailer_name: str
    probe_run_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    # Access status
    access_method: str = ""    # "http_static" | "playwright_browser"
    access_status: str = ""    # "accessible" | "blocked" | "partial" | "maintenance" | "failed"
    http_status: int | None = None
    blocker_type: str = ""     # "http_403" | "maintenance_mode" | "angularjs_spa" | "auth_required" | "captcha" | "timeout"
    blocker_detail: str = ""

    # Products
    products: list[RawProduct] = field(default_factory=list)

    # Evidence
    screenshots: list[str] = field(default_factory=list)
    captured_api_calls: list[dict] = field(default_factory=list)
    probe_notes: list[str] = field(default_factory=list)

    # Manual action flag
    requires_manual_action: bool = False
    manual_action_description: str = ""

    def n_products(self) -> int:
        return len(self.products)

    def n_with_nutrition(self) -> int:
        return sum(1 for p in self.products if p.has_nutrition())

    def n_with_ingredients(self) -> int:
        return sum(1 for p in self.products if p.has_ingredients())

    def summary(self) -> dict:
        return {
            "retailer_id": self.retailer_id,
            "retailer_name": self.retailer_name,
            "probe_run_at": self.probe_run_at,
            "access_method": self.access_method,
            "access_status": self.access_status,
            "http_status": self.http_status,
            "blocker_type": self.blocker_type,
            "blocker_detail": self.blocker_detail,
            "n_products": self.n_products(),
            "n_with_nutrition": self.n_with_nutrition(),
            "n_with_ingredients": self.n_with_ingredients(),
            "screenshots": self.screenshots,
            "n_captured_api_calls": len(self.captured_api_calls),
            "probe_notes": self.probe_notes,
            "requires_manual_action": self.requires_manual_action,
            "manual_action_description": self.manual_action_description,
        }

    def to_dict(self) -> dict:
        d = self.summary()
        d["products"] = [p.to_dict() for p in self.products]
        d["captured_api_calls"] = self.captured_api_calls
        return d


class RetailSource(ABC):
    """Abstract base for retailer probes."""

    retailer_id: str = ""
    retailer_name: str = ""
    retailer_url: str = ""
    country: str = "IL"

    # Probe configuration
    requires_browser: bool = True
    capture_patterns: list[str] = []
    bread_category_urls: list[str] = []

    @abstractmethod
    def probe(self) -> RetailProbeResult:
        """
        Run the full probe: navigate site, extract products, capture evidence.
        Must never raise — catch all exceptions and record them in probe_notes.
        """
        ...

    def _timestamp(self) -> str:
        return datetime.utcnow().isoformat()

    def _empty_result(self, **kwargs) -> RetailProbeResult:
        return RetailProbeResult(
            retailer_id=self.retailer_id,
            retailer_name=self.retailer_name,
            **kwargs,
        )

    def _product(self, **kwargs) -> RawProduct:
        return RawProduct(
            retailer_id=self.retailer_id,
            retailer_name=self.retailer_name,
            scraped_at=self._timestamp(),
            **kwargs,
        )
