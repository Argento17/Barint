"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { motion, useReducedMotion } from "framer-motion";
import { ArrowLeft, ArrowRight, ChevronLeft, Layers3 } from "lucide-react";

import { BariGradeBadge } from "@/components/comparisons/bari-grade-badge";
import { HomeContainer } from "@/components/home/section-frame";
import {
  BREAD_COMPARISON_HREF,
  breadAnalysisArticle,
  getBreadBlogMetaLine,
  getBreadPreviewProducts,
  getBreadPreviewTags,
} from "@/lib/blog/bread-analysis-content";
import { breadEditorial } from "@/lib/comparisons/bread-editorial-content";
import { ARCHETYPE_META, breadProducts } from "@/lib/comparisons/bread-page-data";
import type { BreadProduct } from "@/lib/comparisons/bread-types";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

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

function BreadProductMark({
  product,
  size = "md",
}: {
  product: BreadProduct;
  size?: "sm" | "md";
}) {
  const meta = ARCHETYPE_META[product.archetype];
  const shellClass = size === "sm" ? "h-20 w-14 rounded-[0.9rem]" : "h-24 w-[4.5rem] rounded-[1rem]";

  return (
    <div
      className={cn(
        "relative shrink-0 overflow-hidden border border-black/[0.07] bg-[#FFFDFC] shadow-[0_12px_30px_-26px_rgba(17,19,24,0.28)]",
        shellClass
      )}
      aria-hidden
    >
      <div className="absolute inset-x-0 top-0 h-2.5" style={{ backgroundColor: meta?.color ?? "#7A817C" }} />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(255,255,255,0.94),transparent_48%)]" />
      <div className="relative flex h-full flex-col justify-between px-2 py-3 text-center">
        <div>
          <p className="text-[0.46rem] font-semibold uppercase tracking-[0.12em] text-[#7A817C]">
            {categoryLabel(product.category)}
          </p>
          <p className="mt-2 line-clamp-2 text-[0.52rem] font-bold leading-tight text-[#111318]">
            {product.brand}
          </p>
        </div>
        <div>
          <div className="mx-auto mb-2 h-px w-7 bg-black/[0.08]" />
          <p className="line-clamp-3 text-[0.42rem] leading-tight text-[#7A817C]">{product.name_he}</p>
        </div>
      </div>
    </div>
  );
}

function BreadAnalysisHero() {
  const { hero, disclaimer } = breadAnalysisArticle;

  return (
    <header
      className={cn(
        "relative overflow-hidden border-b border-black/[0.06] bg-[#FFFFFF]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="flex flex-col py-8 md:py-12">
        <Link
          href="/blog"
          className="mb-2 inline-flex shrink-0 items-center gap-2 text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
        >
          <ArrowRight className="size-4" aria-hidden />
          חזרה לבלוג
        </Link>

        <div className="flex max-w-3xl flex-col justify-center text-right">
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#1F8F6A]">
            {hero.eyebrow}
          </p>
          <h1 className="mt-3 text-balance text-3xl font-extrabold leading-[1.1] tracking-[-0.05em] text-[#111318] md:text-4xl lg:text-5xl">
            {hero.title}
          </h1>
          <p className="mt-3 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
            {hero.subtitle}
          </p>
          <p className="mt-2 text-sm text-[#7A817C]">{hero.meta}</p>

          <div className="mt-6 flex gap-8 border-t border-black/[0.06] pt-5">
            <div>
              <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">32</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                מוצרים נותחו
              </p>
            </div>
            <div>
              <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">6</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                דפוסים חוזרים
              </p>
            </div>
            <div>
              <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">5</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                תחומי בדיקה
              </p>
            </div>
          </div>

          <p className="mt-4 max-w-xl text-xs leading-relaxed text-[#7A817C] md:text-sm">
            {disclaimer}
          </p>
        </div>
      </HomeContainer>
    </header>
  );
}

function BreadInsightBlock({ quote, index = 0 }: { quote: string; index?: number }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.blockquote
      initial={reduceMotion ? false : { opacity: 0, x: 12 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.5, delay: index * 0.05 }}
      className="relative border-r-4 border-[#1F8F6A] bg-[#FFFFFF] px-6 py-5 md:px-8"
    >
      <p className="text-lg font-semibold leading-snug tracking-[-0.02em] text-[#111318] md:text-xl">
        {quote}
      </p>
    </motion.blockquote>
  );
}

function FindingCard({
  title,
  finding,
  whyItMatters,
  index,
}: {
  title: string;
  finding: string;
  whyItMatters: string;
  index: number;
}) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.li
      initial={reduceMotion ? false : { opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.05 }}
      className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] px-6 py-6 md:px-8 md:py-7"
    >
      <h3 className="text-xl font-extrabold tracking-[-0.03em] text-[#111318] md:text-2xl">
        {title}
      </h3>
      <p className="mt-3 text-base leading-relaxed text-[#111318]">{finding}</p>
      <p className="mt-4 text-sm leading-relaxed text-[#4E5663]">
        <span className="font-bold text-[#1F8F6A]">למה זה משנה · </span>
        {whyItMatters}
      </p>
    </motion.li>
  );
}

function ComparisonCta({
  title,
  description,
  button,
  variant = "primary",
}: {
  title: string;
  description: string;
  button: string;
  variant?: "primary" | "final";
}) {
  return (
    <aside
      className={cn(
        "relative overflow-hidden rounded-[1.35rem] border p-7 md:p-9",
        variant === "primary"
          ? "border-[#1F8F6A]/18 bg-gradient-to-bl from-[#E8F5EF]/80 via-[#FFFFFF] to-[#F7F7F2]"
          : "border-[#1F8F6A]/22 bg-[#111318] text-[#F7F7F2]"
      )}
    >
      <div className="relative flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
        <div className="max-w-xl space-y-2 text-right">
          {variant === "primary" ? (
            <p className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-[0.16em] text-[#1F8F6A]">
              <Layers3 className="size-4" aria-hidden />
              השוואות · אינטראקטיבי
            </p>
          ) : null}
          <h3
            className={cn(
              "text-xl font-extrabold tracking-[-0.03em] md:text-2xl",
              variant === "final" ? "text-[#F7F7F2]" : "text-[#111318]"
            )}
          >
            {title}
          </h3>
          <p
            className={cn(
              "text-sm leading-relaxed md:text-base",
              variant === "final" ? "text-[#C8CDC9]" : "text-[#4E5663]"
            )}
          >
            {description}
          </p>
        </div>
        <Link
          href={BREAD_COMPARISON_HREF}
          className={cn(
            "inline-flex shrink-0 items-center justify-center gap-2 rounded-full px-6 py-3 text-sm font-bold transition-[transform,box-shadow] duration-300 hover:-translate-y-0.5",
            variant === "final"
              ? "bg-[#1F8F6A] text-[#F7F7F2] shadow-md shadow-[#1F8F6A]/25"
              : "bg-[#1F8F6A] text-[#F7F7F2] shadow-sm shadow-[#1F8F6A]/20"
          )}
        >
          {button}
          <ChevronLeft className="size-4" aria-hidden />
        </Link>
      </div>
    </aside>
  );
}

function PreviewCard({
  product,
  highlighted,
  onSelect,
}: {
  product: BreadProduct;
  highlighted: boolean;
  onSelect: () => void;
}) {
  const tags = getBreadPreviewTags(product);

  return (
    <button
      type="button"
      onClick={onSelect}
      className={cn(
        "group w-full rounded-[1.2rem] border p-4 text-right transition-[border-color,box-shadow,background-color] duration-300 md:p-5",
        highlighted
          ? "border-[#1F8F6A]/28 bg-[#1F8F6A]/[0.05] shadow-[0_8px_32px_-20px_rgba(31,143,106,0.25)]"
          : "border-black/[0.07] bg-[#FFFFFF] hover:border-[#1F8F6A]/18 hover:shadow-sm"
      )}
    >
      <div className="flex items-start gap-4">
        <BreadProductMark product={product} />
        <div className="min-w-0 flex-1">
          <p className="text-[0.65rem] font-bold text-[#1F8F6A]">{ARCHETYPE_META[product.archetype].labelShort}</p>
          <h3 className="mt-1 text-base font-extrabold leading-snug text-[#111318]">{product.name_he}</h3>
          <div className="mt-3 flex items-center gap-2">
            <span className="text-[0.65rem] font-bold text-[#7A817C]">ציון Bari</span>
            <BariGradeBadge
              score={product.score}
              grade={product.grade}
              gradeLabel={product.grade_label}
              size="sm"
            />
          </div>
          <div className="mt-3 flex flex-wrap gap-1.5">
            {tags.map((tag) => (
              <span
                key={tag}
                className="rounded-md border border-black/[0.06] bg-[#F7F7F2]/90 px-2 py-0.5 text-[0.65rem] font-semibold text-[#4E5663]"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>
    </button>
  );
}

function BreadHowToRead() {
  const { howToRead } = breadAnalysisArticle;
  const reduceMotion = useReducedMotion();

  return (
    <section id="how-to-read" className="scroll-mt-24">
      <h2 className="text-xl font-extrabold tracking-[-0.03em] text-[#111318] md:text-2xl">
        {howToRead.title}
      </h2>
      <p className="mt-3 max-w-2xl text-base font-medium leading-relaxed text-[#111318]">
        {howToRead.lead}
      </p>

      <div className="mt-6 overflow-hidden rounded-[1.15rem] border border-black/[0.07] bg-[#FFFFFF]">
        <table className="w-full text-right text-sm">
          <tbody>
            {howToRead.rows.map((row, i) => (
              <motion.tr
                key={row.label}
                initial={reduceMotion ? false : { opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="border-b border-black/[0.05] last:border-0"
              >
                <th className="w-[28%] bg-[#F7F7F2]/80 px-4 py-4 align-top text-xs font-extrabold text-[#1F8F6A] md:px-5">
                  {row.label}
                </th>
                <td className="px-4 py-4 leading-relaxed text-[#4E5663] md:px-5">{row.text}</td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function ArchetypeCard({
  archetype,
  index,
}: {
  archetype: (typeof breadEditorial.archetypes)[number];
  index: number;
}) {
  const reduceMotion = useReducedMotion();
  const meta = ARCHETYPE_META[archetype.id];

  return (
    <motion.li
      initial={reduceMotion ? false : { opacity: 0, y: 10 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.05 }}
      className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] p-5"
    >
      <div className="mb-4 h-1 w-10 rounded-full" style={{ backgroundColor: meta.color }} />
      <p className="text-xl font-extrabold tracking-[-0.03em] text-[#111318]">{archetype.label}</p>
      <p className="mt-2 text-sm font-medium text-[#7A817C]">{archetype.subtitle}</p>
      <p className="mt-4 text-sm leading-relaxed text-[#4E5663]">{archetype.insight}</p>
      <p className="mt-4 border-t border-black/[0.06] pt-4 text-sm leading-relaxed text-[#4E5663]">
        <span className="font-semibold text-[#111318]">בדרך כלל:</span> {archetype.tradeoff}
      </p>
    </motion.li>
  );
}

function LookalikeCard({
  item,
  index,
}: {
  item: (typeof breadEditorial.lookalikes)[number];
  index: number;
}) {
  const reduceMotion = useReducedMotion();
  const leftProduct = breadProducts.find((product) => product.name_he === item.left.name);
  const rightProduct = breadProducts.find((product) => product.name_he === item.right.name);

  return (
    <motion.div
      initial={reduceMotion ? false : { opacity: 0, y: 10 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.05 }}
      className="overflow-hidden rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF]"
    >
      <div className="border-b border-black/[0.06] px-5 py-4">
        <h3 className="text-lg font-extrabold leading-relaxed tracking-[-0.03em] text-[#111318]">
          {item.headline}
        </h3>
      </div>

      <div className="grid gap-px bg-black/[0.06] md:grid-cols-2">
        {[item.left, item.right].map((side, sideIndex) => {
          const product = sideIndex === 0 ? leftProduct : rightProduct;
          return (
            <div key={side.name} className="bg-[#FFFFFF] p-5 text-right">
              <div className="flex items-start gap-4">
                {product ? <BreadProductMark product={product} size="sm" /> : null}
                <div className="min-w-0 flex-1">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-[0.68rem] font-semibold uppercase tracking-[0.18em] text-[#7A817C]">
                        {side.label}
                      </p>
                      <p className="mt-1 text-base font-bold leading-snug text-[#111318]">
                        {side.name}
                      </p>
                    </div>
                    <BariGradeBadge
                      score={side.score}
                      grade={side.grade}
                      gradeLabel={side.grade === "A" ? "מצוין" : side.grade === "B" ? "טוב" : side.grade === "C" ? "בינוני" : side.grade === "D" ? "חלש" : "נמוך"}
                      size="sm"
                    />
                  </div>
                  <p className="mt-4 text-sm leading-relaxed text-[#4E5663]">{side.detail}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="space-y-3 border-t border-black/[0.06] bg-[#F7F7F2]/70 px-5 py-4 text-right">
        <p className="text-sm leading-relaxed text-[#4E5663]">
          <span className="font-semibold text-[#111318]">למה נפתח פער: </span>
          {item.insight}
        </p>
        <p className="rounded-[1rem] border border-[#1F8F6A]/12 bg-[#FFFFFF]/85 px-4 py-3 text-sm leading-relaxed text-[#111318]">
          {item.takeaway}
        </p>
      </div>
    </motion.div>
  );
}

export function BreadAnalysisArticle() {
  const article = breadAnalysisArticle;
  const previewProducts = getBreadPreviewProducts();
  const [highlighted, setHighlighted] = useState(previewProducts[0]?.id ?? "");
  const reduceMotion = useReducedMotion();

  return (
    <main className={cn("bg-[#F7F7F2] text-[#111318]", siteHeaderOffsetClass)}>
      <article>
        <BreadAnalysisHero />

        <HomeContainer className="py-10 md:py-14">
          <div className="mx-auto max-w-3xl space-y-5">
            {article.lead.map((paragraph) => (
              <p key={paragraph.slice(0, 28)} className="text-lg leading-[1.8] text-[#111318] md:text-xl">
                {paragraph}
              </p>
            ))}
          </div>
        </HomeContainer>

        <HomeContainer className="pb-4">
          <div className="mx-auto max-w-3xl">
            <BreadInsightBlock quote={article.editorialInsights[0]!} index={0} />
          </div>
        </HomeContainer>

        <section className="border-y border-black/[0.06] bg-[#FFFFFF] py-14 md:py-20">
          <HomeContainer>
            <header className="mx-auto mb-10 max-w-3xl text-right md:mb-14">
              <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
                תובנות מהשטח
              </p>
              <h2 className="mt-2 text-3xl font-extrabold tracking-[-0.05em] text-[#111318] md:text-4xl">
                {article.findings.title}
              </h2>
              <p className="mt-4 text-base leading-relaxed text-[#4E5663]">
                {article.findings.subtitle}
              </p>
            </header>
            <ul className="mx-auto flex max-w-3xl flex-col gap-5 md:gap-6">
              {article.findings.items.map((item, i) => (
                <FindingCard
                  key={item.title}
                  title={item.title}
                  finding={item.finding}
                  whyItMatters={item.whyItMatters}
                  index={i}
                />
              ))}
            </ul>
          </HomeContainer>
        </section>

        <HomeContainer className="py-8">
          <div className="mx-auto max-w-3xl">
            <BreadInsightBlock quote={article.editorialInsights[1]!} index={1} />
          </div>
        </HomeContainer>

        <HomeContainer className="space-y-16 py-8 md:space-y-24 md:py-12">
          <div className="mx-auto max-w-5xl space-y-16 md:space-y-24">
            <section id="archetypes">
              <header className="mb-8">
                <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
                  {article.archetypes.title}
                </h2>
                <p className="mt-3 max-w-2xl text-base leading-relaxed text-[#4E5663]">
                  {article.archetypes.subtitle}
                </p>
              </header>
              <ul className="grid gap-4 md:grid-cols-2">
                {breadEditorial.archetypes.map((archetype, index) => (
                  <ArchetypeCard key={archetype.id} archetype={archetype} index={index} />
                ))}
              </ul>
            </section>

            <section id="lookalikes">
              <header className="mb-8">
                <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
                  {article.lookalikes.title}
                </h2>
                <p className="mt-3 max-w-2xl text-base leading-relaxed text-[#4E5663]">
                  {article.lookalikes.subtitle}
                </p>
              </header>
              <div className="grid gap-5 xl:grid-cols-2">
                {breadEditorial.lookalikes.map((item, index) => (
                  <LookalikeCard key={item.id} item={item} index={index} />
                ))}
              </div>
            </section>

            <BreadInsightBlock quote={article.editorialInsights[2]!} index={2} />

            <section id="preview">
              <header className="mb-8">
                <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
                  {article.productPreview.title}
                </h2>
                <p className="mt-3 max-w-2xl text-base leading-relaxed text-[#4E5663]">
                  {article.productPreview.subtitle}
                </p>
                <p className="mt-2 text-sm text-[#7A817C]">{getBreadBlogMetaLine()}</p>
              </header>
              <div className="grid gap-3 sm:grid-cols-2">
                {previewProducts.map((product) => (
                  <PreviewCard
                    key={product.id}
                    product={product}
                    highlighted={product.id === highlighted}
                    onSelect={() => setHighlighted(product.id)}
                  />
                ))}
              </div>
            </section>

            <BreadHowToRead />

            <ComparisonCta
              variant="primary"
              title={article.ctaPrimary.title}
              description={article.ctaPrimary.description}
              button={article.ctaPrimary.button}
            />

            <section id="conclusion">
              <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
                {article.conclusion.title}
              </h2>
              <div className="mt-6 space-y-4">
                {article.conclusion.paragraphs.map((paragraph) => (
                  <p
                    key={paragraph.slice(0, 22)}
                    className="text-base leading-[1.75] text-[#4E5663] md:text-lg"
                  >
                    {paragraph}
                  </p>
                ))}
              </div>
            </section>

            <section
              id="methodology"
              className="rounded-[1.15rem] border border-black/[0.06] bg-[#FFFFFF]/60 p-6 md:p-8"
            >
              <h2 className="text-lg font-extrabold text-[#111318]">{article.methodology.title}</h2>
              <ol className="mt-4 grid gap-3 md:grid-cols-3">
                {article.methodology.steps.map((step, i) => (
                  <li key={step.title} className="list-none text-sm">
                    <span className="font-mono text-xs font-bold text-[#1F8F6A]">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <p className="mt-1 font-bold text-[#111318]">{step.title}</p>
                    <p className="mt-1 leading-relaxed text-[#7A817C]">{step.text}</p>
                  </li>
                ))}
              </ol>
              <p className="mt-4 text-xs leading-relaxed text-[#7A817C]">
                {article.methodology.footnote}
              </p>
            </section>

            <ComparisonCta
              variant="final"
              title={article.conclusion.title}
              description="כל 32 המוצרים, סינון לפי סוגי לחם, ופירוט מוצר-מוצר בדוח ההשוואה."
              button={article.conclusion.cta}
            />
          </div>
        </HomeContainer>

        <HomeContainer className="pb-14">
          <footer className="mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-4 border-t border-black/[0.06] pt-8">
            <Link
              href={BREAD_COMPARISON_HREF}
              className="inline-flex items-center gap-2 text-sm font-semibold text-[#1F8F6A] hover:underline"
            >
              דוח ההשוואה המלא
              <ArrowLeft className="size-4" aria-hidden />
            </Link>
            <Link href="/blog" className="text-sm font-semibold text-[#4E5663] hover:text-[#111318]">
              חזרה לבלוג
            </Link>
          </footer>
        </HomeContainer>
      </article>
    </main>
  );
}
