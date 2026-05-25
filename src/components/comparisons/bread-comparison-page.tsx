"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { motion, useReducedMotion } from "framer-motion";
import { ArrowRight, ChevronDown, ChevronLeft } from "lucide-react";

import { BariGradeBadge } from "@/components/comparisons/bari-grade-badge";
import { HomeContainer } from "@/components/home/section-frame";
import { BREAD_BLOG_HREF } from "@/lib/blog/bread-analysis-content";
import {
  ARCHETYPE_META,
  breadComparisonFilters,
  breadCountVisible,
  breadMatchesFilters,
  breadProducts,
  getBreadFlagshipProducts,
  getBreadRowEmphasis,
  sortBreadProducts,
} from "@/lib/comparisons/bread-page-data";
import { breadEditorial } from "@/lib/comparisons/bread-editorial-content";
import type { BreadFilterId, BreadProduct } from "@/lib/comparisons/bread-types";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

const howToReadBreadComparison = [
  "הציון משקף מבנה דגן, תסיסה, מקור סיבים ורמת עיבוד בהשוואה למוצרים דומים.",
  "לחם עם יותר סיבים אינו בהכרח פשוט יותר. חשוב גם מאיזה מקור הם מגיעים.",
  "למה קיבל את הציון? פותח את רשימת הרכיבים, הגורמים שחיזקו את המוצר, והגורמים שגרעו ממנו.",
  "ההשוואה נועדה לעזור לקרוא את המדף בצורה מסודרת, לא להחליף שיקול אישי או תזונתי.",
] as const;

function ingredientCount(product: BreadProduct) {
  return product.ingredients_display
    .split(",")
    .map((part) => part.trim())
    .filter(Boolean).length;
}

function categoryLabel(category: BreadProduct["category"]) {
  switch (category) {
    case "bread":
      return "לחם";
    case "cracker":
      return "קרקר";
    case "crispbread":
      return "קריספ";
  }
}

function fermentationLabel(quality: BreadProduct["ferm_q"]) {
  switch (quality) {
    case "traditional":
      return "מחמצת אמיתית";
    case "mixed":
      return "מחמצת + שמרים";
    case "flavor_only":
      return "מחמצת לטעם";
    case "none":
      return "ללא תסיסה";
  }
}

function fiberSourceLabel(quality: BreadProduct["fiber_q"]) {
  switch (quality) {
    case "structural":
      return "מתוך הדגן";
    case "hybrid":
      return "מקור מעורב";
    case "isolated":
      return "מתוסף מבודד";
  }
}

function grainStructureLabel(gss: number) {
  if (gss >= 75) return "מבנה דגני מובהק";
  if (gss >= 50) return "מבנה ביניים";
  if (gss >= 30) return "מבנה מעורב";
  return "מבנה רחוק מדגן מלא";
}

function buildRaisesScore(product: BreadProduct): string[] {
  const lines: string[] = [];

  if (product.gss >= 75) lines.push("הבסיס הדגני נשאר ברור יחסית גם אחרי האפייה.");
  if (ingredientCount(product) <= 4) lines.push("רשימת הרכיבים קצרה ופשוטה יחסית.");
  if (product.ferm_q === "traditional") lines.push("מחמצת אמיתית תרמה למבנה ולפרשנות הקטגוריאלית.");
  if (product.ferm_q === "mixed") lines.push("יש מרכיב תסיסה ממשי, גם אם לא מלא.");
  if (product.fiber_q === "structural") lines.push("הסיבים מגיעים מתוך הדגן עצמו ולא רק מתוספת חיצונית.");
  if (product.nutrition.sugar_g <= 2) lines.push("רמת הסוכר נמוכה יחסית לפורמט.");

  if (lines.length === 0) {
    lines.push("בתוך המשפחה שלו, אין כאן גורם אחד בולט במיוחד שמושך מעלה.");
  }

  return lines;
}

function buildLowersScore(product: BreadProduct): string[] {
  const lines: string[] = [];

  if (product.gss <= 35) lines.push("מבנה הדגן התרחק מהמוצר הבסיסי בקטגוריה.");
  if (ingredientCount(product) >= 7) lines.push("רשימת הרכיבים ארוכה יחסית ומרמזת על יותר שכבות הרכבה.");
  if (product.fiber_q === "isolated") lines.push("חלק מהסיבים מגיעים מתוספים מבודדים ולא מתוך הדגן עצמו.");
  if (product.ferm_q === "flavor_only") lines.push("המחמצת מתפקדת בעיקר כשכבת טעם, לא כתהליך מלא.");
  if (product.ferm_q === "none") lines.push("אין תרומת תסיסה שמוסיפה עומק מבני למוצר.");
  if (product.nutrition.sugar_g >= 5) lines.push("רמת הסוכר גבוהה יחסית למשפחה שלו.");
  if (product.red_labels.length > 0) lines.push(`יש גם סימונים אדומים: ${product.red_labels.join(" · ")}.`);

  if (lines.length === 0) {
    lines.push("אין כאן גורם שלילי אחד חריג, אלא חבילה כוללת בינונית יותר.");
  }

  return lines;
}

function buildRelativeToPeers(product: BreadProduct) {
  const peers = breadProducts.filter((peer) => peer.archetype === product.archetype);
  const meta = ARCHETYPE_META[product.archetype];

  if (peers.length <= 1) {
    return `המוצר מייצג כמעט לבדו את משפחת ${meta.label}, ולכן נקרא בעיקר מול הפורמט עצמו.`;
  }

  const average = peers.reduce((sum, peer) => sum + peer.score, 0) / peers.length;
  const diff = product.score - average;

  if (diff >= 6) {
    return `בתוך משפחת ${meta.label}, המוצר הזה נמצא מעל הממוצע בעיקר בזכות מבנה פשוט יותר או בסיס דגני ברור יותר.`;
  }

  if (diff <= -6) {
    return `בתוך משפחת ${meta.label}, המוצר הזה יורד מתחת לממוצע כשההרכבה נעשית מורכבת יותר או רחוקה יותר מהדגן.`;
  }

  return `בתוך משפחת ${meta.label}, המוצר הזה יושב קרוב לממוצע ומשקף היטב את הטריידאוף הרגיל של הקבוצה.`;
}

function buildTradeoffNote(product: BreadProduct) {
  if (product.delta >= 6) {
    return `הניתוח המבני חיזק את המוצר ב-${product.delta.toFixed(1)} נקודות לעומת הציון הבסיסי.`;
  }

  if (product.delta <= -6) {
    return `הניתוח המבני הוריד את המוצר ב-${Math.abs(product.delta).toFixed(1)} נקודות לעומת הציון הבסיסי.`;
  }

  return "הפער בין הציון הבסיסי לציון הסופי היה מתון יחסית.";
}

function BreadProductMark({
  product,
  size = "md",
}: {
  product: BreadProduct;
  size?: "sm" | "md" | "lg";
}) {
  const meta = ARCHETYPE_META[product.archetype];
  const shellClass =
    size === "lg"
      ? "h-28 w-20 rounded-[1.1rem]"
      : size === "sm"
        ? "h-20 w-14 rounded-[0.9rem]"
        : "h-24 w-[4.5rem] rounded-[1rem]";
  const categoryText = size === "lg" ? "text-[0.52rem]" : "text-[0.46rem]";
  const brandText = size === "lg" ? "text-[0.58rem]" : "text-[0.5rem]";

  return (
    <div
      className={cn(
        "relative shrink-0 overflow-hidden border border-black/[0.07] bg-[#FFFDFC] shadow-[0_12px_30px_-26px_rgba(17,19,24,0.28)]",
        shellClass
      )}
      aria-hidden
    >
      <div
        className="absolute inset-x-0 top-0 h-2.5"
        style={{ backgroundColor: meta?.color ?? "#7A817C" }}
      />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(255,255,255,0.94),transparent_48%)]" />
      <div className="relative flex h-full flex-col justify-between px-2 py-3 text-center">
        <div>
          <p className={cn("font-semibold uppercase tracking-[0.12em] text-[#7A817C]", categoryText)}>
            {categoryLabel(product.category)}
          </p>
          <p className={cn("mt-2 line-clamp-2 font-bold leading-tight text-[#111318]", brandText)}>
            {product.brand}
          </p>
        </div>
        <div>
          <div className="mx-auto mb-2 h-px w-7 bg-black/[0.08]" />
          <p className={cn("line-clamp-3 leading-tight text-[#7A817C]", categoryText)}>
            {product.name_he}
          </p>
        </div>
      </div>
    </div>
  );
}

function BreadHero() {
  const { hero, lead } = breadEditorial;

  return (
    <header
      className={cn(
        "relative overflow-hidden border-b border-black/[0.06] bg-[#FFFFFF] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="flex flex-col py-8 md:py-12">
        <Link
          href="/hashvaot"
          className="mb-4 inline-flex w-fit shrink-0 items-center gap-2 text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
        >
          <ArrowRight className="size-4" aria-hidden />
          חזרה להשוואות
        </Link>

        <div className="max-w-3xl text-right">
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#1F8F6A]">
            {hero.eyebrow}
          </p>
          <h1 className="mt-3 text-balance text-3xl font-extrabold leading-[1.1] tracking-[-0.05em] text-[#111318] md:text-4xl lg:text-5xl">
            {hero.title}
            <br />
            <span className="text-[#1F8F6A]">{hero.titleEm}</span>
          </h1>
          <p className="mt-3 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
            {lead[0]} {lead[1]}
          </p>
          <p className="mt-2 text-sm text-[#7A817C]">{lead[3]}</p>

          <div className="mt-6 flex gap-8 border-t border-black/[0.06] pt-5">
            {hero.kpis.map((kpi) => (
              <div key={kpi.label}>
                <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">
                  {kpi.value}
                </p>
                <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                  {kpi.label}
                </p>
              </div>
            ))}
          </div>

          <p className="mt-5 text-sm font-semibold text-[#1F8F6A]">
            <Link href={BREAD_BLOG_HREF} className="hover:underline">
              קראו את הניתוח בבלוג ←
            </Link>
          </p>
        </div>
      </HomeContainer>
    </header>
  );
}

function BreadComparisonBridge() {
  return (
    <section className="border-b border-black/[0.06] bg-[#F7F7F2] py-12 md:py-16">
      <HomeContainer>
        <div className="mx-auto max-w-2xl text-right">
          <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.28em] text-[#1F8F6A]/80">
            ניתוח
          </p>
          <p className="mt-4 text-lg leading-relaxed text-[#4E5663]">
            רוצים את הסיפור המלא מאחורי הממצאים? בבלוג מחכה הניתוח העריכתי של מדף הלחמים:
            הדפוסים שחזרו, הפערים בין מחמצת אמיתית למחמצת כטעם, והדרך שבה מוצרים דומים
            נבנים אחרת לגמרי.
          </p>
          <Link
            href={BREAD_BLOG_HREF}
            className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-[#1F8F6A] hover:underline"
          >
            לניתוח המדף בבלוג
            <ChevronLeft className="size-4" aria-hidden />
          </Link>
        </div>
      </HomeContainer>
    </section>
  );
}

function BreadProductStrip({
  selectedId,
  onSelect,
}: {
  selectedId: string;
  onSelect: (product: BreadProduct) => void;
}) {
  const products = getBreadFlagshipProducts();
  const reduceMotion = useReducedMotion();

  return (
    <section id="product-strip" className="border-b border-black/[0.06] bg-[#F7F7F2] py-12 md:py-16">
      <HomeContainer className="space-y-6">
        <div className="max-w-2xl text-right">
          <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.28em] text-[#1F8F6A]/80">
            מדף · השוואה
          </p>
          <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] md:text-3xl">
            שישה מוצרים, שישה מבנים
          </h2>
          <p className="mt-2 text-sm leading-relaxed text-[#4E5663]">
            לחצו על מוצר כדי לראות את אותה שפת השוואה של עמוד החלב, עכשיו על מדף הלחמים.
          </p>
        </div>

        <div className="-mx-5 overflow-x-auto px-5 pb-2 sm:-mx-6 sm:px-6 md:overflow-visible">
          <div className="flex gap-4 md:grid md:grid-cols-3 md:gap-5 lg:grid-cols-3">
            {products.map((product, index) => {
              const selected = product.id === selectedId;
              const meta = ARCHETYPE_META[product.archetype];

              return (
                <motion.button
                  key={product.id}
                  type="button"
                  onClick={() => onSelect(product)}
                  initial={reduceMotion ? false : { opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.08, duration: 0.5 }}
                  className={cn(
                    "group relative min-w-[17rem] shrink-0 overflow-hidden rounded-[1.35rem] border text-right transition-[border-color,box-shadow,transform] duration-500 md:min-w-0",
                    selected
                      ? "border-[#1F8F6A]/35 bg-[#111318] shadow-[0_32px_80px_-40px_rgba(31,143,106,0.35)] ring-1 ring-[#1F8F6A]/25"
                      : "border-black/[0.08] bg-[#FFFFFF]/90 shadow-[0_20px_60px_-48px_rgba(17,19,24,0.25)] hover:-translate-y-1 hover:border-[#1F8F6A]/20"
                  )}
                >
                  <div
                    className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100"
                    style={{
                      background: `radial-gradient(circle at 80% 20%, ${(meta?.color ?? "#1F8F6A")}22, transparent 55%)`,
                    }}
                    aria-hidden
                  />
                  <div className="relative flex flex-col gap-4 p-5 md:p-6">
                    <div className="flex items-start justify-between gap-3">
                      <BreadProductMark product={product} size="lg" />
                      <BariGradeBadge
                        score={product.score}
                        grade={product.grade}
                        gradeLabel={product.grade_label}
                        size="sm"
                      />
                    </div>
                    <div>
                      <p
                        className={cn(
                          "text-xs font-bold",
                          selected ? "text-[#1F8F6A]" : "text-[#7A817C]"
                        )}
                      >
                        {meta?.labelShort}
                      </p>
                      <h3
                        className={cn(
                          "mt-1 text-base font-extrabold leading-snug tracking-[-0.03em]",
                          selected ? "text-[#F7F7F2]" : "text-[#111318]"
                        )}
                      >
                        {product.name_he}
                      </h3>
                      <p
                        className={cn(
                          "mt-2 line-clamp-2 text-sm leading-relaxed",
                          selected ? "text-[#C8CDC9]" : "text-[#4E5663]"
                        )}
                      >
                        {product.finding ?? product.insight}
                      </p>
                    </div>
                  </div>
                </motion.button>
              );
            })}
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}

function ProductShelfRow({
  product,
  emphasis,
  rank,
}: {
  product: BreadProduct;
  emphasis: "emphasized" | "muted" | "neutral";
  rank: number;
}) {
  const [expanded, setExpanded] = useState(false);
  const reduceMotion = useReducedMotion();
  const muted = emphasis === "muted";
  const meta = ARCHETYPE_META[product.archetype];
  const raisesScore = useMemo(() => buildRaisesScore(product), [product]);
  const lowersScore = useMemo(() => buildLowersScore(product), [product]);
  const relativeToPeers = useMemo(() => buildRelativeToPeers(product), [product]);
  const tradeoffNote = useMemo(() => buildTradeoffNote(product), [product]);

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
          <BreadProductMark product={product} size="lg" />
          <div className="min-w-0 flex-1 pt-0.5">
            <p className="text-base font-extrabold leading-snug text-[#111318] sm:text-lg">
              {product.name_he}
            </p>
            <p className="mt-0.5 text-xs font-medium text-[#7A817C]">{product.brand}</p>
            <div className="mt-2.5">
              <span className="inline-flex h-5 items-center rounded-full bg-[#F7F7F2] px-2.5 text-[0.65rem] font-semibold text-[#4E5663]">
                {meta?.labelShort}
              </span>
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
          <p className="text-[0.62rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">
            סיבים / 100 ג׳
          </p>
          <p className="mt-0.5 text-base font-extrabold tabular-nums text-[#111318]">
            {product.nutrition.fiber_g} ג׳
          </p>
        </div>
        <div className="rounded-lg bg-[#F7F7F2]/80 px-3 py-2.5">
          <p className="text-[0.62rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">
            חלבון / 100 ג׳
          </p>
          <p className="mt-0.5 text-base font-extrabold tabular-nums text-[#111318]">
            {product.nutrition.protein_g} ג׳
          </p>
        </div>
        <div className="rounded-lg bg-[#F7F7F2]/80 px-3 py-2.5">
          <p className="text-[0.62rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">
            מקור סיבים
          </p>
          <p className="mt-0.5 text-xs font-medium leading-snug text-[#4E5663]">
            {fiberSourceLabel(product.fiber_q)}
          </p>
        </div>
        <div className="rounded-lg bg-[#F7F7F2]/80 px-3 py-2.5">
          <p className="text-[0.62rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">
            מבנה דגן
          </p>
          <p className="mt-0.5 text-xs font-medium leading-snug text-[#4E5663]">
            {grainStructureLabel(product.gss)}
          </p>
        </div>
      </div>

      <p className="px-4 pb-3 text-sm leading-relaxed text-[#4E5663] sm:pl-14">
        <span className="font-bold text-[#111318]">בקצרה: </span>
        {product.finding ?? product.insight}
      </p>

      <div className="space-y-2 px-4 pb-4 sm:pl-14">
        <button
          type="button"
          onClick={() => setExpanded((value) => !value)}
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
              <p className="mt-1.5 text-sm leading-relaxed text-[#4E5663]">{product.insight}</p>
            </div>
            <div>
              <h4 className="text-xs font-bold text-[#1F8F6A]">מה מעלה את הציון?</h4>
              <ul className="mt-1.5 list-inside list-disc space-y-1 text-sm text-[#4E5663]">
                {raisesScore.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-bold text-[#111318]">מה מוריד את הציון?</h4>
              <ul className="mt-1.5 list-inside list-disc space-y-1.5 text-sm leading-relaxed text-[#4E5663]">
                {lowersScore.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-bold text-[#111318]">בהשוואה למוצרים דומים</h4>
              <p className="mt-1.5 text-sm leading-relaxed text-[#4E5663]">{relativeToPeers}</p>
            </div>
            <p className="rounded-lg border border-black/[0.06] bg-[#F7F7F2]/70 px-3 py-2.5 text-sm leading-relaxed text-[#4E5663]">
              <span className="font-bold text-[#111318]">עוד הקשר: </span>
              {tradeoffNote}
            </p>
            <div className="grid gap-2 sm:grid-cols-3">
              <div className="rounded-lg bg-[#F7F7F2]/80 px-3 py-2.5">
                <p className="text-[0.62rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">
                  תסיסה
                </p>
                <p className="mt-0.5 text-xs font-medium leading-snug text-[#4E5663]">
                  {fermentationLabel(product.ferm_q)}
                </p>
              </div>
              <div className="rounded-lg bg-[#F7F7F2]/80 px-3 py-2.5">
                <p className="text-[0.62rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">
                  מספר רכיבים
                </p>
                <p className="mt-0.5 text-base font-extrabold tabular-nums text-[#111318]">
                  {ingredientCount(product)}
                </p>
              </div>
              <div className="rounded-lg bg-[#F7F7F2]/80 px-3 py-2.5">
                <p className="text-[0.62rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">
                  קטגוריה
                </p>
                <p className="mt-0.5 text-xs font-medium leading-snug text-[#4E5663]">
                  {categoryLabel(product.category)}
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.article>
  );
}

export function BreadComparisonPage() {
  const flagship = useMemo(() => getBreadFlagshipProducts(), []);
  const defaultProduct = flagship[0] ?? breadProducts[0];
  const [selectedProduct, setSelectedProduct] = useState<BreadProduct>(defaultProduct);
  const [activeFilters, setActiveFilters] = useState<Set<BreadFilterId>>(new Set());

  const visibleProducts = useMemo(
    () =>
      sortBreadProducts(
        breadProducts.filter((product) => breadMatchesFilters(product, activeFilters)),
        "score"
      ),
    [activeFilters]
  );

  const visibleCount = breadCountVisible(activeFilters);

  const toggleFilter = (filterId: BreadFilterId) => {
    setActiveFilters((previous) => {
      const next = new Set(previous);
      if (next.has(filterId)) next.delete(filterId);
      else next.add(filterId);
      return next;
    });
  };

  return (
    <main className="relative bg-[#F7F7F2] text-[#111318]">
      <BreadHero />
      <BreadComparisonBridge />
      <BreadProductStrip
        selectedId={selectedProduct.id}
        onSelect={(product) => setSelectedProduct(product)}
      />

      <section
        id="comparison-grid"
        className="border-t border-black/[0.08] bg-[#F7F7F2] py-14 md:py-20"
      >
        <HomeContainer className="space-y-8">
          <p className="rounded-[1rem] border border-black/[0.06] bg-[#FFFFFF] px-4 py-3 text-sm leading-relaxed text-[#4E5663]">
            <span className="font-bold text-[#111318]">מידע, לא המלצה.</span> הציון משקף מבנה,
            רכיבים והקשר קטגוריאלי בין מוצרים דומים במדף הישראלי. הוא לא מחליף התאמה אישית,
            רפואית או תזונתית.
          </p>

          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/80">
                מנוע השוואה
              </p>
              <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] md:text-3xl">
                כל המוצרים · סינון ופירוט
              </h2>
              <p className="mt-2 max-w-xl text-sm leading-relaxed text-[#4E5663]">
                {visibleCount} מוצרים מוצגים מתוך {breadProducts.length} · ממוין לפי ציון Bari
              </p>
            </div>
            <Link
              href="#product-strip"
              className="text-sm font-semibold text-[#1F8F6A] hover:underline"
            >
              חזרה למדגם המוצרים
            </Link>
          </div>

          <div className="flex flex-wrap gap-2">
            {breadComparisonFilters.map((filter) => {
              const on = activeFilters.has(filter.id);
              return (
                <button
                  key={filter.id}
                  type="button"
                  onClick={() => toggleFilter(filter.id)}
                  className={cn(
                    "rounded-full border px-3.5 py-2 text-sm font-semibold transition-colors",
                    on
                      ? "border-[#1F8F6A]/35 bg-[#1F8F6A] text-[#F7F7F2]"
                      : "border-black/[0.08] bg-[#FFFFFF] text-[#4E5663] hover:border-[#1F8F6A]/20"
                  )}
                >
                  {filter.label}
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
                אין מוצרים התואמים לסינון. נסו להסיר פילטר אחד או יותר.
              </p>
            ) : (
              visibleProducts.map((product, index) => (
                <ProductShelfRow
                  key={product.id}
                  product={product}
                  rank={index + 1}
                  emphasis={getBreadRowEmphasis(product, activeFilters)}
                />
              ))
            )}
          </div>

          <section className="rounded-[1.25rem] border border-black/[0.08] bg-[#FFFFFF]/80 p-6 md:p-8">
            <h2 className="text-xl font-extrabold">איך לקרוא את ההשוואה</h2>
            <ul className="mt-4 space-y-3">
              {howToReadBreadComparison.map((line) => (
                <li key={line} className="flex gap-3 text-sm leading-relaxed text-[#4E5663]">
                  <span className="mt-2 size-1.5 shrink-0 rounded-full bg-[#1F8F6A]" />
                  {line}
                </li>
              ))}
            </ul>
          </section>

          <Link
            href="/hashvaot"
            className="inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition hover:text-[#111318]"
          >
            <ArrowRight className="size-4" aria-hidden />
            חזרה להשוואות
          </Link>
        </HomeContainer>
      </section>
    </main>
  );
}
