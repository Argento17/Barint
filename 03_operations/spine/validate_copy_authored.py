#!/usr/bin/env python3
"""
validate_copy_authored.py — consumer copy enforcement gate (P541).

CHECK 1: zero-tolerance banned-phrase scan (data-state / score-mechanism narration).
CHECK 2: sentence-level mass-templating (identical sentence on >threshold products).
CHECK 3: exact baseline fingerprint match (author_copy.py template phrases).
CHECK 4: field-level mass-template (scalar free-prose only; bariInterpretation excluded).
CHECK 5: recite-vs-insight scan (TASK-546 prevention item #1) — WARN ONLY, does
         NOT affect exit code. Flags rowVerdict/insightLine/consumerTakeaway
         lines that just recite >=2 chip values (grams/%/mg/calories/ingredient
         counts) with no verdict-marker word — a data-dump for author review.

Exit codes (mirror validate_comparison_page.py):
  0  pass
  1  any check failed
  2  usage / load error

Usage:
  python validate_copy_authored.py --json <frontend_json>
  python validate_copy_authored.py --json <page.json> --emit-json
  python validate_copy_authored.py --selftest   # recite-check confusion-matrix proof
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import warnings
from collections import Counter, defaultdict
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass

# Import copy_constants with in-file fallback if the module is unavailable.
_COPY_CONSTANTS_PATH = (
    Path(__file__).resolve().parent.parent
    / "page_generator" / "copy" / "copy_constants.py"
)

_FALLBACK_BANNED: tuple[str, ...] = (
    "צילום תווית",
    "חוסר ודאות",
    "מאומת במלואו",
    "נשארת זהירה",
    "נשארים זהירים",
    "משאירה מקום לספק",
    "הנתונים כאן זמינים",
    "הערכה זהירה",
    "טקסט העמוד",
    "לא מאומת",
    "בגדר הערכה",
    "רמת ביטחון",
    "מהימנות הנתונים",
    "מגביל את הציון",
    "קובע את הציון",
    "הגורם המגביל",
    "מוריד את הציון",
    "משפיעים על הציון",
    "ממתן את הציון",
    "עוצר ב-",
    "הציון נשאר",
    "הציון יורד",
    "מעצב את הציון",
    "תורם לתחושת שובע",
    "הציון מבטא הערכה",
)

_FALLBACK_SENTENCE_THRESHOLD = 10

_MASS_TEMPLATE_FIELDS: frozenset[str] = frozenset({
    "insightLine",
    "rowVerdict",
    "consumerTakeaway",
    "expansion.consumerExplanation.whyRated",
    "expansion.consumerExplanation.takeaway",
})

_SENTENCE_SPLIT_RE = re.compile(r"[.!?]+")

# Baseline bariInterpretation template: "<dim_note> — <strength_phrase> (<score>)"
_BARI_INTERP_TEMPLATE = re.compile(
    r"^(.+?) — (ביצועים גבוהים|ביצועים בינוניים|ביצועים נמוכים) \(\d+\)$"
)

_BARI_RAW_PER100G = re.compile(
    r"\d+(?:\.\d+)?\s*(?:גרם|קלוריות|קק\"ל)"
)


def _load_copy_constants():
    spec = importlib.util.spec_from_file_location("copy_constants", _COPY_CONSTANTS_PATH)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_FALLBACK_RECITE_MARKERS: tuple[str, ...] = (
    "אבל", "יחסית", "צנוע", "צנועה", "נוטה", "דוחף", "דוחפת", "מתפקד",
    "קינוח", "מקור", "בזכות", "מספיק", "למרות", "פונקציונלית",
    "בטווח הרגיל", "הטווח הרגיל", "על חשבון", "אמיתי", "אמיתית", "אמיתיים",
    "כמעט סמלית", "מעבר ל", "גבוה", "גבוהה", "נמוך", "נמוכה",
    "קרוב ל", "כדי ל", "בעוד", "לעומת", "יותר מ", "פחות מ",
    "עדיין", "במקום", "בלי", "מול", "אפס",
    "מתחת", "פשוט", "מייצר", "יוצר",
    "מינימלי", "תרגיל שיווקי",
)

_FALLBACK_RECITE_CHIP_PATTERNS: tuple[str, ...] = (
    r"ל-?100\s*גרם",
    r"\d+(?:\.\d+)?\s*%",
    r'\d+(?:\.\d+)?\s*(?:מ"ג|מ״ג|מג)',
    r"\d+(?:\.\d+)?\s*גרם",
    r"\d+(?:\.\d+)?\s*קלוריות",
    r"\d+\s*רכיבים",
    r"(?:שנים עשר|שלושה עשר|ארבעה עשר|חמישה עשר|שישה עשר|אחד עשר|"
    r"שני|שתי|שלושה|שלוש|ארבעה|ארבע|חמישה|חמש|שישה|שש|שבעה|שבע|"
    r"שמונה|תשעה|תשע|עשרה|עשר)\s*רכיבים",
)

_FALLBACK_RECITE_FIELDS: frozenset[str] = frozenset({
    "rowVerdict", "insightLine", "consumerTakeaway",
})

_FALLBACK_RECITE_MIN_CHIP_TOKENS = 2


def _resolve_constants() -> dict:
    mod = _load_copy_constants()
    if mod is None:
        warnings.warn(
            "copy_constants import failed — using in-file fallback banned list",
            stacklevel=2,
        )
        return {
            "banned": list(_FALLBACK_BANNED),
            # No fallback patterns: if copy_constants failed to import we already
            # warned. CHECK 6 degrades to a no-op rather than to a wrong regex.
            "banned_patterns": [],
            "sentence_threshold": _FALLBACK_SENTENCE_THRESHOLD,
            "fingerprints": [],
            "sentence_repeat_fields": frozenset({
                "insightLine",
                "rowVerdict",
                "consumerTakeaway",
                "expansion.consumerExplanation.whyRated",
                "expansion.consumerExplanation.takeaway",
                "expansion.consumerExplanation.context",
            }),
            "recite_markers": list(_FALLBACK_RECITE_MARKERS),
            "recite_chip_patterns": list(_FALLBACK_RECITE_CHIP_PATTERNS),
            "recite_fields": _FALLBACK_RECITE_FIELDS,
            "recite_min_chip_tokens": _FALLBACK_RECITE_MIN_CHIP_TOKENS,
        }
    sentence_fields = getattr(mod, "SENTENCE_REPEAT_FIELDS", None)
    recite_fields = getattr(mod, "RECITE_CHECK_FIELDS", None)
    return {
        "banned": mod.get_banned_phrases(),
        "banned_patterns": (
            mod.get_banned_patterns() if hasattr(mod, "get_banned_patterns") else []
        ),
        "sentence_threshold": getattr(mod, "SENTENCE_REPEAT_THRESHOLD", _FALLBACK_SENTENCE_THRESHOLD),
        "fingerprints": mod.get_author_copy_fingerprints(),
        "sentence_repeat_fields": sentence_fields or frozenset(),
        "recite_markers": mod.get_recite_verdict_markers() if hasattr(mod, "get_recite_verdict_markers") else list(_FALLBACK_RECITE_MARKERS),
        "recite_chip_patterns": mod.get_recite_chip_token_patterns() if hasattr(mod, "get_recite_chip_token_patterns") else list(_FALLBACK_RECITE_CHIP_PATTERNS),
        "recite_fields": recite_fields or _FALLBACK_RECITE_FIELDS,
        "recite_min_chip_tokens": getattr(mod, "RECITE_MIN_CHIP_TOKENS", _FALLBACK_RECITE_MIN_CHIP_TOKENS),
    }


def build_fingerprint_set() -> tuple[frozenset[str], dict[str, int]]:
    """Return (substring_fingerprints, derivation_counts)."""
    consts = _resolve_constants()
    fingerprints = consts["fingerprints"]
    derivation = {
        "parsed_from_constants": len(fingerprints),
        "hand_listed_inline": 0,
        "total_unique_substring": len(fingerprints),
    }
    return frozenset(fingerprints), derivation


def _shape_finding(bc: str, path: str, expected: str, got) -> dict:
    """A malformed-container finding: makes a wrong JSON shape VISIBLE (a FAIL)
    instead of a crash or a silent skip (TASK-576 blindness #1)."""
    preview = got if isinstance(got, str) else repr(got)
    return {
        "check": "malformed_shape",
        "barcode": bc,
        "field": path,
        "expected": expected,
        "got_type": type(got).__name__,
        "text_preview": preview[:120],
    }


def iter_consumer_copy_fields(
    product,
) -> tuple[list[tuple[str, str]], list[dict]]:
    """
    Return (fields, malformed) for a product.

    fields    — [(field_path, text), …] for every scanned consumer-copy field.
    malformed — [shape_finding, …] for any nested container whose JSON shape is
                wrong (e.g. granola ships expansion.consumerExplanation as a bare
                str, and limitingFactors as either str[] or {text,…}[]).

    Every nested container is walked defensively: str / None / dict / list are all
    tolerated at every level. A wrong shape produces a FINDING (visible → FAIL),
    never an AttributeError and never a silent skip (TASK-576 blindness #1).
    """
    out: list[tuple[str, str]] = []
    malformed: list[dict] = []

    if not isinstance(product, dict):
        return out, [_shape_finding("?", "<product>", "dict", product)]

    bc = str(product.get("barcode", "?"))

    def add(path: str, val) -> None:
        if isinstance(val, str) and val.strip():
            out.append((f"{bc}:{path}", val))

    def add_list(path: str, val) -> None:
        """Walk a rendered list field. Tolerates None (empty), a bare str (a
        degenerate single value — flagged AND scanned), str items, or
        {text: str, …} items (the limitingFactors magnitude shape)."""
        if val is None:
            return
        if isinstance(val, str):
            malformed.append(_shape_finding(bc, path, "list", val))
            add(path, val)  # still scan the stray string for a leak
            return
        if isinstance(val, (list, tuple)):
            for i, item in enumerate(val):
                if isinstance(item, str):
                    add(f"{path}[{i}]", item)
                elif isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str):
                        add(f"{path}[{i}].text", text)
                    else:
                        malformed.append(
                            _shape_finding(bc, f"{path}[{i}]", "str|{text:str}", item)
                        )
                elif item is None:
                    continue
                else:
                    malformed.append(_shape_finding(bc, f"{path}[{i}]", "str|dict", item))
            return
        malformed.append(_shape_finding(bc, path, "list", val))

    add("insightLine", product.get("insightLine"))
    add("rowVerdict", product.get("rowVerdict"))
    add("consumerTakeaway", product.get("consumerTakeaway"))

    # ── expansion container ──────────────────────────────────────────────────
    exp = product.get("expansion")
    if exp is None:
        exp = {}
    elif not isinstance(exp, dict):
        malformed.append(_shape_finding(bc, "expansion", "dict", exp))
        exp = {}

    # Rendered expansion prose (TASK-576 blindness #2 — field coverage):
    #   comparisonContext → expansion-section.tsx ShelfContextSection L721
    #   positiveSignals[] → expansion-section.tsx AssessmentSection L515
    #   limitingFactors[] → expansion-section.tsx AssessmentSection L580
    add("expansion.comparisonContext", exp.get("comparisonContext"))
    add_list("expansion.positiveSignals", exp.get("positiveSignals"))
    add_list("expansion.limitingFactors", exp.get("limitingFactors"))

    # ── consumerExplanation container (granola ships this as str | None) ─────
    ce = exp.get("consumerExplanation")
    if ce is None:
        ce = {}
    elif isinstance(ce, str):
        # Wrong shape: the component reads .whyRated/.good/… off an object, so a
        # bare str renders nothing — but it must be VISIBLE, not silently skipped.
        malformed.append(_shape_finding(bc, "expansion.consumerExplanation", "dict", ce))
        add("expansion.consumerExplanation", ce)  # scan the stray string too
        ce = {}
    elif not isinstance(ce, dict):
        malformed.append(_shape_finding(bc, "expansion.consumerExplanation", "dict", ce))
        ce = {}

    add("expansion.consumerExplanation.whyRated", ce.get("whyRated"))
    add("expansion.consumerExplanation.takeaway", ce.get("takeaway"))
    add("expansion.consumerExplanation.context", ce.get("context"))
    add_list("expansion.consumerExplanation.good", ce.get("good"))
    add_list("expansion.consumerExplanation.watchOut", ce.get("watchOut"))

    # ── bariInterpretation pillars ───────────────────────────────────────────
    bi = product.get("bariInterpretation")
    if isinstance(bi, (list, tuple)):
        for i, entry in enumerate(bi):
            if isinstance(entry, dict):
                add(f"bariInterpretation[{i}].interpretation", entry.get("interpretation"))
    elif bi is not None:
        malformed.append(_shape_finding(bc, "bariInterpretation", "list", bi))

    return out, malformed


def _mass_template_field(field_path: str) -> bool:
    return field_path in _MASS_TEMPLATE_FIELDS


def _sentence_repeat_field(field_path: str) -> bool:
    """True when field_path (without barcode/index) is eligible for sentence repeat."""
    base = field_path
    if base.startswith("bariInterpretation["):
        return False
    if base.startswith("expansion.consumerExplanation.good["):
        return False
    if base.startswith("expansion.consumerExplanation.watchOut["):
        return False
    consts = _resolve_constants()
    return base in consts["sentence_repeat_fields"]


def _split_sentences(text: str) -> list[str]:
    parts = _SENTENCE_SPLIT_RE.split(text)
    return [p.strip() for p in parts if p.strip()]


def _normalize_sentence(sentence: str) -> str:
    return " ".join(sentence.split())


# ---------------------------------------------------------------------------
# CHECK 5: recite-vs-insight (TASK-546 prevention item #1). WARN only.
# ---------------------------------------------------------------------------

_RECITE_PATTERN_CACHE: dict[tuple[str, ...], list[re.Pattern]] = {}


def _compiled_chip_patterns(pattern_strs: list[str]) -> list[re.Pattern]:
    key = tuple(pattern_strs)
    cached = _RECITE_PATTERN_CACHE.get(key)
    if cached is None:
        cached = [re.compile(p) for p in pattern_strs]
        _RECITE_PATTERN_CACHE[key] = cached
    return cached


def count_chip_tokens(text: str, pattern_strs: list[str]) -> int:
    """
    Count distinct (non-overlapping) chip-value token spans in text.
    Overlapping matches from different patterns (e.g. "100 גרם" matched by
    both the bare-gram pattern and the "ל-100 גרם" pattern) are merged so the
    same numeric mention is never double-counted.
    """
    spans: list[tuple[int, int]] = []
    for pat in _compiled_chip_patterns(pattern_strs):
        for m in pat.finditer(text):
            spans.append(m.span())
    if not spans:
        return 0
    spans.sort()
    merged: list[list[int]] = []
    for s, e in spans:
        if merged and s < merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return len(merged)


def has_verdict_marker(text: str, markers: list[str]) -> str | None:
    """Return the first verdict-marker substring found in text, or None."""
    for marker in markers:
        if marker in text:
            return marker
    return None


def is_recite_line(text: str, *, patterns: list[str], markers: list[str], min_tokens: int) -> bool:
    """
    True when text is a "recite" line: >= min_tokens chip-value tokens AND
    no verdict-marker word — i.e. it reads back the row's own chips with no
    judgment/comparison/tradeoff/causal point.
    """
    if count_chip_tokens(text, patterns) < min_tokens:
        return False
    return has_verdict_marker(text, markers) is None


def check_copy_authored(data: dict, *, threshold: int | None = None) -> dict:
    """
    Run all copy-authored checks on a loaded frontend JSON dict.
    Returns a result dict with pass/fail and findings.
    """
    consts = _resolve_constants()
    banned = consts["banned"]
    banned_patterns = [(name, re.compile(rx)) for name, rx in consts.get("banned_patterns", [])]
    sentence_threshold = threshold if threshold is not None else consts["sentence_threshold"]
    fingerprints, derivation = build_fingerprint_set()
    recite_markers = consts["recite_markers"]
    recite_patterns = consts["recite_chip_patterns"]
    recite_fields = consts["recite_fields"]
    recite_min_tokens = consts["recite_min_chip_tokens"]

    products = data.get("products") or []
    banned_hits: list[dict] = []
    sentence_repeat_hits: list[dict] = []
    phrase_hits: list[dict] = []
    template_hits: list[dict] = []
    raw_gram_hits: list[dict] = []
    recite_hits: list[dict] = []
    pattern_hits: list[dict] = []
    shape_hits: list[dict] = []

    # field_path (without barcode) -> list of (barcode, text)
    by_field: dict[str, list[tuple[str, str]]] = defaultdict(list)
    # normalized sentence -> set of barcodes
    sentence_barcodes: dict[str, set[str]] = defaultdict(set)
    sentence_samples: dict[str, str] = {}

    for product in products:
        if not isinstance(product, dict):
            continue
        bc = str(product.get("barcode", "?"))
        fields, product_shape_hits = iter_consumer_copy_fields(product)
        shape_hits.extend(product_shape_hits)
        for field_path, text in fields:
            short_path = field_path.split(":", 1)[-1]
            by_field[short_path].append((bc, text))

            # CHECK 1: banned phrases (zero tolerance)
            for phrase in banned:
                if phrase in text:
                    banned_hits.append({
                        "check": "banned_phrase",
                        "barcode": bc,
                        "field": short_path,
                        "phrase": phrase,
                        "text_preview": text[:120],
                    })
                    break

            # CHECK 6: banned pattern families (zero tolerance). Catches the
            # paraphrases a literal banned-phrase list structurally cannot —
            # see copy_constants.BANNED_CONSUMER_PATTERNS for why this exists.
            for pname, prx in banned_patterns:
                m = prx.search(text)
                if m:
                    pattern_hits.append({
                        "check": "banned_pattern",
                        "barcode": bc,
                        "field": short_path,
                        "pattern": pname,
                        "matched": m.group(),
                        "text_preview": text[:120],
                    })
                    break

            # CHECK 2: sentence-level repetition (free-prose only)
            if _sentence_repeat_field(short_path):
                for raw_sent in _split_sentences(text):
                    norm = _normalize_sentence(raw_sent)
                    if len(norm) < 15:
                        continue
                    sentence_barcodes[norm].add(bc)
                    sentence_samples.setdefault(norm, raw_sent[:120])

            # CHECK 3: baseline fingerprint substring
            for phrase in fingerprints:
                if phrase in text:
                    phrase_hits.append({
                        "check": "fingerprint",
                        "barcode": bc,
                        "field": short_path,
                        "fingerprint": phrase,
                        "text_preview": text[:120],
                    })
                    break

            m = _BARI_INTERP_TEMPLATE.match(text.strip())
            if m:
                template_hits.append({
                    "check": "bari_template",
                    "barcode": bc,
                    "field": short_path,
                    "fingerprint": f"bariInterpretation template ({m.group(1)} — {m.group(2)} (N))",
                    "text_preview": text[:120],
                })

            if short_path.startswith("bariInterpretation[") and _BARI_RAW_PER100G.search(text):
                raw_gram_hits.append({
                    "check": "bari_raw_gram",
                    "barcode": bc,
                    "field": short_path,
                    "fingerprint": "bariInterpretation raw per-100g numeric",
                    "text_preview": text[:120],
                })

            # CHECK 5: recite-vs-insight (WARN only — does not affect `passed`)
            if short_path in recite_fields:
                n_tokens = count_chip_tokens(text, recite_patterns)
                if n_tokens >= recite_min_tokens and has_verdict_marker(text, recite_markers) is None:
                    recite_hits.append({
                        "check": "recite_no_verdict",
                        "barcode": bc,
                        "field": short_path,
                        "chip_token_count": n_tokens,
                        "text_preview": text[:200],
                    })

    for sentence, barcodes in sentence_barcodes.items():
        if len(barcodes) > sentence_threshold:
            sentence_repeat_hits.append({
                "check": "sentence_repeat",
                "sentence": sentence_samples.get(sentence, sentence)[:120],
                "count": len(barcodes),
                "threshold": sentence_threshold,
                "barcodes_sample": sorted(barcodes)[:8],
            })

    # CHECK 4: field-level mass-template (scalar free-prose only)
    mass_hits: list[dict] = []
    for field_path, entries in by_field.items():
        if not _mass_template_field(field_path):
            continue
        counter = Counter(text for _, text in entries)
        for text, count in counter.items():
            if count > sentence_threshold:
                barcodes = [b for b, t in entries if t == text]
                mass_hits.append({
                    "check": "mass_template",
                    "field": field_path,
                    "count": count,
                    "threshold": sentence_threshold,
                    "barcodes_sample": barcodes[:8],
                    "text_preview": text[:120],
                })

    # NOTE: recite_hits is intentionally excluded from `findings` — CHECK 5 is
    # WARN-only (flag-for-author-review) per owner instruction and must never
    # move `passed` or the process exit code.
    findings = (
        banned_hits + pattern_hits + shape_hits + sentence_repeat_hits + phrase_hits
        + template_hits + raw_gram_hits + mass_hits
    )
    passed = len(findings) == 0
    return {
        "passed": passed,
        "product_count": len(products),
        "fingerprint_derivation": derivation,
        "fingerprint_count": derivation["total_unique_substring"],
        "banned_hits": len(banned_hits),
        "banned_pattern_hits": len(pattern_hits),
        "shape_hits": len(shape_hits),
        "sentence_repeat_hits": len(sentence_repeat_hits),
        "phrase_hits": len(phrase_hits),
        "template_hits": len(template_hits),
        "raw_gram_hits": len(raw_gram_hits),
        "mass_template_hits": len(mass_hits),
        "findings": findings[:50],
        "recite_warn_hits": len(recite_hits),
        "recite_warnings": recite_hits[:50],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Consumer copy enforcement gate (P541)")
    ap.add_argument("--json", required=True, help="Frontend comparison JSON path")
    ap.add_argument("--emit-json", action="store_true", help="Emit machine-readable JSON on stdout")
    consts = _resolve_constants()
    default_thr = consts["sentence_threshold"]
    ap.add_argument(
        "--threshold", type=int, default=default_thr,
        help=f"Mass-template / sentence-repeat threshold (default {default_thr})",
    )
    args = ap.parse_args(argv)

    try:
        with open(args.json, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[ERROR] cannot load {args.json}: {exc}", file=sys.stderr)
        return 2

    result = check_copy_authored(data, threshold=args.threshold)
    n = result["product_count"]
    deriv = result["fingerprint_derivation"]

    if args.emit_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if result["passed"] else "FAIL"
        print(
            f"[{status}] copy-authored  ({n} products, "
            f"{result['fingerprint_count']} fingerprints, "
            f"banned={result['banned_hits']} banned_pattern={result.get('banned_pattern_hits', 0)} "
            f"shape={result.get('shape_hits', 0)} "
            f"sentence_repeat={result['sentence_repeat_hits']}, "
            f"fingerprint={result['phrase_hits']} mass={result['mass_template_hits']}, "
            f"recite_WARN={result['recite_warn_hits']})"
        )
        if not result["passed"]:
            for hit in result["findings"][:12]:
                check = hit.get("check", "")
                if check == "banned_phrase":
                    print(
                        f"  · {hit['barcode']} {hit['field']}: "
                        f"banned {hit['phrase']!r}"
                    )
                elif check == "banned_pattern":
                    print(
                        f"  · {hit['barcode']} {hit['field']}: "
                        f"banned pattern [{hit['pattern']}] matched {hit['matched']!r}"
                    )
                elif check == "sentence_repeat":
                    print(
                        f"  · sentence-repeat {hit['count']}x "
                        f"(>{hit['threshold']}): {hit['sentence']!r} "
                        f"e.g. {hit['barcodes_sample'][:3]}"
                    )
                elif check == "mass_template":
                    print(
                        f"  · mass-template {hit['field']}: {hit['count']}x "
                        f"(>{hit['threshold']}) e.g. {hit['barcodes_sample'][:3]}"
                    )
                elif check == "malformed_shape":
                    print(
                        f"  · {hit['barcode']} {hit['field']}: "
                        f"malformed shape (expected {hit['expected']}, "
                        f"got {hit['got_type']}) {hit['text_preview']!r}"
                    )
                elif "fingerprint" in hit:
                    print(
                        f"  · {hit['barcode']} {hit['field']}: "
                        f"matched {hit['fingerprint']!r}"
                    )

        # CHECK 5 WARN section — printed regardless of pass/fail; never touches exit code.
        if result["recite_warn_hits"]:
            print(f"[WARN] recite-vs-insight: {result['recite_warn_hits']} line(s) flagged for author review")
            for hit in result["recite_warnings"][:12]:
                print(
                    f"  · {hit['barcode']} {hit['field']} "
                    f"({hit['chip_token_count']} chip tokens, no verdict marker): "
                    f"{hit['text_preview']!r}"
                )

    return 0 if result["passed"] else 1


def _run_selftest(argv: list[str] | None = None) -> int:
    """
    Confusion-matrix self-test for CHECK 5 (TASK-546 prevention item #1):
      - all 12 fixture negatives (_fixtures/recite_negative.txt) MUST be flagged.
      - false-positive count on the 67-product owner-approved yogurt corpus
        (rowVerdict/insightLine/consumerTakeaway = 201 lines) is reported honestly.
    Exits 0 iff 12/12 negatives are caught (the hard assertion). The false-positive
    count is informational — it is the heuristic's measured ceiling, not a gate.
    """
    consts = _resolve_constants()
    markers = consts["recite_markers"]
    patterns = consts["recite_chip_patterns"]
    min_tokens = consts["recite_min_chip_tokens"]

    fixtures_path = Path(__file__).resolve().parent / "_fixtures" / "recite_negative.txt"
    try:
        negatives = [
            line.strip() for line in fixtures_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except OSError as exc:
        print(f"[ERROR] cannot load fixtures {fixtures_path}: {exc}", file=sys.stderr)
        return 2

    caught = 0
    missed: list[str] = []
    for neg in negatives:
        if is_recite_line(neg, patterns=patterns, markers=markers, min_tokens=min_tokens):
            caught += 1
        else:
            missed.append(neg)

    print(f"[NEGATIVES] {caught}/{len(negatives)} pre-fix yogurt rowVerdicts flagged")
    for m in missed:
        print(f"  MISSED (should have been flagged): {m!r}")

    good_json_paths = [
        Path(r"C:\bari\bari-web\src\data\comparisons\yogurt_spoonable_frontend_v1.json"),
        Path(r"C:\bari\bari-web\src\data\comparisons\yogurt_drinkable_frontend_v1.json"),
    ]
    good_lines: list[tuple[str, str, str, str]] = []  # (source, barcode, field, text)
    for p in good_json_paths:
        if not p.exists():
            print(f"[WARN] good-corpus file not found, skipping FP measurement: {p}", file=sys.stderr)
            continue
        with open(p, encoding="utf-8") as f:
            page = json.load(f)
        for product in page.get("products") or []:
            bc = str(product.get("barcode", "?"))
            for field in ("rowVerdict", "insightLine", "consumerTakeaway"):
                val = product.get(field)
                if isinstance(val, str) and val.strip():
                    good_lines.append((p.name, bc, field, val))

    fp_count = 0
    fp_samples: list[tuple[str, str, str]] = []
    for _src, bc, field, text in good_lines:
        if is_recite_line(text, patterns=patterns, markers=markers, min_tokens=min_tokens):
            fp_count += 1
            fp_samples.append((bc, field, text))

    if good_lines:
        print(f"[FALSE-POSITIVES] {fp_count}/{len(good_lines)} owner-approved lines flagged")
        for bc, field, text in fp_samples:
            print(f"  · {bc} {field}: {text[:160]!r}")
    else:
        print("[FALSE-POSITIVES] skipped — no good-corpus files found")

    ok = caught == len(negatives)
    print(f"[SELFTEST {'PASS' if ok else 'FAIL'}] negatives_caught={caught}/{len(negatives)} "
          f"false_positives={fp_count}/{len(good_lines) if good_lines else 'n/a'}")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_run_selftest())
    sys.exit(main())