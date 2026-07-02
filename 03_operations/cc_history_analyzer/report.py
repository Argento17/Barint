#!/usr/bin/env python3
"""HTML report builder for the Claude Code History Analyzer.
Pure stdlib. Produces one self-contained, offline HTML file with CSS visuals."""
import html, datetime, statistics

DOW = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

def esc(s): return html.escape(str(s))

def fmt_int(n):
    try: return f"{int(n):,}"
    except: return str(n)

def fmt_tok(n):
    n=int(n)
    if n>=1e9: return f"{n/1e9:.1f}B"
    if n>=1e6: return f"{n/1e6:.1f}M"
    if n>=1e3: return f"{n/1e3:.1f}K"
    return str(n)

def bar_rows(items, total=None, maxn=15, unit=""):
    items=items[:maxn]
    mx=max((v for _,v in items), default=1) or 1
    rows=[]
    for label,v in items:
        w=max(1,int(v/mx*100))
        pct=f" ({v/total*100:.0f}%)" if total else ""
        rows.append(
          f'<div class="bar"><div class="bl" title="{esc(label)}">{esc(label)}</div>'
          f'<div class="bt"><div class="bf" style="width:{w}%"></div>'
          f'<span class="bv">{fmt_int(v)}{unit}{pct}</span></div></div>')
    return "\n".join(rows)

def heatmap(by_dow, by_hour_by_dow=None, by_hour=None):
    # simple two strips: day-of-week and hour-of-day
    def strip(counter, labels):
        mx=max(counter.values(), default=1) or 1
        cells=[]
        for i,lab in enumerate(labels):
            v=counter.get(i, counter.get(str(i),0))
            inten=v/mx
            bg=f"rgba(99,102,241,{0.12+0.88*inten:.2f})"
            cells.append(f'<div class="hc" style="background:{bg}" title="{esc(lab)}: {fmt_int(v)}">'
                         f'<span class="hl">{esc(lab)}</span><span class="hv">{fmt_int(v)}</span></div>')
        return '<div class="heat">'+"".join(cells)+'</div>'
    out=strip({int(k):v for k,v in by_dow.items()}, DOW)
    out+=strip({int(k):v for k,v in by_hour.items()}, [f"{h:02d}" for h in range(24)])
    return out

def daily_spark(by_day):
    days=sorted(by_day.items())
    if not days: return ""
    mx=max(v for _,v in days) or 1
    bars=[]
    for day,v in days:
        h=max(2,int(v/mx*120))
        bars.append(f'<div class="sb" style="height:{h}px" title="{esc(day)}: {fmt_int(v)} msgs"></div>')
    first=days[0][0]; last=days[-1][0]
    return (f'<div class="spark">{"".join(bars)}</div>'
            f'<div class="sparklab"><span>{esc(first)}</span><span>{len(days)} active days</span><span>{esc(last)}</span></div>')

def build_insights(d):
    """Auto-generate data-driven findings: pros, cons, skill ideas, automation."""
    agg=d["agg"]; pros=[]; cons=[]; skills=[]; autos=[]
    tools=agg.get("tools",{}); slash=agg.get("slash",{})
    tok=agg.get("tokens",{})
    cache_read=tok.get("cache_read",0); inp=tok.get("input",0)
    total_in=cache_read+inp+tok.get("cache_creation",0)
    # cache efficiency
    if total_in:
        ce=cache_read/total_in
        if ce>0.6: pros.append(f"Strong prompt-cache reuse — {ce*100:.0f}% of all input tokens are cache reads, which keeps cost and latency down.")
        elif ce<0.35: cons.append(f"Low prompt-cache reuse ({ce*100:.0f}%). Long gaps between turns (>5 min) drop the cache; batching work into tighter sessions would cut cost.")
    # tool errors
    te=agg.get("tool_errors",0); tc=agg.get("tool_calls_total",1) or 1
    er=te/tc
    if er>0.08: cons.append(f"{te:,} tool calls returned errors ({er*100:.1f}% of {tc:,}). Worth checking the top failing commands — recurring failures are friction you can design out.")
    else: pros.append(f"Low tool-error rate ({er*100:.1f}% of {tc:,} calls) — the workflow rarely thrashes on broken commands.")
    # subagent usage
    sd=agg.get("subagent_dispatches",0)
    if sd>50: pros.append(f"Heavy delegation — {sd:,} sub-agent dispatches. You lean on the orchestrator/agent model rather than doing everything in one context.")
    # interrupts as friction signal
    inter=agg.get("interrupts",0); up=agg.get("user_prompts",1) or 1
    if inter > 0.15*up:
        cons.append(f"You interrupted the agent mid-action {inter:,} times (vs {up:,} real prompts). Frequent interrupts usually mean the agent goes too far before checking in — tighter, smaller-scoped asks or a confirm-first habit would reduce wasted work.")
    # pasted mega-prompts
    pl=d.get("prompt_len",{})
    if pl.get("mean",0) > 3*max(pl.get("median",1),1) and pl.get("mean",0)>250:
        pros.append(f"You write rich, self-contained prompts (median {pl.get('median')} words, but a long tail of large pasted specs). That front-loading is exactly the orchestrator pattern — and it's the strongest argument for turning the repeated specs into reusable skills.")
    # confirmations
    cf=agg.get("confirmations",0)
    if cf>40:
        autos_hint=f"You typed {cf:,} bare approvals (yes/continue/go ahead). If those are mostly routine, a wider permission allowlist (or acceptEdits mode) would remove that tap-tap-tap."
        cons.append(autos_hint)
    # bash heaviness
    top_tool=max(tools.items(), key=lambda x:x[1]) if tools else None
    if top_tool and top_tool[0]=="Bash" and tools.get("Bash",0) > 2*max((v for k,v in tools.items() if k!="Bash"), default=1):
        autos.append("Bash dominates tool use by a wide margin. Recurring shell snippets (the same git/python/grep invocations) are prime candidates for a saved script or skill so you stop retyping them.")
    # high-frequency intents -> concrete skill proposals (the strong signal).
    # EXISTING = skills already present in this workspace (so we flag gaps vs dupes).
    EXISTING = {
        "score":"bari-bsip2-scoring-governance / spine_flip","corpus":"bari-category-factory",
        "page":"bari-category-factory","gate":"bari-qa-audit","audit":"bari-qa-audit",
        "report":"/roadmap + orchestrator audit","copy":"(content two-gate — manual)",
        "close":"/orchestrate (closing authority)","task":"/orchestrate + tasks/new_task.py",
        "render":"(manual — render_local_page stage)","verify":"/verify",
    }
    PROPOSAL = {
        "score":"/rescore <category> — flip the scoring switch, re-score, diff vs the committed baseline, emit the movement table.",
        "gate":"/category-gate <category> — render-verify (restart dev server + check real DOM) THEN run the adversarial red-team gate, in one step.",
        "copy":"/copy-signoff <category> — run the mandatory two-gate (Content Agent + Red-Team) over every consumer-facing string and block until both sign off.",
        "render":"/render-verify <category> — restart the dev server and assert score==trace, images resolve, no leakage, before you ever eyeball it.",
        "corpus":"/corpus <category> — shelf-map → filter → BSIP enrich → QA, end to end on the uniform spine path.",
        "report":"/telemetry — orchestrator audit: per-lane ledger (tokens/tools/wall/outcome), rework %, error origin-vs-catch.",
        "close":"/close-task <id> — read the DoD, verify each return-block claim at file:line, then set CLOSED with a close_reason.",
        "audit":"/conformance — run conformance.py --all and report which live categories re-flow vs are non-conforming.",
        "page":"/build-page <category> — run the uniform generate_page path end to end (scoring + copy + render contract).",
    }
    # #1 signal: structured TASK / delegation specs typed by hand
    fw=dict(d.get("first_words",[]))
    taskspecs = fw.get("<task>",0) + fw.get("you",0)   # "TASK-NNN ..." and "You are <Agent>..."
    if taskspecs>=20:
        skills.insert(0,(taskspecs,
            "/dispatch-spec — scaffold the 5-part delegation/TASK spec (objective · context · DoD · lane · return-contract) from a one-line ask, so you stop hand-writing the same structured prompt.",
            "NEW — your most-repeated manual pattern"))
    done=set()
    for iw,cnt in d.get("intents",[]):
        if iw in PROPOSAL and PROPOSAL[iw] not in done and cnt>=18:
            exists=EXISTING.get(iw)
            status = f"partially covered by {exists}" if exists else "NEW — no skill yet"
            skills.append((cnt, PROPOSAL[iw], status))
            done.add(PROPOSAL[iw])
    # intents -> automation
    intents=d.get("intents",[])
    intent_map={
        "render":"Render-and-verify a page locally (restart dev server, check DOM).",
        "red-team":"Run the adversarial red-team gate on a category.",
        "redteam":"Run the adversarial red-team gate on a category.",
        "dispatch":"Dispatch a lane (C1/C2/C3) with the standard delegation spec.",
        "close":"Close a TASK after verifying its return-block claims against artifacts.",
        "verify":"Verify return-block claims at file:line before closing.",
        "report":"Generate a status/telemetry report.",
        "score":"Re-score a corpus and diff against the committed baseline.",
        "commit":"Stage, branch-guard and commit with the Co-Authored-By footer.",
        "render-verify":"Render + red-team gate as one terminal step.",
    }
    seen=set()
    for iw,cnt in intents:
        if cnt>=20 and iw in intent_map and intent_map[iw] not in seen:
            autos.append(f'"{iw}" appears in ~{cnt:,} prompts → automate: {intent_map[iw]}')
            seen.add(intent_map[iw])
    # slash command adoption
    if slash:
        autos.append("You already use slash-commands ("+", ".join("/"+k for k,_ in sorted(slash.items(),key=lambda x:-x[1])[:6])+"). The recurring manual prompts below that have no slash-command equivalent are the gap to close.")
    return pros, cons, skills, autos

def build_html(d, path):
    agg=d["agg"]
    pros,cons,skills,autos = build_insights(d)
    tok=agg.get("tokens",{})
    durs=d.get("session_dur_min",[])
    med_dur=statistics.median(durs) if durs else 0
    msgc=d.get("session_msgcounts",[])
    med_msg=statistics.median(msgc) if msgc else 0
    days=agg.get("by_day",{})
    daterange="—"
    if days:
        ks=sorted(days); daterange=f"{ks[0]} → {ks[-1]}"

    # project byte breakdown
    pb=agg.get("project_bytes",{})
    pb_items=sorted(((k,v) for k,v in pb.items()), key=lambda x:-x[1])
    pb_items=[(k.replace("C--","").replace("-","/"),v/1e6) for k,v in pb_items]

    def section(title, body, sub=""):
        s=f'<div class="card"><h2>{esc(title)}</h2>'
        if sub: s+=f'<p class="sub">{esc(sub)}</p>'
        return s+body+"</div>"

    KPI = lambda v,l: f'<div class="kpi"><div class="kn">{v}</div><div class="kl">{esc(l)}</div></div>'
    kpis = "".join([
        KPI(fmt_int(d["sessions_total"]), "conversations"),
        KPI(fmt_int(agg["types"].get("user",0)+agg["types"].get("assistant",0)), "messages"),
        KPI(fmt_int(agg.get("user_prompts",0)), "your prompts"),
        KPI(fmt_int(agg.get("tool_calls_total",0)), "tool calls"),
        KPI(fmt_int(agg.get("subagent_dispatches",0)), "sub-agent runs"),
        KPI(fmt_tok(sum(tok.values())), "tokens"),
        KPI("$"+fmt_int(round(d["cost_estimate_usd"])), "list-price value*"),
        KPI(f"{med_dur:.0f}m", "median session"),
    ])

    insight_card = ""
    if pros or cons:
        insight_card = (
            '<div class="twocol">'
            '<div><h3 class="good">What\'s working</h3><ul class="ins">'
            + "".join(f"<li>{esc(p)}</li>" for p in pros) + "</ul></div>"
            '<div><h3 class="bad">Friction / opportunities</h3><ul class="ins">'
            + "".join(f"<li>{esc(c)}</li>" for c in cons) + "</ul></div></div>")

    skill_card=""
    if skills:
        rows=[]
        for v,desc,status in skills:
            badge = "new" if status.startswith("NEW") else "exists"
            rows.append(f'<div class="rec"><div class="recn">{fmt_int(v)}×</div>'
                        f'<div><div class="recd">{esc(desc)}</div>'
                        f'<div class="recx"><span class="tag {badge}">{esc(status)}</span></div></div></div>')
        skill_card="".join(rows)

    auto_card="<ul class='ins'>"+"".join(f"<li>{esc(a)}</li>" for a in autos)+"</ul>" if autos else "<p class='sub'>No strong automation signal.</p>"

    rec_rows=[]
    for key,v in d["top_recurring"][:25]:
        if v<2: continue
        ex=d["norm_example"].get(key,"")
        rec_rows.append(f'<tr><td class="cnt">{fmt_int(v)}×</td><td>{esc(ex)}</td></tr>')
    rec_table="<table class='rt'><thead><tr><th>Times</th><th>Representative prompt (recurring pattern)</th></tr></thead><tbody>"+"".join(rec_rows)+"</tbody></table>"

    css = """
*{box-sizing:border-box}body{margin:0;font:15px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#0b0c10;color:#e8eaf0}
.wrap{max-width:1080px;margin:0 auto;padding:32px 20px 80px}
h1{font-size:30px;margin:0 0 4px}.lead{color:#9aa0b5;margin:0 0 26px}
.card{background:#15171f;border:1px solid #242736;border-radius:14px;padding:22px 24px;margin:18px 0}
.card h2{font-size:19px;margin:0 0 14px}.sub{color:#8a90a6;margin:-6px 0 16px;font-size:13.5px}
.kgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.kpi{background:#15171f;border:1px solid #242736;border-radius:12px;padding:16px}
.kn{font-size:26px;font-weight:700;color:#fff}.kl{color:#8a90a6;font-size:12.5px;margin-top:2px}
.bar{display:flex;align-items:center;gap:10px;margin:5px 0}
.bl{width:190px;flex:none;font-size:13px;color:#c7cbdb;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:right}
.bt{position:relative;flex:1;background:#1d2030;border-radius:6px;height:22px}
.bf{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,#6366f1,#8b5cf6);border-radius:6px}
.bv{position:absolute;right:8px;top:50%;transform:translateY(-50%);font-size:12px;color:#e8eaf0;text-shadow:0 1px 2px #000}
.twocol{display:grid;grid-template-columns:1fr 1fr;gap:24px}
h3.good{color:#34d399}h3.bad{color:#f59e0b}h3{font-size:15px;margin:0 0 8px}
ul.ins{margin:0;padding-left:18px}ul.ins li{margin:7px 0;color:#d3d7e6}
.heat{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0 18px}
.hc{width:42px;height:46px;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.hl{font-size:11px;color:#cfd3e3}.hv{font-size:11px;color:#fff;font-weight:600}
.spark{display:flex;align-items:flex-end;gap:2px;height:124px;border-bottom:1px solid #2a2e40;padding-bottom:0}
.sb{flex:1;min-width:2px;background:linear-gradient(180deg,#8b5cf6,#6366f1);border-radius:2px 2px 0 0}
.sparklab{display:flex;justify-content:space-between;color:#8a90a6;font-size:12px;margin-top:6px}
.rec{display:flex;gap:14px;padding:10px 0;border-top:1px solid #242736}
.recn{font-weight:700;color:#8b5cf6;width:54px;flex:none}.recd{color:#e8eaf0}.recx{color:#8a90a6;font-size:12.5px;margin-top:4px}
.tag{display:inline-block;padding:2px 9px;border-radius:20px;font-size:11.5px;font-weight:600}
.tag.new{background:rgba(52,211,153,.15);color:#34d399}.tag.exists{background:rgba(245,158,11,.13);color:#f59e0b}
table.rt{width:100%;border-collapse:collapse;font-size:13.5px}
.rt th{text-align:left;color:#8a90a6;font-weight:600;border-bottom:1px solid #2a2e40;padding:6px 8px}
.rt td{padding:7px 8px;border-bottom:1px solid #1c1f2c;vertical-align:top}
.rt td.cnt{color:#8b5cf6;font-weight:700;white-space:nowrap}
.foot{color:#6b7088;font-size:12px;margin-top:30px;text-align:center}
@media(max-width:760px){.kgrid{grid-template-columns:repeat(2,1fr)}.twocol{grid-template-columns:1fr}.bl{width:110px}}
"""
    H=[]
    H.append(f"<!doctype html><html lang=en><head><meta charset=utf-8>"
             f"<meta name=viewport content='width=device-width,initial-scale=1'>"
             f"<title>Claude Code — Your Workflow Report</title><style>{css}</style></head><body><div class=wrap>")
    H.append(f"<h1>Your Claude Code Workflow — Analyzed</h1>"
             f"<p class=lead>Every conversation on this machine · {esc(daterange)} · "
             f"{fmt_int(agg.get('scanned_files',0))} transcript files · generated {esc(d['generated'])}</p>")
    H.append('<div class=kgrid>'+kpis+'</div>')

    if insight_card:
        H.append(section("The headline", insight_card,
                 "Auto-derived from your actual usage — not generic advice."))

    H.append(section("Activity over time", daily_spark(days),
             "Each bar = messages on that day."))
    H.append(section("When you work", heatmap(agg.get("by_dow",{}), by_hour=agg.get("by_hour",{})),
             "Top strip = day of week · bottom strip = hour of day (local of record)."))

    H.append(section("Which tools you lean on",
             bar_rows(sorted(agg.get("tools",{}).items(),key=lambda x:-x[1]), total=agg.get("tool_calls_total")),
             "How the assistant spends its actions on your behalf."))

    if agg.get("slash"):
        H.append(section("Slash-commands / skills you already use",
                 bar_rows(sorted(agg["slash"].items(),key=lambda x:-x[1]))))

    intents=d.get("intents",[])
    if intents:
        H.append(section("What you keep asking for (by intent)",
                 bar_rows(intents, maxn=18, unit=" prompts"),
                 "How often each action-word shows up across your real prompts — your workflow's center of gravity."))

    H.append(section("Recurring phrasings you type manually",
             rec_table,
             "Normalized prompts (SKUs / task-ids / paths masked). Repeated phrasings = automate these."))

    if skills:
        H.append(section("Skills worth creating", skill_card,
                 "Each is a request you repeat enough to package as a /command or skill."))

    H.append(section("Automation candidates", auto_card))

    H.append(section("Models used",
             bar_rows(sorted(agg.get("models",{}).items(),key=lambda x:-x[1]))))

    H.append(section("Where the work happened (git branches)",
             bar_rows(sorted(agg.get("branches",{}).items(),key=lambda x:-x[1]), maxn=12)))

    H.append(section("Most-touched files",
             bar_rows(sorted(agg.get("edited_files",{}).items(),key=lambda x:-x[1]), maxn=12)))

    # token detail
    tokrows=bar_rows([("cache read",tok.get("cache_read",0)),("input",tok.get("input",0)),
                      ("cache creation",tok.get("cache_creation",0)),("output",tok.get("output",0))])
    H.append(section("Token footprint", tokrows,
             f"Estimated cost ≈ ${d['cost_estimate_usd']:,} (rough blended public list prices; cache reads ~10% of input)."))

    H.append("<p class=foot>* &ldquo;List-price value&rdquo; = what this volume of tokens would cost at public API list prices. "
             "On a Claude subscription this is value received, <b>not</b> a bill you paid. "
             "Re-run <code>python analyze.py</code> anytime to refresh this report.</p>")
    H.append("</div></body></html>")
    with open(path,"w",encoding="utf-8") as f:
        f.write("".join(H))
