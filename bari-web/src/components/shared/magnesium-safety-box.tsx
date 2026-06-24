"use client";

// TASK-384A: Magnesium top safety box.
//
// Content sourced from: magnesium_clinical_content_spec_v2.md §3
//   §3.1 Kidney disease (כליות)
//   §3.2 Supplemental UL / GI tolerability — conditional framing (NOT "no toxicity")
//   §3.3 GI side effects (dose + form dependent)
//   §3.4.1 Antibiotics (quinolones + tetracyclines)
//   §3.4.2 Bisphosphonates
//   §3.4.3 PPIs
//   §3.4.4 Diuretics (loop/thiazide deplete; K-sparing retain)
//   §3.5 Standard disclaimer
//
// Mobile behaviour:
//   Always-visible = MINIMAL BANNER only (~1 line + icon):
//     "⚠ מינון מעל 350 מ״ג / בעיות כליות / תרופות — קרא פרטי בטיחות ▼"
//   Full content (all 2 primary lines, GI section, 4 drug-interaction classes, disclaimer)
//   behind toggle. Collapsed by default on mobile.
//   Target: first product row ≤350px from top at 390×812px (≥3 rows above fold).
// Desktop (md+): fuller always-visible layout (primary lines shown, secondary behind toggle).
//
// Content status: passed naturalness gate (0 HIGH) + red-team gate (TASK-384A). Go-live ready.
//
// UL framing: uses owner-approved conditional sentence:
//   "באנשים בריאים החשש העיקרי הוא אי-נוחות עיכולית;
//    באנשים עם מחלת כליות או שימוש בתרופות מסוימות נדרש ייעוץ רפואי."
//   NOT "no toxicity concern."
//
// HARD: NO absorbed-mg, NO fake-precision, NO framework terms in rendered JSX.

import { useState } from "react";
import { cn } from "@/lib/utils";

// ─── Safety line data ────────────────────────────────────────────────────────
// Sourced verbatim from magnesium_clinical_content_spec_v2.md §3 Hebrew content.
// Each entry: { icon, title, body }

interface SafetyLine {
  icon: string;
  title: string;
  body: string;
}

// Section A — always visible on DESKTOP (md+); on mobile, only minimal banner is shown
const SAFETY_LINES_PRIMARY: SafetyLine[] = [
  {
    icon: "⚠",
    title: "בעיות כליות",
    // §3.1
    body: "מגנזיום מופרש דרך הכליות. כשהכליות אינן פועלות בצורה מלאה, מגנזיום מתוסף עלול להצטבר בדם. אם אתם סובלים מבעיות כליות — התייעצו עם רופא לפני נטילת תוסף מגנזיום.",
  },
  {
    icon: "📊",
    title: "גבול עליון לתוספים",
    // §3.2 — conditional framing, owner-approved sentence
    body: 'IOM/NASEM קבעו שגבול של 350 מ"ג ביום מתוספים הוא הרמה שמעליה חלק מהאנשים עלולים לחוות שלשול או אי-נוחות עיכולית. באנשים בריאים החשש העיקרי הוא אי-נוחות עיכולית; באנשים עם מחלת כליות או שימוש בתרופות מסוימות נדרש ייעוץ רפואי. מגנזיום מהמזון לא נחשב לגבול הזה.',
  },
];

// Section B — expanded on mobile, always visible on desktop
const SAFETY_LINES_SECONDARY: SafetyLine[] = [
  {
    icon: "🤢",
    title: "תופעות עיכוליות",
    // §3.3
    body: "תוספי מגנזיום עלולים לגרום לאי-נוחות בבטן, בחילה או שלשול — בעיקר במינונים גבוהים ובצורות כמו אוקסיד, שנספגות פחות ומצטברות יותר במעיים. צורות עם ספיגה גבוהה יחסית (ציטראט, ביסגליצינט) נוחות בדרך כלל יותר לקיבה.",
  },
];

// Drug interaction section — also expanded on mobile
const DRUG_INTERACTIONS: SafetyLine[] = [
  {
    icon: "💊",
    title: "אנטיביוטיקה (קינולונים וטטרציקלינים)",
    // §3.4.1
    body: 'מגנזיום עלול להפחית את ספיגת האנטיביוטיקה. מומלץ להפריד בין הנטילות — 2 שעות לפני האנטיביוטיקה או 4–6 שעות אחריה. (NIH ODS, מרץ 2024)',
  },
  {
    icon: "💊",
    title: "תרופות לאוסטיאופורוזיס (ביספוספונטים)",
    // §3.4.2
    body: 'מגנזיום עלול להפחית את ספיגת התרופה. יש ליטול את התרופה לפחות שעתיים לפני תוסף המגנזיום. (NIH ODS, מרץ 2024)',
  },
  {
    icon: "💊",
    title: 'תרופות למניעת חומציות (PPI כגון אומפרזול)',
    // §3.4.3
    body: 'שימוש ממושך ב-PPI עלול להפחית ספיגת מגנזיום ולהוביל לרמות נמוכות בדם. ה-FDA דרש אזהרה על כך (2011). אם אתם נוטלים PPI לאורך זמן — התייעצו עם רופא. (FDA Drug Safety Communication 2011; NIH ODS 2024)',
  },
  {
    icon: "💊",
    title: "משתנים",
    // §3.4.4
    body: 'משתנים מסוג לופ (פורוסמיד/לסיקס) ותיאזיד מגבירים הפרשת מגנזיום בשתן — שימוש ממושך עלול לגרום לחסר. משתנים חוסכי-אשלגן (ספירונולקטון, אמילוריד) פועלים הפוך ומשמרים מגנזיום. אם אתם נוטלים משתנים — בדקו עם הרופא. (NIH ODS, מרץ 2024)',
  },
];

// Standard disclaimer — §3.5
const DISCLAIMER =
  "המידע הזה הוא לצורכי הכרה בלבד, ואינו ייעוץ רפואי. לפני תחילת נטילת כל תוסף, ובמיוחד אם אתם נוטלים תרופות קבועות, סובלים ממחלה כרונית, בהריון או מניקות — התייעצו עם רופא, פרמקולוג קליני, או דיאטן/ית קלינ/ית.";

// ─── Safety line row ──────────────────────────────────────────────────────────
function SafetyLineRow({ line }: { line: SafetyLine }) {
  return (
    <div
      style={{
        display: "flex",
        gap: "8px",
        alignItems: "flex-start",
        padding: "8px 0",
        borderTop: "1px solid rgba(17,19,24,0.06)",
      }}
    >
      <span
        style={{ fontSize: "14px", lineHeight: 1, marginTop: "1px", flexShrink: 0 }}
        aria-hidden
      >
        {line.icon}
      </span>
      <div>
        <p
          style={{
            margin: "0 0 2px",
            fontSize: "12px",
            fontWeight: 700,
            color: "#3C3A34",
            lineHeight: 1.3,
          }}
        >
          {line.title}
        </p>
        <p
          style={{
            margin: 0,
            fontSize: "12px",
            lineHeight: 1.55,
            color: "#6A6147",
          }}
        >
          {line.body}
        </p>
      </div>
    </div>
  );
}

// ─── Main component ───────────────────────────────────────────────────────────

export function MagnesiumSafetyBox() {
  const [expanded, setExpanded] = useState(false);

  return (
    <div
      className="rounded-[9px] border border-[#ECE3C8] bg-[#FBF8EE] text-[12px] leading-normal"
      // Mobile: tight horizontal padding only (py managed per section below).
      // Desktop: standard px-3 py-3 retained via md: override.
      style={{ padding: "0" }}
      dir="rtl"
    >
      {/* ── MOBILE minimal banner (visible on mobile, hidden on md+) ──────────
          Single compact line: shield icon + key caution text + toggle button.
          Taps once to reveal full safety detail.
          Owner-approved conditional UL framing; no "no toxicity" absolute.
          Target: ≤50px rendered height on mobile. */}
      <div
        className="md:hidden"
        style={{
          display: "flex",
          alignItems: "center",
          gap: "6px",
          padding: "8px 12px",
          flexWrap: "wrap",
        }}
      >
        <span style={{ fontSize: "13px", flexShrink: 0 }} aria-hidden>⚠</span>
        <span
          style={{
            fontSize: "11.5px",
            fontWeight: 600,
            color: "#6B5A1E",
            lineHeight: 1.4,
            flex: 1,
            minWidth: 0,
          }}
        >
          מינון מעל 350 מ&quot;ג / בעיות כליות / תרופות מסוימות — מידע בטיחות חשוב
        </span>
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          style={{
            background: "none",
            border: "none",
            padding: "0",
            fontSize: "11px",
            fontWeight: 700,
            color: "#1F8F6A",
            cursor: "pointer",
            flexShrink: 0,
            textDecoration: "underline",
          }}
          aria-expanded={expanded}
        >
          {expanded ? "סגור ▲" : "פרטי בטיחות נוספים ▼"}
        </button>
      </div>

      {/* ── DESKTOP header + primary lines (hidden on mobile, always shown md+) */}
      <div className="hidden md:block" style={{ padding: "12px 12px 0" }}>
        {/* Header */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "6px",
            marginBottom: "4px",
          }}
        >
          <span style={{ fontSize: "14px" }} aria-hidden>🛡</span>
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "10.5px",
              fontWeight: 700,
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              color: "#6B5A1E",
            }}
          >
            מידע בטיחות חשוב
          </span>
        </div>
        {SAFETY_LINES_PRIMARY.map((line) => (
          <SafetyLineRow key={line.title} line={line} />
        ))}
      </div>

      {/* ── Expandable section ────────────────────────────────────────────────
          Mobile:   visible only when expanded
          Desktop:  always shown */}
      <div
        className={cn(!expanded ? "hidden md:block" : undefined)}
        style={{ padding: "0 12px 12px" }}
      >
        {/* On mobile (expanded): show header + primary lines first */}
        <div className="md:hidden" style={{ paddingTop: "4px" }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              marginBottom: "4px",
            }}
          >
            <span style={{ fontSize: "14px" }} aria-hidden>🛡</span>
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "10.5px",
                fontWeight: 700,
                letterSpacing: "0.14em",
                textTransform: "uppercase",
                color: "#6B5A1E",
              }}
            >
              מידע בטיחות חשוב
            </span>
          </div>
          {SAFETY_LINES_PRIMARY.map((line) => (
            <SafetyLineRow key={`mob-${line.title}`} line={line} />
          ))}
        </div>

        {SAFETY_LINES_SECONDARY.map((line) => (
          <SafetyLineRow key={line.title} line={line} />
        ))}

        {/* Drug interactions sub-section */}
        <p
          style={{
            marginTop: "10px",
            marginBottom: "0",
            fontSize: "11px",
            fontWeight: 700,
            color: "#5C5035",
            fontFamily: "var(--font-mono)",
            letterSpacing: "0.08em",
            textTransform: "uppercase",
          }}
        >
          אינטרקציות עם תרופות
        </p>
        {DRUG_INTERACTIONS.map((line) => (
          <SafetyLineRow key={line.title} line={line} />
        ))}

        {/* Standard disclaimer */}
        <p
          style={{
            marginTop: "10px",
            marginBottom: 0,
            fontSize: "11px",
            lineHeight: 1.55,
            color: "#6A6147",
            borderTop: "1px solid rgba(17,19,24,0.06)",
            paddingTop: "8px",
          }}
        >
          {DISCLAIMER}
        </p>
      </div>
    </div>
  );
}
