"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

import { BreadConfidencePill } from "@/components/bread/bread-confidence-pill";
import { BreadShelfProductImage } from "@/components/bread/bread-shelf-product-image";
import { HomeContainer } from "@/components/home/section-frame";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import { BREAD_BLOG_HREF } from "@/lib/blog/bread-analysis-content";
import {
  BREAD_CLUSTER_FILTERS,
  BREAD_REPORT_STATS,
  breadComparisonPairs,
  breadHeroProducts,
  breadInsightBlocks,
  breadProductMatchesFilter,
  breadScoredProducts,
  breadTransparencyProducts,
  fermentationSignal,
  formatBreadNumber,
  breadScoreObservation,
  formatBreadScoreLine,
} from "@/lib/comparisons/bread-page-data";
import type { BreadFilterId, BreadProduct } from "@/lib/comparisons/bread-types";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

function ComparisonHero() {
  const reduceMotion = useReducedMotion();

  return (
    <section className="relative overflow-hidden border-b border-black/[0.06] bg-[#F7F7F2]">
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.12]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(17,19,24,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(17,19,24,0.07) 1px, transparent 1px)",
          backgroundSize: "26px 26px",
        }}
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_65%_55%_at_100%_0%,rgba(31,143,106,0.14),transparent_60%)]"
        aria-hidden
      />

      <HomeContainer className="relative grid gap-10 py-14 md:grid-cols-[minmax(0,1.35fr)_minmax(320px,0.95fr)] md:items-center md:py-20">
        <div>
          <p className="text-[0.7rem] font-bold uppercase tracking-[0.28em] text-[#1F8F6A]">
            BREAD INVESTIGATION
          </p>
          <h1 className="mt-4 text-4xl font-extrabold tracking-[-0.055em] text-[#111318] md:text-[3.35rem] md:leading-[1.02]">
            מה באמת יש בלחם שלכם?
          </h1>
          <p className="mt-4 max-w-3xl text-xl font-semibold leading-snug tracking-[-0.02em] text-[#313834] md:text-2xl">
            ניתחנו 256 מוצרי לחם ממדף שופרסל. רק 81 קיבלו מספיק נתונים לניתוח מהימן.
            בחרנו 31 מוצרים שמייצגים את המגוון הקיים.
          </p>
          <p className="mt-5 max-w-3xl rounded-[1rem] border border-black/[0.07] bg-[#FFFFFF]/80 px-4 py-3 text-sm leading-relaxed text-[#4E5663]">
            הניתוח מבוסס על מדף שופרסל בלבד, ולא על סקר שוק ישראלי. חלק מהמוצרים לא קיבלו ציון
            מפני שהנתונים הציבוריים לא הספיקו לניתוח.
          </p>

          <div className="mt-7 grid gap-3 sm:grid-cols-3">
            {[
              { value: BREAD_REPORT_STATS.scanned, label: "מוצרים שנסרקו" },
              { value: BREAD_REPORT_STATS.sufficient, label: "עם נתונים מספיקים" },
              { value: BREAD_REPORT_STATS.featured, label: "נבחרו לדף" },
            ].map((item) => (
              <div
                key={item.label}
                className="rounded-[1.15rem] border border-black/[0.07] bg-[#FFFFFF]/90 px-4 py-4 shadow-[0_18px_50px_-40px_rgba(17,19,24,0.35)]"
              >
                <p className="text-3xl font-extrabold tracking-[-0.05em] text-[#111318]">{item.value}</p>
                <p className="mt-1 text-sm text-[#4E5663]">{item.label}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="relative rounded-[1.6rem] border border-black/[0.08] bg-[#FFFFFF]/80 p-5 shadow-[0_32px_90px_-56px_rgba(17,19,24,0.35)]">
          <div className="grid min-h-[360px] grid-cols-3 gap-4">
            {breadHeroProducts.map((product, index) => (
              <motion.div
                key={product.id}
                animate={reduceMotion ? undefined : { y: [0, -5, 0] }}
                transition={{
                  duration: 5.5 + index * 0.5,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className={cn(
                  "flex items-end justify-center rounded-[1.15rem] border border-black/[0.06] bg-[linear-gradient(180deg,#FFFFFF_0%,#F4F6F3_100%)]",
                  index === 1 && "translate-y-8",
                  index === 4 && "translate-y-10"
                )}
              >
                <BreadShelfProductImage
                  product={product}
                  size="lg"
                  className="mx-auto my-2 border-0 shadow-none"
                />
              </motion.div>
            ))}
          </div>
          <p className="mt-4 text-center text-xs font-semibold tracking-wide text-[#7A817C]">
            לחם, מחמצת, דגנים, קרקרים ופערי שקיפות על אותו מדף
          </p>
        </div>
      </HomeContainer>
    </section>
  );
}

function ScoreCell({ product }: { product: BreadProduct }) {
  const scoreLine = formatBreadScoreLine(product);

  return (
    <div className="min-w-[9.5rem]">
      {scoreLine ? (
        <>
          <p className="text-lg font-extrabold tabular-nums leading-none text-[#111318]">{scoreLine}</p>
          <p className="mt-1.5 text-xs font-medium leading-5 text-[#4E5663]">
            {breadScoreObservation(product)}
          </p>
        </>
      ) : (
        <p className="text-sm font-semibold text-[#5E6672]">ללא ציון</p>
      )}
      <BreadConfidencePill
        label={product.confidence_label_he}
        level={product.confidence_level}
        className="mt-2"
      />
    </div>
  );
}

function ComparisonTable({ products }: { products: BreadProduct[] }) {
  return (
    <div className="overflow-hidden bg-[#FFFFFF]/95">
      <div className="px-5 py-4">
        <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">טבלת ההשוואה</h2>
        <p className="mt-1 text-sm text-[#4E5663]">
          קריאה מהירה של המדף: מוצר, ציון, סיבים, תסיסה, מבנה והערה אחת שמסבירה למה הוא כאן.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[980px] text-right">
          <thead className="bg-[#F7F7F2]/75 text-sm text-[#5B645F]">
            <tr>
              <th className="px-5 py-3 font-bold">מוצר</th>
              <th className="px-5 py-3 font-bold">ציון</th>
              <th className="px-5 py-3 font-bold">סיבים</th>
              <th className="px-5 py-3 font-bold">תסיסה</th>
              <th className="px-5 py-3 font-bold">מבנה</th>
              <th className="px-5 py-3 font-bold">הערה</th>
            </tr>
          </thead>
          <tbody className={BARI_COMPARISON_TOKENS.rows.zebraContainerClass}>
            {products.map((product) => {
              const fermentation = fermentationSignal(product.fermentation_status_he);

              return (
                <tr key={product.id} className={cn("align-top", BARI_COMPARISON_TOKENS.rows.zebraRowClass)}>
                  <td className="px-5 py-4">
                    <a
                      href={product.source_url}
                      target="_blank"
                      rel="noreferrer"
                      className="group flex min-w-[16rem] items-start gap-4"
                    >
                      <BreadShelfProductImage product={product} size="sm" className="shrink-0" />
                      <div className="min-w-0">
                        <p className="font-extrabold leading-snug text-[#111318] group-hover:text-[#1F8F6A]">
                          {product.name_he}
                        </p>
                        <p className="mt-1 text-xs text-[#7A817C]">{product.category_label_he}</p>
                      </div>
                    </a>
                  </td>
                  <td className="px-5 py-4">
                    <ScoreCell product={product} />
                  </td>
                  <td className="px-5 py-4 text-sm font-semibold tabular-nums text-[#111318]">
                    {formatBreadNumber(product.fiber_g, "g")}
                  </td>
                  <td className="px-5 py-4 text-sm text-[#313834]">
                    <span title={fermentation.tooltip} className="inline-flex items-center gap-2">
                      <span aria-hidden>{fermentation.icon}</span>
                      <span>{fermentation.label}</span>
                    </span>
                  </td>
                  <td className="px-5 py-4 text-sm leading-relaxed text-[#313834]">
                    {product.structural_summary_he}
                  </td>
                  <td className="px-5 py-4 text-sm leading-relaxed text-[#4E5663]">
                    {product.why_featured_he}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function InsightBlocks() {
  return (
    <section>
      <div className="mb-5">
        <p className="text-sm font-bold uppercase tracking-[0.2em] text-[#7A817C]">מה מצאנו במדף</p>
        <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          ארבע תובנות שעזרו לנו לקרוא את המדף
        </h2>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {breadInsightBlocks.map((block) => (
          <article
            key={block.id}
            className="rounded-[1.25rem] border border-black/[0.08] bg-[#FFFFFF]/92 p-6 shadow-[0_18px_50px_-38px_rgba(17,19,24,0.28)]"
          >
            <h3 className="text-xl font-extrabold tracking-[-0.03em] text-[#111318]">{block.title}</h3>
            <p className="mt-3 text-sm leading-7 text-[#4E5663]">{block.body}</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {block.supporting.map((name) => (
                <span
                  key={name}
                  className="rounded-full border border-black/[0.06] bg-[#F7F7F2] px-3 py-1 text-xs font-semibold text-[#4E5663]"
                >
                  {name}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function PairCard({ pair }: { pair: (typeof breadComparisonPairs)[number] }) {
  return (
    <article className="rounded-[1.35rem] border border-black/[0.08] bg-[#FFFFFF]/95 p-5 shadow-[0_18px_50px_-38px_rgba(17,19,24,0.28)]">
      <p className="text-[0.68rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]">{pair.kicker}</p>
      <h3 className="mt-2 text-xl font-extrabold tracking-[-0.03em] text-[#111318]">{pair.title}</h3>
      <div className="mt-5 grid gap-4 md:grid-cols-2">
        {[pair.left, pair.right].map((product) => (
          <div
            key={product.id}
            className="rounded-[1.15rem] border border-black/[0.07] bg-[#F7F7F2]/60 p-4"
          >
            <div className="flex items-start gap-3">
              <BreadShelfProductImage product={product} size="md" className="shrink-0" />
              <div className="min-w-0">
                <p className="font-extrabold leading-snug text-[#111318]">{product.name_he}</p>
                <p className="mt-1 text-xs text-[#7A817C]">{product.category_label_he}</p>
                <div className="mt-3 space-y-1.5">
                  {formatBreadScoreLine(product) ? (
                    <>
                      <p className="text-base font-extrabold tabular-nums text-[#111318]">
                        {formatBreadScoreLine(product)}
                      </p>
                      <p className="text-sm leading-6 text-[#4E5663]">
                        {breadScoreObservation(product)}
                      </p>
                    </>
                  ) : (
                    <p className="text-sm font-semibold text-[#5E6672]">ללא ציון</p>
                  )}
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  <BreadConfidencePill
                    label={product.confidence_label_he}
                    level={product.confidence_level}
                  />
                  <span className="rounded-full border border-black/[0.06] bg-[#FFFFFF] px-2.5 py-1 text-[0.72rem] font-semibold text-[#4E5663]">
                    סיבים {formatBreadNumber(product.fiber_g, "g")}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      <p className="mt-4 text-sm leading-7 text-[#4E5663]">{pair.caption}</p>
    </article>
  );
}

function TransparencyArchive() {
  return (
    <section className="rounded-[1.6rem] border border-black/[0.08] bg-[#ECEFED] px-6 py-8 md:px-8">
      <div className="max-w-3xl">
        <p className="text-[0.68rem] font-bold uppercase tracking-[0.24em] text-[#68726B]">
          Missing information archive
        </p>
        <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          מוצרים שלא קיבלו ציון
        </h2>
        <p className="mt-3 text-sm leading-7 text-[#4E5663]">
          לא מציגים ציון כשאין מספיק נתונים ציבוריים. זו לא הערכה שלילית על המוצר, אלא סימון
          ברור של חוסר המידע הזמין לנו.
        </p>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {breadTransparencyProducts.map((product) => (
          <article
            key={product.id}
            className="rounded-[1.2rem] border border-black/[0.07] bg-[#F7F7F2]/80 p-4"
          >
            <div className="flex items-start gap-3">
              <BreadShelfProductImage product={product} size="sm" className="shrink-0" />
              <div className="min-w-0">
                <h3 className="font-extrabold leading-snug text-[#111318]">{product.name_he}</h3>
                <p className="mt-2 rounded-full border border-[#8A8F98]/16 bg-[#EEF0F2] px-2.5 py-1 text-[0.72rem] font-semibold text-[#4E5663]">
                  אין ציון — אין נתוני רכיבים מספיקים
                </p>
              </div>
            </div>
            <p className="mt-4 text-sm leading-7 text-[#4E5663]">{product.suggested_card_blurb_he}</p>
          </article>
        ))}
      </div>

      <p className="mt-6 text-sm leading-relaxed text-[#4E5663]">
        <span className="font-bold text-[#111318]">46% מהמוצרים שסרקנו</span> לא הציגו נתוני רכיבים
        מלאים. זו מגבלה של זמינות הנתונים הציבוריים, לא של הניתוח עצמו.
      </p>
    </section>
  );
}

export function BreadComparisonDashboard() {
  const [activeFilter, setActiveFilter] = useState<BreadFilterId>("all");

  const visibleProducts = useMemo(
    () => breadScoredProducts.filter((product) => breadProductMatchesFilter(product, activeFilter)),
    [activeFilter]
  );

  return (
    <main
      className={cn(
        "relative min-h-screen overflow-hidden bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <ComparisonHero />

      <HomeContainer className="relative space-y-12 py-12 md:py-16">
        <section className="space-y-5">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-sm font-bold uppercase tracking-[0.2em] text-[#7A817C]">מנוע השוואה</p>
              <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
                כל 31 המוצרים, בלי גרפים שמסתירים את הסיפור
              </h2>
              <p className="mt-2 text-sm leading-relaxed text-[#4E5663]">
                מוצגים כעת {visibleProducts.length} מוצרים מתוך {breadScoredProducts.length} שקיבלו ציון.
              </p>
            </div>
            <Link href={BREAD_BLOG_HREF} className="text-sm font-semibold text-[#1F8F6A] hover:underline">
              לסיפור המלא בכתבה
            </Link>
          </div>

          <div className="flex flex-wrap gap-2">
            {BREAD_CLUSTER_FILTERS.map((filter) => {
              const active = activeFilter === filter.id;
              return (
                <button
                  key={filter.id}
                  type="button"
                  onClick={() => setActiveFilter(filter.id)}
                  className={cn(
                    "rounded-full border px-3.5 py-2 text-sm font-semibold transition-colors",
                    active
                      ? "border-[#1F8F6A]/30 bg-[#1F8F6A] text-[#F7F7F2]"
                      : "border-black/[0.08] bg-[#FFFFFF]/85 text-[#4E5663] hover:border-[#1F8F6A]/20 hover:text-[#111318]"
                  )}
                >
                  {filter.label}
                </button>
              );
            })}
          </div>

          <ComparisonTable products={visibleProducts} />
        </section>

        <InsightBlocks />

        <section className="space-y-4">
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.2em] text-[#7A817C]">זוגות להשוואה</p>
            <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
              שלושה מוצרים שנראים קרובים, אבל מספרים סיפורים שונים
            </h2>
          </div>
          <div className="grid gap-4">
            {breadComparisonPairs.map((pair) => (
              <PairCard key={pair.id} pair={pair} />
            ))}
          </div>
        </section>

        <TransparencyArchive />

        <section className="rounded-[1.25rem] border border-black/[0.08] bg-[#FFFFFF]/80 p-6 md:p-7">
          <details>
            <summary className="cursor-pointer text-sm font-bold text-[#111318]">
              על הניתוח והמתודולוגיה
            </summary>
            <p className="mt-4 max-w-4xl text-sm leading-7 text-[#4E5663]">
              כל המוצרים נסרקו ממדף שופרסל בין 25 ל-26 במאי 2026. הנתונים על רכיבים, ערכים
              תזונתיים ותמונות נאספו מדפי המוצר הציבוריים. הציון נשען על בסיס הדגן, מקור הסיבים,
              מנגנון התסיסה ורמת העיבוד. ציון לא מוצג כאשר הנתונים הציבוריים לא מספיקים לניתוח
              מהימן. זהו ניתוח של מדף אחד, לא של כל השוק הישראלי.
            </p>
          </details>
        </section>

        <footer className="flex flex-col gap-4 border-t border-black/[0.06] pt-10 sm:flex-row sm:items-center sm:justify-between">
          <Link
            href={BREAD_BLOG_HREF}
            className="inline-flex items-center gap-2 text-sm font-bold text-[#1F8F6A] hover:underline"
          >
            לקריאת הכתבה הראשית
            <ChevronLeft className="size-4" aria-hidden />
          </Link>
          <Link href="/blog" className="text-sm font-semibold text-[#4E5663] hover:text-[#111318]">
            לכל הכתבות
          </Link>
        </footer>
      </HomeContainer>
    </main>
  );
}
