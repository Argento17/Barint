// Bari — One-Table Prototype · components
// IMP-1 thesis: ONE row component renders both phone and desktop via container
// queries — not two hand-maintained components. IMP-4: it carries the v2 features
// the spec never shipped (aligned metric column, band rail, dividers, promoted
// confidence). The `mode` prop ("v2" | "v1") shows the consolidation payoff.

const { useState, useRef, useCallback } = React;

const GRADE = {
  A: { bg: "var(--grade-a-bg)", tx: "var(--grade-a-text)", bd: "var(--grade-a-border)", label: "מצוין" },
  B: { bg: "var(--grade-b-bg)", tx: "var(--grade-b-text)", bd: "var(--grade-b-border)", label: "טוב" },
  C: { bg: "var(--grade-c-bg)", tx: "var(--grade-c-text)", bd: "var(--grade-c-border)", label: "בינוני" },
  D: { bg: "var(--grade-d-bg)", tx: "var(--grade-d-text)", bd: "var(--grade-d-border)", label: "חלש" },
  E: { bg: "var(--grade-e-bg)", tx: "var(--grade-e-text)", bd: "var(--grade-e-border)", label: "נמוך" },
};
const CONF = {
  verified: { dot: "#1F8F6A", label: "נתונים מלאים" },
  partial: { dot: "#B5882F", label: "נתונים חלקיים" },
  insufficient: { dot: "#B5BBB6", label: "נתונים חסרים" },
};

function GradeBadge({ score, grade }) {
  const g = GRADE[grade] || GRADE.C;
  return (
    <span className="gradeBadge" style={{ background: g.bg, color: g.tx, borderColor: g.bd }}>
      <b className="bari-score">{score}</b>
      <span className="gletter">{grade}</span>
    </span>
  );
}

function ConfidenceTag({ confidence }) {
  const c = CONF[confidence] || CONF.partial;
  return (
    <span className="confTag" aria-label={c.label}>
      <span className="confDot" style={{ background: c.dot }} aria-hidden></span>
      <span className="confLabel">{c.label}</span>
    </span>
  );
}

// Protein bar 0–20 · additives pips 0–5 · base % bar 0–100 (v2 spec §4).
// Fixed widths → columns align across every row. That alignment IS the differentiator.
function MetricColumn({ metrics }) {
  const { protein, additives, base } = metrics;
  const pPct = Math.max(0, Math.min(100, (protein / 20) * 100));
  const pTone = protein >= 10 ? "#1F8F6A" : protein < 5 ? "#B5882F" : "#B5BBB6";
  const aTone = additives <= 1 ? "#1F8F6A" : additives >= 4 ? "#B5882F" : "#9AA09B";
  return (
    <div className="metricCol" role="group" aria-label="מדדי מוצר">
      <div className="metric" aria-label={`חלבון ${protein} גרם`}>
        <div className="metricTop"><span className="metricK">חלבון</span><span className="metricV">{protein}<i> ג׳</i></span></div>
        <div className="bar"><span style={{ width: `${pPct}%`, background: pTone }}></span></div>
      </div>
      <div className="metric" aria-label={`${additives} תוספי מזון`}>
        <div className="metricTop"><span className="metricK">תוספים</span><span className="metricV">{additives}</span></div>
        <div className="pips">
          {[0, 1, 2, 3, 4].map((i) => (
            <span key={i} className="pip" style={{ background: i < additives ? aTone : "#E6E6E0" }}></span>
          ))}
        </div>
      </div>
      <div className="metric" aria-label={`אחוז גרגר ${base}`}>
        <div className="metricTop"><span className="metricK">% גרגר</span><span className="metricV">{base}<i>%</i></span></div>
        <div className="bar"><span style={{ width: `${base}%`, background: base >= 80 ? "#1F8F6A" : base < 55 ? "#B5882F" : "#9AA09B" }}></span></div>
      </div>
    </div>
  );
}

function RowReason({ reason }) {
  if (!reason || (!reason.positive && !reason.limiting)) return null;
  return (
    <div className="reason">
      {reason.positive ? <p className="rpos"><b aria-hidden>+ </b>{reason.positive}</p> : null}
      {reason.limiting ? <p className="rlim"><b aria-hidden>− </b>{reason.limiting}</p> : null}
    </div>
  );
}

function Expansion({ p, mode }) {
  const e = p.expansion;
  return (
    <div className="expInner">
      {e.positive && e.positive.length ? (
        <div className="expBlock">
          <h4 className="expH pos">מה עובד לטובת המוצר?</h4>
          <ul>{e.positive.map((l) => <li key={l}>{l}</li>)}</ul>
        </div>
      ) : null}
      {e.limiting && e.limiting.length ? (
        <div className="expBlock">
          <h4 className="expH">מה מגביל את הציון?</h4>
          <ul>{e.limiting.map((l) => <li key={l}>{l}</li>)}</ul>
        </div>
      ) : null}
      {e.bottom ? <p className="bottom"><b>בשורה התחתונה: </b>{e.bottom}</p> : null}
      {/* v2 §7: technical details inline — one disclosure, not a second toggle. */}
      <div className="tech">
        {e.ingredients ? <p><span className="techK">רכיבים</span>{e.ingredients}</p> : <p className="techMuted">רשימת רכיבים מלאה לא אומתה במקור.</p>}
        <p className="techNote">{e.serving}</p>
      </div>
      {/* v1 kept confidence in a 10px footnote here; v2 promotes it to the row. */}
      {mode === "v1" ? <p className="confFootnote">{CONF[p.confidence].label}</p> : null}
    </div>
  );
}

// THE single responsive row. Phone vs desktop is pure CSS (container queries) —
// the DOM is identical. `mode` toggles v1 (insightLine, buried confidence) vs v2.
function ComparisonRow({ p, rank, open, onToggle, mode, registerRow }) {
  const v2 = mode === "v2";
  return (
    <article className="row" data-band={window.bandOf(p.score).id} ref={(el) => registerRow(p.id, el)}>
      <button className="rowHead" aria-expanded={open} onClick={() => onToggle(p.id)}>
        <span className="rank bari-mono">{rank}</span>
        <span className="thumb" style={{ backgroundImage: `url(${p.img})` }} aria-hidden></span>
        <span className="nameCol">
          <span className="pname">{p.name}</span>
          {v2 ? <RowReason reason={p.rowReason} /> : <span className="insight">בקצרה: {p.insightLine}</span>}
        </span>
        {v2 ? <MetricColumn metrics={p.metrics} /> : <span className="metricColSpacer" aria-hidden></span>}
        <span className="gradeCol">
          <GradeBadge score={p.score} grade={p.grade} />
          {v2 ? <ConfidenceTag confidence={p.confidence} /> : null}
          <svg className={`chev ${open ? "open" : ""}`} viewBox="0 0 16 16" width="15" height="15" aria-hidden><path d="M4 6l4 4 4-4" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/></svg>
        </span>
      </button>
      <div className={`exp ${open ? "open" : ""}`}>
        <div className="expClip"><Expansion p={p} mode={mode} /></div>
      </div>
    </article>
  );
}

// Score-band jump rail (v2 §3) — sticky side affordance, click = scroll only.
function BandRail({ products, onJump }) {
  const total = products.length;
  return (
    <aside className="rail" aria-label="ניווט לפי טווח ציון">
      <p className="railTitle">טווחי ציון</p>
      {window.SCORE_BANDS.map((b) => {
        const items = products.filter((p) => p.score >= b.min && p.score <= b.max);
        if (!items.length) return null;
        return (
          <button key={b.id} className="railBand" onClick={() => onJump(items[0].id)}>
            <span className="railRow">
              <span className="railLabel">{b.label}</span>
              <span className="railCount bari-mono">{items.length}</span>
            </span>
            <span className="railBar"><i style={{ width: `${(items.length / total) * 100}%`, background: b.tone }}></i></span>
          </button>
        );
      })}
    </aside>
  );
}

function ComparisonTable({ products, mode }) {
  const [open, setOpen] = useState(() => new Set([products[0]?.id]));
  const scrollRef = useRef(null);
  const rowRefs = useRef({});
  const registerRow = useCallback((id, el) => { if (el) rowRefs.current[id] = el; }, []);
  const onToggle = useCallback((id) => {
    setOpen((cur) => { const n = new Set(cur); n.has(id) ? n.delete(id) : n.add(id); return n; });
  }, []);
  // Rail jump: scroll the list container only (never scrollIntoView — §7 anti-yank).
  const onJump = useCallback((id) => {
    const el = rowRefs.current[id], scroll = scrollRef.current;
    if (!el || !scroll) return;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    scroll.scrollTo({ top: el.offsetTop - 8, behavior: reduce ? "auto" : "smooth" });
  }, []);

  let lastBand = null;
  return (
    <div className="workspace">
      <div className={`listScroll ${mode === "v1" ? "list-v1" : "list-v2"}`} ref={scrollRef}>
        {mode === "v2" ? (
          <div className="colHead" aria-hidden>
            <span className="rank">#</span><span></span>
            <span>מוצר ותובנה</span><span className="chMetric">חלבון · תוספים · % גרגר</span>
            <span className="chGrade">ציון · {products.length}</span>
          </div>
        ) : null}
        {products.map((p, i) => {
          const band = window.bandOf(p.score);
          const showDivider = mode === "v2" && band.id !== lastBand;
          lastBand = band.id;
          return (
            <React.Fragment key={p.id}>
              {showDivider ? (
                <div className="bandDivider"><span className="bdLine"></span><span className="bdLabel" style={{ color: band.tone }}>{band.label}</span><span className="bdLine"></span></div>
              ) : null}
              <ComparisonRow p={p} rank={i + 1} open={open.has(p.id)} onToggle={onToggle} mode={mode} registerRow={registerRow} />
            </React.Fragment>
          );
        })}
      </div>
      {mode === "v2" ? <BandRail products={products} onJump={onJump} /> : null}
    </div>
  );
}

Object.assign(window, { ComparisonTable });
