"use client";

import { Fragment } from "react";
import Link from "next/link";
import { ArrowLeft, ChevronLeft } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

import { UpfArticleHero } from "@/components/blog/upf-article-hero";
import { UpfConditionsGrid } from "@/components/blog/upf-conditions-grid";
import { UpfConfidenceLadder } from "@/components/blog/upf-confidence-ladder";
import { UpfSchematicSplit } from "@/components/blog/upf-schematic-split";
import { UpfEmulsifierSpectrum } from "@/components/blog/upf-emulsifier-spectrum";
import { UpfMechanismList } from "@/components/blog/upf-mechanism-list";
import { HomeContainer } from "@/components/home/section-frame";
import { HASHVAOT_HREF, upfArticle } from "@/lib/blog/upf-article-content";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

type Section = {
  id: string;
  eyebrowLabel: string;
  title: string;
  paragraphs: string[];
  infographicAfterParagraph?: number;
  infographic?: "conditions" | "confidence" | "schematic" | "spectrum";
  afterInfographicLead?: string;
  mechItems?: { id: string; title: string; text: string }[];
};

const INFOGRAPHIC_COMPONENTS = {
  conditions: UpfConditionsGrid,
  confidence: UpfConfidenceLadder,
  schematic: UpfSchematicSplit,
  spectrum: UpfEmulsifierSpectrum,
} as const;

/**
 * Renders inline `**bold**` markers (as inline emphasis) and inline `[n]`
 * citation markers (as superscript links to the reference list) from the
 * vetted draft's own text, without dangerouslySetInnerHTML. Copy itself is
 * ported verbatim from the approved draft -- this only interprets markup the
 * draft already contains.
 */
function RichParagraph({ text, className }: { text: string; className?: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*|\[\d+\])/g).filter(Boolean);
  return (
    <p className={className}>
      {parts.map((part, i) => {
        if (part.startsWith("**") && part.endsWith("**")) {
          return (
            <strong key={i} className="font-extrabold text-[#111318]">
              {part.slice(2, -2)}
            </strong>
          );
        }
        const citeMatch = /^\[(\d+)\]$/.exec(part);
        if (citeMatch) {
          const n = citeMatch[1];
          return (
            <a
              key={i}
              href={`#ref-${n}`}
              className="mx-0.5 font-mono text-[0.7em] font-bold text-[#167A58] align-super no-underline"
            >
              [{n}]
            </a>
          );
        }
        return <Fragment key={i}>{part}</Fragment>;
      })}
    </p>
  );
}

function ArticleSection({
  section,
  tone,
}: {
  section: Section;
  tone: "cream" | "white";
}) {
  const reduceMotion = useReducedMotion();
  const InfographicComponent = section.infographic ? INFOGRAPHIC_COMPONENTS[section.infographic] : null;
  const infographicIndex = section.infographicAfterParagraph ?? -1;

  return (
    <section
      id={section.id}
      className={cn(
        "border-t border-black/6 py-10 md:py-14",
        tone === "white" ? "bg-[#FFFFFF]" : "bg-[#F7F7F2]",
      )}
    >
      <HomeContainer>
        <div className="mx-auto max-w-3xl">
          <header className="mb-6 text-right">
            <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#167A58]">
              {section.eyebrowLabel}
            </p>
            <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
              {section.title}
            </h2>
          </header>
          <div className="space-y-4">
            {section.paragraphs.map((p, i) => (
              <Fragment key={i}>
                <motion.div
                  initial={reduceMotion ? false : { opacity: 0, y: 6 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-30px" }}
                  transition={{ duration: 0.35, delay: Math.min(i, 3) * 0.03 }}
                >
                  <RichParagraph
                    text={p}
                    className="text-base leading-[1.85] text-[#111318] md:text-lg"
                  />
                </motion.div>
                {InfographicComponent && i === infographicIndex ? (
                  <div className="py-2">
                    <InfographicComponent />
                  </div>
                ) : null}
              </Fragment>
            ))}
          </div>

          {section.afterInfographicLead && section.mechItems ? (
            <div className="mt-8">
              <UpfMechanismList lead={section.afterInfographicLead} items={section.mechItems} />
            </div>
          ) : null}
        </div>
      </HomeContainer>
    </section>
  );
}

function RecentArticleCard({
  href,
  title,
  description,
  category,
  readTime,
  cta,
  comingSoon,
}: {
  href: string;
  title: string;
  description: string;
  category: string;
  readTime: string;
  cta: string;
  comingSoon?: boolean;
}) {
  return (
    <li className="rounded-[1.1rem] border border-black/[0.07] bg-[#FFFFFF] p-5">
      <p className="text-[0.65rem] font-bold uppercase tracking-[0.12em] text-[#5E6672]">
        {category} · {readTime}
      </p>
      <h3 className="mt-2 text-base font-extrabold leading-snug tracking-[-0.02em] text-[#111318]">
        {title}
      </h3>
      <p className="mt-2 text-sm leading-relaxed text-[#4E5663]">{description}</p>
      {comingSoon ? (
        <p className="mt-4 text-xs font-bold text-[#5E6672]">בקרוב</p>
      ) : (
        <Link
          href={href}
          className="mt-4 inline-flex items-center gap-1.5 text-xs font-bold text-[#167A58] hover:underline"
        >
          {cta}
          <ChevronLeft className="size-3.5" aria-hidden />
        </Link>
      )}
    </li>
  );
}

export function UpfArticle() {
  const article = upfArticle as unknown as {
    sections: Section[];
    disclaimer: { title: string; text: string };
    references: {
      id: string;
      text: string;
      title: string;
      journal: string;
      citation: string;
      doi: string;
      pmid: string;
    }[];
    conclusion: { cta: string };
    recentAnalyses: {
      title: string;
      items: {
        slug: string;
        href: string;
        title: string;
        description: string;
        category: string;
        readTime: string;
        cta: string;
        comingSoon?: boolean;
      }[];
    };
  };

  return (
    <div className={cn("bg-[#F7F7F2] text-[#111318]", siteHeaderOffsetClass)}>
      <article>
        <UpfArticleHero />

        {/* Body sections -- ported verbatim from the approved draft (TASK-502
            content draft v2), with the 4 owner-approved infographics inset at
            the same points the visual spec places them. */}
        {article.sections.map((section, i) => (
          <ArticleSection key={section.id} section={section} tone={i % 2 === 0 ? "cream" : "white"} />
        ))}

        {/* Important note (disclaimer) */}
        <HomeContainer className="py-8 md:py-10">
          <div className="mx-auto max-w-3xl">
            <div className="rounded-[1rem] border border-black/6 bg-[#EDF4EF] p-5 md:p-6" dir="rtl">
              <h2 className="mb-2 text-base font-extrabold text-[#111318]">{article.disclaimer.title}</h2>
              <p className="text-sm leading-relaxed text-[#4E5663]">{article.disclaimer.text}</p>
            </div>
          </div>
        </HomeContainer>

        {/* References */}
        <HomeContainer className="pb-8">
          <div className="mx-auto max-w-3xl border-t border-black/[0.08] pt-8">
            <p className="mb-5 font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#167A58]">
              מקורות
            </p>
            <ol className="flex flex-col gap-4" dir="ltr">
              {article.references.map((ref) => (
                <li key={ref.id} id={`ref-${ref.id}`} className="grid grid-cols-[1.75rem_1fr] gap-3 text-left">
                  <span className="font-mono text-xs font-bold text-[#167A58]">[{ref.id}]</span>
                  <p className="text-[13px] leading-[1.6] text-[#4E5663]">
                    {ref.text} <span className="font-semibold text-[#111318]">{ref.title}</span>{" "}
                    <em className="not-italic font-medium">{ref.journal}.</em> {ref.citation}{" "}
                    <span className="font-mono text-xs text-[#5E6672]">
                      DOI:{" "}
                      <a
                        href={`https://doi.org/${ref.doi}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[#167A58] hover:underline"
                      >
                        {ref.doi}
                      </a>{" "}
                      · PMID:{" "}
                      <a
                        href={`https://pubmed.ncbi.nlm.nih.gov/${ref.pmid}/`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[#167A58] hover:underline"
                      >
                        {ref.pmid}
                      </a>
                    </span>
                  </p>
                </li>
              ))}
            </ol>
          </div>
        </HomeContainer>

        {/* Final CTA */}
        <HomeContainer className="space-y-10 py-8 md:space-y-14 md:py-10">
          <div className="mx-auto max-w-4xl space-y-10 md:space-y-14">
            <aside className="relative overflow-hidden rounded-[1.35rem] border border-[#1F8F6A]/22 bg-[#111318] p-7 md:p-9">
              <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
                <div className="max-w-xl space-y-2 text-right">
                  <h3 className="text-xl font-extrabold tracking-[-0.03em] text-[#F7F7F2] md:text-2xl">
                    רוצים לראות השוואות נוספות?
                  </h3>
                  <p className="text-sm leading-relaxed text-[#C8CDC9] md:text-base">
                    דגנים, גבינות, חמאה, יוגורטים, חומוס ועוד — כל קטגוריה עם ניתוח מלא ומנוע השוואה אינטראקטיבי.
                  </p>
                </div>
                <Link
                  href={HASHVAOT_HREF}
                  className="inline-flex shrink-0 items-center justify-center gap-2 rounded-full bg-[#167A58] px-6 py-3 text-sm font-bold text-[#F7F7F2] shadow-md shadow-[#1F8F6A]/25 transition-[transform,box-shadow] duration-300 hover:-translate-y-0.5"
                >
                  {article.conclusion.cta}
                  <ChevronLeft className="size-4" aria-hidden />
                </Link>
              </div>
            </aside>

            {/* Recent articles */}
            <section id="recent">
              <h2 className="mb-6 text-xl font-extrabold tracking-[-0.03em] text-[#111318]">
                {article.recentAnalyses.title}
              </h2>
              <ul className="grid gap-4 sm:grid-cols-3">
                {article.recentAnalyses.items.map((item) => (
                  <RecentArticleCard key={item.slug} {...item} />
                ))}
              </ul>
            </section>
          </div>
        </HomeContainer>

        <HomeContainer className="pb-14">
          <footer className="mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-4 border-t border-black/6 pt-8">
            <Link
              href={HASHVAOT_HREF}
              className="inline-flex items-center gap-2 text-sm font-semibold text-[#167A58] hover:underline"
            >
              כל ניתוחי המדף
              <ArrowLeft className="size-4" aria-hidden />
            </Link>
            <Link href="/blog" className="text-sm font-semibold text-[#4E5663] hover:text-[#111318]">
              חזרה לבלוג
            </Link>
          </footer>
        </HomeContainer>
      </article>
    </div>
  );
}
