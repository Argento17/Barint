#!/usr/bin/env python3
"""
Claude Code History Analyzer  (dynamic, re-runnable)
====================================================
Scans EVERY Claude Code conversation transcript on this machine
(~/.claude/projects/**/*.jsonl  -- which already includes worktree sessions,
because Claude Code keys storage by the working-directory path), aggregates
the data, mines it for patterns, and writes a single self-contained HTML report.

Run:  python analyze.py
Out:  ./cc_history_report.html   (+ ./cc_history_data.json raw aggregates)

No external dependencies. Streams files line-by-line so the 1GB+ corpus
fits in memory.
"""
import json, glob, os, re, html, collections, datetime, statistics, sys

HOME = os.path.expanduser("~")
PROJECTS_DIR = os.path.join(HOME, ".claude", "projects")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_OUT = os.path.join(OUT_DIR, "cc_history_report.html")
JSON_OUT = os.path.join(OUT_DIR, "cc_history_data.json")

# ---- approximate blended $/Mtok (input, output) for cost estimate only ----
PRICE = {
    "opus":   (15.0, 75.0),
    "sonnet": (3.0, 15.0),
    "haiku":  (0.80, 4.0),
    "fable":  (3.0, 15.0),
}
def price_for(model):
    m = (model or "").lower()
    for k in PRICE:
        if k in m: return PRICE[k]
    return (3.0, 15.0)

_UNUSED_STOP = ("""a an the and or but if then of to in on for with at by from as is are was were be been being this that these those it its it's i you we they he she them us our your my me do does did doing have has had can could should would will shall may might must not no yes please let lets need want make made get got go going run ran use used using it's also just like so than too very can't dont don't into out up down over under again more most some any all each both few other such only own same here there what which who whom how when where why""").split()

INTENT_WORDS = [
    "fix","render","red-team","redteam","red team","dispatch","close","score","scoring",
    "verify","report","review","generate","page","build","check","audit","update","run",
    "create","add","analyze","read","commit","push","test","gate","corpus","copy","write",
    "deploy","clean","refactor","orchestrate","roadmap","task","skill","worktree","compare",
]

def norm_prompt(t):
    t = t.lower()
    t = re.sub(r"sp-\d+", "<sku>", t)
    t = re.sub(r"task-\d+", "<task>", t)
    t = re.sub(r"[a-z]:\\[^\s]+", "<path>", t)
    t = re.sub(r"/[^\s]+", "<path>", t)
    t = re.sub(r"\d+", "<n>", t)
    t = re.sub(r"[^a-z0-9<>\s\-]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def main():
    files = sorted(glob.glob(os.path.join(PROJECTS_DIR, "*", "*.jsonl")))
    if not files:
        print("No transcripts found at", PROJECTS_DIR); sys.exit(1)

    agg = {
        "scanned_files": len(files),
        "projects": collections.Counter(),
        "project_bytes": collections.Counter(),
        "types": collections.Counter(),
        "models": collections.Counter(),
        "tools": collections.Counter(),
        "slash": collections.Counter(),
        "branches": collections.Counter(),
        "perm_modes": collections.Counter(),
        "versions": collections.Counter(),
        "by_day": collections.Counter(),
        "by_dow": collections.Counter(),      # 0=Mon
        "by_hour": collections.Counter(),
        "tokens": {"input":0,"output":0,"cache_read":0,"cache_creation":0},
        "tokens_by_model": collections.defaultdict(lambda: {"input":0,"output":0,"cache_read":0,"cache_creation":0}),
        "tool_errors": 0,
        "tool_calls_total": 0,
        "edited_files": collections.Counter(),
        "subagent_dispatches": 0,
        "user_prompts": 0,           # genuine human/pasted prompts (not tool results / slash / meta)
        "confirmations": 0,          # bare yes/continue/approved turns
        "interrupts": 0,             # [Request interrupted by user]
        "context_continuations": 0,  # auto compaction summary turns
        "prompt_len_words": [],
    }
    NOISE_PREFIX = (
        "this session is being continued",
        "caveat: the messages below",
        "[request interrupted",
        "your task is to create a detailed summary",
        "api error", "[image]",
    )
    CONFIRM = {"yes","y","ok","okay","continue","go on","go ahead","go ahead.","yes go ahead",
               "approved","confirmed","confirmed.","go","do it","proceed","yep","sure","thanks",
               "great","perfect","next","resume","yes.","continue.","please continue"}
    sessions = {}                    # sid -> {"start":ts,"end":ts,"msgs":int,"project":p}
    norm_counter = collections.Counter()
    norm_example = {}
    intent_counter = collections.Counter()
    first_words = collections.Counter()

    def parse_ts(s):
        try: return datetime.datetime.fromisoformat(s.replace("Z","+00:00"))
        except: return None

    for fn in files:
        proj = os.path.basename(os.path.dirname(fn))
        agg["projects"][proj] += 1
        try: agg["project_bytes"][proj] += os.path.getsize(fn)
        except OSError: pass
        with open(fn, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line: continue
                try: d = json.loads(line)
                except Exception: continue
                t = d.get("type","?")
                agg["types"][t] += 1
                ts = parse_ts(d.get("timestamp",""))
                sid = d.get("sessionId")
                if sid:
                    s = sessions.setdefault(sid, {"start":None,"end":None,"msgs":0,"project":proj})
                    s["msgs"] += 1
                    if ts:
                        if s["start"] is None or ts < s["start"]: s["start"] = ts
                        if s["end"] is None or ts > s["end"]: s["end"] = ts
                if d.get("gitBranch"): agg["branches"][d["gitBranch"]] += 1
                if d.get("permissionMode"): agg["perm_modes"][d["permissionMode"]] += 1
                if d.get("version"): agg["versions"][d["version"]] += 1
                if ts:
                    agg["by_day"][ts.date().isoformat()] += 1
                    agg["by_dow"][ts.weekday()] += 1
                    agg["by_hour"][ts.hour] += 1

                msg = d.get("message",{})
                if t == "assistant" and isinstance(msg, dict):
                    model = msg.get("model")
                    if model: agg["models"][model] += 1
                    u = msg.get("usage",{}) or {}
                    it=u.get("input_tokens",0) or 0; ot=u.get("output_tokens",0) or 0
                    cr=u.get("cache_read_input_tokens",0) or 0; cc=u.get("cache_creation_input_tokens",0) or 0
                    agg["tokens"]["input"]+=it; agg["tokens"]["output"]+=ot
                    agg["tokens"]["cache_read"]+=cr; agg["tokens"]["cache_creation"]+=cc
                    tm=agg["tokens_by_model"][model or "?"]
                    tm["input"]+=it; tm["output"]+=ot; tm["cache_read"]+=cr; tm["cache_creation"]+=cc
                    content = msg.get("content")
                    if isinstance(content,list):
                        for b in content:
                            if not isinstance(b,dict): continue
                            if b.get("type")=="tool_use":
                                name=b.get("name","?")
                                agg["tools"][name]+=1; agg["tool_calls_total"]+=1
                                if name in ("Task","Agent"): agg["subagent_dispatches"]+=1
                                inp=b.get("input",{}) or {}
                                if name in ("Edit","Write","Read","NotebookEdit"):
                                    fp=inp.get("file_path") or inp.get("notebook_path")
                                    if fp: agg["edited_files"][fp]+=1

                elif t == "user" and isinstance(msg, dict):
                    content = msg.get("content")
                    is_toolresult=False; txt=""
                    if isinstance(content,list):
                        for b in content:
                            if isinstance(b,dict) and b.get("type")=="tool_result":
                                is_toolresult=True
                                tc=b.get("content")
                                if isinstance(tc,list):
                                    for x in tc:
                                        if isinstance(x,dict) and x.get("type")=="text" and "is_error" in b:
                                            pass
                                if b.get("is_error"): agg["tool_errors"]+=1
                            if isinstance(b,dict) and b.get("type")=="text":
                                txt += b.get("text","")+" "
                    elif isinstance(content,str):
                        txt=content
                    # slash command detection
                    m=re.search(r"<command-name>\s*([^<\s]+)", txt)
                    if m:
                        agg["slash"][m.group(1).lstrip("/")] += 1
                        continue
                    if is_toolresult: continue
                    if d.get("promptSource")=="sdk" or d.get("isMeta"):
                        agg["subagent_dispatches"] += 0
                        continue
                    st=txt.strip()
                    if not st: continue
                    if st.startswith("<") or "system-reminder" in st[:60].lower(): continue
                    low_full=st.lower()
                    if any(low_full.startswith(p) for p in NOISE_PREFIX):
                        if low_full.startswith("[request interrupted"): agg["interrupts"]+=1
                        elif low_full.startswith("this session is being continued"): agg["context_continuations"]+=1
                        continue
                    if low_full.rstrip(".! ") in CONFIRM or low_full in CONFIRM:
                        agg["confirmations"]+=1; continue
                    # genuine prompt
                    agg["user_prompts"] += 1
                    words=st.split()
                    agg["prompt_len_words"].append(len(words))
                    n=norm_prompt(st)
                    if n:
                        key=" ".join(n.split()[:14])
                        norm_counter[key]+=1
                        if key not in norm_example: norm_example[key]=st[:240]
                        fw=n.split()[0] if n.split() else ""
                        if fw: first_words[fw]+=1
                    low=" "+st.lower()+" "
                    for iw in INTENT_WORDS:
                        if " "+iw+" " in low or low.strip().startswith(iw):
                            intent_counter[iw]+=1

    # session stats
    durations=[]; msgcounts=[]
    for s in sessions.values():
        msgcounts.append(s["msgs"])
        if s["start"] and s["end"]:
            durations.append((s["end"]-s["start"]).total_seconds()/60.0)

    # cost estimate
    cost=0.0
    for model,tm in agg["tokens_by_model"].items():
        pin,pout=price_for(model)
        # cache_read priced ~0.1x input; cache_creation ~1.25x input (approx)
        cost += (tm["input"]/1e6)*pin + (tm["output"]/1e6)*pout
        cost += (tm["cache_read"]/1e6)*pin*0.1 + (tm["cache_creation"]/1e6)*pin*1.25

    out={
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "agg": {k:(dict(v) if isinstance(v,(collections.Counter,dict)) else v)
                for k,v in agg.items() if k!="tokens_by_model" and k!="prompt_len_words"},
        "tokens_by_model": {k:v for k,v in agg["tokens_by_model"].items()},
        "sessions_total": len(sessions),
        "session_dur_min": durations,
        "session_msgcounts": msgcounts,
        "cost_estimate_usd": round(cost,2),
        "top_recurring": norm_counter.most_common(40),
        "norm_example": norm_example,
        "intents": intent_counter.most_common(),
        "first_words": first_words.most_common(25),
        "prompt_len": {
            "count": len(agg["prompt_len_words"]),
            "median": statistics.median(agg["prompt_len_words"]) if agg["prompt_len_words"] else 0,
            "mean": round(statistics.mean(agg["prompt_len_words"]),1) if agg["prompt_len_words"] else 0,
        },
    }
    with open(JSON_OUT,"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1,default=str)
    print("wrote", JSON_OUT)
    from report import build_html
    build_html(out, HTML_OUT)
    print("wrote", HTML_OUT)

if __name__=="__main__":
    main()
