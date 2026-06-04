"use client";

import { useState, type ReactNode } from "react";

import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import { GLASSBOX_D5D6_ON } from "@/lib/feature-flags";
import { cn } from "@/lib/utils";
import type {
  AdditiveEntry,
  BariConfidence,
  BariExpansionVM,
  BariGlassBoxVM,
  BariNutritionVM,
} from "@/lib/view-models";
import {
  GLASS_BOX_DISCLOSURE_HEADING,
  resolveDisclosureLines,
  resolveWithholdReason,
} from "@/lib/view-models";
import { AdditivePanel } from "@/components/shared/AdditivePanel";

const NUTRIENT_LABELS: { key: keyof BariNutritionVM; label: string; unit: string }[] = [
  { key: "energyKcal", label: 'קק"ל', unit: "" },
  { key: "protein", label: "חלבון", unit: 'ג\'' },
  { key: "sugar", label: "סוכרים", unit: 'ג\'' },
  { key: "fat", label: "שומן", unit: 'ג\'' },
  { key: "satFat", label: "שומן רווי", unit: 'ג\'' },
  { key: "sodium", label: "נתרן", unit: 'מ"ג' },
];

const CONFIDENCE_LABELS: Record<BariConfidence, string> = {
  verified: "נתונים מלאים",
  partial: "נתונים חלקיים",
  insufficient: "נתונים חסרים",
};

const LABEL_POSITIVE = "מה עובד לטובת המוצר?";
const LABEL_LIMITING = "מה מגביל את הציון?";
const LABEL_UNKNOWNS = "מה שלא ניתן לאמת";
const LABEL_CAVEATS = "הערות";
const LABEL_BOTTOM = "בשורה התחתונה";
const LABEL_COMPARISON = "הקשר במדף";
// TASK-179N — Glass Box D5 disclosure section heading comes from the Content-owned copy
// map (GLASS_BOX_DISCLOSURE_HEADING = "מה לא צוין בתווית") so all glass-box strings live
// in one place. Calm, factual register (Q2): "what the label did not state", not an accusation.
const LABEL_DISCLOSURE = GLASS_BOX_DISCLOSURE_HEADING;

function SectionLabel({ children }: { children: string }) {
  return (
    <p className="text-[11px] font-bold leading-snug tracking-[0.01em] text-[#4A524E]">
      {children}
    </p>
  );
}

function InterpretiveSection({
  label,
  spaced,
  children,
}: {
  label: string;
  spaced?: boolean;
  children: ReactNode;
}) {
  return (
    <div className={spaced ? "pt-2.5" : undefined}>
      <SectionLabel>{label}</SectionLabel>
      {children}
    </div>
  );
}

function hasInterpretiveContent(expansion: BariExpansionVM): boolean {
  return Boolean(
    expansion.bottomLine?.trim() ||
      expansion.comparisonContext?.trim() ||
      (expansion.positiveSignals?.length ?? 0) > 0 ||
      (expansion.limitingFactors?.length ?? 0) > 0 ||
      (expansion.unknowns?.length ?? 0) > 0 ||
      (expansion.caveats?.length ?? 0) > 0
  );
}

function NoteList({ lines }: { lines: string[] }) {
  return (
    <ul className="mt-1.5 space-y-1">
      {lines.map((line) => (
        <li key={line} className="flex gap-1.5 text-[12px] leading-relaxed text-[#7A817C]">
          <span className="shrink-0 text-[#C5CAC6]" aria-hidden>
            ·
          </span>
          <span>{line}</span>
        </li>
      ))}
    </ul>
  );
}

function SignalList({ lines, tone }: { lines: string[]; tone: "positive" | "limiting" }) {
  const textClass =
    tone === "positive"
      ? "text-[12px] leading-relaxed text-[#4E5663]"
      : "text-[12px] leading-relaxed text-[#6E756F]";
  const dotClass =
    tone === "positive" ? "text-[#B5BBB6]" : "text-[#C5CAC6]";

  return (
    <ul className="mt-1.5 space-y-1">
      {lines.map((line) => (
        <li key={line} className={`flex gap-1.5 ${textClass}`}>
          <span className={`shrink-0 ${dotClass}`} aria-hidden>
            ·
          </span>
          <span>{line}</span>
        </li>
      ))}
    </ul>
  );
}

function InterpretiveExpansion({
  expansion,
  wide = false,
}: {
  expansion: BariExpansionVM;
  wide?: boolean;
}) {
  if (!hasInterpretiveContent(expansion)) return null;

  const { bottomLine, positiveSignals, limitingFactors, unknowns, caveats, comparisonContext } =
    expansion;

  const hasPositive = (positiveSignals?.length ?? 0) > 0;
  const hasLimiting = (limitingFactors?.length ?? 0) > 0;
  const hasUnknowns = (unknowns?.length ?? 0) > 0;
  const hasCaveats = (caveats?.length ?? 0) > 0;

  if (wide) {
    return (
      <div className="space-y-3 lg:space-y-2.5">
        {hasPositive || hasLimiting ? (
          <div
            className={cn(
              "grid grid-cols-1 gap-y-3",
              hasPositive && hasLimiting && "lg:grid-cols-2 lg:gap-x-12 lg:gap-y-0"
            )}
          >
            {hasPositive ? (
              <InterpretiveSection label={LABEL_POSITIVE}>
                <SignalList lines={positiveSignals!} tone="positive" />
              </InterpretiveSection>
            ) : null}
            {hasLimiting ? (
              <InterpretiveSection label={LABEL_LIMITING} spaced={hasPositive}>
                <SignalList lines={limitingFactors!} tone="limiting" />
              </InterpretiveSection>
            ) : null}
          </div>
        ) : null}

        {hasUnknowns ? (
          <InterpretiveSection label={LABEL_UNKNOWNS} spaced={hasPositive || hasLimiting}>
            <NoteList lines={unknowns!} />
          </InterpretiveSection>
        ) : null}

        {hasCaveats ? (
          <InterpretiveSection
            label={LABEL_CAVEATS}
            spaced={hasPositive || hasLimiting || hasUnknowns}
          >
            <NoteList lines={caveats!} />
          </InterpretiveSection>
        ) : null}

        {bottomLine?.trim() ? (
          <InterpretiveSection
            label={LABEL_BOTTOM}
            spaced={hasPositive || hasLimiting || hasUnknowns || hasCaveats}
          >
            <p className="mt-1.5 text-[13px] leading-[1.55] text-[#2F3531]">{bottomLine}</p>
          </InterpretiveSection>
        ) : null}

        {comparisonContext?.trim() ? (
          <InterpretiveSection label={LABEL_COMPARISON} spaced>
            <p className="mt-1.5 text-[12px] leading-relaxed text-[#7A817C]">
              {comparisonContext}
            </p>
          </InterpretiveSection>
        ) : null}
      </div>
    );
  }

  const sections: { label: string; body: ReactNode }[] = [];

  if (hasPositive) {
    sections.push({
      label: LABEL_POSITIVE,
      body: <SignalList lines={positiveSignals!} tone="positive" />,
    });
  }

  if (hasLimiting) {
    sections.push({
      label: LABEL_LIMITING,
      body: <SignalList lines={limitingFactors!} tone="limiting" />,
    });
  }

  if (hasUnknowns) {
    sections.push({
      label: LABEL_UNKNOWNS,
      body: <NoteList lines={unknowns!} />,
    });
  }

  if (hasCaveats) {
    sections.push({
      label: LABEL_CAVEATS,
      body: <NoteList lines={caveats!} />,
    });
  }

  if (bottomLine?.trim()) {
    sections.push({
      label: LABEL_BOTTOM,
      body: (
        <p className="mt-1.5 text-[13px] leading-[1.55] text-[#2F3531]">{bottomLine}</p>
      ),
    });
  }

  if (comparisonContext?.trim()) {
    sections.push({
      label: LABEL_COMPARISON,
      body: (
        <p className="mt-1.5 text-[12px] leading-relaxed text-[#7A817C]">
          {comparisonContext}
        </p>
      ),
    });
  }

  return (
    <div>
      {sections.map((section, index) => (
        <InterpretiveSection
          key={section.label}
          label={section.label}
          spaced={index > 0}
        >
          {section.body}
        </InterpretiveSection>
      ))}
    </div>
  );
}

function NutritionGrid({
  nutrition,
  servingNote,
}: {
  nutrition: BariNutritionVM;
  servingNote: string;
}) {
  const cells = NUTRIENT_LABELS.filter(({ key }) => nutrition[key] != null);

  if (cells.length === 0) return null;

  return (
    <div>
      {servingNote ? (
        <p
          className="mb-1.5 text-[10px] font-medium leading-none"
          style={{ color: BARI_COMPARISON_TOKENS.methodology.color }}
        >
          {servingNote}
        </p>
      ) : null}
      {/* Adjacent label+value pairs that wrap — readable at any width. (Replaces the
          old justify-between rows, which flung label and value to opposite edges in
          the wide unified table.) */}
      <div className="flex flex-wrap gap-x-6 gap-y-1.5">
        {cells.map(({ key, label, unit }) => {
          const value = nutrition[key];
          return (
            <div key={key} className="flex items-baseline gap-1.5">
              <span className="text-[10px] font-medium leading-none text-[#9A9FA6]">
                {label}
              </span>
              <span className="text-[12px] font-semibold tabular-nums leading-none text-[#6E756F]">
                {typeof value === "number" ? Math.round(value) : "—"}
                {unit && <span className="text-[9px] font-medium text-[#9A9FA6]"> {unit}</span>}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function IngredientList({ ingredients }: { ingredients: string }) {
  const [showAll, setShowAll] = useState(false);

  if (!ingredients) return null;

  return (
    <div>
      <p
        className="text-[11px] leading-relaxed text-[#7A817C]"
        style={
          showAll
            ? undefined
            : {
                display: "-webkit-box",
                WebkitLineClamp: 4,
                WebkitBoxOrient: "vertical",
                overflow: "hidden",
              }
        }
      >
        {ingredients}
      </p>
      {!showAll && (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            setShowAll(true);
          }}
          className="mt-1 text-[11px] font-semibold text-[#1F8F6A]"
        >
          הצג הכל
        </button>
      )}
    </div>
  );
}

function TechnicalDetails({
  expansion,
  d4Additives,
  productId,
  category,
}: {
  expansion: BariExpansionVM;
  /** TASK-179T: D4 additive entries (flag-gated; undefined when flag OFF or not a pilot category). */
  d4Additives?: AdditiveEntry[];
  /** Anonymous shelf position for analytics context. */
  productId?: string;
  /** Category slug for analytics context. */
  category?: string;
}) {
  const nutrition = expansion.nutrition;
  const hasNutrition =
    nutrition != null && Object.values(nutrition).some((v) => v != null);
  const hasIngredients = Boolean(expansion.ingredients?.trim());
  // The additive panel is always rendered for pilot categories when the flag is ON
  // (even for empty — the empty state is part of the engagement gate signal).
  const showAdditivePanel = GLASSBOX_D5D6_ON && d4Additives !== undefined;

  if (!hasNutrition && !hasIngredients && !showAdditivePanel) return null;

  return (
    <div className="mt-3 space-y-2 border-t border-[rgba(17,19,24,0.06)] pt-2.5">
      {/* TASK-179T: AdditivePanel renders BEFORE the nutrition table (spec §5.2). */}
      {showAdditivePanel ? (
        <AdditivePanel
          additives={d4Additives ?? []}
          productId={productId}
          category={category}
        />
      ) : null}
      {hasNutrition && nutrition ? (
        <NutritionGrid nutrition={nutrition} servingNote={expansion.servingNote} />
      ) : null}
      {hasIngredients && expansion.ingredients ? (
        <IngredientList ingredients={expansion.ingredients} />
      ) : null}
    </div>
  );
}

// TASK-179I — Glass Box D5 disclosure note inside the expansion. PLAIN-LANGUAGE ONLY
// (DEC-006 Q4): never a number, never an engine term. Calm register (Q2). Rendered only
// for a demoted product, flag-gated upstream (the prop is undefined when the flag is OFF).
function GlassBoxDisclosure({ glassBox }: { glassBox: BariGlassBoxVM }) {
  // Live JSON carries coded disclosureCodes; resolveDisclosureLines maps them to the
  // calm Hebrew lines (falling back to the preview dataset's authored prose). One place.
  const notes = resolveDisclosureLines(glassBox);
  if (notes.length === 0) return null;

  return (
    <div className="pt-2.5">
      <SectionLabel>{LABEL_DISCLOSURE}</SectionLabel>
      <NoteList lines={notes} />
    </div>
  );
}

export function ExpansionSection({
  expansion,
  confidence,
  onCollapse,
  wide = false,
  confidencePromoted = false,
  glassBox,
  d4Additives,
  productId,
  category,
}: {
  expansion: BariExpansionVM;
  confidence: BariConfidence;
  onCollapse: () => void;
  wide?: boolean;
  /**
   * v2 §5/§6 — when confidence is shown on the collapsed row, the expansion no
   * longer repeats it in the footnote (disclosure de-duplication). Maadanim-only.
   */
  confidencePromoted?: boolean;
  /**
   * TASK-179I — Glass Box D5/D6 presentation. Passed (flag-gated) only for a demoted
   * or withheld product; undefined → no glass-box surface. Drives the plain-language
   * disclosure note (demote) and the withhold reason (withhold). Presentation only.
   */
  glassBox?: BariGlassBoxVM;
  /**
   * TASK-179T — Glass Box W2 D4 additive entries. Passed (flag-gated) only when
   * GLASSBOX_D5D6_ON is true AND the category is a W2 pilot (hummus / maadanim).
   * Undefined → AdditivePanel not rendered. Empty array → panel renders empty state.
   * Presentation only — no score movement.
   */
  d4Additives?: AdditiveEntry[];
  /** Anonymous product shelf position ID for analytics context. */
  productId?: string;
  /** Category slug for analytics context. */
  category?: string;
}) {
  const isWithheld = glassBox?.gateState === "withhold";
  const confidenceText =
    CONFIDENCE_LABELS[confidence] ?? expansion.confidenceLabel;
  const interpretive = hasInterpretiveContent(expansion);
  const hasTechnical =
    (expansion.nutrition != null &&
      Object.values(expansion.nutrition).some((v) => v != null)) ||
    Boolean(expansion.ingredients?.trim()) ||
    // TASK-179T: additive panel counts as "technical" content (so the row never
    // shows the "no details available" fallback when the panel is the only content).
    (GLASSBOX_D5D6_ON && d4Additives !== undefined);

  // Render the "unscored" expansion for two cases:
  //  (a) a genuinely insufficient product (no glass box involved), and
  //  (b) a glass-box WITHHOLD — even when the underlying VM still carries a score/partial
  //      confidence (the D6 gate withholds the grade because the panel is absent). In the
  //      withhold case the graded interpretive/technical content is deliberately suppressed
  //      so the expansion matches the `לא נוקד` chip: a calm reason, no number.
  if (confidence === "insufficient" || isWithheld) {
    // Glass Box WITHHOLD: lead with the plain, calm reason the product is unscored
    // (DEC-006 Q4 — no number, no engine term). TASK-179N C1: the fallback is now the
    // single canonical reason (resolveWithholdReason → GLASS_BOX_WITHHOLD_REASON), so an
    // unscored row reads the SAME sentence whether the reason comes from data or fallback.
    const withheldReason = resolveWithholdReason(isWithheld ? glassBox : undefined);
    return (
      <div
        className={cn("px-4 pb-3", wide && "lg:px-0 lg:pb-2")}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="space-y-2 pt-0.5 lg:space-y-2">
          <p className="text-xs leading-relaxed text-[#6E756F]">{withheldReason}</p>
          <div className="flex items-center justify-between pt-0.5">
            {confidencePromoted ? (
              <span aria-hidden />
            ) : (
              <span
                className="text-[10px]"
                style={{ color: BARI_COMPARISON_TOKENS.methodology.color }}
              >
                {confidenceText}
              </span>
            )}
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onCollapse();
              }}
              className="text-[11px] text-[#AAAAAA]"
            >
              סגור
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={cn("px-4 pb-3", wide && "lg:px-0 lg:pb-1")}
      onClick={(e) => e.stopPropagation()}
    >
      <div className="space-y-0 pt-0.5">
        {interpretive ? (
          <InterpretiveExpansion expansion={expansion} wide={wide} />
        ) : null}

        {glassBox?.gateState === "demote" ? (
          <GlassBoxDisclosure glassBox={glassBox} />
        ) : null}

        {!interpretive && !hasTechnical && glassBox?.gateState !== "demote" ? (
          <p className="text-xs leading-relaxed text-[#6E756F]">
            פרטים נוספים לא זמינים לאריזה זו.
          </p>
        ) : null}

        {hasTechnical ? (
          <TechnicalDetails
            expansion={expansion}
            d4Additives={GLASSBOX_D5D6_ON ? d4Additives : undefined}
            productId={productId}
            category={category}
          />
        ) : null}

        <div className="flex items-center justify-between pt-2 lg:pt-1.5">
          <span
            className="text-[10px]"
            style={{ color: BARI_COMPARISON_TOKENS.methodology.color }}
          >
            {confidenceText}
          </span>
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onCollapse();
            }}
            className="text-[11px] text-[#AAAAAA]"
          >
            סגור
          </button>
        </div>
      </div>
    </div>
  );
}
