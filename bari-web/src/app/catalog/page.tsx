/**
 * /catalog — Public Consumer Product Catalog
 *
 * Server Component — NO auth. Renders UNDER the standard site <SiteHeader/> (from the
 * root layout), exactly like /hashvaot — one consistent site navbar, no navy dashboard
 * chrome. The internal /admin/inventory keeps the navy AppShell; this public page does not.
 *
 * Data: loaded server-side from @/lib/inventory/loader (no auth). Rows passed to
 * CatalogClient; filtering/sorting is client-side.
 *
 * View-model isolation: the loader call is SERVER-SIDE ONLY (this Server Component).
 * Client components under @/components/inventory/ import ONLY from @/lib/view-models.
 *
 * Feature A: product detail expansion. Full BariProductVM map (464 KB serialized,
 * measured 2026-07-01) embedded in page props — under the 1.5 MB threshold.
 * Expansions render lazily on open; only data weight matters at page load.
 */

import type { Metadata } from "next";

import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { HomeContainer } from "@/components/home/section-frame";
import { BlogEditorialBackdrop } from "@/components/blog/blog-editorial-backdrop";
import {
  buildInventoryRows,
  buildInventorySummary,
  buildInventoryProductDetails,
} from "@/lib/inventory/loader";
import { CatalogClient } from "./_catalog-client";
import type { BariProductVM } from "@/lib/view-models";

export const dynamic = "force-dynamic";
export const revalidate = 0;

export const metadata: Metadata = {
  title: "קטלוג המוצרים | Bari",
  description:
    "המוצרים שבארי כבר בדקה, מדורגים לפי קטגוריה, רשת ואיכות תזונתית. הקטלוג גדל כל שבוע.",
  robots: { index: true, follow: true },
};

export default function CatalogPage() {
  // Server-side data load — no auth dependency; same loader used by the admin dashboard.
  const rows = buildInventoryRows();
  const summary = buildInventorySummary(rows);

  // Feature A: Full product details for expansion panels.
  // Map → plain object for serialization across the Server→Client boundary.
  // 464 KB total (measured) — embedded in page props (≤ 1.5 MB threshold).
  const detailsMap = buildInventoryProductDetails();
  const detailsById: Record<string, BariProductVM> = Object.fromEntries(detailsMap);

  return (
    <main
      className={cn(
        "relative overflow-hidden min-h-screen bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <BlogEditorialBackdrop />

      <HomeContainer className="relative py-8 md:py-12">
        <CatalogClient summary={summary} initialRows={rows} detailsById={detailsById} />
      </HomeContainer>
    </main>
  );
}
