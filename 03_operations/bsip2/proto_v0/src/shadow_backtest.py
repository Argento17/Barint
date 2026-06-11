"""
TASK-253 — Project Shadow1 (tech leap 3: Shadow Scoring).

Quant-fund-style backtest for the BSIP2 engine: re-scores every registered
historical corpus under its shipped flag config and diffs against a stored
baseline, with per-product ATTRIBUTION — which dimension / pipeline stage /
mechanism moved which score, by how much. The frozen-impact table is generated
on every diff, replacing "did this touch a frozen category?" as a manual check.

Read-only over all corpora and published artifacts; writes only under
03_operations/shadow/. Never modifies the engine.

Usage (from this src dir or anywhere):
  python shadow_backtest.py baseline [--note "..."] [--corpus NAME ...]
  python shadow_backtest.py diff     [--baseline PATH] [--set FLAG=VAL ...]
                                     [--corpus NAME ...] [--note "..."]
  python shadow_backtest.py status

Exit codes for `diff` (CI-ready):
  0 = clean (no movement anywhere)
  1 = movement in non-frozen corpora only
  2 = FROZEN corpus touched, or an invariant violated
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys

SRC = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(SRC))

SHADOW_ROOT = pathlib.Path(r"C:\Bari\03_operations\shadow")
REGISTRY_PATH = SHADOW_ROOT / "shadow_registry_v1.json"
BASELINES_DIR = SHADOW_ROOT / "baselines"
RUNS_DIR = SHADOW_ROOT / "runs"
CURRENT_POINTER = BASELINES_DIR / "CURRENT.json"

# Same engine-identity file set as the 169D/headpin run records.
ENGINE_FILES = [
    "score_engine.py", "constants.py", "nova_proxy.py", "signal_extractor.py",
    "router_v2.py", "evaluation_scope.py", "input_loader.py",
    "structural_classifier.py", "trace_writer.py",
]

GRADE_RANK = {"E": 0, "D": 1, "C": 2, "B": 3, "A": 4, "S": 5}

# Pipeline stages in engine order — used to attribute WHERE a move entered.
STAGES = ["weighted_dims", "after_cap", "after_penalty", "after_floors", "final"]


# ---------------------------------------------------------------- identity --

def engine_hash() -> str:
    h = hashlib.sha256()
    for f in sorted(ENGINE_FILES):
        h.update(f.encode())
        h.update((SRC / f).read_bytes())
    return h.hexdigest()[:16]


def git_state() -> dict:
    def _git(*args):
        try:
            return subprocess.run(
                ["git", *args], cwd=str(SRC), capture_output=True, text=True,
                timeout=20).stdout.strip()
        except Exception:
            return "unavailable"
    dirty_engine = _git("status", "--porcelain", "--", *ENGINE_FILES)
    return {
        "rev": _git("rev-parse", "--short", "HEAD"),
        "branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
        "engine_files_dirty": sorted(
            line[2:].strip() for line in dirty_engine.splitlines() if line.strip()),
    }


# ----------------------------------------------------------------- scoring --

def _purge_engine_modules():
    """Engine flags are read at import time — force a clean re-import so each
    corpus is scored under exactly its declared flag config."""
    for name, mod in list(sys.modules.items()):
        f = getattr(mod, "__file__", None)
        if f and pathlib.Path(f).resolve().parent == SRC:
            sys.modules.pop(name, None)


def _set_flags(flags: dict):
    """Pin EVERY known flag explicitly — no leakage between corpora or from
    the caller's environment."""
    for k, v in flags.items():
        os.environ[k] = v


def _snapshot(product: dict, cat: dict, nova: dict, r: dict) -> dict:
    return {
        "name": product.get("canonical_name_he", ""),
        "cat": cat.get("category"),
        "subtype": cat.get("category_subtype"),
        "nova": nova.get("nova_level"),
        "score": r.get("final_score_estimate"),
        "grade": r.get("grade_estimate"),
        "ds": r.get("data_sufficiency"),
        "eval_status": r.get("evaluation_status"),
        "dims": r.get("dimension_scores"),
        "stage": {
            "weighted_dims": r.get("weighted_dimension_score"),
            "after_cap": r.get("score_after_cap"),
            "after_penalty": r.get("score_after_penalty"),
            "after_floors": r.get("score_after_floors"),
            "final": r.get("final_score_estimate"),
        },
        "mech": {
            "ferm_bonus": r.get("fermentation_bonus_applied"),
            "ferm_note": r.get("fermentation_bonus_note"),
            "binding_cap": r.get("binding_cap"),
            "caps_applied": r.get("caps_applied"),
            "penalties_applied": r.get("penalties_applied"),
            "penalty_total": r.get("total_penalty_after_scaling"),
            "floors_applied": r.get("floors_applied"),
            "confidence_ceiling": r.get("confidence_ceiling_applied"),
        },
    }


def score_corpus(source: str, flags: dict) -> dict:
    """Score one corpus dir under one pinned flag config. Returns {pid: snapshot}."""
    _set_flags(flags)
    _purge_engine_modules()
    from input_loader import load_batch
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product

    out = {}
    for product in load_batch(pathlib.Path(source)):
        pid = product.get("canonical_product_id", "?")
        try:
            sig = extract_signals(product)
            cat = classify_category(product)
            nova = infer_nova(product, sig["L3_inferred_classifications"])
            ev = assign_evaluation_scope(product, cat["category"])
            r = score_product(product, sig, cat, nova, ev)
            out[pid] = _snapshot(product, cat, nova, r)
        except Exception as e:  # an engine crash IS a finding, not an abort
            out[pid] = {"name": product.get("canonical_name_he", ""),
                        "error": f"{type(e).__name__}: {e}"}
    return out


# ---------------------------------------------------------------- registry --

def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def corpus_configs(registry: dict, only: list[str] | None = None) -> list[dict]:
    defaults = registry["engine_default_flags"]
    out = []
    for c in registry["corpora"]:
        if only and c["name"] not in only:
            continue
        merged = dict(defaults)
        merged.update(c.get("flags", {}))
        out.append({**c, "merged_flags": merged})
    return out


# ---------------------------------------------------------------- baseline --

def cmd_baseline(args) -> int:
    registry = load_registry()
    configs = corpus_configs(registry, args.corpus or None)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    baseline = {
        "baseline_id": f"baseline_{ts}",
        "task": "TASK-253",
        "generated_at": ts,
        "engine_hash": engine_hash(),
        "git": git_state(),
        "registry_version": registry["registry_version"],
        "note": args.note or "",
        "corpora": {},
    }
    total = 0
    for c in configs:
        src = c["source"]
        if not pathlib.Path(src).exists():
            print(f"  {c['name']:22s} MISSING SOURCE: {src}")
            continue
        snaps = score_corpus(src, c["merged_flags"])
        errs = sum(1 for s in snaps.values() if "error" in s)
        baseline["corpora"][c["name"]] = {
            "class": c["class"], "source": src,
            "flags": c["merged_flags"], "n": len(snaps), "errors": errs,
            "products": snaps,
        }
        total += len(snaps)
        print(f"  {c['name']:22s} [{c['class']:9s}] n={len(snaps):3d} errors={errs}")

    BASELINES_DIR.mkdir(parents=True, exist_ok=True)
    path = BASELINES_DIR / f"{baseline['baseline_id']}.json"
    path.write_text(json.dumps(baseline, ensure_ascii=False, indent=1),
                    encoding="utf-8")
    CURRENT_POINTER.write_text(json.dumps({
        "baseline_id": baseline["baseline_id"], "path": str(path),
        "engine_hash": baseline["engine_hash"], "generated_at": ts,
    }, indent=2), encoding="utf-8")
    print(f"\nbaseline {baseline['baseline_id']}  engine={baseline['engine_hash']}  "
          f"corpora={len(baseline['corpora'])}  products={total}")
    print(f"written: {path}")
    return 0


# -------------------------------------------------------------------- diff --

def _stage_entry_point(old_stage: dict, new_stage: dict) -> str | None:
    """First pipeline stage whose value moved — where the change entered."""
    for s in STAGES:
        a, b = old_stage.get(s), new_stage.get(s)
        if a != b:
            return s
    return None


def _jeq(a, b) -> bool:
    return json.dumps(a, sort_keys=True, default=str) == \
           json.dumps(b, sort_keys=True, default=str)


def _diff_product(pid: str, old: dict, new: dict) -> dict | None:
    if "error" in old or "error" in new:
        if old.get("error") == new.get("error"):
            return None
        return {"pid": pid, "name": new.get("name") or old.get("name"),
                "kind": "error_change",
                "old_error": old.get("error"), "new_error": new.get("error"),
                "old_score": old.get("score"), "new_score": new.get("score"),
                "old_grade": old.get("grade"), "new_grade": new.get("grade"),
                "delta": None}
    if old.get("score") == new.get("score") and old.get("grade") == new.get("grade"):
        return None

    delta = None
    if isinstance(old.get("score"), (int, float)) and isinstance(new.get("score"), (int, float)):
        delta = round(new["score"] - old["score"], 2)

    dim_deltas = {}
    od, nd = old.get("dims") or {}, new.get("dims") or {}
    for k in sorted(set(od) | set(nd)):
        a, b = od.get(k), nd.get(k)
        if a != b:
            d = round(b - a, 2) if isinstance(a, (int, float)) and isinstance(b, (int, float)) else None
            dim_deltas[k] = {"old": a, "new": b, "delta": d}

    mech_changes = {}
    om, nm = old.get("mech") or {}, new.get("mech") or {}
    for k in sorted(set(om) | set(nm)):
        if not _jeq(om.get(k), nm.get(k)):
            mech_changes[k] = {"old": om.get(k), "new": nm.get(k)}

    stage_deltas = {}
    for s in STAGES:
        a = (old.get("stage") or {}).get(s)
        b = (new.get("stage") or {}).get(s)
        if a != b:
            d = round(b - a, 2) if isinstance(a, (int, float)) and isinstance(b, (int, float)) else None
            stage_deltas[s] = {"old": a, "new": b, "delta": d}

    other = {}
    for k in ("nova", "ds", "eval_status", "cat", "subtype"):
        if old.get(k) != new.get(k):
            other[k] = {"old": old.get(k), "new": new.get(k)}

    return {
        "pid": pid, "name": new.get("name", ""), "kind": "score_move",
        "old_score": old.get("score"), "new_score": new.get("score"),
        "old_grade": old.get("grade"), "new_grade": new.get("grade"),
        "delta": delta,
        "grade_change": old.get("grade") != new.get("grade"),
        "entered_at_stage": _stage_entry_point(old.get("stage") or {}, new.get("stage") or {}),
        "dim_deltas": dim_deltas,
        "stage_deltas": stage_deltas,
        "mech_changes": mech_changes,
        "other_changes": other,
    }


def _check_invariants(corpus_cfg: dict, snaps: dict) -> list[dict]:
    violations = []
    for inv in corpus_cfg.get("invariants", []):
        if inv["type"] == "no_grade_at_or_above":
            bound = GRADE_RANK[inv["grade"]]
            bad = [{"pid": pid, "name": s.get("name"), "score": s.get("score"),
                    "grade": s.get("grade")}
                   for pid, s in snaps.items()
                   if GRADE_RANK.get(s.get("grade"), -1) >= bound]
            if bad:
                violations.append({"invariant": inv, "products": bad})
    return violations


def cmd_diff(args) -> int:
    if args.baseline:
        baseline_path = pathlib.Path(args.baseline)
    else:
        if not CURRENT_POINTER.exists():
            print("No current baseline. Run `shadow_backtest.py baseline` first.")
            return 3
        baseline_path = pathlib.Path(
            json.loads(CURRENT_POINTER.read_text(encoding="utf-8"))["path"])
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))

    overrides = {}
    for kv in args.set or []:
        k, _, v = kv.partition("=")
        overrides[k.strip()] = v.strip()

    registry = load_registry()
    reg_by_name = {c["name"]: c for c in registry["corpora"]}

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    head_hash = engine_hash()
    report = {
        "run_id": f"shadow_{ts}",
        "task": "TASK-253",
        "generated_at": ts,
        "baseline_id": baseline["baseline_id"],
        "baseline_engine_hash": baseline["engine_hash"],
        "head_engine_hash": head_hash,
        "engine_changed": head_hash != baseline["engine_hash"],
        "git": git_state(),
        "flag_overrides": overrides,
        "note": args.note or "",
        "corpora": {},
    }

    names = args.corpus or list(baseline["corpora"].keys())
    frozen_touched = False
    any_movement = False

    for name in names:
        b = baseline["corpora"].get(name)
        if not b:
            print(f"  {name:22s} not in baseline — skipped")
            continue
        # Apples-to-apples: replay the BASELINE's recorded flags (+ overrides).
        flags = dict(b["flags"])
        flags.update(overrides)
        snaps = score_corpus(b["source"], flags)

        old_pids, new_pids = set(b["products"]), set(snaps)
        moves = []
        for pid in sorted(old_pids & new_pids):
            d = _diff_product(pid, b["products"][pid], snaps[pid])
            if d:
                moves.append(d)
        moves.sort(key=lambda m: abs(m["delta"]) if m["delta"] is not None else 1e9,
                   reverse=True)

        reg_cfg = reg_by_name.get(name, {"invariants": []})
        violations = _check_invariants(reg_cfg, snaps)

        corpus_moved = bool(moves or (old_pids - new_pids) or (new_pids - old_pids))
        if corpus_moved:
            any_movement = True
        if b["class"] == "frozen" and (corpus_moved or violations):
            frozen_touched = True
        if violations:
            any_movement = True

        report["corpora"][name] = {
            "class": b["class"],
            "flags": flags,
            "n": len(snaps),
            "moved": len(moves),
            "grade_changes": sum(1 for m in moves if m.get("grade_change")),
            "added_pids": sorted(new_pids - old_pids),
            "removed_pids": sorted(old_pids - new_pids),
            "invariant_violations": violations,
            "moves": moves,
        }
        print(f"  {name:22s} [{b['class']:9s}] n={len(snaps):3d} "
              f"moved={len(moves):3d} grade_changes="
              f"{report['corpora'][name]['grade_changes']:3d}"
              f"{'  INVARIANT VIOLATION' if violations else ''}")

    if frozen_touched:
        verdict, exit_code = "FROZEN_TOUCHED", 2
    elif any_movement:
        verdict, exit_code = "MOVEMENT", 1
    else:
        verdict, exit_code = "CLEAN", 0
    report["verdict"] = verdict
    report["exit_code"] = exit_code

    run_dir = RUNS_DIR / report["run_id"]
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "shadow_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    (run_dir / "shadow_report.md").write_text(
        render_md(report), encoding="utf-8")
    print(f"\nverdict: {verdict}  (baseline {baseline['baseline_id']}, "
          f"engine {baseline['engine_hash']} -> {head_hash})")
    print(f"written: {run_dir / 'shadow_report.md'}")
    return exit_code


# ------------------------------------------------------------------ report --

def _fmt_score(s):
    return "—" if s is None else s


def render_md(report: dict) -> str:
    L = []
    L.append(f"# Shadow Backtest — {report['run_id']}")
    L.append("")
    L.append(f"- **Verdict: {report['verdict']}** (exit {report['exit_code']})")
    L.append(f"- Baseline: `{report['baseline_id']}` (engine `{report['baseline_engine_hash']}`)")
    L.append(f"- Head engine: `{report['head_engine_hash']}`"
             f"{' — **engine code changed**' if report['engine_changed'] else ' — engine code identical'}")
    g = report["git"]
    L.append(f"- Git: `{g['rev']}` on `{g['branch']}`"
             + (f" — dirty engine files: {', '.join(g['engine_files_dirty'])}"
                if g["engine_files_dirty"] else ""))
    if report["flag_overrides"]:
        L.append(f"- Flag overrides (what-if): `{report['flag_overrides']}`")
    if report["note"]:
        L.append(f"- Note: {report['note']}")
    L.append("")

    # --- The generated frozen-impact table (the point of the leap) ---
    L.append("## Frozen impact — generated on every change")
    L.append("")
    L.append("| Corpus | Class | n | Moved | Grade changes | Invariants | Status |")
    L.append("|---|---|---|---|---|---|---|")
    for name, c in report["corpora"].items():
        if c["class"] != "frozen":
            continue
        inv = "VIOLATED" if c["invariant_violations"] else "ok"
        touched = c["moved"] or c["added_pids"] or c["removed_pids"] or c["invariant_violations"]
        status = "**TOUCHED — frozen-invariant breach**" if touched else "untouched"
        L.append(f"| {name} | frozen | {c['n']} | {c['moved']} | "
                 f"{c['grade_changes']} | {inv} | {status} |")
    L.append("")

    L.append("## All corpora")
    L.append("")
    L.append("| Corpus | Class | n | Moved | Grade changes | Added | Removed |")
    L.append("|---|---|---|---|---|---|---|")
    for name, c in report["corpora"].items():
        L.append(f"| {name} | {c['class']} | {c['n']} | {c['moved']} | "
                 f"{c['grade_changes']} | {len(c['added_pids'])} | {len(c['removed_pids'])} |")
    L.append("")

    # --- Movers with attribution ---
    cap = 60
    shown = 0
    for name, c in report["corpora"].items():
        if not c["moves"] and not c["invariant_violations"]:
            continue
        L.append(f"## {name} — {c['moved']} moved")
        L.append("")
        for v in c["invariant_violations"]:
            inv = v["invariant"]
            L.append(f"**INVARIANT VIOLATED** — `{inv['type']} {inv.get('grade','')}`"
                     f" ({inv.get('why','')}):")
            for p in v["products"]:
                L.append(f"- {p['pid']} «{p['name']}» = {p['score']}/{p['grade']}")
            L.append("")
        if c["moves"]:
            L.append("| Product | Old | New | Δ | Entered at | Top attribution |")
            L.append("|---|---|---|---|---|---|")
        for m in c["moves"]:
            if shown >= cap:
                L.append(f"| … | | | | | report truncated at {cap} rows — full detail in shadow_report.json |")
                break
            if m["kind"] == "error_change":
                attr = f"error: `{m.get('old_error')}` → `{m.get('new_error')}`"
                L.append(f"| {m['pid']} «{m['name']}» | "
                         f"{_fmt_score(m['old_score'])}/{m['old_grade'] or '—'} | "
                         f"{_fmt_score(m['new_score'])}/{m['new_grade'] or '—'} | — | — | {attr} |")
                shown += 1
                continue
            dims = sorted(m["dim_deltas"].items(),
                          key=lambda kv: abs(kv[1]["delta"]) if kv[1]["delta"] is not None else 0,
                          reverse=True)[:3]
            attr_bits = [f"{k} {v['delta']:+g}" for k, v in dims
                         if v["delta"] is not None]
            for k, v in list(m["mech_changes"].items())[:2]:
                if k in ("ferm_note",):
                    continue
                attr_bits.append(f"{k} changed")
            if not attr_bits:
                # No dim/mech-level signal (e.g. a silent cap on the aggregate):
                # fall back to the stage where the move entered.
                st = m["entered_at_stage"]
                sd = (m["stage_deltas"] or {}).get(st, {})
                if sd.get("delta") is not None:
                    attr_bits.append(f"{st} {sd['delta']:+g}")
            attr = "; ".join(attr_bits) or "see json"
            grade_mark = " **(grade)**" if m["grade_change"] else ""
            L.append(f"| {m['pid']} «{m['name']}» | {m['old_score']}/{m['old_grade']} | "
                     f"{m['new_score']}/{m['new_grade']}{grade_mark} | "
                     f"{m['delta']:+g} | {m['entered_at_stage'] or '—'} | {attr} |")
            shown += 1
        L.append("")

    if report["verdict"] == "CLEAN":
        L.append("_No movement on any corpus — engine behavior identical to baseline._")
        L.append("")
    return "\n".join(L)


# ------------------------------------------------------------------ status --

def cmd_status(args) -> int:
    if not CURRENT_POINTER.exists():
        print("No baseline captured yet.")
        return 0
    ptr = json.loads(CURRENT_POINTER.read_text(encoding="utf-8"))
    print(f"current baseline : {ptr['baseline_id']}")
    print(f"engine hash      : {ptr['engine_hash']}")
    print(f"captured at      : {ptr['generated_at']}")
    print(f"file             : {ptr['path']}")
    head = engine_hash()
    print(f"HEAD engine hash : {head}"
          + ("  (UNCHANGED)" if head == ptr["engine_hash"]
             else "  (ENGINE CHANGED — run `diff`)"))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Project Shadow1 — engine backtest (TASK-253)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("baseline", help="capture baseline snapshot of all corpora")
    b.add_argument("--note", default="")
    b.add_argument("--corpus", action="append", help="limit to corpus name (repeatable)")
    b.set_defaults(fn=cmd_baseline)

    d = sub.add_parser("diff", help="re-score at HEAD and diff vs baseline")
    d.add_argument("--baseline", help="baseline file (default: CURRENT)")
    d.add_argument("--set", action="append", metavar="FLAG=VAL",
                   help="what-if flag override (repeatable)")
    d.add_argument("--corpus", action="append", help="limit to corpus name (repeatable)")
    d.add_argument("--note", default="")
    d.set_defaults(fn=cmd_diff)

    s = sub.add_parser("status", help="show current baseline vs HEAD engine")
    s.set_defaults(fn=cmd_status)

    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
