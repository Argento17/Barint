"""RETIRED — Figma client not used.

Design tokens live in bari-web/colors_and_type.css (in-repo, no API key needed).
The Design Agent reads that file directly for drift detection.
This client is kept for reference only — do not call it.

Original purpose: read Figma design file for token drift detection.
Replaced by: direct file read of bari-web/colors_and_type.css (2026-06-06).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from .http import HttpError, get_json

CLIENT_VERSION = "1.0"
API = "https://api.figma.com/v1"


def _headers() -> dict[str, str]:
    tok = os.environ.get("FIGMA_TOKEN", "")
    return {"X-Figma-Token": tok} if tok else {}


def is_configured() -> bool:
    return bool(os.environ.get("FIGMA_TOKEN"))


def _file_key(file_key: str | None) -> str:
    return file_key or os.environ.get("FIGMA_FILE_KEY", "")


@dataclass
class FileMeta:
    key: str
    name: str | None = None
    last_modified: str | None = None
    version: str | None = None
    component_names: list[str] = field(default_factory=list)
    found: bool = True


@dataclass
class StyleToken:
    name: str                # e.g. "color/score/A"
    style_type: str          # FILL | TEXT | EFFECT | GRID
    key: str
    description: str | None = None


def get_file(file_key: str | None = None, depth: int = 1) -> FileMeta:
    """Fetch file metadata + top-level component names. `depth` limits node-tree recursion
    (1 = pages only) to keep the payload small. found=False if the file/token is rejected."""
    key = _file_key(file_key)
    try:
        data = get_json(f"{API}/files/{key}", params={"depth": depth}, headers=_headers())
    except HttpError as e:
        if e.status in (403, 404):
            return FileMeta(key=key, found=False)
        raise
    comps = data.get("components", {}) or {}
    names = [c.get("name") for c in comps.values() if c.get("name")]
    return FileMeta(
        key=key,
        name=data.get("name"),
        last_modified=data.get("lastModified"),
        version=data.get("version"),
        component_names=sorted(set(names)),
    )


def get_styles(file_key: str | None = None) -> list[StyleToken]:
    """Published styles (color/text/effect/grid) — the design-token source of truth to
    diff against the implemented Tailwind/token set."""
    key = _file_key(file_key)
    data = get_json(f"{API}/files/{key}/styles", headers=_headers())
    out: list[StyleToken] = []
    for s in data.get("meta", {}).get("styles", []):
        out.append(StyleToken(
            name=s.get("name") or "",
            style_type=s.get("style_type") or "",
            key=s.get("key") or "",
            description=s.get("description") or None,
        ))
    return out


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"Figma configured: {is_configured()} (needs FIGMA_TOKEN + a file key)")
    if not is_configured() or not _file_key(None):
        print("NEEDS-ENV-VERIFY: set FIGMA_TOKEN + FIGMA_FILE_KEY, then re-run.")
        raise SystemExit(0)
    try:
        f = get_file()
        print(f"file={f.name!r} found={f.found} modified={f.last_modified} "
              f"components={len(f.component_names)}")
        styles = get_styles()
        print(f"styles={len(styles)}: {[s.name for s in styles[:5]]}")
    except HttpError as e:
        print(f"call failed (HTTP {e.status}): check token/file key. {e}")
