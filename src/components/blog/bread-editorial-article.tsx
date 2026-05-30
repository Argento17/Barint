"use client";

import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { BreadShelfProductImage } from "@/components/bread/bread-shelf-product-image";
import { BreadConfidencePill } from "@/components/bread/bread-confidence-pill";
import { HomeContainer } from "@/components/home/section-frame";
import {
  breadScoreObservation,
  fermentationSignal,
  formatBreadNumber,
  formatBreadScoreLine,
  getBreadProductById,
} from "@/lib/comparisons/bread-page-data";
import type {
  BreadArticleBlockTone,
  BreadArticleContent,
} from "@/lib/comparisons/bread-types";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

const toneStyles = {
  neutral: "border-black/[0.08] bg-[#FFFFFF]/88 text-[#313834]",
  positive: "border-[#1F8F6A]/16 bg-[#EEF7F2] text-[#1D3A2E]",
  warning: "border-[#C98A00]/18 bg-[#FCF5E6] text-[#5E4B13]",
} as const satisfies Record<BreadArticleBlockTone, string>;

function ProductMetaRow({
  product,
}: {
  product: NonNullable<ReturnType<typeof getBreadProductById>>;
}) {
  const fermentation = fermentationSignal(product.fermentation_status_he);
  const scoreLine = formatBreadScoreLine(product);

  return (
    <div className="mt-3 flex flex-wrap items-start gap-2">
      {scoreLine ? (
        <div className="inline-flex min-w-[7.5rem] flex-col gap-0.5 rounded-[0.85rem] border border-black/[0.08] bg-[#FFFFFF] px-2.5 py-2">
          <span className="text-[0.8rem] font-extrabold tabular-nums leading-none text-[#111318]">
            {scoreLine}
          </span>
          <span className="text-[0.65rem] font-medium leading-4 text-[#5A6170]">
            {breadScoreObservation(product)}
          </span>
        </div>
      ) : (
        <span className="inline-flex rounded-full border border-black/[0.08] bg-[#F3F4F5] px-2.5 py-1 text-[0.68rem] font-bold text-[#5E6672]">
          ללא ציון
        </span>
      )}
      <BreadConfidencePill label={product.confidence_label_he} level={product.confidence_level} />
      <span className="inline-flex items-center rounded-full border border-black/[0.08] bg-[#FFFFFF] px-2.5 py-1 text-[0.68rem] font-semibold text-[#4E5663]">
        סיבים {formatBreadNumber(product.fiber_g, "g")}
      </span>
      <span className="inline-flex items-center gap-1.5 rounded-full border border-black/[0.08] bg-[#F7F7F2] px-2.5 py-1 text-[0.68rem] font-semibold text-[#4E5663]">
        <span aria-hidden>{fermentation.icon}</span>
        {fermentation.label}
      </span>
    </div>
  );
}

function LeadMention({
  productId,
  kicker,
  note,
}: NonNullable<BreadArticleContent["leadMentions"]>[number]) {
  const product = getBreadProductById(productId);
  if (!product) return null;

  return (
    <article className="rounded-[1rem] border border-black/[0.07] bg-[#FFFFFF]/88 px-4 py-3">
      {kicker ? (
        <p className="text-[0.68rem] font-bold uppercase tracking-[0.18em] text-[#1F8F6A]">
          {kicker}
        </p>
      ) : null}
      <p className="mt-1 text-sm font-extrabold tracking-[-0.02em] text-[#111318]">{product.name_he}</p>
      <p className="mt-1.5 text-sm leading-6 text-[#4E5663]">{note}</p>
    </article>
  );
}

function EvidenceItem({
  item,
}: {
  item: Extract<BreadArticleContent["blocks"][number], { type: "evidenceStrip" }>["items"][number];
}) {
  const product = getBreadProductById(item.productId);
  if (!product) return null;

  return (
    <article
      className={cn(
        "rounded-[1.1rem] border bg-[#FFFFFF]/94 p-4",
        toneStyles[item.tone ?? "neutral"]
      )}
    >
      <div className="flex items-start gap-3">
        <BreadShelfProductImage product={product} size="sm" className="shrink-0" />
        <div className="min-w-0 flex-1">
          {item.kicker ? (
            <p className="text-[0.68rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
              {item.kicker}
            </p>
          ) : null}
          <h3 className="mt-1 text-base font-extrabold tracking-[-0.03em] text-[#111318]">
            {product.name_he}
          </h3>
          <p className="mt-2 text-sm leading-6 text-[#313834]">{item.note}</p>
          {item.evidence ? (
            <p className="mt-2 text-xs font-semibold leading-5 text-[#5A6170]">{item.evidence}</p>
          ) : null}
        </div>
      </div>
      <ProductMetaRow product={product} />
    </article>
  );
}

function ComparisonSide({
  side,
}: {
  side: Extract<BreadArticleContent["blocks"][number], { type: "comparison" }>["left"];
}) {
  const product = getBreadProductById(side.productId);
  if (!product) return null;

  return (
    <article className="rounded-[1.15rem] border border-black/[0.08] bg-[#FFFFFF]/94 p-4">
      <div className="flex items-start gap-3">
        <BreadShelfProductImage product={product} size="sm" className="shrink-0" />
        <div className="min-w-0 flex-1">
          <p className="text-[0.68rem] font-bold uppercase tracking-[0.18em] text-[#1F8F6A]">{side.label}</p>
          <h3 className="mt-1 text-base font-extrabold tracking-[-0.03em] text-[#111318]">{product.name_he}</h3>
          {side.evidence ? (
            <p className="mt-2 text-sm leading-6 text-[#313834]">{side.evidence}</p>
          ) : null}
        </div>
      </div>
      <ul className="mt-3 space-y-2 border-t border-black/[0.06] pt-3 text-sm leading-6 text-[#4E5663]">
        {side.points.map((point) => (
          <li key={point} className="flex gap-2">
            <span className="mt-2 size-1.5 shrink-0 rounded-full bg-[#1F8F6A]" aria-hidden />
            <span>{point}</span>
          </li>
        ))}
      </ul>
      <ProductMetaRow product={product} />
    </article>
  );
}

function ArticleBlock({
  block,
}: {
  block: BreadArticleContent["blocks"][number];
}) {
  switch (block.type) {
    case "narrative":
      return (
        <section className={cn("grid gap-4", block.sideNote ? "lg:grid-cols-[minmax(0,2fr)_minmax(220px,0.9fr)]" : "")}>
          <div className="max-w-3xl space-y-4">
            {block.title ? (
              <h2 className="text-[1.7rem] font-extrabold tracking-[-0.045em] text-[#111318]">{block.title}</h2>
            ) : null}
            {block.paragraphs.map((paragraph) => (
              <p key={paragraph} className="text-[1.02rem] leading-8 text-[#313834]">
                {paragraph}
              </p>
            ))}
          </div>
          {block.sideNote ? (
            <aside className="self-start rounded-[1.05rem] border border-black/[0.07] bg-[#FFFFFF]/82 p-4">
              <p className="text-[0.68rem] font-bold uppercase tracking-[0.2em] text-[#7A817C]">
                {block.sideNote.label}
              </p>
              <p className="mt-2 text-sm leading-6 text-[#4E5663]">{block.sideNote.text}</p>
            </aside>
          ) : null}
        </section>
      );
    case "insight":
      return (
        <section className={cn("rounded-[1.25rem] border p-5 md:p-6", toneStyles[block.tone ?? "neutral"])}>
          <p className="text-[0.68rem] font-bold uppercase tracking-[0.22em] text-[#1F8F6A]">{block.eyebrow}</p>
          <div className="mt-2 grid gap-4 lg:grid-cols-[minmax(0,1.5fr)_minmax(0,1fr)]">
            <div>
              <h2 className="text-[1.7rem] font-extrabold tracking-[-0.045em] text-[#111318]">{block.title}</h2>
              <p className="mt-3 text-[1rem] leading-8 text-current">{block.body}</p>
            </div>
            {block.bullets?.length ? (
              <ul className="space-y-3 border-t border-black/[0.06] pt-4 text-sm leading-6 lg:border-t-0 lg:border-r lg:pr-4 lg:pt-0">
                {block.bullets.map((bullet) => (
                  <li key={bullet} className="flex gap-2">
                    <span className="mt-2 size-1.5 shrink-0 rounded-full bg-current" aria-hidden />
                    <span>{bullet}</span>
                  </li>
                ))}
              </ul>
            ) : null}
          </div>
        </section>
      );
    case "evidenceStrip":
      return (
        <section className="rounded-[1.25rem] border border-black/[0.08] bg-[#FFFFFF]/88 p-5 md:p-6">
          <div className="max-w-3xl">
            <h2 className="text-[1.7rem] font-extrabold tracking-[-0.045em] text-[#111318]">{block.title}</h2>
            {block.intro ? (
              <p className="mt-3 text-[1rem] leading-8 text-[#313834]">{block.intro}</p>
            ) : null}
          </div>
          <div
            className={cn(
              "mt-4 grid gap-3",
              block.columns === 3 ? "lg:grid-cols-3" : "md:grid-cols-2"
            )}
          >
            {block.items.map((item) => (
              <EvidenceItem key={`${item.productId}-${item.note}`} item={item} />
            ))}
          </div>
        </section>
      );
    case "comparison":
      return (
        <section className="rounded-[1.25rem] border border-black/[0.08] bg-[#FFFFFF]/92 p-5 md:p-6">
          {block.eyebrow ? (
            <p className="text-[0.68rem] font-bold uppercase tracking-[0.22em] text-[#1F8F6A]">{block.eyebrow}</p>
          ) : null}
          <h2 className="mt-2 text-[1.7rem] font-extrabold tracking-[-0.045em] text-[#111318]">{block.title}</h2>
          {block.intro ? (
            <p className="mt-3 max-w-3xl text-[1rem] leading-8 text-[#313834]">{block.intro}</p>
          ) : null}
          <div className="mt-4 grid gap-3 lg:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] lg:items-start">
            <ComparisonSide side={block.left} />
            <div className="hidden self-center px-2 text-sm font-bold uppercase tracking-[0.26em] text-[#7A817C] lg:block">
              מול
            </div>
            <ComparisonSide side={block.right} />
          </div>
          <p className="mt-4 border-t border-black/[0.06] pt-4 text-sm font-semibold leading-7 text-[#313834]">
            {block.takeaway}
          </p>
        </section>
      );
    case "microShelf":
      return (
        <section className="rounded-[1.15rem] border border-black/[0.08] bg-[#F9F8F4] px-5 py-4">
          <h2 className="text-[1.45rem] font-extrabold tracking-[-0.04em] text-[#111318]">{block.title}</h2>
          {block.intro ? (
            <p className="mt-2 max-w-3xl text-sm leading-7 text-[#4E5663]">{block.intro}</p>
          ) : null}
          <div className="mt-3 grid gap-x-6 gap-y-3 md:grid-cols-2">
            {block.items.map((item) => {
              const product = getBreadProductById(item.productId);
              if (!product) return null;

              return (
                <article key={`${item.productId}-${item.note}`} className="border-t border-black/[0.08] py-3 first:border-t-0 first:pt-0 md:first:border-t">
                  {item.kicker ? (
                    <p className="text-[0.66rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
                      {item.kicker}
                    </p>
                  ) : null}
                  <p className="mt-1 text-sm font-extrabold text-[#111318]">{product.name_he}</p>
                  <p className="mt-1 text-sm leading-6 text-[#4E5663]">{item.note}</p>
                </article>
              );
            })}
          </div>
        </section>
      );
    case "table":
      return (
        <section className="overflow-hidden bg-[#FFFFFF]/95">
          <div className="px-5 py-4">
            <h2 className="text-[1.55rem] font-extrabold tracking-[-0.04em] text-[#111318]">{block.title}</h2>
            {block.note ? (
              <p className="mt-1 text-sm leading-6 text-[#4E5663]">{block.note}</p>
            ) : null}
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full text-right">
              <thead className="bg-[#F7F7F2]/85">
                <tr className="text-sm text-[#5F6762]">
                  <th className="px-4 py-3 font-bold">מוצר</th>
                  <th className="px-4 py-3 font-bold">ציון</th>
                  <th className="px-4 py-3 font-bold">מה בדקנו</th>
                  <th className="px-4 py-3 font-bold">מה למדנו</th>
                </tr>
              </thead>
              <tbody className="bari-zebra-rows">
                {block.rows.map((row) => {
                  const product = getBreadProductById(row.productId);
                  if (!product) return null;

                  return (
                    <tr key={row.productId} className="align-top text-sm odd:bg-[#FFFFFF] even:bg-[#F9F9F9]">
                      <td className="px-4 py-4 font-semibold text-[#111318]">
                        {product.name_he}
                      </td>
                      <td className="px-4 py-4 font-semibold tabular-nums text-[#313834]">{row.score}</td>
                      <td className="px-4 py-4 text-[#4E5663]">{row.whatWeChecked}</td>
                      <td className="px-4 py-4 text-[#4E5663]">{row.whatWeLearned}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      );
    default:
      return null;
  }
}

export function BreadEditorialArticle({ article }: { article: BreadArticleContent }) {
  return (
    <main
      className={cn(
        "relative min-h-screen overflow-hidden bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_60%_45%_at_80%_0%,rgba(31,143,106,0.09),transparent_60%)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.11]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(17,19,24,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(17,19,24,0.06) 1px, transparent 1px)",
          backgroundSize: "28px 28px",
        }}
        aria-hidden
      />

      <HomeContainer className="relative py-8 md:py-10 lg:py-12">
        <header className="max-w-5xl border-b border-black/[0.06] pb-6 md:pb-8">
          <p className="text-[0.7rem] font-bold uppercase tracking-[0.28em] text-[#1F8F6A]">
            {article.eyebrow}
          </p>
          <h1 className="mt-4 text-4xl font-extrabold tracking-[-0.055em] text-[#111318] md:text-[3.2rem] md:leading-[1.05]">
            {article.title}
          </h1>
          <p className="mt-4 max-w-3xl text-xl font-semibold leading-snug tracking-[-0.02em] text-[#313834] md:text-2xl">
            {article.deck}
          </p>
          <p className="mt-4 text-sm text-[#7A817C]">{article.metaLine}</p>
          {article.scopeNote ? (
            <p className="mt-5 max-w-3xl rounded-[1rem] border border-[#1F8F6A]/12 bg-[#FFFFFF]/80 px-4 py-3 text-sm leading-relaxed text-[#4E5663]">
              <span className="font-bold text-[#111318]">מסגרת הניתוח:</span> {article.scopeNote}
            </p>
          ) : null}
          <div className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
            {article.contextStats.map((stat) => (
              <article
                key={`${stat.value}-${stat.label}`}
                className="rounded-[1rem] border border-black/[0.07] bg-[#FFFFFF]/84 px-4 py-3"
              >
                <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">{stat.value}</p>
                <p className="mt-1 text-sm font-semibold text-[#313834]">{stat.label}</p>
                {stat.note ? <p className="mt-1 text-xs leading-5 text-[#7A817C]">{stat.note}</p> : null}
              </article>
            ))}
          </div>
        </header>

        <section className="grid gap-5 pt-6 lg:grid-cols-[minmax(0,2fr)_minmax(250px,0.9fr)]">
          <div className="max-w-3xl space-y-4">
            {article.intro.map((paragraph) => (
              <p key={paragraph} className="text-[1.02rem] leading-8 text-[#313834]">
                {paragraph}
              </p>
            ))}
          </div>
          {article.leadMentions?.length ? (
            <aside className="self-start rounded-[1.1rem] border border-black/[0.08] bg-[#FFFFFF]/86 p-4">
              <p className="text-[0.68rem] font-bold uppercase tracking-[0.22em] text-[#1F8F6A]">
                מוצרים שחזרו בקריאה
              </p>
              <div className="mt-3 space-y-3">
                {article.leadMentions.map((mention) => (
                  <LeadMention key={`${mention.productId}-${mention.note}`} {...mention} />
                ))}
              </div>
            </aside>
          ) : null}
        </section>

        <div className="space-y-5 pt-6 md:space-y-6">
          {article.blocks.map((block, index) => (
            <ArticleBlock key={`${article.slug}-${block.type}-${index}`} block={block} />
          ))}
        </div>

        <footer className="mt-8 flex flex-col gap-4 border-t border-black/[0.06] pt-6 sm:flex-row sm:items-center sm:justify-between">
          <Link
            href={article.ctaHref}
            className="inline-flex items-center gap-2 text-sm font-bold text-[#1F8F6A] hover:underline"
          >
            {article.ctaLabel}
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
