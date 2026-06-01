"use client";

import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { ComparisonMoment } from "@/components/snack/comparison-moment";
import { MapSection } from "@/components/snack/map-section";
import { SnackScoreChip } from "@/components/snack/snack-score-chip";
import { SnackShelfProductImage } from "@/components/snack/snack-shelf-product-image";
import { SnackShelfStatBar } from "@/components/snack/snack-shelf-stat-bar";
import { HomeContainer } from "@/components/home/section-frame";
import {
  snackBlogCta,
  snackBlogMap,
  snackShelfIntro,
  snackWellnessComparisons,
  snackWellnessFindings,
  snackWellnessHero,
  snackWellnessSynthesis,
} from "@/lib/blog/snack-editorial-content";
import {
  SNACK_COMPARISON_HREF,
  snackDisplayableProducts,
  snackProducts,
} from "@/lib/comparisons/snack-page-data";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

function getSnack(id: string) {
  return snackProducts.find((item) => item.id === id);
}

export function SnackFlagshipArticle() {
  const heroProducts = snackWellnessHero.productIds
    .map((id) => getSnack(id))
    .filter((item): item is NonNullable<typeof item> => Boolean(item));

  return (
    <main className={cn("min-h-screen bg-[#F7F7F2] text-[#111318]", siteHeaderOffsetClass)}>
      <section className="border-b border-black/[0.06] bg-[#FFFFFF]/80">
        <HomeContainer className="py-12 md:py-16">
          <div className="mx-auto max-w-3xl text-center">
            <h1 className="text-[2rem] font-extrabold leading-tight tracking-[-0.055em] md:text-[2.625rem]">
              {snackWellnessHero.headlineLines.map((line) => (
                <span key={line} className="block">
                  {line}
                </span>
              ))}
            </h1>
            <p className="mt-4 text-lg text-[#4E5663]">{snackWellnessHero.subline}</p>
          </div>

          <div className="mx-auto mt-10 grid max-w-2xl gap-8 md:grid-cols-2">
            {heroProducts.map((product) => (
              <div key={product.id} className="flex flex-col items-center">
                <SnackShelfProductImage product={product} variant="hero" />
                <div className="mt-4">
                  <SnackScoreChip
                    score={product.score}
                    grade={product.grade}
                    displayable={product.displayable}
                    variant="hero"
                  />
                </div>
              </div>
            ))}
          </div>

          <p className="mx-auto mt-8 max-w-xl text-center text-base text-[#313834]">
            {snackWellnessHero.driverSubline}
          </p>
        </HomeContainer>
      </section>

      <HomeContainer className="max-w-3xl space-y-0 py-12 md:py-16">
        <section>
          <p className="text-base leading-8 text-[#313834]">{snackShelfIntro}</p>
          <div className="mt-6">
            <SnackShelfStatBar />
          </div>
        </section>

        <section className="py-12 md:py-16">
          <div className="grid gap-4 md:grid-cols-3">
            {snackWellnessFindings.map((finding) => (
              <article
                key={finding.title}
                className="rounded-[1rem] border border-black/[0.08] bg-[#FFFFFF]/95 p-5"
              >
                <p className="text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                  {finding.tag}
                </p>
                <p className="mt-3 text-[1.25rem] font-bold leading-snug text-[#111318]">
                  {finding.title}
                </p>
                <p className="mt-2 text-sm leading-7 text-[#4E5663]">{finding.body}</p>
              </article>
            ))}
          </div>
        </section>

        <MapSection
          title={snackBlogMap.title}
          caption={snackBlogMap.caption}
          products={snackDisplayableProducts}
          annotatedIds={[...snackBlogMap.annotatedIds]}
          annotations={snackBlogMap.annotations}
        />

        {snackWellnessComparisons.map((moment) => (
          <ComparisonMoment key={moment.title} {...moment} />
        ))}

        <section className="py-12 md:py-16">
          <p className="text-base leading-8 text-[#313834]">{snackWellnessSynthesis}</p>
        </section>

        <section className="border-t border-black/[0.06] py-12 text-center md:py-16">
          <p className="text-sm text-[#4E5663]">{snackBlogCta.line}</p>
          <Link
            href={SNACK_COMPARISON_HREF}
            className="mt-4 inline-flex items-center gap-2 text-base font-bold text-[#1F8F6A] hover:underline"
          >
            {snackBlogCta.button}
            <ChevronLeft className="size-4" aria-hidden />
          </Link>
        </section>

        <section className="pb-16" />
      </HomeContainer>
    </main>
  );
}
