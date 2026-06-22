"use client";

import { useState, type ReactNode } from "react";

import { GLASSBOX_D5D6_ON } from "@/lib/feature-flags";
import { cn } from "@/lib/utils";
import type {
  AdditiveEntry,
  BariConfidence,
  BariExpansionVM,
  BariGlassBoxVM,
  BariNutritionVM,
  BariProcessingSignalVM,
  BariProductVM,
} from "@/lib/view-models";
import {
  GLASS_BOX_DISCLOSURE_HEADING,
  resolveDisclosureLines,
  resolveWithholdReason,
} from "@/lib/view-models";
import { NewAdditivePanel } from "@/components/shared/AdditivePanel";
import { ProcessingSignalNote } from "@/components/shared/processing-signal-note";
import { DeepDiveSection, hasDeepDiveContent } from "@/components/shared/deep-dive-section";

// ─── Label constants (verbatim — spec §1, non-negotiable) ─────────────────────
const LABEL_POSITIVE = "מה עובד לטובת המוצר?";
const LABEL_LIMITING = "מה מגביל את הציון?";
const LABEL_COMPARISON = "הקשר במדף";
const LABEL_NUTRITION = "ערכים תזונתיים";
const LABEL_ADDITIVES = "תוספי מזון";
// Legacy / glass-box labels kept for those paths
const LABEL_UNKNOWNS = "מה שלא ניתן לאמת";
const LABEL_CAVEATS = "הערות";
const LABEL_DISCLOSURE = GLASS_BOX_DISCLOSURE_HEADING;

// ─── Confidence labels ────────────────────────────────────────────────────────
const CONFIDENCE_LABELS: Record<BariConfidence, string> = {
  verified: "נתונים מלאים",
  partial: "נתונים חלקיים",
  insufficient: "נתונים חסרים",
};

// Confidence dot/ring colors (spec §3.6, polish R-12)
const CONF_COLORS: Record<BariConfidence, string> = {
  verified: "var(--bari-green)",
  partial: "#B5882F",
  insufficient: "#B5BBB6",
};

// ─── Normalise limitingFactors ────────────────────────────────────────────────
// The VM accepts either legacy string[] or new { text, magnitude }[].
// This helper normalises to { text, magnitude }[] for the renderer.
type LimitingFactor = { text: string; magnitude: number };

function normaliseLimits(
  raw: string[] | { text: string; magnitude: number }[] | undefined
): LimitingFactor[] {
  if (!raw || raw.length === 0) return [];
  if (typeof raw[0] === "string") {
    return (raw as string[]).map((s) => ({ text: s, magnitude: 0 }));
  }
  return raw as { text: string; magnitude: number }[];
}

// ─── Category-scoped nutrition scales (spec §3.4) ─────────────────────────────
// "Set per category — do not reuse dairy scales for hummus."
// Format: { max, goodAbove?, goodBelow?, warnAbove?, warnBelow? }
interface NutrientScale {
  max: number;
  goodAbove?: number;  // protein: ≥5 → green
  warnBelow?: number;  // protein: <3 → amber
  goodBelow?: number;  // sugar: ≤1 → green
  warnAbove?: number;  // sugar: ≥6 → amber
}

interface CategoryNutritionConfig {
  energyKcal: NutrientScale;
  protein: NutrientScale;
  sugar: NutrientScale;
  sodium: NutrientScale;
  servingLabel: string;
}

const CATEGORY_NUTRITION: Record<string, CategoryNutritionConfig> = {
  // Dairy / milk (spec §3.4 dairy shown as example)
  milk: {
    energyKcal: { max: 80 },
    protein: { max: 8, goodAbove: 5, warnBelow: 3 },
    sugar: { max: 8, goodBelow: 1, warnAbove: 6 },
    sodium: { max: 80 },
    servingLabel: "ל-100 מ״ל",
  },
  // Hummus: protein runs 0–22 (spec §3.4 example)
  hummus: {
    energyKcal: { max: 350 },
    protein: { max: 22, goodAbove: 10, warnBelow: 4 },
    sugar: { max: 5, goodBelow: 1, warnAbove: 4 },
    sodium: { max: 600 },
    servingLabel: "ל-100 גרם",
  },
  // Bread
  bread: {
    energyKcal: { max: 350 },
    protein: { max: 16, goodAbove: 8, warnBelow: 3 },
    sugar: { max: 10, goodBelow: 1, warnAbove: 6 },
    sodium: { max: 600 },
    servingLabel: "ל-100 גרם",
  },
  // Cereals / granola
  cereals: {
    energyKcal: { max: 450 },
    protein: { max: 20, goodAbove: 10, warnBelow: 5 },
    sugar: { max: 30, goodBelow: 5, warnAbove: 20 },
    sodium: { max: 400 },
    servingLabel: "ל-100 גרם",
  },
  granola: {
    energyKcal: { max: 480 },
    protein: { max: 20, goodAbove: 10, warnBelow: 5 },
    sugar: { max: 35, goodBelow: 5, warnAbove: 22 },
    sodium: { max: 400 },
    servingLabel: "ל-100 גרם",
  },
  // Snacks
  snacks: {
    energyKcal: { max: 600 },
    protein: { max: 20, goodAbove: 8, warnBelow: 3 },
    sugar: { max: 30, goodBelow: 3, warnAbove: 15 },
    sodium: { max: 800 },
    servingLabel: "ל-100 גרם",
  },
  // Cheese
  cheese: {
    energyKcal: { max: 400 },
    protein: { max: 30, goodAbove: 20, warnBelow: 8 },
    sugar: { max: 5, goodBelow: 1, warnAbove: 3 },
    sodium: { max: 800 },
    servingLabel: "ל-100 גרם",
  },
  "hard-cheeses": {
    energyKcal: { max: 420 },
    protein: { max: 32, goodAbove: 22, warnBelow: 10 },
    sugar: { max: 3, goodBelow: 0.5, warnAbove: 2 },
    sodium: { max: 900 },
    servingLabel: "ל-100 גרם",
  },
  "brined-cheeses": {
    energyKcal: { max: 350 },
    protein: { max: 25, goodAbove: 16, warnBelow: 8 },
    sugar: { max: 3, goodBelow: 0.5, warnAbove: 2 },
    sodium: { max: 1000 },
    servingLabel: "ל-100 גרם",
  },
  // Juices
  juices: {
    energyKcal: { max: 80 },
    protein: { max: 2 },
    sugar: { max: 15, goodBelow: 5, warnAbove: 10 },
    sodium: { max: 50 },
    servingLabel: "ל-100 מ״ל",
  },
  // Protein bars (TASK-365): high-protein shelf (23–36g/100g), sugar 1.7–35g/100g.
  // Scales tuned to the real corpus range so bars differentiate within the shelf.
  "protein-bars": {
    energyKcal: { max: 520 },
    protein: { max: 40, goodAbove: 28, warnBelow: 25 },
    sugar: { max: 40, goodBelow: 4, warnAbove: 15 },
    sodium: { max: 600 },
    servingLabel: "ל-100 גרם",
  },
  // Cookies
  "cookies-coffee": {
    energyKcal: { max: 550 },
    protein: { max: 15, goodAbove: 7, warnBelow: 3 },
    sugar: { max: 40, goodBelow: 5, warnAbove: 25 },
    sodium: { max: 600 },
    servingLabel: "ל-100 גרם",
  },
  cakes: {
    energyKcal: { max: 550 },
    protein: { max: 10, goodAbove: 5, warnBelow: 2 },
    sugar: { max: 45, goodBelow: 8, warnAbove: 28 },
    sodium: { max: 500 },
    servingLabel: "ל-100 גרם",
  },
};

// Default scales (fallback when category not in map)
const DEFAULT_NUTRITION: CategoryNutritionConfig = {
  energyKcal: { max: 400 },
  protein: { max: 20, goodAbove: 8, warnBelow: 3 },
  sugar: { max: 20, goodBelow: 3, warnAbove: 12 },
  sodium: { max: 600 },
  servingLabel: "ל-100 גרם",
};

const CATEGORY_NUTRITION_ALIASES: Record<string, string> = {
  "breakfast-cereals": "cereals",
};

function getCategoryNutrition(category?: string): CategoryNutritionConfig {
  if (!category) return DEFAULT_NUTRITION;
  const resolved = CATEGORY_NUTRITION_ALIASES[category] ?? category;
  return CATEGORY_NUTRITION[resolved] ?? DEFAULT_NUTRITION;
}

function getNutrientScale(
  config: CategoryNutritionConfig,
  key: keyof BariNutritionVM
): NutrientScale {
  switch (key) {
    case "energyKcal":
      return config.energyKcal;
    case "protein":
      return config.protein;
    case "sugar":
      return config.sugar;
    case "sodium":
      return config.sodium;
    default:
      return { max: 100 };
  }
}

// Bar fill tone for a nutrient value (spec §3.4)
// NOTE: use literal hex values for green, not var(--bari-green). The CSS custom property
// is defined only in colors_and_type.css (a reference file), not imported by the Next.js
// app. var(--bari-green) resolves to 'initial' at runtime → transparent fill → invisible bar.
// This matches the approach in confidence-marker.tsx which says "the project has no CSS
// custom properties for them" and inlines the hex directly. #1F8F6A = bari-green.
function nutrientTone(key: keyof BariNutritionVM, value: number, scale: NutrientScale): string {
  if (key === "protein") {
    if (scale.goodAbove !== undefined && value >= scale.goodAbove) return "#1F8F6A";
    if (scale.warnBelow !== undefined && value < scale.warnBelow) return "#C49A4A";
    return "#9AA09B";
  }
  if (key === "sugar") {
    if (scale.goodBelow !== undefined && value <= scale.goodBelow) return "#1F8F6A";
    if (scale.warnAbove !== undefined && value >= scale.warnAbove) return "#C49A4A";
    return "#9AA09B";
  }
  // energy and sodium stay neutral grey
  return "#9AA09B";
}

// ─── SVG glyphs (spec §3.1, polish R-09) ─────────────────────────────────────
// Shared box outline tokens — one weight/radius rhythm across all dropdown panels
// Single visible outline used on ALL dropdown boxes (owner: boxes must be consistent —
// either all outlined or none; the old --hairline-soft neutral read as borderless next
// to the green positive box). One clearly-visible neutral border everywhere.
const BOX_BORDER_NEUTRAL = "1px solid rgba(17,19,24,0.13)";
const BOX_BORDER_POSITIVE = "1px solid rgba(17,19,24,0.13)";
const BOX_RADIUS_PANEL = "var(--radius-xl)";
const BOX_RADIUS_CELL = "var(--radius-md)";
const BOX_PADDING_PANEL = "18px 16px";

// Typography roles (dropdown-only — reuse existing tokens, no new sizes)
const FONT_PANEL_TITLE = {
  fontFamily: "var(--font-heading)",
  fontWeight: 800,
  fontSize: "13px",
  letterSpacing: "-0.01em",
} as const;
const FONT_BODY = {
  fontSize: "13px",
  lineHeight: 1.5,
} as const;

// Plus: exact mirror of DashGlyph (same ring geometry/size/placement, transparent
// fill) with a green + in place of the dash. The earlier white-disc fill made it
// read as a plain filled dot, not a "+" paired with the "−" (owner issue #2).
function PlusGlyph() {
  return (
    <svg
      width="15"
      height="15"
      viewBox="0 0 16 16"
      aria-hidden
      className="shrink-0 mt-[1px]"
    >
      {/* literal hex (not CSS var()) — var() does not resolve as an SVG
          presentation attribute, which is why this glyph was invisible. Mirrors
          DashGlyph's grey ring/dash with the brand greens (#1F8F6A / #176F53). */}
      <circle
        cx="8"
        cy="8"
        r="7.2"
        fill="none"
        stroke="#1F8F6A"
        strokeWidth="1.5"
      />
      <path
        d="M8 5v6M5 8h6"
        fill="none"
        stroke="#176F53"
        strokeWidth="1.8"
        strokeLinecap="round"
      />
    </svg>
  );
}

// Check: green ring (opacity 0.7 per R-09) + checkmark in bari-green-deep
function CheckGlyph() {
  return (
    <svg
      width="15"
      height="15"
      viewBox="0 0 16 16"
      aria-hidden
      className="shrink-0 mt-[1px]"
    >
      <circle
        cx="8"
        cy="8"
        r="7.2"
        fill="none"
        stroke="#1F8F6A"
        strokeWidth="1.3"
        opacity="0.7"
      />
      <path
        d="M5 8.2l2 2 4-4.2"
        fill="none"
        stroke="#176F53"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

// Dash: neutral ring (strokeWidth 1.5 per R-09) + dash in fg3
function DashGlyph() {
  return (
    <svg
      width="15"
      height="15"
      viewBox="0 0 16 16"
      aria-hidden
      className="shrink-0 mt-[1px]"
    >
      <circle
        cx="8"
        cy="8"
        r="7.2"
        fill="none"
        stroke="#C2C7C0"
        strokeWidth="1.5"
      />
      <path
        d="M5 8h6"
        fill="none"
        stroke="#7A817C"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

// ─── Section header (spec §1: mono uppercase label + hairline rule) ───────────
function SectionHeader({ label, suffix }: { label: string; suffix?: string }) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: "10px",
        marginBottom: "12px",
      }}
    >
      <span
        style={{
          fontFamily: "var(--font-mono)",
          fontSize: "10.5px",
          fontWeight: 700,
          letterSpacing: "0.16em",
          textTransform: "uppercase",
          color: "var(--fg3)",
          whiteSpace: "nowrap",
        }}
      >
        {label}
        {suffix ? (
          <span
            style={{
              fontWeight: 500,
              letterSpacing: "0.06em",
              textTransform: "none",
              marginInlineStart: "6px",
            }}
          >
            · {suffix}
          </span>
        ) : null}
      </span>
      <span
        style={{
          flex: 1,
          height: "1px",
          background: "var(--hairline-faint)",
        }}
        aria-hidden
      />
    </div>
  );
}

// ─── Section wrapper (spec R-01: 24px top gap, 20px at <640px) ───────────────
function Section({
  label,
  suffix,
  children,
  first = false,
}: {
  label: string;
  suffix?: string;
  children: ReactNode;
  first?: boolean;
}) {
  return (
    <div
      style={{
        // R-01: 24px between sections (18px tightens to 20px on mobile via responsive)
        paddingTop: first ? "4px" : "24px",
      }}
      className={first ? undefined : "sm:pt-[24px] max-sm:pt-[20px]"}
    >
      <SectionHeader label={label} suffix={suffix} />
      {children}
    </div>
  );
}

// ─── §3.1 Assessment section ─────────────────────────────────────────────────

function AssessmentSection({
  positiveSignals,
  limitingFactors,
}: {
  positiveSignals: string[];
  limitingFactors: LimitingFactor[];
}) {
  const hasLimits = limitingFactors.length > 0;

  return (
    // wlGrid: 2-col → 1-col < 640px
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "14px",
      }}
      className="max-sm:!grid-cols-1"
    >
      {/* Positive panel */}
      <div
        style={{
          borderRadius: BOX_RADIUS_PANEL,
          padding: BOX_PADDING_PANEL,
          background: "#F1F8F4",
          border: BOX_BORDER_POSITIVE,
        }}
      >
        <p
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            margin: "0 0 11px",
            ...FONT_PANEL_TITLE,
            color: "var(--bari-green-deep)",
          }}
        >
          {LABEL_POSITIVE}
          {/* Count pill — R-05: ringed, near-transparent */}
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "10px",
              fontWeight: 700,
              padding: "2px 7px",
              borderRadius: "999px",
              letterSpacing: "0.02em",
              background: "rgba(31,143,106,0.10)",
              color: "var(--bari-green-deep)",
              border: "1px solid rgba(31,143,106,0.18)",
            }}
          >
            {positiveSignals.length}
          </span>
        </p>
        {positiveSignals.map((signal, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              gap: "9px",
              alignItems: "flex-start",
              // R-02: item row padding 9px
              padding: "9px 0",
              ...FONT_BODY,
              color: "var(--fg2)",
              borderTop: i === 0 ? undefined : "1px solid rgba(17,19,24,0.04)",
            }}
          >
            <PlusGlyph />
            <span>{signal}</span>
          </div>
        ))}
      </div>

      {/* Limits panel */}
      <div
        style={{
          borderRadius: BOX_RADIUS_PANEL,
          padding: BOX_PADDING_PANEL,
          background: "#FAFAF7",
          border: BOX_BORDER_NEUTRAL,
        }}
      >
        <p
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            margin: "0 0 11px",
            ...FONT_PANEL_TITLE,
            color: "var(--fg1)",
          }}
        >
          {LABEL_LIMITING}
          {/* Count pill only when > 0 (spec §3.1) — R-05: ringed neutral */}
          {hasLimits ? (
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "10px",
                fontWeight: 700,
                padding: "2px 7px",
                borderRadius: "999px",
                letterSpacing: "0.02em",
                background: "rgba(17,19,24,0.05)",
                color: "var(--fg2)",
                border: "1px solid var(--hairline)",
              }}
            >
              {limitingFactors.length}
            </span>
          ) : null}
        </p>

        {hasLimits ? (
          limitingFactors.map((lf, i) => (
            <div
              key={i}
              style={{
                display: "flex",
                gap: "9px",
                alignItems: "flex-start",
                // R-02: item row padding 9px
                padding: "9px 0",
                ...FONT_BODY,
                color: "var(--fg2)",
                borderTop: i === 0 ? undefined : "1px solid rgba(17,19,24,0.04)",
              }}
            >
              <DashGlyph />
              {/* Text only — the magnitude track was empty on every category
                  (string magnitudes fail the numeric fill test), so it read as a
                  stray underline that made the two columns' separators look
                  mismatched (owner issue #1). Removed for column symmetry. */}
              <span style={{ flex: 1, minWidth: 0 }}>{lf.text}</span>
            </div>
          ))
        ) : (
          /* Empty state: green check + text, no count pill */
          <div
            style={{
              display: "flex",
              gap: "8px",
              alignItems: "center",
              ...FONT_BODY,
              color: "var(--bari-green-deep)",
              padding: "9px 0",
            }}
          >
            <CheckGlyph />
            אין גורמים מגבילים מהותיים
          </div>
        )}
      </div>
    </div>
  );
}

// ─── §3.2 Shelf context ───────────────────────────────────────────────────────

function ShelfContextSection({
  rank,
  categoryTotal,
  comparisonContext,
}: {
  rank: number;
  categoryTotal: number;
  comparisonContext: string;
}) {
  // Position marker: best rank (1) sits at end (right in RTL).
  // inset-inline-start = 100% − (rank−1)/(categoryTotal−1) × 100%
  const markerPct =
    categoryTotal > 1
      ? 100 - ((rank - 1) / (categoryTotal - 1)) * 100
      : 50;

  return (
    <div
      style={{
        background: "#F6F7F4",
        border: BOX_BORDER_NEUTRAL,
        borderRadius: BOX_RADIUS_PANEL,
        padding: BOX_PADDING_PANEL,
      }}
    >
      {/* Top row: rank + category meta */}
      <div
        style={{
          display: "flex",
          alignItems: "baseline",
          justifyContent: "space-between",
          gap: "12px",
          flexWrap: "wrap",
        }}
      >
        <span
          style={{
            fontFamily: "var(--font-heading)",
            fontWeight: 800,
            fontSize: "15px",
            letterSpacing: "-0.02em",
            color: "var(--fg1)",
          }}
        >
          מדורג{" "}
          <strong style={{ color: "var(--bari-green-deep)" }}>{rank}</strong>
          {" "}מתוך {categoryTotal}
        </span>
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "10.5px",
            letterSpacing: "0.08em",
            color: "var(--fg3)",
          }}
        >
          לכל המדף
        </span>
      </div>

      {/* Position track: gradient (dimmed) + product marker (full opacity, on top).
          direction:ltr so the marker's physical `left` maps cleanly onto the
          90deg gradient (orange/worst at left → green/best at right); best rank
          lands on the green end. The marker must NOT inherit the gradient's
          opacity, so it's a sibling — not a child — of the dimmed bar. */}
      <div
        style={{
          position: "relative",
          height: "14px",
          margin: "14px 0 12px",
          direction: "ltr",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: 0,
            right: 0,
            transform: "translateY(-50%)",
            height: "6px",
            borderRadius: "4px",
            background:
              "linear-gradient(90deg, #C77F5A 0%, #C49A4A 35%, #9A9A5E 60%, #3FA07E 82%, #1F8F6A 100%)",
            opacity: 0.65,
          }}
          aria-hidden
        />
        <span
          style={{
            position: "absolute",
            top: "50%",
            left: `${markerPct}%`,
            width: "14px",
            height: "14px",
            borderRadius: "50%",
            background: "#FFFFFF",
            border: "3px solid var(--fg1)",
            transform: "translate(-50%, -50%)",
            boxShadow: "0 1px 3px rgba(0,0,0,0.28)",
            zIndex: 1,
          }}
          aria-hidden
        />
      </div>

      {/* Prose context */}
      <p
        style={{
          margin: 0,
          ...FONT_BODY,
          lineHeight: 1.6,
          color: "var(--fg2)",
        }}
      >
        {comparisonContext}
      </p>
    </div>
  );
}

// ─── §3.3 Nutrition + ingredients ────────────────────────────────────────────

const NUTRITION_KEYS: {
  key: keyof BariNutritionVM;
  label: string;
  unit: string;
}[] = [
  { key: "protein", label: "חלבון", unit: "ג׳" },
  { key: "sugar", label: "סוכר", unit: "ג׳" },
  { key: "energyKcal", label: "אנרגיה", unit: 'קק״ל' },
  { key: "sodium", label: "נתרן", unit: 'מ״ג' },
];

function NutritionSection({
  nutrition,
  ingredients,
  category,
}: {
  nutrition: BariNutritionVM;
  ingredients: string | null;
  category?: string;
}) {
  const catConfig = getCategoryNutrition(category);
  const displayedCells = NUTRITION_KEYS.filter(({ key }) => nutrition[key] != null);

  return (
    <div>
      {/* 4-up grid → 2-col < 640px (spec §3.4, §5) */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: "10px",
        }}
        className="max-sm:!grid-cols-2"
      >
        {displayedCells.map(({ key, label, unit }) => {
          const value = nutrition[key];
          if (value == null) return null;

          const scale = getNutrientScale(catConfig, key);
          const tone = nutrientTone(key, value as number, scale);
          const barPct = Math.max(3, Math.min(100, ((value as number) / scale.max) * 100));

          return (
            <div
              key={key}
              style={{
                background: "var(--surface)",
                border: BOX_BORDER_NEUTRAL,
                borderRadius: BOX_RADIUS_CELL,
                padding: "12px",
              }}
              aria-label={`${label} ${typeof value === "number" ? Math.round(value) : "—"} ${unit}`}
            >
              <div
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: "10px",
                  letterSpacing: "0.06em",
                  color: "var(--fg3)",
                }}
              >
                {label}
              </div>
              {/* R-04: numeral 21px, unit 12px */}
              <div
                style={{
                  fontFamily: "var(--font-heading)",
                  fontWeight: 800,
                  // R-04: 21px (up from 19px)
                  fontSize: "21px",
                  letterSpacing: "-0.03em",
                  fontVariantNumeric: "tabular-nums",
                  color: "var(--fg1)",
                  margin: "5px 0 9px",
                }}
              >
                {typeof value === "number" ? Math.round(value) : "—"}
                <i
                  style={{
                    fontStyle: "normal",
                    // R-04: 12px (up from 11px)
                    fontSize: "12px",
                    fontWeight: 600,
                    color: "var(--fg3)",
                    marginInlineStart: "2px",
                  }}
                >
                  {unit}
                </i>
              </div>
              {/* Mini-bar with scale anchors (0–max) */}
              <div aria-hidden>
                <div
                  style={{
                    height: "4px",
                    borderRadius: "3px",
                    background: "#EEEEE8",
                    overflow: "hidden",
                  }}
                >
                  <i
                    style={{
                      display: "block",
                      height: "100%",
                      borderRadius: "3px",
                      background: tone,
                      width: `${barPct}%`,
                    }}
                  />
                </div>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginTop: "4px",
                    fontFamily: "var(--font-mono)",
                    fontSize: "10px",
                    letterSpacing: "0.04em",
                    color: "var(--fg4)",
                    direction: "ltr",
                  }}
                >
                  <span>0</span>
                  <span>{scale.max}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Ingredients line */}
      <div style={{ marginTop: "12px", ...FONT_BODY, lineHeight: 1.6, color: "var(--fg2)" }}>
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "10px",
            letterSpacing: "0.06em",
            color: "var(--fg3)",
            textTransform: "uppercase",
            marginInlineEnd: "8px",
          }}
        >
          רכיבים
        </span>
        {ingredients ? (
          <IngredientText ingredients={ingredients} />
        ) : (
          <span style={{ color: "var(--fg3)", fontStyle: "normal" }}>
            רשימת רכיבים מלאה לא אומתה במקור.
          </span>
        )}
      </div>
    </div>
  );
}

function IngredientText({ ingredients }: { ingredients: string }) {
  const [expanded, setExpanded] = useState(false);

  if (expanded) {
    return <span>{ingredients}</span>;
  }

  // Truncate at 180 chars; prefer sentence break
  const MAX = 180;
  if (ingredients.length <= MAX) return <span>{ingredients}</span>;

  const preview = ingredients.slice(0, MAX).trimEnd() + "…";
  return (
    <>
      <span>{preview}</span>
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          setExpanded(true);
        }}
        style={{
          marginInlineStart: "6px",
          fontSize: "12px",
          fontWeight: 600,
          color: "var(--bari-green)",
          background: "transparent",
          border: "none",
          cursor: "pointer",
          padding: 0,
        }}
      >
        הצג הכל
      </button>
    </>
  );
}

// ─── §3.6 Confidence footer ───────────────────────────────────────────────────
// R-12: hollow ring for partial/insufficient, solid fill for verified.

function ConfDot({ confidence }: { confidence: BariConfidence }) {
  const color = CONF_COLORS[confidence];

  if (confidence === "verified") {
    // Solid 7px fill circle
    return (
      <span
        style={{
          display: "inline-block",
          width: "7px",
          height: "7px",
          borderRadius: "50%",
          background: color,
          flexShrink: 0,
        }}
        aria-hidden
      />
    );
  }

  // R-12: hollow 9px ring for partial/insufficient
  return (
    <span
      style={{
        display: "inline-block",
        width: "9px",
        height: "9px",
        borderRadius: "50%",
        background: "transparent",
        border: `1.5px solid ${color}`,
        flexShrink: 0,
      }}
      aria-hidden
    />
  );
}

function ExpansionFooter({
  confidence,
  confidenceText,
  confidenceTooltip,
  sourceLine,
  onCollapse,
  hide,
}: {
  confidence: BariConfidence;
  confidenceText: string;
  confidenceTooltip: string | null;
  sourceLine?: string | null;
  onCollapse: () => void;
  hide?: boolean;
}) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: "8px",
        marginTop: "16px",
        paddingTop: "13px",
        borderTop: "1px solid var(--hairline-faint)",
        flexWrap: "wrap",
      }}
    >
      {!hide ? (
        <span
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: "6px",
            fontFamily: "var(--font-mono)",
            fontSize: "10.5px",
            letterSpacing: "0.04em",
            color: "var(--fg3)",
          }}
        >
          <ConfDot confidence={confidence} />
          {confidenceText}
        </span>
      ) : null}
      {confidenceTooltip && !hide ? (
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "10px",
            color: "var(--fg4)",
            letterSpacing: "0.04em",
          }}
        >
          {confidenceTooltip}
        </span>
      ) : null}
      {sourceLine ? (
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "10px",
            letterSpacing: "0.06em",
            color: "var(--fg4)",
            marginInlineStart: "auto",
          }}
        >
          {sourceLine}
        </span>
      ) : null}
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          onCollapse();
        }}
        style={{
          marginInlineStart: sourceLine ? "0" : "auto",
          fontSize: "11px",
          color: "#666C67",
          background: "transparent",
          border: "none",
          cursor: "pointer",
          padding: 0,
          flexShrink: 0,
        }}
      >
        סגור
      </button>
    </div>
  );
}

// ─── Glass Box disclosure (legacy path, carried unchanged) ────────────────────
function NoteList({ lines }: { lines: string[] }) {
  return (
    <ul style={{ margin: "6px 0 0", padding: 0, listStyle: "none", display: "flex", flexDirection: "column", gap: "4px" }}>
      {lines.map((line) => (
        <li key={line} style={{ display: "flex", gap: "6px", fontSize: "12px", lineHeight: 1.5, color: "#5E6560" }}>
          <span style={{ flexShrink: 0, color: "#C5CAC6" }} aria-hidden>·</span>
          <span>{line}</span>
        </li>
      ))}
    </ul>
  );
}

function GlassBoxDisclosure({ glassBox }: { glassBox: BariGlassBoxVM }) {
  const notes = resolveDisclosureLines(glassBox);
  if (notes.length === 0) return null;
  return (
    <div style={{ paddingTop: "10px" }}>
      <p style={{ fontSize: "11px", fontWeight: "bold", color: "#4A524E", margin: "0 0 4px" }}>
        {LABEL_DISCLOSURE}
      </p>
      <NoteList lines={notes} />
    </div>
  );
}

// ─── Main ExpansionSection ────────────────────────────────────────────────────

export function ExpansionSection({
  expansion,
  confidence,
  confidenceLabelHe,
  confidenceTooltipHe,
  onCollapse,
  wide = false,
  confidencePromoted = false,
  glassBox,
  d4Additives,
  d3Processing,
  productId,
  category,
  rowVerdict,
  consumerExplanation,
  bestUseCases,
  consumerTakeaway,
  bariInterpretation,
  rank,
  categoryTotal,
}: {
  expansion: BariExpansionVM;
  confidence: BariConfidence;
  confidenceLabelHe?: string;
  confidenceTooltipHe?: string;
  onCollapse: () => void;
  wide?: boolean;
  confidencePromoted?: boolean;
  glassBox?: BariGlassBoxVM;
  d4Additives?: AdditiveEntry[];
  d3Processing?: BariProcessingSignalVM;
  productId?: string;
  category?: string;
  rowVerdict?: string;
  consumerExplanation?: NonNullable<BariExpansionVM["consumerExplanation"]> | null;
  bestUseCases?: string[];
  consumerTakeaway?: string;
  bariInterpretation?: NonNullable<BariProductVM["bariInterpretation"]>;
  /** TASK-346: rank within category corpus (for shelf-context positional track). */
  rank?: number;
  /** TASK-346: total products in category corpus (denominator for rank). */
  categoryTotal?: number;
}) {
  const isWithheld = glassBox?.gateState === "withhold";

  const confidenceText =
    confidenceLabelHe?.trim() ||
    CONFIDENCE_LABELS[confidence] ||
    expansion.confidenceLabel;
  const confidenceTooltip = confidenceTooltipHe?.trim() || null;

  const hasNutrition =
    expansion.nutrition != null &&
    Object.values(expansion.nutrition).some((v) => v != null);
  const hasIngredients = Boolean(expansion.ingredients?.trim());
  const showAdditivePanel = GLASSBOX_D5D6_ON && d4Additives !== undefined;
  const hasTechnical = hasNutrition || hasIngredients || showAdditivePanel;

  const deepDiveProps = {
    consumerExplanation: consumerExplanation ?? expansion.consumerExplanation ?? null,
    bestUseCases,
    consumerTakeaway,
    bariInterpretation,
  };
  const hasDeepDive = hasDeepDiveContent(deepDiveProps);

  // ── Withhold / insufficient path (unchanged logic, updated close button) ──
  if (confidence === "insufficient" || isWithheld) {
    const withheldReason = resolveWithholdReason(isWithheld ? glassBox : undefined);
    return (
      <div
        className={cn("px-4 pb-3", wide && "lg:px-0 lg:pb-2")}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ paddingTop: "2px" }}>
          <p style={{ fontSize: "12px", lineHeight: 1.6, color: "#6E756F" }}>{withheldReason}</p>
          <ExpansionFooter
            confidence={confidence}
            confidenceText={confidenceText}
            confidenceTooltip={confidenceTooltip}
            sourceLine={expansion.sourceLine}
            onCollapse={onCollapse}
            hide={confidencePromoted && !confidenceTooltip}
          />
        </div>
      </div>
    );
  }

  // ── Normalise VM data ───────────────────────────────────────────────────────
  const positiveSignals = expansion.positiveSignals ?? [];
  const limitingFactors = normaliseLimits(expansion.limitingFactors);
  const hasAssessment = positiveSignals.length > 0 || expansion.limitingFactors !== undefined;
  const hasShelfCtx =
    rank !== undefined &&
    categoryTotal !== undefined &&
    Boolean(expansion.comparisonContext?.trim());
  // Legacy unknowns/caveats (carried for backward compat but rendered after main 5 sections)
  const hasUnknowns = (expansion.unknowns?.length ?? 0) > 0;
  const hasCaveats = (expansion.caveats?.length ?? 0) > 0;

  // ── Full expansion body ─────────────────────────────────────────────────────
  return (
    <div
      className={cn("px-4 pb-3", wide && "lg:px-0 lg:pb-1")}
      onClick={(e) => e.stopPropagation()}
      dir="rtl"
    >
      {/* ── Section 1: Assessment (works / limits) ──────────────────────── */}
      {hasAssessment ? (
        <Section label="הערכת המוצר" first>
          <AssessmentSection
            positiveSignals={positiveSignals}
            limitingFactors={limitingFactors}
          />
        </Section>
      ) : rowVerdict?.trim() ? (
        <div style={{ paddingTop: "4px" }}>
          <p style={{ fontSize: "13px", lineHeight: 1.55, color: "#2F3531" }}>{rowVerdict}</p>
        </div>
      ) : null}

      {/* ── Section 2: Shelf context ─────────────────────────────────────── */}
      {hasShelfCtx ? (
        <Section label={LABEL_COMPARISON}>
          <ShelfContextSection
            rank={rank!}
            categoryTotal={categoryTotal!}
            comparisonContext={expansion.comparisonContext!}
          />
        </Section>
      ) : null}

      {/* ── Section 3: Nutrition + ingredients ───────────────────────────── */}
      {hasTechnical ? (
        <Section
          label={LABEL_NUTRITION}
          suffix={
            expansion.servingNote?.trim() ||
            getCategoryNutrition(category).servingLabel
          }
        >
          {hasNutrition && expansion.nutrition ? (
            <NutritionSection
              nutrition={expansion.nutrition}
              ingredients={expansion.ingredients ?? null}
              category={category}
            />
          ) : hasIngredients ? (
            <div style={{ ...FONT_BODY, lineHeight: 1.6, color: "var(--fg2)" }}>
              <span
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: "10px",
                  letterSpacing: "0.06em",
                  color: "var(--fg3)",
                  textTransform: "uppercase",
                  marginInlineEnd: "8px",
                }}
              >
                רכיבים
              </span>
              <IngredientText ingredients={expansion.ingredients!} />
            </div>
          ) : null}
        </Section>
      ) : null}

      {/* ── Section 4: Additives sub-dropdown ────────────────────────────── */}
      {showAdditivePanel ? (
        <Section label={LABEL_ADDITIVES}>
          <NewAdditivePanel
            additives={d4Additives ?? []}
            productId={productId}
            category={category}
          />
        </Section>
      ) : null}

      {/* ── Fallback: no content at all ──────────────────────────────────── */}
      {!hasAssessment &&
      !rowVerdict?.trim() &&
      !hasShelfCtx &&
      !hasTechnical &&
      !hasDeepDive &&
      glassBox?.gateState !== "demote" &&
      !d3Processing ? (
        <p style={{ paddingTop: "2px", fontSize: "12px", lineHeight: 1.6, color: "#6E756F" }}>
          פרטים נוספים לא זמינים לאריזה זו.
        </p>
      ) : null}

      {/* ── Glass Box demote disclosure ───────────────────────────────────── */}
      {glassBox?.gateState === "demote" ? (
        <GlassBoxDisclosure glassBox={glassBox} />
      ) : null}

      {/* ── D3 Processing signal ─────────────────────────────────────────── */}
      {d3Processing ? <ProcessingSignalNote signal={d3Processing} /> : null}

      {/* ── Deep-dive (TASK-332) ─────────────────────────────────────────── */}
      {hasDeepDive ? <DeepDiveSection {...deepDiveProps} /> : null}

      {/* ── Legacy unknowns / caveats (backward compat) ──────────────────── */}
      {hasUnknowns ? (
        <div style={{ paddingTop: "16px" }}>
          <p style={{ fontSize: "11px", fontWeight: "bold", color: "#4A524E", margin: "0 0 4px" }}>
            {LABEL_UNKNOWNS}
          </p>
          <NoteList lines={expansion.unknowns!} />
        </div>
      ) : null}
      {hasCaveats ? (
        <div style={{ paddingTop: "16px" }}>
          <p style={{ fontSize: "11px", fontWeight: "bold", color: "#4A524E", margin: "0 0 4px" }}>
            {LABEL_CAVEATS}
          </p>
          <NoteList lines={expansion.caveats!} />
        </div>
      ) : null}

      {/* ── Footer ───────────────────────────────────────────────────────── */}
      <ExpansionFooter
        confidence={confidence}
        confidenceText={confidenceText}
        confidenceTooltip={confidenceTooltip}
        sourceLine={expansion.sourceLine}
        onCollapse={onCollapse}
        hide={confidencePromoted && !confidenceTooltip}
      />
    </div>
  );
}
