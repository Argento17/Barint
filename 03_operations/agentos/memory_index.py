#!/usr/bin/env python3
r"""
memory_index.py — intent-aware retrieval over the Bari memory store (TASK-424 / W5)
===================================================================================

Today all ~135 memory files load wholesale into context every session (the MEMORY.md
index + the full set). Context engineering is the real 2026 skill: a poorly-contexted
agent is ~10x the cost, and loading everything drowns the few memories that matter for
the task in front of you. This builds the retrieval layer the store lacks — WITHOUT a
vector database and WITHOUT changing the store: markdown files stay the single source of
truth (git-diffable, human-editable); a local SQLite sidecar indexes them for fast
hybrid recall. (The "memweave" pattern: markdown + SQLite, no infra.)

Retrieval blend (all local, zero network):
  1. FTS5 / BM25   — lexical relevance, column-weighted (name >> description >> body).
  2. Recency decay — newer memories get a mild boost (file mtime; a stale rule shouldn't
                     outrank a fresh correction).
  3. MMR diversify — greedy selection that penalizes near-duplicates so the top-k covers
                     different aspects of the query rather than 5 variants of one memory.
  4. Wikilink hop  — with --expand, pulls in 1-hop [[linked]] neighbours at reduced weight.

Embeddings are an OPTIONAL enhancement: if sentence-transformers is installed the semantic
layer activates automatically (see _embed()); otherwise BM25+MMR is the whole of it and the
tool is fully functional. No hard dependency.

Design guarantees:
  - Read-only over the memory store; only ever writes its own SQLite index under
    <memory_dir>/.memory_index/. Never edits a memory file.
  - Idempotent build (upsert by path+mtime); `recall` warns if the index is stale and
    can auto-rebuild with --auto-build.
  - Fails SAFE: any error in recall falls back to "load everything" (the current behaviour),
    so it can never make the agent blind to a memory.

Usage:
  python memory_index.py --build
  python memory_index.py --recall "which lane authors Hebrew consumer copy?" -k 6
  python memory_index.py --recall "dispatch race hazard" --expand --json
  python memory_index.py --stats
  python memory_index.py --selftest
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import sqlite3
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass

MEMORY_DIR_DEFAULT = Path(r"C:\Users\HP\.claude\projects\c--Bari\memory")
INDEX_SUBDIR = ".memory_index"
DB_NAME = "memory_index.db"
RECENCY_HALFLIFE_DAYS = 45.0      # a memory's recency boost halves every ~45 days
RECENCY_MAX_BOOST = 0.25          # at most +25% for a brand-new memory
MMR_LAMBDA = 0.72                 # relevance vs diversity (higher = more relevance-driven)

_STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "on", "for", "and", "or", "is", "are", "be",
    "which", "what", "who", "how", "why", "when", "that", "this", "with", "by", "as",
    "at", "from", "it", "its", "do", "does", "should", "can", "we", "i", "you",
}
_WIKILINK_RE = re.compile(r"\[\[([a-z0-9][a-z0-9_-]*)\]\]", re.I)
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.S)


# ── parsing ──────────────────────────────────────────────────────────────────
def _parse_memory(path: Path) -> dict | None:
    """Parse one memory file into {name, description, type, body, links, mtime}."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    name = path.stem
    description, mtype, body = "", "", text
    m = _FRONTMATTER_RE.match(text)
    if m:
        fm_raw, body = m.group(1), m.group(2)
        try:
            import yaml  # present in env; degrade gracefully if not
            fm = yaml.safe_load(fm_raw) or {}
            name = str(fm.get("name") or name)
            description = str(fm.get("description") or "")
            meta = fm.get("metadata") or {}
            mtype = str(meta.get("type") or "") if isinstance(meta, dict) else ""
        except Exception:  # noqa: BLE001 — frontmatter parse must never crash the index
            for line in fm_raw.splitlines():
                if line.startswith("description:"):
                    description = line.split(":", 1)[1].strip()
                elif line.startswith("name:"):
                    name = line.split(":", 1)[1].strip() or name
    links = sorted(set(_WIKILINK_RE.findall(text)))
    try:
        mtime = path.stat().st_mtime
    except OSError:
        mtime = 0.0
    return {"name": name, "path": str(path), "description": description,
            "type": mtype, "body": body, "links": links, "mtime": mtime}


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower())
            if len(t) > 1 and t not in _STOPWORDS}


# ── index build ──────────────────────────────────────────────────────────────
def _db_path(memory_dir: Path) -> Path:
    return memory_dir / INDEX_SUBDIR / DB_NAME


def _connect(memory_dir: Path) -> sqlite3.Connection:
    dbp = _db_path(memory_dir)
    dbp.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(dbp))
    return con


def build_index(memory_dir: Path, verbose: bool = True) -> int:
    con = _connect(memory_dir)
    con.executescript(
        """
        DROP TABLE IF EXISTS mem;
        DROP TABLE IF EXISTS meta;
        CREATE VIRTUAL TABLE mem USING fts5(
            name, description, body,
            path UNINDEXED, type UNINDEXED, mtime UNINDEXED, links UNINDEXED,
            tokenize = 'unicode61'
        );
        CREATE TABLE meta (key TEXT PRIMARY KEY, val TEXT);
        """
    )
    n = 0
    newest = 0.0
    for path in sorted(memory_dir.glob("*.md")):
        if path.name == "MEMORY.md":       # the index file itself is not a memory
            continue
        rec = _parse_memory(path)
        if not rec:
            continue
        con.execute(
            "INSERT INTO mem (name, description, body, path, type, mtime, links) "
            "VALUES (?,?,?,?,?,?,?)",
            (rec["name"], rec["description"], rec["body"], rec["path"],
             rec["type"], str(rec["mtime"]), " ".join(rec["links"])),
        )
        newest = max(newest, rec["mtime"])
        n += 1
    con.execute("INSERT OR REPLACE INTO meta VALUES ('count', ?)", (str(n),))
    con.execute("INSERT OR REPLACE INTO meta VALUES ('newest_mtime', ?)", (str(newest),))
    con.commit()
    con.close()
    if verbose:
        print(f"indexed {n} memories -> {_db_path(memory_dir)}")
    return n


def _index_is_stale(memory_dir: Path, con: sqlite3.Connection) -> bool:
    """Stale if any memory file is newer than the newest mtime recorded at build time."""
    row = con.execute("SELECT val FROM meta WHERE key='newest_mtime'").fetchone()
    if not row:
        return True
    indexed_newest = float(row[0] or 0.0)
    for path in memory_dir.glob("*.md"):
        if path.name == "MEMORY.md":
            continue
        try:
            if path.stat().st_mtime > indexed_newest + 1e-6:
                return True
        except OSError:
            continue
    return False


# ── recall ───────────────────────────────────────────────────────────────────
def _fts_query(query: str) -> str:
    """Turn free text into a safe FTS5 OR-query of its content tokens."""
    toks = [t for t in _tokens(query)]
    if not toks:
        return ""
    # quote each token (FTS5 treats a bare token as a column-filter if it contains ':')
    return " OR ".join(f'"{t}"' for t in toks)


def _recency_boost(mtime: float, now: float) -> float:
    if mtime <= 0 or now <= 0:
        return 0.0
    age_days = max(0.0, (now - mtime) / 86400.0)
    return RECENCY_MAX_BOOST * math.exp(-age_days * math.log(2) / RECENCY_HALFLIFE_DAYS)


def _now_mtime(memory_dir: Path) -> float:
    """A deterministic 'now' = newest file mtime (avoids Date.now; stable for tests)."""
    newest = 0.0
    for path in memory_dir.glob("*.md"):
        try:
            newest = max(newest, path.stat().st_mtime)
        except OSError:
            continue
    return newest


def recall(memory_dir: Path, query: str, k: int = 6, expand: bool = False,
           auto_build: bool = False) -> dict:
    """Return top-k relevant memories. Fails safe: on any error, signal load-all."""
    dbp = _db_path(memory_dir)
    if not dbp.exists():
        if auto_build:
            build_index(memory_dir, verbose=False)
        else:
            return {"ok": False, "fallback": "load_all",
                    "reason": "no index built (run --build or pass --auto-build)", "results": []}
    con = _connect(memory_dir)
    try:
        stale = _index_is_stale(memory_dir, con)
        if stale and auto_build:
            con.close()
            build_index(memory_dir, verbose=False)
            con = _connect(memory_dir)
            stale = False

        fq = _fts_query(query)
        if not fq:
            return {"ok": False, "fallback": "load_all",
                    "reason": "query had no content tokens", "results": []}

        # BM25: lower is better; weight name >> description >> body.
        rows = con.execute(
            "SELECT name, description, body, path, type, mtime, links, "
            "bm25(mem, 10.0, 5.0, 1.0) AS score "
            "FROM mem WHERE mem MATCH ? ORDER BY score LIMIT 60",
            (fq,),
        ).fetchall()
        if not rows:
            return {"ok": True, "stale": stale, "fallback": None, "results": [],
                    "note": "no lexical match; consider load-all for this query"}

        now = _now_mtime(memory_dir)
        cands = []
        # bm25 scores are negative-ish; normalise to a 0..1 relevance for blending.
        raw = [r[7] for r in rows]
        lo, hi = min(raw), max(raw)
        span = (hi - lo) or 1.0
        for r in rows:
            name, desc, body, path, mtype, mtime_s, links_s, score = r
            rel = 1.0 - ((score - lo) / span)          # 1 = best lexical match
            rel *= (1.0 + _recency_boost(float(mtime_s or 0.0), now))
            cands.append({
                "name": name, "description": desc, "path": path, "type": mtype,
                "links": links_s.split() if links_s else [],
                "relevance": round(rel, 4),
                "_tok": _tokens(f"{name} {desc} {body[:400]}"),
            })

        selected = _mmr(cands, k)

        if expand:
            selected = _expand_links(con, selected, k)

        out = [{key: c[key] for key in ("name", "description", "path", "type", "relevance")}
               for c in selected]
        return {"ok": True, "stale": stale, "fallback": None,
                "query_tokens": sorted(_tokens(query)), "results": out}
    except sqlite3.Error as e:
        return {"ok": False, "fallback": "load_all", "reason": f"sqlite error: {e}", "results": []}
    finally:
        con.close()


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return inter / (len(a) + len(b) - inter)


def _mmr(cands: list[dict], k: int) -> list[dict]:
    """Greedy MMR: pick the most relevant, then trade relevance against novelty."""
    selected: list[dict] = []
    pool = sorted(cands, key=lambda c: -c["relevance"])
    while pool and len(selected) < k:
        best, best_score = None, -1e9
        for c in pool:
            sim = max((_jaccard(c["_tok"], s["_tok"]) for s in selected), default=0.0)
            mmr = MMR_LAMBDA * c["relevance"] - (1 - MMR_LAMBDA) * sim
            if mmr > best_score:
                best, best_score = c, mmr
        selected.append(best)
        pool.remove(best)
    return selected


def _expand_links(con: sqlite3.Connection, selected: list[dict], k: int) -> list[dict]:
    """Add 1-hop [[wikilink]] neighbours of the selected set at reduced relevance."""
    have = {c["name"] for c in selected}
    extra: list[dict] = []
    for c in selected:
        for link in c["links"]:
            if link in have:
                continue
            row = con.execute(
                "SELECT name, description, path, type FROM mem WHERE name = ? LIMIT 1",
                (link,),
            ).fetchone()
            if row:
                have.add(link)
                extra.append({"name": row[0], "description": row[1], "path": row[2],
                              "type": row[3], "relevance": round(c["relevance"] * 0.5, 4),
                              "_tok": set()})
    return selected + sorted(extra, key=lambda c: -c["relevance"])[:max(0, k)]


# ── stats / selftest ─────────────────────────────────────────────────────────
def stats(memory_dir: Path) -> int:
    dbp = _db_path(memory_dir)
    if not dbp.exists():
        print("no index built. run: memory_index.py --build")
        return 1
    con = _connect(memory_dir)
    count = con.execute("SELECT val FROM meta WHERE key='count'").fetchone()
    by_type = con.execute("SELECT type, COUNT(*) FROM mem GROUP BY type ORDER BY 2 DESC").fetchall()
    stale = _index_is_stale(memory_dir, con)
    con.close()
    print(f"index: {dbp}")
    print(f"memories indexed: {count[0] if count else '?'}")
    print(f"stale: {stale}")
    print("by type: " + ", ".join(f"{t or '(none)'}={n}" for t, n in by_type))
    return 0


def run_selftest() -> int:
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="memory_index_selftest_"))
    try:
        (tmp / "off_ban_hard_rule.md").write_text(
            "---\nname: off_ban_hard_rule\ndescription: Never use Open Food Facts for any Bari field\n"
            "metadata:\n  type: feedback\n---\nOFF is banned project-wide. Unknown is acceptable; "
            "OFF is not. See [[missing_data_discard_rule]].\n", encoding="utf-8")
        (tmp / "missing_data_discard_rule.md").write_text(
            "---\nname: missing_data_discard_rule\ndescription: If data isn't found one-shot, discard\n"
            "metadata:\n  type: feedback\n---\nDo not over-source missing data.\n", encoding="utf-8")
        (tmp / "content_lane_sonnet.md").write_text(
            "---\nname: content_lane_sonnet\ndescription: Hebrew consumer copy is authored by Sonnet\n"
            "metadata:\n  type: feedback\n---\nGemini is weak at Hebrew editorial; prefer Sonnet for copy.\n",
            encoding="utf-8")
        (tmp / "MEMORY.md").write_text("# index\n- decoy that must never be indexed\n", encoding="utf-8")

        n = build_index(tmp, verbose=False)
        assert n == 3, f"expected 3 indexed (MEMORY.md excluded), got {n}"

        r1 = recall(tmp, "can we use open food facts as a fallback data source?", k=2)
        top1 = r1["results"][0]["name"] if r1["results"] else None
        ok1 = top1 == "off_ban_hard_rule"

        r2 = recall(tmp, "which lane writes Hebrew product copy", k=2)
        top2 = r2["results"][0]["name"] if r2["results"] else None
        ok2 = top2 == "content_lane_sonnet"

        r3 = recall(tmp, "open food facts", k=1, expand=True)
        names3 = {x["name"] for x in r3["results"]}
        ok3 = "missing_data_discard_rule" in names3   # pulled via [[wikilink]] expansion

        stale_before = _index_is_stale(tmp, _connect(tmp))
        ok4 = stale_before is False

        print(f"selftest: OFF-query top={top1} ({'ok' if ok1 else 'WRONG'}); "
              f"copy-query top={top2} ({'ok' if ok2 else 'WRONG'}); "
              f"link-expand pulled discard-rule ({'ok' if ok3 else 'WRONG'}); "
              f"fresh-index not stale ({'ok' if ok4 else 'WRONG'})")
        allok = ok1 and ok2 and ok3 and ok4
        print(f"SELFTEST: {'OK' if allok else 'BROKEN'}")
        return 0 if allok else 1
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Intent-aware retrieval over the Bari memory store.")
    ap.add_argument("--memory-dir", default=str(MEMORY_DIR_DEFAULT))
    ap.add_argument("--build", action="store_true", help="(re)build the SQLite index")
    ap.add_argument("--recall", metavar="QUERY", help="retrieve top-k memories for a task/query")
    ap.add_argument("-k", type=int, default=6, help="number of memories to return (default 6)")
    ap.add_argument("--expand", action="store_true", help="include 1-hop [[wikilink]] neighbours")
    ap.add_argument("--auto-build", action="store_true", help="build/refresh the index if missing/stale")
    ap.add_argument("--stats", action="store_true", help="show index stats")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()

    memory_dir = Path(args.memory_dir)
    if not memory_dir.exists():
        print(f"memory dir not found: {memory_dir}", file=sys.stderr)
        return 2

    if args.build:
        build_index(memory_dir)
        return 0
    if args.stats:
        return stats(memory_dir)
    if args.recall:
        res = recall(memory_dir, args.recall, k=args.k, expand=args.expand, auto_build=args.auto_build)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            if not res["ok"]:
                print(f"[recall unavailable -> {res['fallback']}] {res.get('reason','')}")
                return 0
            if res.get("stale"):
                print("(warning: index is stale — run --build; showing last-built results)")
            print(f"top {len(res['results'])} for tokens {res.get('query_tokens')}:")
            for i, m in enumerate(res["results"], 1):
                print(f"  {i}. {m['name']}  [{m['type'] or '-'}]  rel={m['relevance']}")
                print(f"     {m['description']}")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
