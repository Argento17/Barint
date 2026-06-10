"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";

import { CategoryHero } from "@/components/shared/category-hero";
import { CategoryPrologue } from "@/components/shared/category-prologue";
import { MethodologyFooter } from "@/components/shared/methodology-footer";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";
import type {
  FrozenVegetablesBand,
  FrozenVegetablesNutrition,
  FrozenVegetablesProduct,
} from "@/lib/comparisons/frozen-vegetables-comparison-page-data";

// ---------------------------------------------------------------------------
// TASK-235 Phase 4 — SELF-CONTAINED, SCORE-FREE Frozen Vegetables v2 page.
//
// Deliberately does NOT use the shared ComparisonPage: that component force-renders
// the shared MethodologyFooter with a hardcoded "הציון מסכם…" note and a partial-badge
// disclosure that also says "הציון" — both are score-leaks on a score-free page and both
// are shared (editing them would change every other category). This composition reuses
// only the SAFE shared atoms (CategoryHero, CategoryPrologue, MethodologyFooter — fed
// frozen's OWN score-free lines) and renders its own band/row layout.
//
// No score chip, no grade, no A/B/C/D, no cross-band ranking, no "best".
// ---------------------------------------------------------------------------

export interface FrozenVegetablesComparisonPageProps {
  bands: readonly FrozenVegetablesBand[];
  products: readonly FrozenVegetablesProduct[];
  hero: { eyebrow: string; title: string };
  metadataLine: string;
  prologueSentences: readonly string[];
  categoryNote: string;
  methodologyLines: readonly string[];
  /** Score-free closing note — used INSTEAD of the shared "הציון מסכם…" string. */
  footerNote: string;
}

// Label nutrition rows, in display order. Only fields present on the label render;
// an absent field is undefined and is skipped entirely (never shown as 0 — Phase 4 rule).
const NUTRIENT_ROWS: {
  key: keyof FrozenVegetablesNutrition;
  label: string;
  unit: string;
}[] = [
  { key: "energyKcal", label: 'קק"ל', unit: "" },
  { key: "protein", label: "חלבון", unit: "ג'" },
  { key: "carbs", label: "פחמימות", unit: "ג'" },
  { key: "sugar", label: "סוכרים", unit: "ג'" },
  { key: "fiber", label: "סיבים", unit: "ג'" },
  { key: "fat", label: "שומן", unit: "ג'" },
  { key: "satFat", label: "שומן רווי", unit: "ג'" },
  { key: "sodium", label: "נתרן", unit: 'מ"ג' },
];

function StandingMarkerTag({ marker }: { marker: string }) {
  // Neutral TYPE tag (רכיב אחד / קטנייה / ארוחה / תיבול) — not a quality badge.
  // Achromatic, no color encoding.
  return (
    <span className="inline-flex items-center rounded-full border border-[rgba(17,19,24,0.10)] bg-[#F7F7F2] px-2 py-0.5 text-[0.62rem] font-bold leading-none text-[#5E6672]">
      {marker}
    </span>
  );
}

function ProductThumb({ product }: { product: FrozenVegetablesProduct }) {
  const [failed, setFailed] = useState(false);

  if (product.imageUrl && !failed) {
    return (
      <div className="relative h-full w-full shrink-0 overflow-hidden rounded-2xl border border-black/[0.06] bg-gradient-to-b from-[#FFFFFF] to-[#F7F7F2] shadow-sm">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={product.imageUrl}
          alt=""
          className="h-full w-full object-contain p-2"
          sizes="96px"
          loading="lazy"
          decoding="async"
          onError={() => setFailed(true)}
        />
      </div>
    );
  }

  return (
    <div
      className="relative h-full w-full shrink-0 overflow-hidden rounded-2xl border border-black/[0.06] bg-gradient-to-b from-[#111318] to-[#2D3138] shadow-sm"
      aria-hidden
    >
      <div className="flex h-full flex-col items-center justify-center px-1 text-center">
        <p className="text-[0.55rem] font-bold uppercase tracking-[0.08em] text-white/70">
          Bari
        </p>
        <p className="mt-0.5 line-clamp-2 text-[0.6rem] font-semibold leading-tight text-white">
          {product.name.split(" ").slice(0, 3).join(" ")}
        </p>
      </div>
    </div>
  );
}

function NutritionTable({ nutrition }: { nutrition: FrozenVegetablesNutrition }) {
  // Render ONLY the fields present on the label; never show 0 for an absent field.
  const rows = NUTRIENT_ROWS.filter(({ key }) => nutrition[key] != null);
  if (rows.length === 0) return null;

  return (
    <div className="pt-2.5">
      <p className="text-[11px] font-bold leading-snug tracking-[0.01em] text-[#4A524E]">
        ערכים לפי התווית (ל-100 גרם)
      </p>
      <dl className="mt-1.5 grid grid-cols-2 gap-x-4 gap-y-1 sm:grid-cols-4">
        {rows.map(({ key, label, unit }) => (
          <div key={key} className="flex items-baseline justify-between gap-1">
            <dt className="text-[11.5px] text-[#6E756F]">{label}</dt>
            <dd className="text-[11.5px] font-semibold tabular-nums text-[#2E3531]">
              {nutrition[key]}
              {unit ? ` ${unit}` : ""}
            </dd>
          </div>
        ))}
      </dl>
    </div>
  );
}

function FactList({ items }: { items: string[] }) {
  if (items.length === 0) return null;
  return (
    <ul className="mt-1.5 space-y-1">
      {items.map((line, i) => (
        <li
          key={`${i}-${line.slice(0, 16)}`}
          className="flex gap-1.5 text-[11.5px] leading-[1.5] text-[#3E444A]"
        >
          <span className="select-none text-[#1F8F6A]" aria-hidden>
            •
          </span>
          {/* USDA generic-reference strings are preserved EXACTLY as authored. */}
          <span>{line}</span>
        </li>
      ))}
    </ul>
  );
}

function FrozenExpansion({ product }: { product: FrozenVegetablesProduct }) {
  const { expansion } = product;
  return (
    <div className="px-4 pb-4 pt-1">
      {expansion.ingredients ? (
        <div className="pt-2.5">
          <p className="text-[11px] font-bold leading-snug tracking-[0.01em] text-[#4A524E]">
            רכיבים
          </p>
          <p className="mt-1 text-[11.5px] leading-[1.55] text-[#3E444A]">
            {expansion.ingredients}
          </p>
        </div>
      ) : null}

      <NutritionTable nutrition={expansion.nutrition} />

      {/* not_characterized → identity/composition only (positiveFacts already empty or a
          single composition line). No synthesized benefit/micronutrient claim is added. */}
      {expansion.positiveFacts.length > 0 ? (
        <div className="pt-2.5">
          <p className="text-[11px] font-bold leading-snug tracking-[0.01em] text-[#4A524E]">
            {expansion.notCharacterized ? "הרכב" : "מה המוצר מביא"}
          </p>
          <FactList items={expansion.positiveFacts} />
        </div>
      ) : null}

      {expansion.whatToKnow.length > 0 ? (
        <div className="pt-2.5">
          <p className="text-[11px] font-bold leading-snug tracking-[0.01em] text-[#4A524E]">
            {expansion.whatToKnowHeader}
          </p>
          <FactList items={expansion.whatToKnow} />
        </div>
      ) : null}

      {expansion.bottomLine ? (
        <div className="pt-2.5">
          <p className="text-[11px] font-bold leading-snug tracking-[0.01em] text-[#4A524E]">
            בשורה התחתונה
          </p>
          <p className="mt-1 text-[11.5px] leading-[1.55] text-[#3E444A]">
            {expansion.bottomLine}
          </p>
        </div>
      ) : null}
    </div>
  );
}

function FrozenRow({ product }: { product: FrozenVegetablesProduct }) {
  const [open, setOpen] = useState(false);

  return (
    <article className="bari-cmp-row">
      <button
        type="button"
        className="bari-cmp-rowhead"
        aria-expanded={open}
        aria-label={product.name}
        onClick={() => setOpen((v) => !v)}
        style={{ gridTemplateColumns: "auto 1fr auto", gridTemplateAreas: '"thumb name grade"' }}
      >
        <span className="bari-cmp-thumbcell">
          <ProductThumb product={product} />
        </span>
        <span className="bari-cmp-namecell">
          <span className="flex items-center gap-2">
            <span className="min-w-0 truncate text-[0.97rem] font-bold leading-[1.3] tracking-[-0.01em] text-[#111318]">
              {product.name}
            </span>
            <StandingMarkerTag marker={product.standingMarker} />
          </span>
          {/* Collapsed row = the 2-line human verdict. No score, no grade. */}
          <p className="mt-[5px] text-[0.8rem] leading-[1.45] text-[#3C443F]">
            {product.verdictLine1}
          </p>
          <p className="mt-[2px] text-[0.8rem] leading-[1.45] text-[#6E756F]">
            {product.verdictLine2}
          </p>
        </span>
        <span className="bari-cmp-gradecell">
          <ChevronDown
            strokeWidth={1.75}
            aria-hidden
            className={cn(
              "size-[15px] shrink-0 text-[#B5BBB6] transition-transform duration-200 motion-reduce:transition-none",
              open && "rotate-180 text-[#9A9FA6]"
            )}
          />
        </span>
      </button>

      <div className={cn("bari-cmp-exp", open && "is-open")} aria-hidden={!open}>
        <div className="bari-cmp-expclip">
          <div>{open ? <FrozenExpansion product={product} /> : null}</div>
        </div>
      </div>
    </article>
  );
}

function BandSection({
  band,
  products,
}: {
  band: FrozenVegetablesBand;
  products: readonly FrozenVegetablesProduct[];
}) {
  if (products.length === 0) return null;
  return (
    <section>
      <div className="bari-cmp-divider">
        <h2 className="bari-cmp-divider-label text-[#3E5A4C]">{band.title}</h2>
        <span className="bari-cmp-divider-line" aria-hidden />
        <StandingMarkerTag marker={band.standingMarker} />
      </div>
      <div className="bari-zebra-rows overflow-hidden">
        {products.map((product) => (
          <FrozenRow key={product.id} product={product} />
        ))}
      </div>
    </section>
  );
}

export function FrozenVegetablesComparisonPage({
  bands,
  products,
  hero,
  metadataLine,
  prologueSentences,
  categoryNote,
  methodologyLines,
  footerNote,
}: FrozenVegetablesComparisonPageProps) {
  return (
    <div className="min-h-screen bg-[#EFEFEB] sm:py-8 lg:py-10" dir="rtl">
      <div
        className={cn(
          "mx-auto w-full overflow-hidden bg-white",
          "max-w-[640px] sm:rounded-[1.5rem] sm:shadow-xl",
          "lg:max-w-[1180px] lg:rounded-[1.25rem] lg:shadow-[0_24px_70px_-44px_rgba(17,19,24,0.4)]"
        )}
      >
        <CategoryHero eyebrow={hero.eyebrow} title={hero.title} metadata={metadataLine} wide />
        <CategoryPrologue sentences={[...prologueSentences]} wide />

        {categoryNote ? (
          <div className={cn("px-4 pb-1", comparisonWebSectionPaddingClass())}>
            <p className="whitespace-pre-line rounded-[9px] border border-[#ECE3C8] bg-[#FBF8EE] px-3 py-2 text-[12px] leading-[1.5] text-[#6A6147]">
              {categoryNote}
            </p>
          </div>
        ) : null}

        <div className="mt-2">
          {bands.map((band) => (
            <BandSection
              key={band.id}
              band={band}
              // Within a band, products stay in file order — no cross-band ranking, no "best".
              products={products.filter((p) => p.band === band.id)}
            />
          ))}
        </div>

        {/* Score-free footer: frozen's OWN footerNote, NOT the shared "הציון מסכם…" note. */}
        <MethodologyFooter lines={[...methodologyLines, footerNote]} wide />
      </div>
    </div>
  );
}
