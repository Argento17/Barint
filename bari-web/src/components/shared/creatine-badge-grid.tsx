"use client";

// TASK-492C: Creatine badge grid — expansion-only panel.
// Mirrors magnesium-badge-grid.tsx structure (component_build_sequence_v1.md pattern reuse).
//
// Creatine has NO A–E grade and NO numeric score (Product ruling 1). The headline is the
// dose-honesty verdict (rowVerdict, on the collapsed row); this grid carries the supporting
// facts in the expansion: form, dose, dose-honesty, certification tier, price-per-3g.
//
// Layout: same 3-col (md+) / 2-col (mobile) card grid as the magnesium badge grid, 5 badges.
//
// Data source: CreatineBadgesVM fields from creatine-page-data.ts.
// Hard constraints honoured:
//   - NO A–E grade / no numeric score anywhere in this component
//   - cert_label always carries the two-tier distinction verbatim — never simplified to a checkmark
//   - price_per_3g_label renders "—" style fallback when not computable (never estimated)

import type { CreatineBadgesVM } from "@/lib/view-models";

const BADGE_TITLES = [
  "צורה כימית", // Badge 1
  "מינון קריאטין למנה", // Badge 2
  "שקיפות מינון", // Badge 3
  "בדיקת צד-שלישי", // Badge 4
  "מחיר לגרם אפקטיבי", // Badge 5
] as const;

function doseHonestyTone(tier: CreatineBadgesVM["doseHonesty"]): { color: string; dotFilled: boolean } {
  if (tier === "honest") return { color: "#1F8F6A", dotFilled: true };
  if (tier === "below_floor") return { color: "#B5882F", dotFilled: false };
  return { color: "#6E756D", dotFilled: false };
}

function CertPill({ tier, label }: { tier: CreatineBadgesVM["certTier"]; label: string }) {
  const isDirectoryVerified = tier === "directory_verified";
  return (
    <span
      data-testid="creatine-cert-pill"
      data-cert-tier={tier ?? "none"}
      style={{
        display: "inline-flex",
        alignItems: "center",
        padding: "3px 8px",
        borderRadius: "999px",
        fontSize: "11px",
        fontWeight: 600,
        lineHeight: 1.4,
        backgroundColor: isDirectoryVerified ? "#F0F4F1" : "#F3F4F2",
        border: `1px solid ${isDirectoryVerified ? "#C6D4CB" : "#D8DDD9"}`,
        color: isDirectoryVerified ? "#3A6B50" : "#4E5663",
      }}
    >
      {label}
    </span>
  );
}

function BadgeCard({ title, children }: { title: string; children: React.ReactNode }) {
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

export function CreatineBadgeGrid({ badges }: { badges: CreatineBadgesVM }) {
  const honestyTone = doseHonestyTone(badges.doseHonesty);

  return (
    <div dir="rtl">
      <div
        style={{
          display: "grid",
          gap: "8px",
          gridTemplateColumns: "repeat(3, 1fr)",
        }}
        className="max-sm:grid-cols-2!"
      >
        {/* Badge 1 — form */}
        <BadgeCard title={BADGE_TITLES[0]}>
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

        {/* Badge 2 — dose */}
        <BadgeCard title={BADGE_TITLES[1]}>
          <span
            style={{
              fontFamily: "var(--font-heading)",
              fontWeight: 800,
              fontSize: "17px",
              letterSpacing: "-0.02em",
              color: "var(--fg1, #111318)",
            }}
          >
            {badges.dose_label}
          </span>
        </BadgeCard>

        {/* Badge 3 — dose-honesty verdict */}
        <BadgeCard title={BADGE_TITLES[2]}>
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "5px",
              fontSize: "12px",
              fontWeight: 600,
              color: honestyTone.color,
            }}
          >
            <span
              style={{
                display: "inline-block",
                width: "7px",
                height: "7px",
                borderRadius: "50%",
                background: honestyTone.dotFilled ? honestyTone.color : "transparent",
                border: !honestyTone.dotFilled ? `1.5px solid ${honestyTone.color}` : undefined,
                flexShrink: 0,
              }}
              aria-hidden
            />
            {badges.dose_honesty_label}
          </span>
        </BadgeCard>

        {/* Badge 4 — cert tier */}
        <BadgeCard title={BADGE_TITLES[3]}>
          <CertPill tier={badges.certTier} label={badges.cert_label} />
        </BadgeCard>

        {/* Badge 5 — price per 3g */}
        <BadgeCard title={BADGE_TITLES[4]}>
          <span
            style={{
              fontSize: "13px",
              fontWeight: 700,
              color: badges.price_per_3g_label ? "var(--fg1, #111318)" : "#6E756D",
              lineHeight: 1.3,
            }}
          >
            {badges.price_per_3g_label ?? "לא ניתן לחישוב"}
          </span>
        </BadgeCard>
      </div>

      <p
        style={{
          marginTop: "10px",
          marginBottom: 0,
          fontSize: "11px",
          color: "#6E756D",
          lineHeight: 1.55,
        }}
      >
        אין ציון או דירוג אותיות לקריאטין. קריאטין מונוהידראט במינון הוגן עובד באותה מידה בין המותגים — הדירוג בעמוד זה נשען על שקיפות המינון והמחיר לגרם.
      </p>
    </div>
  );
}
