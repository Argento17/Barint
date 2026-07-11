"""
verify_citations.py — C0-style deterministic citation integrity gate.

Purpose:
    Extract every PMID and DOI from governance/evidence files, resolve each
    identifier against its authoritative registry (PubMed for PMIDs; CrossRef
    for DOIs), and compare the resolved paper metadata against the claimed
    context in the file.

    Verdict per citation:
        PASS            — resolves + topic/author/year consistent with context
        MISMATCH        — resolves but to a clearly different topic/author/year
        FABRICATED      — PMID does not resolve at all, or resolves to a
                          completely different field (e.g. cheese claim →
                          leukemia paper); treated as the highest-severity flag
        UNRESOLVED-DOI  — CrossRef could not resolve the DOI (network/rate
                          limit); human review required; does NOT hard-fail

Exit codes:
    0 — all PASS (or only UNRESOLVED-DOI warnings)
    1 — any MISMATCH or FABRICATED citations found
    2 — only UNRESOLVED-DOI warnings (no hard fails; human review needed)

    Note: exit 2 is returned only when there are zero MISMATCHes/FABRICATEDs
    but at least one UNRESOLVED-DOI.  Exit 0 means truly all-clean.

Usage:
    python verify_citations.py path/to/file.md
    python verify_citations.py --all
    python verify_citations.py --pmid 31122155   (single-PMID spot check)

Configuration:
    DEFAULT_SCAN_FILES — list of repo-relative paths scanned under --all.
    Edit the list at the bottom of this file to add/remove targets.

Rate limiting:
    PubMed E-utilities polite limit: 3 req/s without API key.
    The validator sleeps 0.35 s between PMID fetches and caches within a run.
    Set NCBI_API_KEY in the environment to raise the limit to ~10 req/s.

Author: Research Agent (TASK-383)
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
import time
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Force UTF-8 stdout/stderr so Hebrew and special characters don't crash on
# Windows consoles configured for CP-1252
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Ensure repo root is on sys.path so the existing clients are importable
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve()
_REPO_ROOT = _HERE.parents[2]          # 03_operations/validators/ -> repo root
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

try:
    from integrations.clients.literature import pubmed_fetch
    from integrations.clients.crossref import get_doi, CrossrefWork
    from integrations.clients.http_client import HttpError
    _CLIENTS_AVAILABLE = True
except ImportError as _ie:
    print(f"[WARN] Could not import clients: {_ie}", file=sys.stderr)
    print("[WARN] Running in OFFLINE mode — all ids will be UNRESOLVED-DOI/FABRICATED",
          file=sys.stderr)
    _CLIENTS_AVAILABLE = False

# ---------------------------------------------------------------------------
# Regex patterns for identifier extraction
# ---------------------------------------------------------------------------
# PMID: "PMID 31122155", "PMID: 31122155", "PMID31122155", "pmid 31122155"
# We capture the 7-8 digit number that follows "PMID" (with optional colon/space)
_PMID_RE = re.compile(
    r"(?<!\w)PMID[:\s]*(\d{7,8})(?!\d)",
    re.IGNORECASE,
)

# DOI: starts with "10." followed by registrant + suffix.
# Must be preceded by "doi" or "DOI" keyword or "/doi.org/" to avoid false matches
# on plain decimal numbers.
_DOI_KW_RE = re.compile(
    r"(?:doi[:\s/]*|https?://(?:dx\.)?doi\.org/)(10\.\d{4,9}/\S+?)(?=[,\s\)\]>\"\'`]|$)",
    re.IGNORECASE,
)
# Also catch raw DOIs in study_objects source_doi fields: source_doi: "10.XXXX/..."
# Python re doesn't support \K — use a non-greedy capturing group instead
_DOI_RAW_RE = re.compile(
    r"source_doi[:\s\"\']+?(10\.\d{4,9}/[^\s\"\'`\)]+)",
    re.IGNORECASE,
)

# Number of surrounding lines to include in context (each side)
_CONTEXT_LINES = 3
# Maximum characters of context to display
_CONTEXT_DISPLAY = 200


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
@dataclass
class CitationResult:
    id_type: str           # "PMID" | "DOI"
    raw_id: str            # the identifier as found in the file
    file_path: str
    line_number: int
    context: str           # surrounding text (~6 lines)
    real_title: Optional[str] = None
    real_authors: Optional[str] = None    # first author + year
    real_year: Optional[str] = None
    real_journal: Optional[str] = None
    real_abstract: Optional[str] = None
    verdict: str = "PENDING"             # PASS | MISMATCH | FABRICATED | UNRESOLVED-DOI
    reason: str = ""


# ---------------------------------------------------------------------------
# Caches
# ---------------------------------------------------------------------------
_pmid_cache: dict[str, object] = {}      # PMID -> Paper | None (None = not found)
_doi_cache: dict[str, object] = {}       # DOI  -> CrossrefWork | None


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------
def _build_context(lines: list[str], lineno: int) -> str:
    """
    Build a multi-line context string: _CONTEXT_LINES lines before + the
    target line + _CONTEXT_LINES lines after.  This gives the heuristic
    enough surrounding text to assess topic match, even when the DOI/PMID
    sits on a sparse table-row line.
    """
    # lineno is 1-indexed
    idx = lineno - 1
    start = max(0, idx - _CONTEXT_LINES)
    end = min(len(lines), idx + _CONTEXT_LINES + 1)
    return " ".join(l.strip() for l in lines[start:end])


def _extract_citations(text: str, file_path: str) -> list[CitationResult]:
    """Parse text line-by-line and return all PMID/DOI occurrences with context."""
    results: list[CitationResult] = []
    lines = text.splitlines()
    seen_ids: set[tuple[str, str]] = set()  # (id_type, raw_id) — dedup globally per file

    for lineno, line in enumerate(lines, start=1):
        # --- PMIDs ---
        for m in _PMID_RE.finditer(line):
            pmid = m.group(1)
            key = ("PMID", pmid)
            if key in seen_ids:
                continue
            seen_ids.add(key)
            ctx = _build_context(lines, lineno)
            results.append(CitationResult(
                id_type="PMID",
                raw_id=pmid,
                file_path=file_path,
                line_number=lineno,
                context=ctx,
            ))

        # --- DOIs (keyword-anchored) ---
        for m in _DOI_KW_RE.finditer(line):
            doi = m.group(1).rstrip(".,;)")
            key = ("DOI", doi)
            if key in seen_ids:
                continue
            seen_ids.add(key)
            ctx = _build_context(lines, lineno)
            results.append(CitationResult(
                id_type="DOI",
                raw_id=doi,
                file_path=file_path,
                line_number=lineno,
                context=ctx,
            ))

        # --- DOIs (source_doi: "10.xxx/..." pattern) ---
        for m in _DOI_RAW_RE.finditer(line):
            doi = m.group(1).rstrip(".,;\"'`)")
            # Skip template placeholders
            if "XXXX" in doi or "xxxx" in doi:
                continue
            key = ("DOI", doi)
            if key in seen_ids:
                continue
            seen_ids.add(key)
            ctx = _build_context(lines, lineno)
            results.append(CitationResult(
                id_type="DOI",
                raw_id=doi,
                file_path=file_path,
                line_number=lineno,
                context=ctx,
            ))

    return results


# ---------------------------------------------------------------------------
# Topic mismatch heuristic
# ---------------------------------------------------------------------------
# Key domain words for food/nutrition/supplement science that should appear
# either in the claimed context OR in the resolved paper's title+abstract.
# Conservative: if NONE of the domain words from context match the paper,
# classify MISMATCH. False-positives are acceptable; false negatives are not.

_FOOD_NUTRITION_WORDS = frozenset({
    # food/ingredient categories
    "cheese", "dairy", "milk", "yogurt", "yoghurt", "butter", "fat", "protein",
    "fiber", "fibre", "cholesterol", "ldl", "saturated", "omega", "glucose",
    "sugar", "sodium", "carbohydrate", "calorie", "caloric", "diet", "dietary",
    "food", "nutrition", "nutrient", "nutrients", "nutritional",
    "ferment", "fermented", "lactose", "calcium", "emulsifier", "additive",
    "preservative", "processing", "ultra-processed", "nova", "cancer",
    "cardiovascular", "cvd", "obesity", "diabetes", "metabolic",
    "gut", "microbiome", "intestinal", "microbiota",
    "amino acid", "diaas", "pdcaas", "protein quality", "whey", "casein",
    "soy", "soybean", "plant", "grain", "oat", "seed", "nut", "legume",
    "sorbate", "sorbic", "citric", "nitrite", "nitrate", "nitro",
    "potassium", "sodium nitrite", "emulsifying", "health outcome", "cohort",
    "randomized", "rct", "meta-analysis", "systematic review", "systematic",
    # supplement / micronutrient
    "magnesium", "zinc", "vitamin", "mineral", "supplement", "deficiency",
    "blood pressure", "hypertension", "cardiovascular disease",
    "polysorbate", "mono-", "diglyceride", "cellulose", "carrageenan", "lecithin",
    # processing science
    "ultra-processing", "classification", "processed food", "public health",
    "acid", "acidulant", "antioxidant", "preservatives", "sorbates",
    "ppc", "spi", "wpi", "wpc", "pig model", "ileal", "digestibility",
    # additive-specific E-numbers referenced in context
    "e330", "e200", "e202", "e203", "e224", "e250", "e460", "e466", "e471",
    "e472", "e250", "citrate",
    # disease/outcome keywords that ARE food-relevant
    "prostate cancer", "breast cancer", "colorectal", "carcinogen",
    "genotoxic", "genotoxicity", "mutagenic", "inflammatory", "inflammation",
    # protein quality study keywords
    "digestible indispensable amino acid", "diaas", "score", "protein source",
    "animals", "pig", "pea protein", "soy protein",
    # ---------------------------------------------------------------------------
    # TASK-528: medical / pharmacology / body-composition literature
    # GLP-1 agonists, incretins, and weight-management drugs sit at the
    # intersection of food/nutrition science and clinical pharmacology.  Papers
    # on these topics are legitimate Bari evidence sources but their titles
    # contain none of the food-domain words above, causing false MISMATCH.
    # Adding these terms expands the positive-signal vocabulary WITHOUT touching
    # _RED_FLAG_WORDS (which remains unchanged and still blocks unrelated fields
    # such as stroke/leukemia/schizophrenia/ophthalmology).
    # ---------------------------------------------------------------------------
    # GLP-1 / incretin pharmacology
    "glp-1", "glp1", "glp-1ra", "glp-1 receptor", "incretin", "incretins",
    "semaglutide", "liraglutide", "tirzepatide", "dulaglutide", "exenatide",
    "ozempic", "wegovy", "mounjaro", "victoza", "trulicity",
    "sglt2", "sglt-2", "sglt2i", "dpp-4", "dpp4",
    # body composition / lean mass (common in weight-loss RCTs cited by Bari)
    "lean mass", "lean body mass", "fat mass", "body composition",
    "muscle mass", "skeletal muscle", "sarcopenia", "sarcopenic",
    "fat-free mass", "fat free mass", "body weight",
    # weight management / obesity pharmacotherapy outcomes
    "weight loss", "weight reduction", "weight management",
    "bariatric", "anti-obesity", "adipose", "adiposity",
    # clinical trial / meta-analysis terms for pharmacology studies
    "network meta-analysis", "pharmacotherapy", "pharmacological",
    "clinical trial", "randomised controlled", "randomized controlled",
    "intervention", "placebo-controlled",
})

# Words that, if they appear in the RESOLVED title but NOT anywhere in the
# multi-line context, strongly suggest a wrong paper (different clinical field)
_RED_FLAG_WORDS = frozenset({
    "stroke", "cerebral", "leukemia", "leukaemia", "nursing", "case study",
    "dermatology", "ophthalmology", "orthopedic", "orthopaedic", "trauma",
    "surgery", "obstetrics", "psychiatry", "schizophrenia", "alzheimer",
    "parkinson", "epilepsy", "sepsis", "perioperative", "anesthesia",
    "anaesthesia", "fracture", "wound", "renal failure", "dialysis",
    "transplant", "graft", "neonate", "neonatal", "pediatric surgery",
    "spinal", "urology", "urolog", "egocentric", "allocentric", "neglect",
    "visual neglect", "neurology", "neuroscience", "microrna", "mrna",
    "myeloid", "leukemia", "acute myeloid", "nurse", "workplace",
})


def _topic_consistent(context: str, real_title: str,
                      real_abstract: Optional[str]) -> tuple[bool, str]:
    """
    Conservative heuristic: returns (is_consistent, reason_string).
    Bias toward MISMATCH over PASS — false positives are acceptable.

    Logic:
    1. If the resolved paper title/abstract contains a red-flag clinical word
       that does NOT appear anywhere in the context -> MISMATCH
    2. If at least one food/nutrition domain word is shared between context
       and the resolved paper -> PASS
    3. Otherwise -> MISMATCH (conservative)
    """
    ctx_lower = context.lower()
    title_lower = (real_title or "").lower()
    abstract_lower = (real_abstract or "").lower()
    combined_real = title_lower + " " + abstract_lower

    # Rule 1: red-flag word in resolved paper that has no foothold in context
    for flag in _RED_FLAG_WORDS:
        if flag in combined_real and flag not in ctx_lower:
            return False, f"resolved title/abstract contains '{flag}' with no match in context"

    # Rule 2: at least one shared domain word
    ctx_matches = [w for w in _FOOD_NUTRITION_WORDS
                   if w in ctx_lower and w in combined_real]
    if ctx_matches:
        return True, f"shared domain words: {', '.join(ctx_matches[:6])}"

    # Rule 3: if context is very sparse (< 40 chars), be conservative-pass
    # to avoid penalising single-line cite entries that lack surrounding text
    if len(context.strip()) < 40:
        return True, "context too short for heuristic — conservative PASS (flag for human)"

    # Rule 4: if the resolved title itself contains very generic food-science terms
    # (the context may be thin but the paper is clearly on-topic).
    # TASK-528: also accept medical/pharmacology/body-composition titles that are
    # legitimate Bari evidence sources (GLP-1/incretin/lean-mass/weight-loss RCTs).
    generic_ok = any(w in title_lower for w in (
        "food", "dietary", "nutrition", "nutrient", "diet", "protein",
        "amino acid", "digestib", "fatty acid", "cancer", "cardiovascular",
        "additive", "sorbic", "nitrate", "nitrite", "preservative", "emulsifier",
        # GLP-1 / incretin pharmacology (TASK-528)
        "glp-1", "glp1", "incretin", "semaglutide", "liraglutide", "tirzepatide",
        "dulaglutide", "exenatide", "sglt2", "sglt-2", "dpp-4", "dpp4",
        # body composition / lean mass (TASK-528)
        "lean mass", "lean body mass", "body composition", "fat mass",
        "muscle mass", "skeletal muscle", "sarcopenia",
        # weight management outcomes (TASK-528)
        "weight loss", "weight reduction", "anti-obesity", "adiposity",
        "pharmacotherapy",
    ))
    if generic_ok:
        return True, f"resolved title contains food/nutrition/pharmacology term; context is '{context[:60]}...'"

    return False, "no shared nutrition/food domain words between context and resolved paper"


# ---------------------------------------------------------------------------
# Secondary corroboration layer — author-surname + year cross-check
# ---------------------------------------------------------------------------
# Reconstructed from 03_operations/validators/__pycache__/verify_citations.cpython-314.pyc
# (compiled 2026-06-25, structurally newer than the c90d49ef committed source).
# Rationale (from the .pyc's own selftest fixtures): _topic_consistent alone
# can be fooled by a "same-domain swap" — a fabricated/mismatched citation
# that happens to share nutrition/food vocabulary with the correct paper
# (e.g. context claims "Thorning et al. 2017" but the PMID actually resolves
# to Salas-Salvado's unrelated dairy-matrix RCT). This layer runs AFTER
# _topic_consistent returns True and requires the resolved record's author
# surname and/or publication year to corroborate what the context claims.
_AUTHOR_YEAR_RE = re.compile(
    r"\b([A-Z][a-zA-Z\-']{2,})\s*(?:et\s+al\.?,?)?\s*[\(,]?\s*((?:19|20)\d{2})\b"
)
_MIN_SURNAME_LEN = 3
_YEAR_TOLERANCE = 1

# Capitalized tokens that are NOT author surnames — common words, journal
# abbreviations, org/acronym names, and Bari-internal vocabulary that would
# otherwise false-positive as a "surname" in the regex above.
_STOP_WORDS = frozenset({
    "The", "And", "For", "From", "With", "This", "That", "In", "On", "An",
    "At", "By", "Of", "To", "A", "Is", "Are", "Was", "Were", "Also", "Has",
    "Have", "Had", "Not", "But", "Can", "May", "Will", "Should", "Over",
    "Into", "When", "Where", "Which", "Who", "Its", "Their", "They", "We",
    "Our", "Both", "Each", "Such", "Thus",
    "PMID", "DOI", "RCT", "LDL", "HDL", "BMI", "CVD", "NOVA", "Cochrane",
    "PubMed", "CrossRef",
    "Am", "Clin", "Nutr", "Int", "Eur", "Sci", "Med", "Rev", "Res", "Soc",
    "Adv", "BMJ", "NEJM", "JAMA", "EHJ", "Lancet", "Nature", "Science",
    "EFSA", "JECFA", "IARC", "USDA", "ECHA", "FSANZ", "ANSES", "PLoS",
    "Medicine", "Foods", "Nutrients", "AJCN", "BJN", "JN", "EUR", "INT", "ADV",
    "Agent", "Product", "Research", "Nutrition", "Task", "Finding", "Owner",
    "Evidence", "Signal", "Rule", "Gate", "Review",
    "Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    "Recorded", "Updated", "Created", "Closed", "Opened", "Version",
})
# Case-insensitive lookup set (TASK-452 follow-up fix): _AUTHOR_YEAR_RE can
# capture all-caps acronyms (e.g. "WHO", journal abbreviations like "IJE")
# that don't title-case-match _STOP_WORDS verbatim, letting them slip through
# as fake author surnames. Membership is checked case-insensitively; the
# stop-word list itself (_STOP_WORDS) is left untouched.
_STOP_WORDS_LOWER = frozenset(w.lower() for w in _STOP_WORDS)

# Anchors used to locate the SPECIFIC identifier occurrence within a
# multi-citation context block (see _parse_context_author_year docstring).
_ID_ANCHOR_RE = re.compile(r"PMID[:\s]*\d{7,8}|10\.\d{4,9}/\S+")


def _parse_context_author_year(context: str, raw_id: str) -> tuple[Optional[str], Optional[int]]:
    """
    Extract the first parseable (author_surname, year) pair from citation context.

    Returns (surname_lower, year_int) or (None, None) when nothing is found.
    Either component may be None independently.

    We look for the most common academic citation patterns:
        Author YYYY
        Author et al. YYYY
        (Author, YYYY)
        Author (YYYY)

    IMPORTANT: to avoid false positives from multi-citation context blocks
    (where 6 lines of context can contain author names of ADJACENT papers),
    we anchor the search window to the SPECIFIC identifier (raw_id) being
    validated rather than the first identifier found.  We parse the text in
    the 80-char window BEFORE that specific identifier occurrence.

    If raw_id is not found in context (unusual), we fall back to the first
    identifier found.  If no identifier found at all, we skip extraction
    (return None, None) — this is the conservative safe default.
    """
    search_text = context
    anchor_pos = None
    if raw_id:
        escaped = re.escape(raw_id)
        specific_match = re.search(escaped, context, re.IGNORECASE)
        if specific_match:
            anchor_pos = specific_match.start()
    if anchor_pos is None:
        fallback = _ID_ANCHOR_RE.search(context)
        if fallback:
            anchor_pos = fallback.start()
    if anchor_pos is not None:
        pre_start = max(0, anchor_pos - 80)
        search_text = context[pre_start:anchor_pos]

    candidates = []
    for m in _AUTHOR_YEAR_RE.finditer(search_text):
        surname_raw = m.group(1)
        year_raw = m.group(2)
        if surname_raw.lower() in _STOP_WORDS_LOWER:
            continue
        if len(surname_raw) < _MIN_SURNAME_LEN:
            continue
        if not surname_raw[0].isupper():
            continue
        candidates.append((surname_raw.lower(), int(year_raw)))

    if candidates:
        return candidates[-1]  # closest to the anchor (last match before it)
    return None, None


def _author_year_corroborate(context: str, resolved_authors, resolved_year,
                             raw_id: str) -> tuple[bool, str]:
    """
    Secondary corroboration check (runs AFTER topic_consistent returns True).

    Returns (corroborates: bool, reason: str).

    True  = the resolved record's author surname and/or year corroborate (or
            do not contradict) what the citation context claims.
    False = a specific conflict was found (wrong surname and/or wrong year) —
            this is the "same-domain swap" fabrication pattern.
    """
    surname, ctx_year = _parse_context_author_year(context, raw_id)
    if surname is None and ctx_year is None:
        return True, "no parseable author/year in context — conservative pass"

    resolved_lower = [a.lower() for a in (resolved_authors or [])] if isinstance(resolved_authors, list) else (
        [str(resolved_authors).lower()] if resolved_authors else []
    )

    year_conflict = False
    year_reason = ""
    if ctx_year is not None and resolved_year:
        try:
            res_year_int = int(str(resolved_year)[:4])
            diff = abs(ctx_year - res_year_int)
            if diff > _YEAR_TOLERANCE:
                year_conflict = True
                year_reason = f"year conflict: context claims {ctx_year}, resolved record is {res_year_int}"
        except ValueError:
            pass

    surname_conflict = False
    surname_reason = ""
    if surname is not None and resolved_lower:
        found_in_any = any(surname in a for a in resolved_lower)
        if not found_in_any:
            resolved_display = ", ".join(resolved_lower[:3])
            surname_conflict = True
            surname_reason = f"surname conflict: context cites '{surname}', resolved first authors are [{resolved_display}]"

    if year_conflict or surname_conflict:
        parts = [r for r in (surname_reason, year_reason) if r]
        return False, "; ".join(parts)

    reason_parts = []
    if surname is not None and resolved_lower and any(surname in a for a in resolved_lower):
        reason_parts.append(f"surname '{surname}' found in resolved authors")
    if ctx_year is not None and resolved_year:
        reason_parts.append(f"year {ctx_year} within tolerance")
    return True, "; ".join(reason_parts) if reason_parts else "corroboration passed"


# ---------------------------------------------------------------------------
# Resolution functions
# ---------------------------------------------------------------------------
_SLEEP_BETWEEN_CALLS = 0.35   # seconds — stays under PubMed 3 req/s limit


def _resolve_pmid(pmid: str) -> tuple[Optional[object], str]:
    """
    Resolve a PMID. Returns (Paper | None, status).
    status: "found" | "not_found"
    Caches results within a run.
    """
    if pmid in _pmid_cache:
        paper = _pmid_cache[pmid]
        return paper, ("found" if paper is not None else "not_found")

    if not _CLIENTS_AVAILABLE:
        _pmid_cache[pmid] = None
        return None, "not_found"

    time.sleep(_SLEEP_BETWEEN_CALLS)
    try:
        papers = pubmed_fetch([pmid])
        if papers:
            _pmid_cache[pmid] = papers[0]
            return papers[0], "found"
        else:
            _pmid_cache[pmid] = None
            return None, "not_found"
    except Exception as exc:
        print(f"[WARN] PubMed fetch error for PMID {pmid}: {exc}", file=sys.stderr)
        _pmid_cache[pmid] = None
        return None, "not_found"


def _resolve_doi(doi: str) -> tuple[Optional[object], str]:
    """
    Resolve a DOI via CrossRef. Returns (CrossrefWork | None, status).
    status: "found" | "not_found" | "error"
    CrossRef is flaky — errors mark UNRESOLVED-DOI, not hard-fail.
    """
    if doi in _doi_cache:
        work = _doi_cache[doi]
        return work, ("found" if (work is not None and work.found) else "not_found")

    if not _CLIENTS_AVAILABLE:
        _doi_cache[doi] = None
        return None, "error"

    time.sleep(_SLEEP_BETWEEN_CALLS)
    try:
        work = get_doi(doi)
        _doi_cache[doi] = work
        if work.found:
            return work, "found"
        else:
            return None, "not_found"
    except Exception as exc:
        print(f"[WARN] CrossRef fetch error for DOI {doi}: {exc}", file=sys.stderr)
        _doi_cache[doi] = None
        return None, "error"


# ---------------------------------------------------------------------------
# Core classification
# ---------------------------------------------------------------------------
def _classify_pmid(result: CitationResult) -> CitationResult:
    paper, status = _resolve_pmid(result.raw_id)

    if status == "not_found" or paper is None:
        result.verdict = "FABRICATED"
        result.reason = f"PMID {result.raw_id} returned no record from PubMed"
        return result

    # Populate resolved metadata
    result.real_title = paper.title
    result.real_year = paper.year
    result.real_journal = paper.journal
    result.real_abstract = getattr(paper, "abstract", None)
    authors = getattr(paper, "authors", [])
    result.real_authors = (
        f"{authors[0]} et al." if len(authors) > 1
        else (authors[0] if authors else "unknown")
    )

    # Topic consistency check
    consistent, topic_reason = _topic_consistent(
        result.context, paper.title, result.real_abstract
    )
    if not consistent:
        result.verdict = "MISMATCH"
        result.reason = topic_reason
        return result

    # Secondary corroboration: author-surname + year cross-check.
    # Catches "same-domain swap" fabrications that pass the topic-word
    # heuristic but cite the wrong specific paper.
    corroborated, corr_reason = _author_year_corroborate(
        result.context, authors, result.real_year, result.raw_id
    )
    if corroborated:
        result.verdict = "PASS"
        result.reason = f"{topic_reason}; {corr_reason}"
    else:
        result.verdict = "MISMATCH"
        result.reason = f"topic OK but {corr_reason}"

    return result


def _classify_doi(result: CitationResult) -> CitationResult:
    work, status = _resolve_doi(result.raw_id)

    if status == "error":
        result.verdict = "UNRESOLVED-DOI"
        result.reason = "CrossRef returned a network/HTTP error — manual check required"
        return result

    if status == "not_found" or work is None:
        result.verdict = "UNRESOLVED-DOI"
        result.reason = "DOI not found in CrossRef registry"
        return result

    # Populate resolved metadata
    result.real_title = work.title
    result.real_year = str(work.year) if work.year else None
    result.real_journal = work.container

    if work.is_retracted:
        result.verdict = "MISMATCH"
        result.reason = f"RETRACTED — update_types={work.update_types}"
        return result

    if not work.title:
        result.verdict = "UNRESOLVED-DOI"
        result.reason = "CrossRef returned a record but title is empty"
        return result

    consistent, topic_reason = _topic_consistent(result.context, work.title, None)
    if not consistent:
        result.verdict = "MISMATCH"
        result.reason = topic_reason
        return result

    # Secondary corroboration: year cross-check (CrossrefWork exposes no
    # structured author list, so only the year half of the check applies).
    corroborated, corr_reason = _author_year_corroborate(
        result.context, None, result.real_year, result.raw_id
    )
    if corroborated:
        result.verdict = "PASS"
        result.reason = f"{topic_reason}; {corr_reason}"
    else:
        result.verdict = "MISMATCH"
        result.reason = f"topic OK but {corr_reason}"

    return result


def classify_citation(result: CitationResult) -> CitationResult:
    if result.id_type == "PMID":
        return _classify_pmid(result)
    elif result.id_type == "DOI":
        return _classify_doi(result)
    else:
        result.verdict = "UNRESOLVED-DOI"
        result.reason = "Unknown id type"
        return result


# ---------------------------------------------------------------------------
# File scanner
# ---------------------------------------------------------------------------
def scan_file(file_path: str) -> list[CitationResult]:
    path = Path(file_path)
    if not path.exists():
        print(f"[ERROR] File not found: {file_path}", file=sys.stderr)
        return []

    text = path.read_text(encoding="utf-8", errors="replace")
    citations = _extract_citations(text, str(path))
    classified = []
    for cit in citations:
        classified.append(classify_citation(cit))
    return classified


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
_VERDICT_ORDER = {"FABRICATED": 0, "MISMATCH": 1, "UNRESOLVED-DOI": 2, "PASS": 3}


def _safe_print(s: str) -> None:
    """Print with unicode replacement for any remaining encoding issues."""
    print(s.encode("utf-8", errors="replace").decode("utf-8", errors="replace"))


def _print_table(results: list[CitationResult]) -> None:
    """Print a per-citation results table to stdout."""
    # Sort: worst verdicts first
    sorted_r = sorted(results, key=lambda r: (
        _VERDICT_ORDER.get(r.verdict, 99), r.file_path, r.line_number
    ))

    col = {"verdict": 14, "id": 22, "location": 36, "real_title": 52}

    header = (
        f"{'VERDICT':<{col['verdict']}}"
        f"{'ID':<{col['id']}}"
        f"{'FILE:LINE':<{col['location']}}"
        f"{'RESOLVED TITLE':<{col['real_title']}}"
        f"CONTEXT (snippet)"
    )
    _safe_print("")
    _safe_print(header)
    _safe_print("-" * 165)

    for r in sorted_r:
        loc = f"{Path(r.file_path).name}:{r.line_number}"
        real_t = (r.real_title or "---")[:col["real_title"] - 2]
        # Use only the direct line (first 120 chars) for the display context
        ctx_display = r.context[:120].replace("\n", " ")
        id_str = (
            f"PMID:{r.raw_id}" if r.id_type == "PMID"
            else f"DOI:{r.raw_id[:18]}"
        )
        row = (
            f"{r.verdict:<{col['verdict']}}"
            f"{id_str:<{col['id']}}"
            f"{loc:<{col['location']}}"
            f"{real_t:<{col['real_title']}}"
            f"{ctx_display}"
        )
        _safe_print(row)

    _safe_print("")


def _print_fabricated_detail(results: list[CitationResult]) -> None:
    bad = [r for r in results if r.verdict in ("FABRICATED", "MISMATCH")]
    if not bad:
        _safe_print("\nNo FABRICATED or MISMATCH citations found.")
        return

    _safe_print(f"\n{'='*72}")
    _safe_print(f"FABRICATED / MISMATCH DETAIL ({len(bad)} citations requiring action)")
    _safe_print(f"{'='*72}")
    for r in bad:
        _safe_print(f"\n  [{r.verdict}] {r.id_type}:{r.raw_id}")
        _safe_print(f"  File      : {r.file_path}")
        _safe_print(f"  Line      : {r.line_number}")
        _safe_print(f"  Context   : {r.context[:200]}")
        _safe_print(f"  Real title: {r.real_title or '--- (NOT FOUND IN PUBMED)'}")
        if r.real_year or r.real_journal:
            _safe_print(f"  Real meta : year={r.real_year or 'unknown'} | journal={r.real_journal or 'unknown'}")
        _safe_print(f"  Reason    : {r.reason}")
        url = ""
        if r.id_type == "PMID":
            url = f"https://pubmed.ncbi.nlm.nih.gov/{r.raw_id}/"
        elif r.id_type == "DOI":
            url = f"https://doi.org/{r.raw_id}"
        if url:
            _safe_print(f"  Verify at : {url}")


def _print_summary(results: list[CitationResult]) -> dict[str, int]:
    counts: dict[str, int] = {
        "PASS": 0, "MISMATCH": 0, "FABRICATED": 0, "UNRESOLVED-DOI": 0
    }
    for r in results:
        counts[r.verdict] = counts.get(r.verdict, 0) + 1

    total = len(results)
    _safe_print("=" * 72)
    _safe_print("CITATION INTEGRITY SWEEP -- SUMMARY")
    _safe_print("=" * 72)
    _safe_print(f"  Total identifiers checked  : {total}")
    _safe_print(f"  PASS                       : {counts.get('PASS', 0)}")
    _safe_print(f"  MISMATCH                   : {counts.get('MISMATCH', 0)}")
    _safe_print(f"  FABRICATED                 : {counts.get('FABRICATED', 0)}")
    _safe_print(f"  UNRESOLVED-DOI             : {counts.get('UNRESOLVED-DOI', 0)}")
    _safe_print("=" * 72)
    return counts


# ---------------------------------------------------------------------------
# Offline regression suite for the author/year corroboration layer
# ---------------------------------------------------------------------------
def _run_selftest() -> int:
    """
    Offline-runnable regression tests for the author/year corroboration layer.

    Uses FIXTURED resolved-record data (no live PubMed call) so the suite
    runs deterministically without network access.  Exit 0 = all pass,
    1 = any failure.
    """
    import traceback

    _safe_print("verify_citations --selftest: author-surname + year corroboration")

    def _check(name: str, ctx: str, surname, year, ok: bool):
        try:
            corroborated, reason = _author_year_corroborate(ctx, surname, year, "")
            passed = corroborated == ok
        except Exception:
            traceback.print_exc()
            passed = False
            reason = "EXCEPTION"
        status = "PASS" if passed else "FAIL"
        _safe_print(f"  [{status}] {name}")
        if not passed:
            _safe_print(f"           expected corroborated={ok}, got reason={reason!r}")
        return passed

    total = 0
    passed = 0

    total += 1; passed += _check(
        "TC-1: same-domain swap — Thorning claimed, Salas-Salvado resolved",
        "Thorning et al. 2017, Am J Clin Nutr — RCT n=57 cheese vs butter vs control, LDL; "
        "dairy matrix effect cheese PMID 28615384",
        ["Salas-Salvado"], "2017", False,
    )
    total += 1; passed += _check(
        "TC-2: correct citation — Brassard 2017 matches resolved",
        "Brassard et al. (2017), Am J Clin Nutr. DOI 10.3945/ajcn.116.150300, "
        "PMID 28251937. Multicenter randomized crossover cheese butter LDL.",
        ["Brassard"], "2017", True,
    )
    total += 1; passed += _check(
        "TC-3: no parseable author/year — conservative pass",
        "PMID 28382889 digestibility",
        ["John Doe", "Jane Smith"], None, True,
    )
    total += 1; passed += _check(
        "TC-4: year conflict — context 2019, resolved 2011",
        "Hjerpsted 2019 cheese LDL crossover Am J Clin Nutr PMID 22030228",
        ["Julie Hjerpsted", "Eva Leedo"], "2011", False,
    )
    total += 1; passed += _check(
        "TC-5: year within tolerance (diff=1)",
        "Feeney et al. 2018 dairy matrix cheese LDL PMID 30107488",
        ["Feeney", "Givens"], "2019", True,
    )
    total += 1; passed += _check(
        "TC-6: surname match only (no year in context)",
        "Hjerpsted crossover RCT cheese butter sat-fat LDL PMID 22030228",
        ["Hjerpsted"], None, True,
    )
    total += 1; passed += _check(
        "TC-7: surname mismatch — Kay cited, Pradeilles resolved",
        "Kay et al. 2024, AJCN — meta-analysis cheese sat-fat LDL surrogate PMID 39133879",
        ["Pradeilles"], "2024", False,
    )

    _safe_print(f"\n  {passed}/{total} corroboration self-tests passed")

    # Live spot-check is optional and only runs if clients + network are
    # available; failure here does not fail the offline suite.
    if _CLIENTS_AVAILABLE:
        try:
            dummy = CitationResult(
                id_type="PMID", raw_id="31122155", file_path="<selftest>",
                line_number=0, context="selftest live spot-check PMID 31122155",
            )
            live_result = classify_citation(dummy)
            live_ok = live_result.verdict in ("PASS", "MISMATCH")
            _safe_print(f"  [{'PASS' if live_ok else 'WARN'}] live PubMed connectivity check "
                        f"(PMID 31122155 -> {live_result.verdict})")
        except Exception as exc:
            _safe_print(f"  [WARN] live connectivity check skipped: {exc}")

    return 0 if passed == total else 1


# ---------------------------------------------------------------------------
# Default scan targets (--all mode)
# ---------------------------------------------------------------------------
DEFAULT_SCAN_FILES = [
    # Primary governance + evidence registries
    "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md",
    "01_framework/governance/evidence_registry_v1.md",
    # Additive library + glass box
    "01_framework/glass_box/additive_tiered_library_v1.md",
    "01_framework/glass_box/w2_additive_copy_v1.md",
    "01_framework/glass_box/diaas_source_table_v1.md",
    # Supplement framework
    "01_framework/supplement_framework/methodology_v1.md",
    # Editorial intelligence
    "01_framework/editorial/editorial_intelligence_v3.md",
]


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bari citation integrity gate -- resolves PMIDs/DOIs and detects fabrications.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Exit codes:
              0  All citations PASS (or only UNRESOLVED-DOI warnings)
              1  One or more MISMATCH or FABRICATED citations found
              2  Only UNRESOLVED-DOI warnings (no hard fails; human review needed)

            Examples:
              python verify_citations.py 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
              python verify_citations.py --all
              python verify_citations.py --pmid 31122155
        """),
    )
    parser.add_argument("files", nargs="*", help="One or more file paths to scan")
    parser.add_argument(
        "--all", action="store_true",
        help="Scan all default governance/evidence files",
    )
    parser.add_argument(
        "--pmid", metavar="PMID",
        help="Spot-check a single PMID (resolve and print result; no file scan)",
    )
    parser.add_argument(
        "--repo-root", metavar="PATH",
        default=str(_REPO_ROOT),
        help=f"Repository root (default: {_REPO_ROOT})",
    )
    parser.add_argument(
        "--selftest", action="store_true",
        help="Run built-in regression suite for the author-surname+year "
             "corroboration layer (offline-safe; exit 0 = all pass, 1 = any failure)",
    )
    parser.add_argument(
        "--json", metavar="SOURCE", default=None,
        help="Scan a JSON blob for PMIDs/DOIs instead of files. SOURCE is a "
             "path, or '-' to read from stdin (this is how validate_return.py's "
             "C6 citation check invokes this gate: --json -, contract JSON on stdin).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root)

    # --- Offline regression suite ---
    if args.selftest:
        return _run_selftest()

    # --- Scan a JSON blob (stdin or file) for embedded PMIDs/DOIs ---
    if args.json is not None:
        if args.json == "-":
            blob = sys.stdin.read()
            source_label = "<stdin>"
        else:
            blob = Path(args.json).read_text(encoding="utf-8", errors="replace")
            source_label = args.json
        results = _extract_citations(blob, source_label)
        if not results:
            _safe_print("No PMIDs or DOIs found in JSON input.")
            return 0
        classified = [classify_citation(r) for r in results]
        _print_table(classified)
        _print_fabricated_detail(classified)
        counts = _print_summary(classified)
        n_hard = counts.get("FABRICATED", 0) + counts.get("MISMATCH", 0)
        n_unresolved = counts.get("UNRESOLVED-DOI", 0)
        if n_hard > 0:
            return 1
        if n_unresolved > 0:
            return 2
        return 0

    # --- Spot-check a single PMID ---
    if args.pmid:
        pmid = args.pmid.strip()
        dummy = CitationResult(
            id_type="PMID",
            raw_id=pmid,
            file_path="<command-line>",
            line_number=0,
            context=f"PMID {pmid} spot-check from command line",
        )
        result = classify_citation(dummy)
        _safe_print(f"\nSpot-check PMID {pmid}")
        _safe_print(f"  Verdict : {result.verdict}")
        _safe_print(f"  Title   : {result.real_title or '---'}")
        _safe_print(f"  Year    : {result.real_year or '---'}")
        _safe_print(f"  Journal : {result.real_journal or '---'}")
        _safe_print(f"  Authors : {result.real_authors or '---'}")
        _safe_print(f"  Reason  : {result.reason}")
        if result.real_title:
            _safe_print(f"  URL     : https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
        return 0 if result.verdict == "PASS" else 1

    # --- Determine files to scan ---
    if args.all:
        targets = [str(repo_root / p) for p in DEFAULT_SCAN_FILES]
    elif args.files:
        targets = []
        for f in args.files:
            p = Path(f)
            if not p.is_absolute():
                p = repo_root / p
            targets.append(str(p))
    else:
        parser.print_help()
        return 0

    # --- Scan ---
    all_results: list[CitationResult] = []
    for target in targets:
        print(f"[SCAN] {target}", file=sys.stderr)
        results = scan_file(target)
        print(f"       {len(results)} citations extracted", file=sys.stderr)
        all_results.extend(results)

    if not all_results:
        _safe_print("No PMIDs or DOIs found in scanned files.")
        return 0

    # --- Print table and summary ---
    _print_table(all_results)
    _print_fabricated_detail(all_results)
    counts = _print_summary(all_results)

    # --- Determine exit code ---
    n_hard = counts.get("FABRICATED", 0) + counts.get("MISMATCH", 0)
    n_unresolved = counts.get("UNRESOLVED-DOI", 0)

    if n_hard > 0:
        return 1
    if n_unresolved > 0:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
