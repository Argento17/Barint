/**
 * /p/[barcode] — Canonical per-product page (TASK-471).
 *
 * Server Component. Renders a single product from the LIVE inventory corpus,
 * looked up by barcode (InventoryProductRowVM.sku). Statically generated for
 * every barcode present in the corpus (SSG via generateStaticParams); an
 * unknown barcode 404s via notFound() — never a fabricated page.
 *
 * DISPLAY ONLY: every score/grade/nutrition/ingredient/editorial field is read
 * verbatim from the already-computed BariProductVM (see
 * @/lib/inventory/loader::getProductByBarcode). This route never recomputes,
 * reorders, or rounds anything (View Model v1 boundary).
 *
 * No auth — same public corpus as /catalog and /hashvaot/*.
 */

import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { HomeContainer } from "@/components/home/section-frame";
import { absoluteUrl } from "@/lib/site-url";
import {
  buildBarcodeProductIndex,
  getProductByBarcode,
} from "@/lib/inventory/loader";
import { getComparisonCategory } from "@/lib/comparisons/registry";
import { ScoreChip } from "@/components/shared/score-chip";
import { MethodologyFooter } from "@/components/shared/methodology-footer";
import { NotMedicalAdvice } from "@/components/shared/not-medical-advice";
import { ProductExpansionClient } from "./_expansion-client";

export const dynamicParams = false; // unknown barcode → notFound(), never a fabricated page
export const dynamic = "force-static";

interface PageParams {
  barcode: string;
}

// ── SSG: one static path per barcode in the live corpus ──────────────────────
export function generateStaticParams(): PageParams[] {
  const index = buildBarcodeProductIndex();
  return Array.from(index.keys()).map((barcode) => ({ barcode }));
}

// ── Metadata (Hebrew title/description, OG/twitter cards) ────────────────────
export async function generateMetadata({
  params,
}: {
  params: Promise<PageParams>;
}): Promise<Metadata> {
  const { barcode } = await params;
  const entry = getProductByBarcode(barcode);
  if (!entry) return {};

  const { row, detail } = entry;
  const title = `${detail.name} · ברי`;
  const scoreLine =
    detail.score != null && detail.grade != null
      ? `ציון ${Math.round(detail.score)}, דרגה ${detail.grade}.`
      : "המוצר טרם נוקד.";
  const description = `${detail.name}${row.brand ? ` מבית ${row.brand}` : ""} · ${row.categoryNameHe} ב-Bari. ${scoreLine}`.trim();
  const url = absoluteUrl(`/p/${barcode}`);

  return {
    title,
    description,
    alternates: { canonical: url },
    openGraph: {
      title,
      description,
      url,
      type: "website",
      locale: "he_IL",
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
    },
  };
}

// ── Page ──────────────────────────────────────────────────────────────────────
export default async function ProductPage({
  params,
}: {
  params: Promise<PageParams>;
}) {
  const { barcode } = await params;
  const entry = getProductByBarcode(barcode);
  if (!entry) notFound();

  const { row, detail } = entry;
  const categoryDef = getComparisonCategory(row.categoryId);
  const methodologyLines = [...categoryDef.getPageData().methodologyLines];

  return (
    <main
      className={cn(
        "relative min-h-screen bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="max-w-3xl py-8 md:py-12">
        <div dir="rtl" className="space-y-5">
          {/* Back-link to category comparison page */}
          <Link
            href={row.comparisonHref}
            className="inline-flex items-center gap-1.5 text-sm font-medium transition-colors"
            style={{ color: "var(--fg3, #5E6560)" }}
          >
            <span aria-hidden>→</span>
            חזרה ל{row.categoryNameHe}
          </Link>

          {/* Header card: image, name, brand, category, score */}
          <section
            className="rounded-[18px] border bg-white p-5"
            style={{
              borderColor: "var(--hairline, rgba(17,19,24,0.08))",
              boxShadow: "var(--shadow-card, 0 2px 12px -6px rgba(17,19,24,0.08))",
            }}
          >
            <div className="flex items-start gap-4">
              <ProductHero imageUrl={detail.imageUrl} name={detail.name} />

              <div className="min-w-0 flex-1">
                <p
                  className="text-xs font-bold uppercase tracking-[0.2em]"
                  style={{ color: "var(--fg3, #5E6560)" }}
                >
                  <Link
                    href={row.comparisonHref}
                    className="hover:underline"
                    style={{ color: "#167A58" }}
                  >
                    {row.categoryNameHe}
                  </Link>
                </p>
                <h1
                  className="mt-1 font-extrabold tracking-tight wrap-break-word"
                  style={{
                    fontSize: "clamp(20px, 4vw, 28px)",
                    letterSpacing: "-0.03em",
                    color: "#111318",
                  }}
                >
                  {detail.name}
                </h1>
                {row.brand &&
                !detail.name.toLowerCase().includes(row.brand.toLowerCase()) ? (
                  <p
                    className="mt-1 text-sm font-medium"
                    style={{ color: "#167A58" }}
                  >
                    {row.brand}
                  </p>
                ) : null}
              </div>

              <div className="shrink-0">
                <ScoreChip score={detail.score} grade={detail.grade} />
              </div>
            </div>

            {/* Signed-off editorial verdict, rendered verbatim */}
            {detail.rowVerdict?.trim() ? (
              <p
                className="mt-4 text-[13px] leading-[1.55]"
                style={{ color: "#2F3531" }}
              >
                {detail.rowVerdict}
              </p>
            ) : detail.insightLine ? (
              <p
                className="mt-4 text-[13px] leading-[1.55]"
                style={{ color: "#2F3531" }}
              >
                {detail.insightLine}
              </p>
            ) : null}
          </section>

          {/* Full expansion: assessment, nutrition, ingredients — same component
              the comparison + catalog pages use. Rendered permanently open here
              (no collapse affordance makes sense on a standalone product page). */}
          <section
            className="rounded-[18px] border bg-white"
            style={{
              borderColor: "var(--hairline, rgba(17,19,24,0.08))",
              boxShadow: "var(--shadow-card, 0 2px 12px -6px rgba(17,19,24,0.08))",
            }}
          >
            <div className="pt-4">
              <ProductExpansionClient detail={detail} categoryId={row.categoryId} />
            </div>
          </section>

          {/* Category methodology, verbatim from the category definition */}
          <MethodologyFooter lines={methodologyLines} wide />
          <NotMedicalAdvice className="px-4 -mt-3" />
        </div>
      </HomeContainer>
    </main>
  );
}

// ── Product hero image (large, with letter-tile fallback) ────────────────────
function ProductHero({
  imageUrl,
  name,
}: {
  imageUrl: string | null;
  name: string;
}) {
  const initial = name.trim()[0] ?? "?";

  if (imageUrl) {
    return (
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src={imageUrl}
        alt=""
        className="shrink-0 rounded-2xl object-contain"
        style={{
          width: 84,
          height: 84,
          background: "var(--surface-neutral, #F2F2ED)",
          border: "1px solid rgba(17,19,24,0.07)",
        }}
      />
    );
  }

  return (
    <span
      className="inline-flex shrink-0 items-center justify-center rounded-2xl font-extrabold"
      style={{
        width: 84,
        height: 84,
        background: "var(--surface-neutral, #F2F2ED)",
        border: "1px solid rgba(17,19,24,0.07)",
        color: "var(--fg2, #4E5663)",
        fontSize: 30,
      }}
      aria-hidden="true"
    >
      {initial}
    </span>
  );
}
