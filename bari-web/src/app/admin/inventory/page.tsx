"use client";

/**
 * /admin/inventory — Internal Inventory Dashboard
 *
 * Auth-gated: redirects to /admin (login) when session check fails.
 * Data: fetches from live auth-gated endpoints:
 *   GET /api/admin/inventory          → InventorySummaryVM
 *   GET /api/admin/inventory/products → { rows, total, page }
 *
 * View-model isolation: NO import from scoring/bsip/registry/comparisons modules.
 * Shared components from @/components/inventory/ (shared with /catalog).
 * Navy AppShell stays admin-only.
 */

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/inventory/app-shell";
import { GradeDonut } from "@/components/inventory/retailer-donut";
import { TopCategoriesCard } from "@/components/inventory/top-categories-card";
import { ProductTable } from "@/components/inventory/product-table";
import type { InventorySummaryVM, InventoryProductRowVM } from "@/lib/view-models";
import type { InventoryProductsResponseVM } from "./_types";

// ── Stat card ─────────────────────────────────────────────────────────────────

function StatCard({ label, value, accent }: { label: string; value: string | number; accent?: boolean }) {
  return (
    <div
      className="rounded-[18px] border bg-white p-5"
      style={{ borderColor: accent ? "rgba(30,122,79,0.18)" : "rgba(17,19,24,0.08)" }}
    >
      <p className="text-xs font-bold uppercase tracking-[0.18em]" style={{ color: "var(--fg3, #5E6560)" }}>
        {label}
      </p>
      <p
        className="mt-1 text-3xl font-extrabold tabular-nums"
        style={{ color: "#111318", fontVariantNumeric: "tabular-nums" }}
      >
        {typeof value === "number" ? value.toLocaleString("he-IL") : value}
      </p>
    </div>
  );
}

function SectionHeading({ children }: { children: React.ReactNode }) {
  return <h2 className="mb-4 text-[15px] font-bold" style={{ color: "#111318" }}>{children}</h2>;
}

function Card({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`rounded-[18px] border bg-white p-5 ${className}`} style={{ borderColor: "rgba(17,19,24,0.08)" }}>
      {children}
    </div>
  );
}

function PageSkeleton() {
  return (
    <div className="space-y-6" aria-busy="true" aria-live="polite">
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => <div key={i} className="h-24 animate-pulse rounded-[18px] bg-[#F2F2ED]" />)}
      </div>
      <div className="grid gap-5 lg:grid-cols-2">
        <div className="h-64 animate-pulse rounded-[18px] bg-[#F2F2ED]" />
        <div className="h-64 animate-pulse rounded-[18px] bg-[#F2F2ED]" />
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export const dynamic = "force-dynamic";

export default function InventoryDashboardPage() {
  const router = useRouter();
  const [authState, setAuthState] = useState<"loading" | "ready" | "unauthed">("loading");
  const [summary, setSummary] = useState<InventorySummaryVM | null>(null);
  const [products, setProducts] = useState<InventoryProductRowVM[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [headerSearch, setHeaderSearch] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");

  const handleCategorySelect = useCallback((categoryId: string) => {
    setSelectedCategory(categoryId);
    if (categoryId) {
      const el = document.getElementById("product-table-root");
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, []);

  useEffect(() => {
    void (async () => {
      try {
        const sessionRes = await fetch("/api/admin/session");
        const sessionData = (await sessionRes.json()) as { authed?: boolean };
        if (!sessionData.authed) {
          router.replace("/admin");
          setAuthState("unauthed");
          return;
        }
        setAuthState("ready");

        // TASK 3 live endpoint swap (was mock). The products endpoint caps
        // pageSize at 100; the corpus can exceed that, so fetch page 1, read
        // `total`, then pull any remaining pages so the internal dashboard shows
        // ALL products (no silent truncation) — the table paginates client-side.
        const PAGE = 100;
        const [summaryRes, firstRes] = await Promise.all([
          fetch("/api/admin/inventory"),
          fetch(`/api/admin/inventory/products?pageSize=${PAGE}&page=1`),
        ]);

        if (!summaryRes.ok || !firstRes.ok) {
          setLoadError("שגיאה בטעינת הנתונים. נסה לרענן את העמוד.");
          return;
        }

        const summaryData = (await summaryRes.json()) as InventorySummaryVM;
        const first = (await firstRes.json()) as InventoryProductsResponseVM;

        let allRows = first.rows;
        const totalPages = Math.max(1, Math.ceil(first.total / PAGE));
        if (totalPages > 1) {
          const rest = await Promise.all(
            Array.from({ length: totalPages - 1 }, (_, i) =>
              fetch(`/api/admin/inventory/products?pageSize=${PAGE}&page=${i + 2}`)
                .then((r) => r.json() as Promise<InventoryProductsResponseVM>)
            )
          );
          allRows = allRows.concat(...rest.map((r) => r.rows));
        }

        setSummary(summaryData);
        setProducts(allRows);
      } catch {
        setLoadError("שגיאה בטעינת הנתונים. נסה לרענן את העמוד.");
        setAuthState("ready");
      }
    })();
  }, [router]);

  if (authState === "loading") {
    return (
      <AppShell variant="admin" activeNav="products" searchValue={headerSearch} onSearchChange={setHeaderSearch}>
        <PageSkeleton />
      </AppShell>
    );
  }
  if (authState === "unauthed") return null;

  if (loadError) {
    return (
      <AppShell variant="admin" activeNav="products" searchValue={headerSearch} onSearchChange={setHeaderSearch}>
        <div role="alert" className="py-16 text-center">
          <p className="text-sm font-medium" style={{ color: "#B04510" }}>{loadError}</p>
          <button onClick={() => window.location.reload()} className="mt-4 rounded-full border px-4 py-2 text-sm" style={{ borderColor: "rgba(176,69,16,0.2)", color: "#B04510" }}>
            רענן עמוד
          </button>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell variant="admin" activeNav="products" searchValue={headerSearch} onSearchChange={setHeaderSearch}>
      <div className="mx-auto max-w-6xl space-y-6">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight" style={{ color: "#111318" }}>לוח מחוונים — מלאי</h1>
          {summary && (
            <p className="mt-1 text-xs" style={{ color: "var(--fg3, #5E6560)" }}>
              עודכן: {new Date(summary.generatedAt).toLocaleDateString("he-IL", { day: "numeric", month: "long", year: "numeric" })}
            </p>
          )}
        </div>

        {summary ? (
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <StatCard label="סך מוצרים" value={summary.totalProducts} accent />
            <StatCard label="קטגוריות" value={summary.categoryCount} />
            <StatCard label="מוצרים מדורגים" value={summary.totalProducts - (summary.gradeDistribution.unscored ?? 0)} />
            <StatCard label="ציון A" value={summary.gradeDistribution.A ?? 0} />
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => <div key={i} className="h-24 animate-pulse rounded-[18px] bg-[#F2F2ED]" />)}
          </div>
        )}

        <div className="grid gap-5 lg:grid-cols-2">
          <Card>
            <SectionHeading>פילוח לפי ציון</SectionHeading>
            {summary ? <GradeDonut gradeDistribution={summary.gradeDistribution} /> : <div className="h-48 animate-pulse rounded-xl bg-[#F2F2ED]" />}
          </Card>
          <Card>
            <SectionHeading>קטגוריות מובילות</SectionHeading>
            {summary ? (
              <TopCategoriesCard
                categories={summary.topCategories}
                activeCategoryId={selectedCategory}
                onCategorySelect={handleCategorySelect}
              />
            ) : (
              <div className="h-48 animate-pulse rounded-xl bg-[#F2F2ED]" />
            )}
          </Card>
        </div>

        {/* variant="admin" → shows SKU, no buy affordance; externalQ + externalCategory from lifted state */}
        <Card>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-[15px] font-bold" style={{ color: "#111318" }}>כל המוצרים</h2>
            {selectedCategory && (
              <button
                type="button"
                onClick={() => setSelectedCategory("")}
                className="rounded-full px-3 py-1 text-xs font-semibold transition-colors"
                style={{
                  background: "var(--grade-a-bg, #E7F4EC)",
                  color: "var(--grade-a-text, #155C3C)",
                  border: "1px solid rgba(30,122,79,0.20)",
                }}
              >
                נקה סינון ×
              </button>
            )}
          </div>
          <ProductTable
            rows={products}
            variant="admin"
            externalQ={headerSearch}
            externalCategory={selectedCategory}
          />
        </Card>
      </div>
    </AppShell>
  );
}
