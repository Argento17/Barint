from pathlib import Path

def fix_file(path: Path, replacements):
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text:
            raise SystemExit(f"MISSING in {path}: {old!r}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    print("fixed", path)

fix_file(
    Path(r"c:\Bari\bari-web\src\components\home\featured-comparison-card.tsx"),
    [
        (r"          \u05D4\u05E9\u05D5\u05D5\u05D0\u05D4", '          {"\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4"}'),
        (r"        \u05DC\u05E6\u05E4\u05D9\u05D9\u05D4 \u05D1\u05D4\u05E9\u05D5\u05D5\u05D0\u05D4", '        {"\u05dc\u05e6\u05e4\u05d9\u05d9\u05d4 \u05d1\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4"}'),
    ],
)

fix_file(
    Path(r"c:\Bari\bari-web\src\components\home\hero-still-life.tsx"),
    [
        (r'label="\u05D0\u05D9\u05DB\u05D5\u05EA \u05E8\u05DB\u05D9\u05D1\u05D9\u05DD"', 'label="\u05d0\u05d9\u05db\u05d5\u05ea \u05e8\u05db\u05d9\u05d1\u05d9\u05dd"'),
        (r'label="\u05E2\u05D9\u05D1\u05D5\u05D3 \u05DE\u05D9\u05E0\u05D9\u05DE\u05DC\u05D9"', 'label="\u05e2\u05d9\u05d1\u05d5\u05d3 \u05de\u05d9\u05e0\u05d9\u05de\u05dc\u05d9"'),
    ],
)
