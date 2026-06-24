"use client";

// TASK-384A: Magnesium 6-badge grid — expansion-only panel.
//
// Layout decision (mobile geometry gate):
//   - The full 6-badge grid is rendered ONLY in the expansion panel.
//   - The collapsed row is NOT changed (insightLine already carries elemental mg +
//     BAV class — the 2 most decision-relevant facts — within 72px row height).
//   - This guarantees ≥3 product rows above the fold at 390px width.
//
// Geometry: 3-column grid on md+; 2-column on mobile (each badge ~card height ~72px).
//   At 390px: 2 cols × ~186px = fits. No horizontal overflow.
//   Badge card min-height ~68px on mobile → 3 rows of 2 = 204px for all 6 badges.
//
// Content status: passed naturalness gate (0 HIGH) + red-team gate (TASK-384A). Go-live ready.
//
// Data source: MagnesiumBadgesVM fields from magnesium-page-data.ts.
// Hard constraints honoured:
//   - NO absorbed-mg / "systemic" / fake-precision — only administered elemental mg
//   - NO BAV percentages — class label only (ספיגה גבוהה יחסית etc.)
//   - compound_transparency shown as a sub-line in context, never headline

import type { MagnesiumBadgesVM } from "@/lib/view-models";

// ─── Badge label map ────────────────────────────────────────────────────────
// Badge index → Hebrew title for the badge header
const BADGE_TITLES = [
  "מגנזיום יסודי למנה יומית",  // Badge 1
  "צורת מגנזיום",               // Badge 2
  "זמינות ביולוגית",             // Badge 3
  "התאמה למטרה",                // Badge 4
  "ביטחון תווית",                // Badge 5
  "דגלי בטיחות",                 // Badge 6
] as const;

// ─── Label confidence visual tier ────────────────────────────────────────────
// "מאומת" → green accent; "חלקי" → amber; "לא ניתן לחישוב" → muted
function confidenceTier(label: string): "verified" | "partial" | "unresolved" {
  if (label === "מאומת") return "verified";
  if (label === "חלקי") return "partial";
  return "unresolved";
}

// ─── Safety flag pill ─────────────────────────────────────────────────────────
// UL_EXCEED flags (מינון גבוה, שלשול) get a warm amber tint.
// Universal flags (כליות, תרופות) get a neutral tint.
function SafetyFlagPill({ flag }: { flag: string }) {
  const isHighDose = flag === "מינון גבוה" || flag === "שלשול";
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        padding: "2px 7px",
        borderRadius: "999px",
        fontSize: "11px",
        fontWeight: 600,
        lineHeight: 1.4,
        backgroundColor: isHighDose ? "#FBF8EE" : "#F3F4F2",
        border: `1px solid ${isHighDose ? "#ECE3C8" : "#D8DDD9"}`,
        color: isHighDose ? "#6B5A1E" : "#4E5663",
        whiteSpace: "nowrap",
      }}
    >
      {flag}
    </span>
  );
}

// ─── Single badge card ────────────────────────────────────────────────────────
function BadgeCard({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div
      style={{
        background: "#FAFAF7",
        border: "1px solid rgba(17,19,24,0.10)",
        borderRadius: "var(--radius-md, 8px)",
        padding: "10px 12px",
        display: "flex",
        flexDirection: "column",
        gap: "5px",
        minHeight: "64px",
      }}
    >
      <span
        style={{
          fontFamily: "var(--font-mono)",
          fontSize: "9.5px",
          fontWeight: 700,
          letterSpacing: "0.12em",
          textTransform: "uppercase",
          color: "#6E756D",
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
        }}
      >
        {title}
      </span>
      {children}
    </div>
  );
}

// ─── Main component ───────────────────────────────────────────────────────────

export function MagnesiumBadgeGrid({ badges }: { badges: MagnesiumBadgesVM }) {
  const confTier = confidenceTier(badges.label_confidence_label);
  const confColor =
    confTier === "verified"
      ? "#1F8F6A"
      : confTier === "partial"
      ? "#B5882F"
      : "#6E756D";

  return (
    <div dir="rtl">
      {/* 6-badge grid: 3 cols md+, 2 cols mobile */}
      <div
        style={{
          display: "grid",
          gap: "8px",
          gridTemplateColumns: "repeat(3, 1fr)",
        }}
        className="max-sm:grid-cols-2!"
      >
        {/* Badge 1 — elemental mg */}
        <BadgeCard title={BADGE_TITLES[0]}>
          <span
            style={{
              fontFamily: "var(--font-heading)",
              fontWeight: 800,
              fontSize: "17px",
              letterSpacing: "-0.02em",
              color: "var(--fg1, #111318)",
            }}
          >
            {badges.elemental_mg_label}
          </span>
        </BadgeCard>

        {/* Badge 2 — form */}
        <BadgeCard title={BADGE_TITLES[1]}>
          <span
            style={{
              fontSize: "13px",
              fontWeight: 600,
              color: "var(--fg1, #111318)",
              lineHeight: 1.3,
            }}
          >
            {badges.form_label}
          </span>
        </BadgeCard>

        {/* Badge 3 — bioavailability */}
        <BadgeCard title={BADGE_TITLES[2]}>
          <span
            style={{
              fontSize: "12px",
              fontWeight: 600,
              color: "var(--fg1, #111318)",
              lineHeight: 1.3,
            }}
          >
            {badges.bav_label}
          </span>
        </BadgeCard>

        {/* Badge 4 — suitability */}
        <BadgeCard title={BADGE_TITLES[3]}>
          <span
            style={{
              fontSize: "12px",
              fontWeight: 500,
              color: "var(--fg2, #3C443F)",
              lineHeight: 1.35,
            }}
          >
            {badges.suitability_label}
          </span>
        </BadgeCard>

        {/* Badge 5 — label confidence */}
        <BadgeCard title={BADGE_TITLES[4]}>
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "5px",
              fontSize: "12px",
              fontWeight: 600,
              color: confColor,
            }}
          >
            {/* Confidence dot — matches the confidence-marker.tsx palette */}
            <span
              style={{
                display: "inline-block",
                width: confTier === "verified" ? "7px" : "9px",
                height: confTier === "verified" ? "7px" : "9px",
                borderRadius: "50%",
                background:
                  confTier === "verified" ? confColor : "transparent",
                border:
                  confTier !== "verified"
                    ? `1.5px solid ${confColor}`
                    : undefined,
                flexShrink: 0,
              }}
              aria-hidden
            />
            {badges.label_confidence_label}
          </span>
        </BadgeCard>

        {/* Badge 6 — safety flags */}
        <BadgeCard title={BADGE_TITLES[5]}>
          {badges.safety_flags.length > 0 ? (
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "4px",
              }}
            >
              {badges.safety_flags.map((flag) => (
                <SafetyFlagPill key={flag} flag={flag} />
              ))}
            </div>
          ) : (
            <span
              style={{
                fontSize: "11px",
                color: "#6E756D",
                fontStyle: "normal",
              }}
            >
              לא ניתן להעריך
            </span>
          )}
        </BadgeCard>
      </div>

      {/* Compound mass transparency line — shown only when available */}
      {badges.compound_transparency ? (
        <p
          style={{
            marginTop: "8px",
            marginBottom: 0,
            fontSize: "11px",
            color: "#6E756D",
            lineHeight: 1.5,
            fontFamily: "var(--font-mono)",
            letterSpacing: "0.02em",
          }}
        >
          {badges.compound_transparency}
        </p>
      ) : null}

      {/* Consumer framing disclaimer (spec §2 template) */}
      <p
        style={{
          marginTop: "10px",
          marginBottom: 0,
          fontSize: "11px",
          color: "#6E756D",
          lineHeight: 1.55,
        }}
      >
        הסיכום מבוסס על ההרכב שכתוב על האריזה, ולא על בדיקה רפואית. לפני שימוש לכל מטרה ספציפית — התייעצו עם רופא.
      </p>
    </div>
  );
}
