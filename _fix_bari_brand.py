#!/usr/bin/env python3
"""Replace consumer-facing brand spelling BRI -> BARI in bari-web/src."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "bari-web" / "src"
EXTS = {".tsx", ".ts", ".json"}
SKIP_DIR_NAMES = frozenset({"archive", ".lighthouseci", "scripts"})

BRI = "\u05d1\u05e8\u05d9"
BARI = "\u05d1\u05d0\u05e8\u05d9"
SHBRI = "\u05e9\u05d1\u05e8\u05d9"
SHBARI = "\u05e9\u05d1\u05d0\u05e8\u05d9"

SHEBRI_VERB_RE = re.compile(
    SHBRI + r"(?=\s+(?:\u05de\u05e0\u05e1\u05d4|\u05d1\u05d0\u05d4))"
)

ENGINE_TYPO = re.compile(
    r"(\u05d4\u05de\u05e0\u05d5\u05e2 \u05e9\u05dc )\u05d1\u05e8\u05d9\u05d0(?![\u0590-\u05ff])"
)
LPB = re.compile(
    r"(\u05dc\u05e4\u05d9 \u05d4\u05d1\u05e0\u05ea )"
    + re.escape(BRI)
    + r"(?![\u0590-\u05ff])"
)
SLB = re.compile(
    r"(\u05e9\u05dc )"
    + re.escape(BRI)
    + r"(?=[\.\s,\u2014\u2013\|\)]|$)"
)

_raw_protect = [
    r"\u05d2\u05d5\u05d2[\u05f3']?\u05d9 " + re.escape(BRI),
    r"\u05d2\u05d5\u05d2\u05d9 " + re.escape(BRI),
    re.escape(BRI) + r"-\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4",
    r"\u05d1\u05e0\u05d9[\u05be-]\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4",
    r"\u05d1\u05e8\u05d9\u05d5\u05e9",
    r"\u05d1\u05e8\u05d9\u05e1\u05d8\u05d4",
    r"\u05db\u05d1\u05e8\u05d9\u05e8\u05ea",
    r"\u05d1\u05e8\u05d9\u05e8\u05ea",
    r"\u05d1\u05e8\u05d9\u05e8\u05d4",
    r"\u05d1\u05e8\u05d9\u05d1\u05d5\u05ea",
    r"\u05d1\u05e8\u05d9\u05d1\u05d4",
    r"\u05d1\u05e8\u05d9\u05db\u05d5\u05d6",
    r"\u05d4\u05d1\u05e8\u05d9\u05d0\u05d5\u05ea",
    r"\u05d1\u05e8\u05d9\u05d0\u05d5\u05ea\u05d9\u05ea",
    r"\u05d1\u05e8\u05d9\u05d0\u05d5\u05ea\u05d9",
    r"\u05d1\u05e8\u05d9\u05d0\u05d5\u05ea",
    r"\u05d1\u05e8\u05d9\u05d0\u05d9\u05dd",
    r"\u05d1\u05e8\u05d9\u05d0\u05d4",
    r"\u05d3\u05d2\u05df \u05d1\u05e8\u05d9\u05d0",
    r"\u00ab\u05d1\u05e8\u05d9\u05d0\u00bb",
    r"\u201c\u05d1\u05e8\u05d9\u05d0\u201d",
    r'"\u05d1\u05e8\u05d9\u05d0\u05d9\u05dd?"',
    r'"\u05d1\u05e8\u05d9\u05d0"',
    r"\u05e9\u05d1\u05e8\u05d9",
    r"\u05d1\u05e8\u05d9\u05d0(?![\u0590-\u05ff])",
]
PROTECT_PATTERNS = [re.compile(pat) for pat in _raw_protect]


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def transform(text: str) -> tuple[str, int]:
    n = 0

    def subn(pattern: re.Pattern[str], repl: str, s: str) -> str:
        nonlocal n
        s, c = pattern.subn(repl, s)
        n += c
        return s

    text = subn(ENGINE_TYPO, r"\g<1>" + BARI, text)
    text = subn(LPB, r"\g<1>" + BARI, text)
    text = subn(SLB, r"\g<1>" + BARI, text)
    text = subn(SHEBRI_VERB_RE, SHBARI, text)

    placeholders: dict[str, str] = {}

    def protect(m: re.Match[str]) -> str:
        key = f"\ufffdPROT{len(placeholders)}\ufffd"
        placeholders[key] = m.group(0)
        return key

    for pat in PROTECT_PATTERNS:
        text = pat.sub(protect, text)

    def bri_repl(_m: re.Match[str]) -> str:
        nonlocal n
        n += 1
        return BARI

    BRI_BOUND = re.compile(
        r"(?<![\u0590-\u05FF])" + re.escape(BRI) + r"(?![\u0590-\u05FF\-])"
    )
    text = BRI_BOUND.sub(bri_repl, text)

    for key, val in placeholders.items():
        text = text.replace(key, val)

    return text, n


def main() -> int:
    per_file: list[tuple[str, int]] = []
    total = 0

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in EXTS:
            continue
        if should_skip(path):
            continue
        raw = path.read_text(encoding="utf-8")
        new, count = transform(raw)
        if count and new != raw:
            path.write_text(new, encoding="utf-8", newline="\n")
            rel = path.relative_to(ROOT.parent.parent).as_posix()
            per_file.append((rel, count))
            total += count

    for rel, count in per_file:
        print(f"{count}\t{rel}")
    print(f"TOTAL\t{total}\tfiles\t{len(per_file)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())