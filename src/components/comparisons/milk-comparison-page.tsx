"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { motion, useReducedMotion } from "framer-motion";
import { ChevronDown } from "lucide-react";

import { BariGradeBadge } from "@/components/comparisons/bari-grade-badge";
import { BariInterpretationPanel } from "@/components/comparisons/bari-interpretation-panel";
import { MilkCinematicHero } from "@/components/comparisons/milk-editorial/milk-cinematic-hero";
import { MilkComparisonBridge } from "@/components/comparisons/milk-editorial/milk-comparison-bridge";
import { MilkProductStrip } from "@/components/comparisons/milk-editorial/milk-product-strip";
import { ProductThumbnail } from "@/components/comparisons/product-thumbnail";
import { HomeContainer } from "@/components/home/section-frame";
import { Badge } from "@/components/ui/badge";
import {
  buildConsumerExplanationView,
  mapPillarsForDisplay,
} from "@/lib/comparisons/consumer-explanation-view";
import { getFlagshipProducts } from "@/lib/comparisons/milk-editorial-content";
import {
  comparisonFilters,
  countVisible,
  formatNutrient,
  getRowEmphasis,
  howToReadComparison,
  milkProducts,
  productMatchesFilters,
} from "@/lib/comparisons/milk-page-data";
import type { ComparisonFilterId, MilkComparisonProduct } from "@/lib/comparisons/milk-types";
import { cn } from "@/lib/utils";

function ProductShelfRow({
  product,
  emphasis,
  rank,
}: {
  product: MilkComparisonProduct;
  emphasis: "emphasized" | "muted" | "neutral";
  rank: number;
}) {
  const [expanded, setExpanded] = useState(false);
  const [advanced, setAdvanced] = useState(false);
  const reduceMotion = useReducedMotion();
  const muted = emphasis === "muted";
  const expView = useMemo(
    () => buildConsumerExplanationView(product, milkProducts),
    [product]
  );
  const pillarsDisplay = useMemo(
    () => mapPillarsForDisplay(product.bariInterpretation, product.score),
    [product]
  );
  const title = product.displayTitle ?? product.shortName;
  const subtitle = product.brandLine;

  return (
    <motion.article
      layout={!reduceMotion}
      animate={{ opacity: muted ? 0.38 : 1 }}
      transition={{ duration: 0.3 }}
      className={cn(
        "border-b border-black/[0.06] last:border-0",
        emphasis === "emphasized" && "bg-[#1F8F6A]/[0.035]"
      )}
    >
      <div className="flex flex-col gap-4 p-4 sm:flex-row sm:items-start sm:gap-5">
        <div className="flex min-w-0 flex-1 items-start gap-4">
          <span className="hidden w-6 shrink-0 pt-2 text-center text-xs font-bold tabular-nums text-[#7A817C] sm:block">
            {rank}
          </span>
          <ProductThumbnail product={product} size="lg" />
          <div className="min-w-0 flex-1 pt-0.5">
            <p className="text-base font-extrabold leading-snug text-[#111318] sm:text-lg">
              {title}
            </p>
            {subtitle ? (
              <p className="mt-0.5 text-xs font-medium text-[#7A817C]">{subtitle}</p>
            ) : null}
            <div className="mt-2.5">
              <Badge className="h-5 border-0 bg-[#F7F7F2] px-2.5 text-[0.65rem] font-semibold text-[#4E5663]">
                {product.productTypeLabel}
              </Badge>
            </div>
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-3 sm:flex-col sm:items-end sm:pt-1">
          <BariGradeBadge
            score={product.score}
            grade={product.grade}
            gradeLabel={product.grade_label}
            size="md"
          />
        </div>
      </div>

      <div className="grid gap-2 px-4 pb-3 sm:grid-cols-2 lg:grid-cols-4 lg:pl-14">
        <div className="rounded-lg bg-[#F7F7F2]/80 px-3 py-2.5">
          <p className="text-[0.62rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">חלבון / 100 מ״ל</p>
          <p className="mt-0.5 text-base font-extrabold tabular-nums text-[#111318]">
            {formatNutrient(product.proteinPer100ml)}
          </p>
        </div>
        <div className="rounded-lg bg-[#F7F7F2]/80 px-3 py-2.5">
          <p className="text-[0.62rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">סוכר / 100 מ״ל</p>
          <p className="mt-0.5 text-base font-extrabold tabular-nums text-[#111318]">
            {formatNutrient(product.sugarPer100ml)}
          </p>
        </div>
        <div className="rounded-lg bg-[#F7F7F2]/80 px-3 py-2.5">
          <p className="text-[0.62rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">תוספים</p>
          <p className="mt-0.5 text-xs font-medium leading-snug text-[#4E5663]">
            {product.additivesLabel}
          </p>
        </div>
        <div className="rounded-lg bg-[#F7F7F2]/80 px-3 py-2.5">
          <p className="text-[0.62rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">רכיב עיקרי</p>
          <p className="mt-0.5 text-xs font-medium leading-snug text-[#4E5663]">
            {product.mainIngredient}
          </p>
        </div>
      </div>

      <p className="px-4 pb-3 text-sm leading-relaxed text-[#4E5663] sm:pl-14">
        <span className="font-bold text-[#111318]">בקצרה: </span>
        {expView.takeawayLine}
      </p>

      <div className="space-y-2 px-4 pb-4 sm:pl-14">
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="flex w-full items-center justify-between rounded-lg border border-black/[0.08] bg-[#FFFFFF] px-3 py-2.5 text-sm font-semibold text-[#111318] hover:border-[#1F8F6A]/25"
          aria-expanded={expanded}
        >
          למה קיבל את הציון?
          <ChevronDown
            className={cn("size-4 text-[#7A817C] transition-transform", expanded && "rotate-180")}
          />
        </button>

        <motion.div
          initial={false}
          animate={{ height: expanded ? "auto" : 0, opacity: expanded ? 1 : 0 }}
          transition={{ duration: reduceMotion ? 0 : 0.28 }}
          className="overflow-hidden"
        >
          <div className="space-y-4 rounded-xl border border-black/[0.08] bg-[#FFFFFF]/90 p-4">
            <div>
              <h4 className="text-xs font-bold text-[#111318]">מה חשוב לדעת?</h4>
              <p className="mt-1.5 text-sm leading-relaxed text-[#4E5663]">{expView.whatToKnow}</p>
            </div>
            <div>
              <h4 className="text-xs font-bold text-[#1F8F6A]">מה מעלה את הציון?</h4>
              <ul className="mt-1.5 list-inside list-disc space-y-1 text-sm text-[#4E5663]">
                {expView.raisesScore.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-bold text-[#111318]">מה מוריד את הציון?</h4>
              <ul className="mt-1.5 list-inside list-disc space-y-1.5 text-sm leading-relaxed text-[#4E5663]">
                {expView.lowersScore.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-bold text-[#111318]">בהשוואה למוצרים דומים</h4>
              <p className="mt-1.5 text-sm leading-relaxed text-[#4E5663]">
                {expView.relativeToPeers}
              </p>
            </div>

            {expView.tradeoffNote ? (
              <p className="rounded-lg border border-black/[0.06] bg-[#F7F7F2]/70 px-3 py-2.5 text-sm leading-relaxed text-[#4E5663]">
                <span className="font-bold text-[#111318]">עוד הקשר: </span>
                {expView.tradeoffNote}
              </p>
            ) : null}

            <button
              type="button"
              onClick={() => setAdvanced((v) => !v)}
              className="text-xs font-semibold text-[#1F8F6A] hover:underline"
            >
              {advanced ? "הסתר פירוט לפי היבטים" : "הצג פירוט לפי היבטים (מתקדם)"}
            </button>

            {advanced && pillarsDisplay?.length ? (
              <div className="space-y-4 border-t border-black/[0.06] pt-4">
                <div>
                  <p className="text-sm font-extrabold text-[#111318]">פירוט לפי היבטים</p>
                  <p className="mt-1 text-xs leading-relaxed text-[#7A817C]">
                    מבט מפורט על מבנה, רכיבים ותרומה תזונתית — פרק טכני יחסית.
                  </p>
                </div>
                <BariInterpretationPanel pillars={pillarsDisplay} />
              </div>
            ) : null}
          </div>
        </motion.div>
      </div>
    </motion.article>
  );
}

export function MilkComparisonPage() {
  const flagship = useMemo(() => getFlagshipProducts(), []);
  const defaultProduct = flagship[0] ?? milkProducts[0];
  const [selected, setSelected] = useState<MilkComparisonProduct>(defaultProduct);
  const [activeFilters, setActiveFilters] = useState<Set<ComparisonFilterId>>(new Set());

  const toggleFilter = (id: ComparisonFilterId) => {
    setActiveFilters((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const visibleProducts = useMemo(
    () => milkProducts.filter((p) => productMatchesFilters(p, activeFilters)),
    [activeFilters]
  );

  const visibleCount = countVisible(activeFilters);
  const handleSelect = (product: MilkComparisonProduct) => setSelected(product);

  return (
    <main className="relative bg-[#F7F7F2] text-[#111318]">
      <MilkCinematicHero />
      <MilkComparisonBridge />
      <MilkProductStrip
        selectedBarcode={selected.barcode}
        onSelect={handleSelect}
      />

      <section
        id="comparison-grid"
        className="border-t border-black/[0.08] bg-[#F7F7F2] py-14 md:py-20"
      >
        <HomeContainer className="space-y-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/80">
                מנוע השוואה
              </p>
              <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] md:text-3xl">
                כל המוצרים · סינון ופירוט
              </h2>
              <p className="mt-2 max-w-xl text-sm leading-relaxed text-[#4E5663]">
                {visibleCount} מוצרים מוצגים מתוך {milkProducts.length} · ממוין לפי ציון Bari
              </p>
            </div>
            <Link
              href="/blog/milk-analysis"
              className="text-sm font-semibold text-[#1F8F6A] hover:underline"
            >
              לניתוח המדף בבלוג
            </Link>
          </div>

          <div className="flex flex-wrap gap-2">
            {comparisonFilters.map((f) => {
              const on = activeFilters.has(f.id);
              return (
                <button
                  key={f.id}
                  type="button"
                  onClick={() => toggleFilter(f.id)}
                  className={cn(
                    "rounded-full border px-3.5 py-2 text-sm font-semibold transition-colors",
                    on
                      ? "border-[#1F8F6A]/35 bg-[#1F8F6A] text-[#F7F7F2]"
                      : "border-black/[0.08] bg-[#FFFFFF] text-[#4E5663] hover:border-[#1F8F6A]/20"
                  )}
                >
                  {f.label}
                </button>
              );
            })}
            {activeFilters.size > 0 ? (
              <button
                type="button"
                onClick={() => setActiveFilters(new Set())}
                className="rounded-full px-3 py-2 text-sm font-semibold text-[#7A817C] underline-offset-2 hover:underline"
              >
                נקה סינון
              </button>
            ) : null}
          </div>

          <div className="overflow-hidden rounded-[1.25rem] border border-black/[0.08] bg-[#FFFFFF]/95 shadow-sm">
            {visibleProducts.length === 0 ? (
              <p className="p-8 text-center text-sm text-[#4E5663]">
                אין מוצרים התואמים לסינון — נסו להסיר פילטר.
              </p>
            ) : (
              visibleProducts.map((product, i) => (
                <ProductShelfRow
                  key={product.barcode}
                  product={product}
                  rank={i + 1}
                  emphasis={getRowEmphasis(product, activeFilters)}
                />
              ))
            )}
          </div>

          <section className="rounded-[1.25rem] border border-black/[0.08] bg-[#FFFFFF]/80 p-6 md:p-8">
            <h2 className="text-xl font-extrabold">איך לקרוא את ההשוואה</h2>
            <ul className="mt-4 space-y-3">
              {howToReadComparison.map((line) => (
                <li key={line} className="flex gap-3 text-sm leading-relaxed text-[#4E5663]">
                  <span className="mt-2 size-1.5 shrink-0 rounded-full bg-[#1F8F6A]" />
                  {line}
                </li>
              ))}
            </ul>
          </section>
        </HomeContainer>
      </section>
    </main>
  );
}
