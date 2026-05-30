"use client";

import { useState, type ReactNode } from "react";

import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";
import type { BariConfidence, BariExpansionVM, BariNutritionVM } from "@/lib/view-models";

const NUTRIENT_LABELS: { key: keyof BariNutritionVM; label: string; unit: string }[] = [
  { key: "energyKcal", label: 'קק"ל', unit: "" },
  { key: "protein", label: "חלבון", unit: 'ג\'' },
  { key: "sugar", label: "סוכרים", unit: 'ג\'' },
  { key: "fat", label: "שומן", unit: 'ג\'' },
  { key: "sodium", label: "נתרן", unit: 'מ"ג' },
];

const CONFIDENCE_LABELS: Record<BariConfidence, string> = {
  verified: "נתונים מלאים",
  partial: "נתונים חלקיים",
  insufficient: "נתונים חסרים",
};

const LABEL_POSITIVE = "מה עובד לטובת המוצר?";
const LABEL_LIMITING = "מה מגביל את הציון?";
const LABEL_BOTTOM = "בשורה התחתונה";
const LABEL_COMPARISON = "הקשר במדף";

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
      (expansion.limitingFactors?.length ?? 0) > 0
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

  const { bottomLine, positiveSignals, limitingFactors, comparisonContext } =
    expansion;

  const hasPositive = (positiveSignals?.length ?? 0) > 0;
  const hasLimiting = (limitingFactors?.length ?? 0) > 0;

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

        {bottomLine?.trim() ? (
          <InterpretiveSection
            label={LABEL_BOTTOM}
            spaced={hasPositive || hasLimiting}
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
      <div className="grid grid-cols-1 gap-y-1">
        {cells.map(({ key, label, unit }) => {
          const value = nutrition[key];
          return (
            <div key={key} className="flex items-baseline justify-between gap-3">
              <span className="text-[10px] font-medium leading-none text-[#9A9FA6]">
                {label}
              </span>
              <span className="text-[12px] font-semibold tabular-nums leading-none text-[#6E756F]">
                {typeof value === "number" ? Math.round(value) : "—"}
                {unit && (
                  <span className="text-[9px] font-medium text-[#9A9FA6]">
                    {" "}
                    {unit}
                  </span>
                )}
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

function TechnicalDetails({ expansion }: { expansion: BariExpansionVM }) {
  const nutrition = expansion.nutrition;
  const hasNutrition =
    nutrition != null && Object.values(nutrition).some((v) => v != null);
  const hasIngredients = Boolean(expansion.ingredients?.trim());

  if (!hasNutrition && !hasIngredients) return null;

  return (
    <div className="mt-3 space-y-2 border-t border-[rgba(17,19,24,0.06)] pt-2.5">
      {hasNutrition && nutrition ? (
        <NutritionGrid nutrition={nutrition} servingNote={expansion.servingNote} />
      ) : null}
      {hasIngredients && expansion.ingredients ? (
        <IngredientList ingredients={expansion.ingredients} />
      ) : null}
    </div>
  );
}

export function ExpansionSection({
  expansion,
  confidence,
  onCollapse,
  wide = false,
}: {
  expansion: BariExpansionVM;
  confidence: BariConfidence;
  onCollapse: () => void;
  wide?: boolean;
}) {
  const confidenceText =
    CONFIDENCE_LABELS[confidence] ?? expansion.confidenceLabel;
  const interpretive = hasInterpretiveContent(expansion);
  const hasTechnical =
    (expansion.nutrition != null &&
      Object.values(expansion.nutrition).some((v) => v != null)) ||
    Boolean(expansion.ingredients?.trim());

  if (confidence === "insufficient") {
    return (
      <div
        className={cn("px-4 pb-3", wide && "lg:px-0 lg:pb-2")}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="space-y-2 pt-0.5 lg:space-y-2">
          <p className="text-xs leading-relaxed text-[#6E756F]">
            אין מספיק נתונים לאריזה זו כדי להציג פירוט.
          </p>
          <div className="flex items-center justify-between pt-0.5">
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

  return (
    <div
      className={cn("px-4 pb-3", wide && "lg:px-0 lg:pb-1")}
      onClick={(e) => e.stopPropagation()}
    >
      <div className="space-y-0 pt-0.5">
        {interpretive ? (
          <InterpretiveExpansion expansion={expansion} wide={wide} />
        ) : null}

        {!interpretive && !hasTechnical ? (
          <p className="text-xs leading-relaxed text-[#6E756F]">
            פרטים נוספים לא זמינים לאריזה זו.
          </p>
        ) : null}

        {hasTechnical ? <TechnicalDetails expansion={expansion} /> : null}

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
