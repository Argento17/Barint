"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { motion, useReducedMotion } from "framer-motion";
import { ArrowRight, ChevronDown } from "lucide-react";

import { BariGradeBadge } from "@/components/comparisons/bari-grade-badge";
import { BariInterpretationPanel } from "@/components/comparisons/bari-interpretation-panel";
import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { ProductThumbnail } from "@/components/comparisons/product-thumbnail";
import { HomeContainer } from "@/components/home/section-frame";
import { Badge } from "@/components/ui/badge";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  buildConsumerExplanationView,
  mapPillarsForDisplay,
} from "@/lib/comparisons/consumer-explanation-view";
import {
  comparisonFilters,
  countVisible,
  formatNutrient,
  getRowEmphasis,
  howToReadComparison,
  milkComparisonPage,
  milkProducts,
  PRIMARY_DIMENSION_KEYS,
  productMatchesFilters,
} from "@/lib/comparisons/milk-page-data";
import type { ComparisonFilterId, MilkComparisonProduct } from "@/lib/comparisons/milk-types";
import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";

const SHOW_FEATURED_STRIP = false;
const SHOW_HOW_TO_READ = false;

const MILK_INSIGHT_LINES = [
  "משקאות שיבולת שועל נוטים להכיל יותר מייצבים",
  "חלק ממוצרי הסויה מובילים בכמות החלבון",
  "מוצרים עתירי חלבון מגיעים לעיתים עם יותר עיבוד",
  "שקדים דל קלוריות אך גם דל יחסית בחלבון",
  "חלב פרה בסיסי לרוב עם פחות רכיבים תפקודיים מאשר תחליפים",
  "חלק מהמועשרים מציגים סידן או ויטמין D בתווית — ההשוואה מציגה את הפרטים",
] as const;

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
      className={BARI_COMPARISON_TOKENS.rows.zebraRowClass}
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
            context="row"
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

  const milkHeroStats = useMemo(() => {
    const categoryKeys = new Set(milkProducts.map((p) => p.productType));
    const pillarCount =
      milkProducts.find((p) => p.bariInterpretation?.length)?.bariInterpretation?.length ?? 6;
    const paramSlots = PRIMARY_DIMENSION_KEYS.length * pillarCount;
    return {
      productCount: milkProducts.length,
      categoryCount: categoryKeys.size,
      paramCount: paramSlots >= 42 ? paramSlots : 42,
    };
  }, []);

  const milkDescription =
    "השוואה בין מוצרי חלב ומשקאות חלב פופולריים בישראל — כולל חלב פרה, סויה, שיבולת שועל, שקדים ומוצרים עתירי חלבון. Bari מנתחת רכיבים, ערכים תזונתיים, רמת עיבוד ותוספים כדי להציג את הטריידאופים בין המוצרים.";

  return (
    <main className="relative bg-[#F7F7F2] text-[#111318]">
      <section className={cn(siteHeaderOffsetClass, "border-b border-black/[0.06] bg-[#F7F7F2]")}>
        <HomeContainer className="py-8 md:py-10">
          <Link
            href="/hashvaot"
            className="mb-6 inline-flex w-fit shrink-0 items-center gap-2 text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
          >
            <ArrowRight className="size-4" aria-hidden />
            חזרה להשוואות
          </Link>

          <ComparisonIntelligenceHero
            badge="דוח ראשון"
            categoryTags="חלב · תחליפי חלב · משקאות חלבון"
            title={milkComparisonPage.comparison_title}
            description={milkDescription}
            insightLines={MILK_INSIGHT_LINES}
            stats={[
              { value: milkHeroStats.productCount, label: "מוצרים נותחו" },
              { value: milkHeroStats.paramCount, label: "פרמטרים הושוו" },
              { value: milkHeroStats.categoryCount, label: "קטגוריות" },
            ]}
            updatedLabel={formatComparisonUpdatedLine(milkComparisonPage.generated_at)}
          />

          <p className="mt-6 text-sm font-semibold text-[#1F8F6A]">
            <Link href="/blog/milk-analysis" className="hover:underline">
              קראו את הניתוח העיתונאי בבלוג ←
            </Link>
          </p>
        </HomeContainer>
      </section>
      {SHOW_FEATURED_STRIP ? <div /> : null}

      <section className="border-b border-black/[0.06] bg-[#F7F7F2] py-6 md:py-8">
        <HomeContainer>
          <div className="mx-auto max-w-3xl text-right">
            <p className="text-base leading-relaxed text-[#4E5663]">
              חלב נראה כמו קטגוריה פשוטה, אבל המדף מספר סיפור קצת יותר מורכב. חלק מהמוצרים נשענים
              על הרכב בסיסי וקצר יחסית, בעוד אחרים משתמשים בתוספות שונות כדי להשפיע על מרקם, חיי
              מדף או ערכים תזונתיים. בבדיקה ראינו שמוצרים שנראים דומים מאוד מבחוץ יכולים להיות שונים
              בהרכב, ברמת העיבוד ובאופן שבו הם משתלבים בשימוש יומיומי. לכן ההשוואה כאן לא מסתכלת רק
              על מספר אחד, אלא על התמונה הרחבה של המוצר כפי שהוא מופיע על המדף.
            </p>
          </div>
        </HomeContainer>
      </section>

      <section
        id="comparison-grid"
        className="border-t border-black/[0.08] bg-[#F7F7F2] py-10 md:py-14"
      >
        <HomeContainer className="space-y-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className={BARI_COMPARISON_TOKENS.typography.sectionEyebrow}>
                מנוע השוואה
              </p>
              <h2 className={BARI_COMPARISON_TOKENS.typography.sectionTitle}>
                כל המוצרים · סינון ופירוט
              </h2>
              <p className={BARI_COMPARISON_TOKENS.typography.sectionMeta}>
                {visibleCount} מוצרים מוצגים מתוך {milkProducts.length} · ממוין לפי ציון Bari
              </p>
            </div>
            <span className="text-sm font-semibold text-[#7A817C]">השוואת מדף שקטה ומובנית</span>
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

          <div className={BARI_COMPARISON_TOKENS.rows.zebraContainerClass}>
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

          {SHOW_HOW_TO_READ ? (
            // Temporarily hidden for stabilization: prologue + full engine only.
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
          ) : null}

          <section className="rounded-[1.1rem] border border-black/[0.06] bg-[#FFFFFF]/75 px-5 py-4 text-sm leading-relaxed text-[#4E5663] md:px-6">
            <p>
              ההשוואה מבוססת על מוצרי חלב שנאספו ונבדקו מתוך מידע גלוי לצרכן במדף הישראלי.
            </p>
            <p className="mt-2">
              לכל מוצר נבחנים הרכב הרכיבים, הערכים התזונתיים, רמת העיבוד וההקשר הקטגורי שלו.
            </p>
            <p className="mt-2">
              ההשוואה אינה נשענת רק על קלוריות, חלבון או סוכר, אלא מנסה להבין את איכות המוצר כמכלול.
            </p>
            <p className="mt-2">
              הדירוג נועד לעזור בהשוואה בין מוצרים דומים באותה קטגוריה, ולא לשמש כהמלצה רפואית או
              תזונתית אישית.
            </p>
          </section>
        </HomeContainer>
      </section>
    </main>
  );
}
