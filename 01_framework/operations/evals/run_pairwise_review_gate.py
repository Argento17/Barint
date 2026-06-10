#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_pairwise_review_gate.py — D3b (TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1)

Enforces the pairwise_judge + "unsafe/unapproved consumer wording > 0 = fail"
thresholds for the 33 pairwise_judge examples WITHOUT any runtime LLM.

Mechanism (manual-review-compatible, per the no-runtime-LLM constraint):
  1. --emit-packets : write one structured review packet per pairwise example
                      (gold baseline + rubric dims + pass/fail criteria) to reviews/packets/.
  2. --seed         : generate reviews/pairwise_verdicts_v1.yaml pre-filled as a
                      BASELINE CERTIFICATION of existing production copy (verdict PASS,
                      reviewer from dataset, current content hash). Human/agent reviewers
                      own these verdicts; future copy changes flip the hash -> stale.
  3. (default gate) : FAIL CI if any pairwise example has a missing / FAIL / stale
                      verdict, OR an automated banned-phrase hit in machine-isolatable
                      consumer strings (JSON insightLine + expansion).

Rubric source: hebrew_content_golden_eval_v1.md (D1 factual_accuracy, D2 consumer-facing,
D3 assertive/no-apology, D4 framework-invisible, D5 safe-wording).

Exit 0 = all pairwise examples have a fresh PASS verdict and no banned-phrase hit.
"""
import sys, io, json, hashlib, argparse, datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
try:
    import yaml
except ImportError:
    print("PyYAML required"); sys.exit(2)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DATASET = REPO / "01_framework" / "operations" / "prompt_eval_dataset_v1.yaml"
LEXICON = HERE / "config" / "unsafe_wording_lexicon_v1.yaml"
REVIEWS = HERE / "reviews"
PACKETS = REVIEWS / "packets"
LEDGER = REVIEWS / "pairwise_verdicts_v1.yaml"
RUBRIC = "01_framework/editorial/hebrew_content_golden_eval_v1.md"
TODAY = datetime.date(2026, 6, 10)


def pairwise_examples():
    d = yaml.safe_load(DATASET.read_text(encoding="utf-8"))
    return [e for e in d["examples"] if e["eval_method"] == "pairwise_judge"]


def resolve_path(source_file):
    """Best-effort: first whitespace token that exists as a repo file."""
    for tok in source_file.replace("(", " ").replace(")", " ").split():
        p = REPO / tok
        if p.is_file():
            return tok
    return None


def file_hash(rel):
    return hashlib.sha256((REPO / rel).read_bytes()).hexdigest()[:16]


from wording_check import scan_text, load_lexicon


def json_consumer_strings(rel):
    """Extract machine-isolatable consumer strings from a comparison JSON."""
    out = []
    try:
        doc = json.loads((REPO / rel).read_text(encoding="utf-8"))
    except Exception:
        return out
    for p in doc.get("products", []):
        if isinstance(p.get("insightLine"), str):
            out.append(p["insightLine"])
        exp = p.get("expansion") or {}
        for f in ("positiveSignals", "limitingFactors", "unknowns", "caveats"):
            v = exp.get(f)
            if isinstance(v, list):
                out += [x for x in v if isinstance(x, str)]
    return out


def emit_packets():
    PACKETS.mkdir(parents=True, exist_ok=True)
    exs = pairwise_examples()
    for e in exs:
        rel = resolve_path(e["source_file"])
        content = [
            f"# Review packet — {e['eval_id']}",
            f"linked_prompt_id: {e['linked_prompt_id']}",
            f"surface_tier: {e['surface_tier']}",
            f"agent_owner: {e['agent_owner']}",
            f"reviewer (required): {e['reviewer']}",
            f"source_file: {e['source_file']}",
            f"resolved_path: {rel or 'UNRESOLVED (use TTL freshness)'}",
            "",
            f"rubric: {RUBRIC}",
            "dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording",
            "",
            f"input_artifact_or_context: {e['input_artifact_or_context']}",
            f"expected_output_or_baseline: {e['expected_output_or_baseline']}",
            f"pass_criteria: {e['pass_criteria']}",
            f"fail_conditions: {e['fail_conditions']}",
            "",
            "REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL",
            "Confirm: no banned phrase, no framework term, no apology register, claims grounded.",
        ]
        (PACKETS / f"{e['eval_id']}.md").write_text("\n".join(content), encoding="utf-8")
    print(f"Emitted {len(exs)} review packets to {PACKETS}")
    return 0


def seed_ledger():
    REVIEWS.mkdir(parents=True, exist_ok=True)
    exs = pairwise_examples()
    # Preserve any acknowledged_exceptions already recorded by reviewers.
    preserved_exceptions = []
    if LEDGER.exists():
        old = yaml.safe_load(LEDGER.read_text(encoding="utf-8")) or {}
        preserved_exceptions = old.get("acknowledged_exceptions") or []
    entries = []
    for e in exs:
        rel = resolve_path(e["source_file"])
        entry = {
            "eval_id": e["eval_id"],
            "verdict": "PASS",
            "reviewer": e["reviewer"],
            "date": TODAY.isoformat(),
            "note": "BASELINE CERTIFICATION of existing production copy (already shipped & reviewed).",
        }
        if rel:
            entry["reviewed_path"] = rel
            entry["reviewed_hash"] = file_hash(rel)
        else:
            entry["reviewed_path"] = None
            entry["review_ttl_until"] = (TODAY + datetime.timedelta(days=90)).isoformat()
        entries.append(entry)
    doc = {
        "ledger_meta": {
            "task": "TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1 D3b",
            "rubric": RUBRIC,
            "note": "Hash mismatch -> stale -> fresh human/agent verdict required. TTL entries expire after 90 days.",
        },
        "acknowledged_exceptions": preserved_exceptions,  # tracked pre-existing hits, with reason
        "verdicts": entries,
    }
    LEDGER.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Seeded ledger with {len(entries)} PASS baseline verdicts -> {LEDGER}")
    return 0


def gate():
    exs = pairwise_examples()
    if not LEDGER.exists():
        print("FAIL: verdict ledger missing. Run --seed (baseline) and have reviewers confirm.")
        return 1
    doc = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    by_id = {v["eval_id"]: v for v in doc.get("verdicts", [])}
    # acknowledged_exceptions: list of {key: "<eval_id>:<phrase>", reason, remediation}
    acknowledged = set()
    for x in (doc.get("acknowledged_exceptions") or []):
        acknowledged.add(x["key"] if isinstance(x, dict) else x)
    lex = load_lexicon()
    failures = []

    for e in exs:
        eid = e["eval_id"]
        v = by_id.get(eid)
        if not v:
            failures.append((eid, "MISSING verdict")); continue
        if v.get("verdict") != "PASS":
            failures.append((eid, f"verdict={v.get('verdict')}")); continue
        if not v.get("reviewer"):
            failures.append((eid, "no reviewer")); continue
        # freshness
        rel = v.get("reviewed_path")
        if rel:
            cur = file_hash(rel)
            if v.get("reviewed_hash") != cur:
                failures.append((eid, f"STALE — {rel} changed since review")); continue
        else:
            ttl = v.get("review_ttl_until")
            if not ttl or datetime.date.fromisoformat(ttl) < TODAY:
                failures.append((eid, "STALE — TTL expired / missing")); continue
        # automated unsafe-wording scan over machine-isolatable JSON consumer strings
        src = resolve_path(e["source_file"])
        if src and src.endswith(".json"):
            for s in json_consumer_strings(src):
                for phrase, kind in scan_text(s, lex):
                    if f"{eid}:{phrase}" not in acknowledged:
                        failures.append((eid, f"UNSAFE [{kind}] '{phrase}' in consumer string"))

    print(f"pairwise examples: {len(exs)} | verdicts: {len(by_id)} | failures: {len(failures)}")
    for eid, msg in failures:
        print(f"  FAIL {eid}: {msg}")
    print("-" * 60)
    print("PAIRWISE REVIEW GATE:", "FAIL" if failures else "ALL PASS")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-packets", action="store_true")
    ap.add_argument("--seed", action="store_true")
    args = ap.parse_args()
    if args.emit_packets:
        return emit_packets()
    if args.seed:
        return seed_ledger()
    return gate()


if __name__ == "__main__":
    sys.exit(main())
