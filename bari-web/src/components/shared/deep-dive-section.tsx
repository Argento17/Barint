"use client";

/**
 * DeepDiveSection — shared per-product deep-dive render (TASK-332).
 *
 * Renders up to four sections, each hidden when its data is absent/empty:
 *   1. consumerExplanation  — whyRated + good[] + watchOut[] + context + takeaway
 *   2. bestUseCases         — tag row of use-case labels
 *   3. consumerTakeaway     — single verdict sentence (displayed only when it differs
 *                             meaningfully from consumerExplanation.takeaway, i.e. the
 *                             field is present and non-empty)
 *   4. bariInterpretation   — pillar rows: label + strength + interpretation text
 *
 * Design constraints (TASK-332, canonical component rules):
 *   - Mobile-first: readable at 375px.
 *   - Inline only — no sheet, modal, or overlay.
 *   - No score encoding via colour (ScoreChip rule generalised here: no hue on pillar rows).
 *   - All strings rendered verbatim — no framework terms (BSIP, NOVA, cap, dimension …).
 *   - Token-sourced colours: #4A524E for labels, #5E6560 for body, #1F8F6A for accents.
 *   - Separator between this section and technical details is provided by the caller.
 */

import type { BariProductVM } from "@/lib/view-models";
import { cn } from "@/lib/utils";

// ─── Types re-used from the VM ────────────────────────────────────────────────

type ConsumerExplanation = NonNullable<
  NonNullable<BariProductVM["expansion"]>["consumerExplanation"]
>;
type BariInterpretationPillarV2 = {
  key: string;
  label: string;
  score: number;
  strength: string;
  interpretation: string;
};

/** Type guard — returns true only for the v2 canonical shape used by cheese and future categories. */
function isV2Pillar(
  p: NonNullable<BariProductVM["bariInterpretation"]>[number]
): p is BariInterpretationPillarV2 {
  return "key" in p && "label" in p && "strength" in p && "interpretation" in p;
}

// Expose the v2 type for internal use
type BariInterpretationPillar = BariInterpretationPillarV2;

// ─── Atomic primitives ────────────────────────────────────────────────────────

function SectionLabel({ children }: { children: string }) {
  return (
    <p className="text-[11px] font-bold leading-snug tracking-[0.01em] text-[#4A524E]">
      {children}
    </p>
  );
}

function BulletList({
  lines,
  tone = "neutral",
}: {
  lines: string[];
  tone?: "positive" | "caution" | "neutral";
}) {
  const textClass =
    tone === "positive"
      ? "text-[#4E5663]"
      : tone === "caution"
        ? "text-[#6E756F]"
        : "text-[#5E6560]";
  const dotClass =
    tone === "positive"
      ? "text-[#B5BBB6]"
      : tone === "caution"
        ? "text-[#C5CAC6]"
        : "text-[#C5CAC6]";

  return (
    <ul className="mt-1.5 space-y-1">
      {lines.map((line) => (
        <li key={line} className={cn("flex gap-1.5 text-[12px] leading-relaxed", textClass)}>
          <span className={cn("shrink-0", dotClass)} aria-hidden>
            ·
          </span>
          <span>{line}</span>
        </li>
      ))}
    </ul>
  );
}

// ─── ConsumerExplanation block ────────────────────────────────────────────────

function ConsumerExplanationBlock({
  explanation,
}: {
  explanation: ConsumerExplanation;
}) {
  const hasGood = (explanation.good?.length ?? 0) > 0;
  const hasWatchOut = (explanation.watchOut?.length ?? 0) > 0;
  const hasContext = explanation.context?.trim();
  const hasWhyRated = explanation.whyRated?.trim();

  return (
    <div className="space-y-2.5">
      {hasWhyRated ? (
        <div>
          <SectionLabel>מדוע קיבל את הציון?</SectionLabel>
          <p className="mt-1.5 text-[12px] leading-relaxed text-[#5E6560]">
            {explanation.whyRated}
          </p>
        </div>
      ) : null}

      {hasGood || hasWatchOut ? (
        <div
          className={cn(
            "grid grid-cols-1 gap-y-2.5",
            hasGood && hasWatchOut && "sm:grid-cols-2 sm:gap-x-8 sm:gap-y-0"
          )}
        >
          {hasGood ? (
            <div>
              <SectionLabel>מה עובד לטובת המוצר?</SectionLabel>
              <BulletList lines={explanation.good} tone="positive" />
            </div>
          ) : null}
          {hasWatchOut ? (
            <div>
              <SectionLabel>מה כדאי לדעת?</SectionLabel>
              <BulletList lines={explanation.watchOut} tone="caution" />
            </div>
          ) : null}
        </div>
      ) : null}

      {hasContext ? (
        <div>
          <SectionLabel>הקשר</SectionLabel>
          <p className="mt-1.5 text-[12px] leading-relaxed text-[#5E6560]">{explanation.context}</p>
        </div>
      ) : null}
    </div>
  );
}

// ─── BestUseCases tag row ──────────────────────────────────────────────────────

function BestUseCasesRow({ tags }: { tags: string[] }) {
  return (
    <div>
      <SectionLabel>מתאים במיוחד ל</SectionLabel>
      <div className="mt-1.5 flex flex-wrap gap-1.5" role="list">
        {tags.map((tag) => (
          <span
            key={tag}
            role="listitem"
            className="inline-flex items-center rounded-full border border-[rgba(17,19,24,0.10)] bg-[#F7F7F2] px-2.5 py-0.5 text-[11px] font-medium leading-none text-[#4A524E]"
          >
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── ConsumerTakeaway single verdict line ──────────────────────────────────────

function TakeawayLine({ text }: { text: string }) {
  return (
    <div>
      <SectionLabel>בשורה התחתונה</SectionLabel>
      <p className="mt-1.5 text-[13px] leading-[1.55] font-medium text-[#2F3531]">{text}</p>
    </div>
  );
}

// ─── BariInterpretation pillar rows ────────────────────────────────────────────

/**
 * Strength label → display label (Hebrew). Renders "חזק" / "בינוני" / "חלש" as a
 * tiny pill. No colour encoding (canonical ScoreChip rule applied here too).
 */
function StrengthPill({ strength }: { strength: string }) {
  return (
    <span className="inline-flex items-center rounded border border-[rgba(17,19,24,0.10)] bg-[#F7F7F2] px-1.5 py-0.5 text-[10px] font-medium leading-none text-[#7A817C]">
      {strength}
    </span>
  );
}

function PillarRow({ pillar }: { pillar: BariInterpretationPillar }) {
  return (
    <div className="flex items-start gap-2.5 border-t border-[rgba(17,19,24,0.05)] pt-2 first:border-t-0 first:pt-0">
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-bold leading-snug text-[#4A524E]">
            {pillar.label}
          </span>
          <StrengthPill strength={pillar.strength} />
        </div>
        {pillar.interpretation?.trim() ? (
          <p className="mt-0.5 text-[11px] leading-relaxed text-[#5E6560]">
            {pillar.interpretation}
          </p>
        ) : null}
      </div>
    </div>
  );
}

function PillarList({ pillars }: { pillars: NonNullable<BariProductVM["bariInterpretation"]> }) {
  // Only render v2 pillars — v1 legacy shape is silently skipped.
  const v2Pillars = pillars.filter(isV2Pillar);
  if (v2Pillars.length === 0) return null;
  return (
    <div>
      <SectionLabel>פירוט ממדים</SectionLabel>
      <div className="mt-1.5 space-y-0">
        {v2Pillars.map((pillar) => (
          <PillarRow key={pillar.key} pillar={pillar} />
        ))}
      </div>
    </div>
  );
}

// ─── Main export ──────────────────────────────────────────────────────────────

export interface DeepDiveSectionProps {
  /** consumerExplanation lives in product.expansion.consumerExplanation */
  consumerExplanation?: ConsumerExplanation | null;
  /** Product-level bestUseCases tags. Absent / empty → section hidden. */
  bestUseCases?: string[];
  /** One-sentence verdict. Absent / empty → section hidden. */
  consumerTakeaway?: string;
  /**
   * Pillar breakdown. Accepts either the v2 canonical shape ({ key, label, score, strength,
   * interpretation }) or the legacy v1 shape ({ dimension, score, label_he, explanation_he }).
   * Only v2 pillars are rendered — v1 shape products simply show no pillar section.
   */
  bariInterpretation?: NonNullable<BariProductVM["bariInterpretation"]>;
}

/**
 * Returns true if there is anything to render.
 * Callers can use this to decide whether to render a separator before the section.
 */
export function hasDeepDiveContent(props: DeepDiveSectionProps): boolean {
  const hasV2Pillars = (props.bariInterpretation ?? []).some(isV2Pillar);
  return Boolean(
    props.consumerExplanation?.whyRated?.trim() ||
      (props.consumerExplanation?.good?.length ?? 0) > 0 ||
      (props.consumerExplanation?.watchOut?.length ?? 0) > 0 ||
      props.consumerExplanation?.context?.trim() ||
      (props.bestUseCases?.length ?? 0) > 0 ||
      props.consumerTakeaway?.trim() ||
      hasV2Pillars
  );
}

export function DeepDiveSection({
  consumerExplanation,
  bestUseCases,
  consumerTakeaway,
  bariInterpretation,
}: DeepDiveSectionProps) {
  const hasExplanation = Boolean(
    consumerExplanation?.whyRated?.trim() ||
      (consumerExplanation?.good?.length ?? 0) > 0 ||
      (consumerExplanation?.watchOut?.length ?? 0) > 0 ||
      consumerExplanation?.context?.trim()
  );
  const hasBestUseCases = (bestUseCases?.length ?? 0) > 0;
  // Only show consumerTakeaway if it exists and differs from explanation takeaway
  // (to avoid duplication when both carry the same text)
  const takeawayText =
    consumerTakeaway?.trim() && consumerTakeaway.trim() !== consumerExplanation?.takeaway?.trim()
      ? consumerTakeaway.trim()
      : consumerExplanation?.takeaway?.trim() ?? "";
  const hasTakeaway = Boolean(takeawayText);
  const hasPillars = (bariInterpretation ?? []).some(isV2Pillar);

  if (!hasExplanation && !hasBestUseCases && !hasTakeaway && !hasPillars) return null;

  return (
    <div className="mt-3 space-y-3 border-t border-[rgba(17,19,24,0.06)] pt-2.5">
      {hasExplanation && consumerExplanation ? (
        <ConsumerExplanationBlock explanation={consumerExplanation} />
      ) : null}

      {hasBestUseCases && bestUseCases ? (
        <BestUseCasesRow tags={bestUseCases} />
      ) : null}

      {hasTakeaway ? <TakeawayLine text={takeawayText} /> : null}

      {hasPillars && bariInterpretation ? (
        <PillarList pillars={bariInterpretation} />
      ) : null}
    </div>
  );
}
