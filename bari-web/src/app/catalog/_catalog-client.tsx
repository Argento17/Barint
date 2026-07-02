"use client";

/**
 * CatalogClient — PowerBI-grade data dashboard for the public /catalog page.
 *
 * Layout: KPI strip → filter toolbar + data grid (ProductTable dashboard mode).
 * All KPI numbers derived live from initialRows at render time.
 *
 * Boundary: NO import from lib/comparisons/* / lib/bsip/* / registry / scoring.
 */

import { useMemo } from "react";

import { CatalogKpiStrip } from "@/components/inventory/catalog-kpi-strip";
import { computeCatalogDashboardMetrics } from "@/components/inventory/catalog-dashboard-metrics";
import { ProductTable } from "@/components/inventory/product-table";
import type {
  BariProductVM,
  InventorySummaryVM,
  InventoryProductRowVM,
} from "@/lib/view-models";

interface CatalogClientProps {
  summary: InventorySummaryVM;
  initialRows: InventoryProductRowVM[];
  detailsById: Record<string, BariProductVM>;
}

export function CatalogClient({ summary, initialRows, detailsById }: CatalogClientProps) {
  const metrics = useMemo(
    () => computeCatalogDashboardMetrics(initialRows),
    [initialRows],
  );

  return (
    <div className="space-y-4 lg:space-y-5" dir="rtl">
      <header className="border-b pb-4" style={{ borderColor: "rgba(17,19,24,0.08)" }}>
        <p
          className="font-mono text-[10px] font-bold uppercase tracking-[0.2em]"
          style={{ color: "var(--fg3, #5E6560)" }}
        >
          BARI CATALOG
        </p>
        <h1
          className="mt-1.5 font-extrabold tracking-tight"
          style={{ fontSize: "clamp(22px, 3.5vw, 28px)", letterSpacing: "-0.04em", color: "#111318" }}
        >
          קטלוג המוצרים
        </h1>
        <p className="mt-1 text-xs font-medium" style={{ color: "var(--fg3, #5E6560)" }}>
          {summary.totalProducts.toLocaleString("he-IL")} מוצרים ·{" "}
          {summary.categoryCount.toLocaleString("he-IL")} קטגוריות
        </p>
      </header>

      <CatalogKpiStrip metrics={metrics} />

      <section
        className="overflow-clip rounded-lg border bg-white shadow-[0_1px_4px_rgba(17,19,24,0.06)]"
        style={{ borderColor: "rgba(17,19,24,0.08)" }}
        aria-label="טבלת מוצרים"
      >
        <div
          className="border-b px-4 py-3 lg:px-5"
          style={{ borderColor: "rgba(17,19,24,0.07)", background: "#FAFAF8" }}
        >
          <h2 className="text-sm font-bold" style={{ color: "#111318" }}>
            כל המוצרים
          </h2>
        </div>
        <div className="px-3 py-4 lg:px-5 lg:py-4">
          <ProductTable
            rows={initialRows}
            variant="public"
            appearance="dashboard"
            detailsById={detailsById}
          />
        </div>
      </section>
    </div>
  );
}
