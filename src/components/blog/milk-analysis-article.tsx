"use client";

import Link from "next/link";
import { useState } from "react";
import { motion, useReducedMotion } from "framer-motion";
import { ArrowLeft, ChevronLeft, Layers3 } from "lucide-react";

import { MilkAnalysisHero } from "@/components/blog/milk-analysis-hero";
import { MilkAnalysisHowToRead } from "@/components/blog/milk-analysis-how-to-read";
import { MilkAnalysisInsightBlock } from "@/components/blog/milk-analysis-insight-block";
import { MilkAnalysisScatter } from "@/components/blog/milk-analysis-scatter";
import { MilkAnalysisShelfSpectrum } from "@/components/blog/milk-analysis-shelf-spectrum";
import { MilkAnalysisRecent } from "@/components/blog/milk-analysis-recent";
import { MilkAnalysisSimplicity } from "@/components/blog/milk-analysis-simplicity";
import { ProductThumbnail } from "@/components/comparisons/product-thumbnail";
import { BariGradeBadge } from "@/components/comparisons/bari-grade-badge";
import { HomeContainer } from "@/components/home/section-frame";
import {
  MILK_COMPARISON_HREF,
  getPreviewProducts,
  getPreviewTags,
  milkAnalysisArticle,
} from "@/lib/blog/milk-analysis-content";
import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

function FindingCard({
  title,
  finding,
  whyItMatters,
  index,
  reduceMotion,
}: {
  title: string;
  finding: string;
  whyItMatters: string;
  index: number;
  reduceMotion: boolean | null;
}) {
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
      aria-labelledby={`cta-${variant}`}
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
            id={`cta-${variant}`}
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
          href={MILK_COMPARISON_HREF}
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
  product: MilkComparisonProduct;
  highlighted: boolean;
  onSelect: () => void;
}) {
  const tags = getPreviewTags(product);
  const title = product.displayTitle ?? product.shortName;

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
        <ProductThumbnail
          product={product}
          wrapperClassName="h-[5.5rem] w-[3.75rem] shrink-0 rounded-[1rem] shadow-none"
          imageClassName="p-1"
          imageSizes="60px"
        />
        <div className="min-w-0 flex-1">
          <p className="text-[0.65rem] font-bold text-[#1F8F6A]">{product.productTypeLabel}</p>
          <h3 className="mt-1 text-base font-extrabold leading-snug text-[#111318]">{title}</h3>
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

export function MilkAnalysisArticle() {
  const article = milkAnalysisArticle;
  const previewProducts = getPreviewProducts();
  const [highlighted, setHighlighted] = useState<string>(
    article.productPreview.highlightBarcode
  );
  const reduceMotion = useReducedMotion();

  return (
    <main className={cn("bg-[#F7F7F2] text-[#111318]", siteHeaderOffsetClass)}>
      <article>
        <MilkAnalysisHero />

        {/* Lead — editorial opening */}
        <HomeContainer className="py-10 md:py-14">
          <div className="mx-auto max-w-3xl space-y-5">
            {article.lead.map((p) => (
              <p key={p.slice(0, 24)} className="text-lg leading-[1.8] text-[#111318] md:text-xl">
                {p}
              </p>
            ))}
          </div>
        </HomeContainer>

        <HomeContainer className="pb-4">
          <div className="mx-auto max-w-3xl">
            <MilkAnalysisInsightBlock quote={article.editorialInsights[0]!} index={0} />
          </div>
        </HomeContainer>

        {/* Findings — dominant */}
        <section
          id="findings"
          className="border-y border-black/[0.06] bg-[#FFFFFF] py-14 md:py-20"
        >
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
                  reduceMotion={reduceMotion}
                />
              ))}
            </ul>
          </HomeContainer>
        </section>

        {/* Centerpiece scatter — full width band */}
        <div className="bg-[#F7F7F2] py-14 md:py-20">
          <HomeContainer>
            <div className="mx-auto max-w-[76rem]">
              <MilkAnalysisScatter />
            </div>
          </HomeContainer>
        </div>

        <HomeContainer className="py-8">
          <div className="mx-auto max-w-3xl">
            <MilkAnalysisInsightBlock quote={article.editorialInsights[1]!} index={1} />
          </div>
        </HomeContainer>

        <HomeContainer className="space-y-16 py-8 md:space-y-24 md:py-12">
          <div className="mx-auto max-w-4xl space-y-16 md:space-y-24">
            <MilkAnalysisShelfSpectrum />
            <MilkAnalysisSimplicity />

            <MilkAnalysisInsightBlock quote={article.editorialInsights[2]!} index={2} />

            {/* Product preview */}
            <section id="preview">
              <header className="mb-8">
                <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
                  {article.productPreview.title}
                </h2>
                <p className="mt-3 max-w-2xl text-base leading-relaxed text-[#4E5663]">
                  {article.productPreview.subtitle}
                </p>
              </header>
              <div className="grid gap-3 sm:grid-cols-2">
                {previewProducts.map((product) => (
                  <PreviewCard
                    key={product.barcode}
                    product={product}
                    highlighted={product.barcode === highlighted}
                    onSelect={() => setHighlighted(product.barcode)}
                  />
                ))}
              </div>
            </section>

            <MilkAnalysisHowToRead />

            <ComparisonCta
              variant="primary"
              title={article.ctaPrimary.title}
              description={article.ctaPrimary.description}
              button={article.ctaPrimary.button}
            />

            {/* Conclusion */}
            <section id="conclusion">
              <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
                {article.conclusion.title}
              </h2>
              <div className="mt-6 space-y-4">
                {article.conclusion.paragraphs.map((p) => (
                  <p key={p.slice(0, 20)} className="text-base leading-[1.75] text-[#4E5663] md:text-lg">
                    {p}
                  </p>
                ))}
              </div>
            </section>

            {/* Methodology — light, end */}
            <section id="methodology" className="rounded-[1.15rem] border border-black/[0.06] bg-[#FFFFFF]/60 p-6 md:p-8">
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
              description="כל 18 המוצרים, סינון לפי סוג, ופירוט מוצר-מוצר בדוח ההשוואה."
              button={article.conclusion.cta}
            />

            <MilkAnalysisRecent />
          </div>
        </HomeContainer>

        <HomeContainer className="pb-14">
          <footer className="mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-4 border-t border-black/[0.06] pt-8">
            <Link
              href={MILK_COMPARISON_HREF}
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
