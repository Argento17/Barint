"use client";

/**
 * CatalogClient — content for the public /catalog page.
 *
 * Renders UNDER the standard site <SiteHeader/> (no navy AppShell, no sidebar) — the
 * page wraps this in <main> + <HomeContainer>, matching /hashvaot. Product search lives
 * inside the product table's own filter row (a logical in-place place), so there is no
 * separate header search here.
 *
 * Lifted state: selectedCategory → TopCategoriesCard.activeCategoryId +
 * ProductTable.externalCategory. On mobile, selecting a category scrolls to the table.
 *
 * Feature C: Light-themed right sidebar (RTL-start). Two-column layout under SiteHeader.
 * Desktop: sidebar (220px) on the right, main content fills the rest.
 * Mobile: sidebar collapsed to a horizontal category strip above the table.
 *
 * Boundary: NO import from lib/comparisons/* / lib/bsip/* / registry / scoring.
 */

import { useState, useCallback } from "react";
import Image from "next/image";

import { GradeDonut } from "@/components/inventory/retailer-donut";
import { TopCategoriesCard } from "@/components/inventory/top-categories-card";
import { ProductTable } from "@/components/inventory/product-table";
import type {
  BariProductVM,
  InventorySummaryVM,
  InventoryProductRowVM,
} from "@/lib/view-models";

// OLI catalog mascot — intrinsic pixel size of the keyed/cropped asset.
// (Set from the processed public/mascots/mascot-oli-catalog.png; drives aspect ratio only.)
const OLI_CATALOG_W = 1374;
const OLI_CATALOG_H = 969;

interface CatalogClientProps {
  summary: InventorySummaryVM;
  initialRows: InventoryProductRowVM[];
  /** Feature A: Full product details keyed by product ID for expansion panels. */
  detailsById: Record<string, BariProductVM>;
}

// ── Card shell ────────────────────────────────────────────────────────────────

function CardShell({ children, heading }: { children: React.ReactNode; heading: string }) {
  return (
    <section
      className="rounded-[18px] border bg-white p-5"
      style={{
        borderColor: "var(--hairline, rgba(17,19,24,0.08))",
        boxShadow: "var(--shadow-card, 0 2px 12px -6px rgba(17,19,24,0.08))",
      }}
    >
      <div className="mb-3 flex items-center justify-between">
        <h2 className="font-bold" style={{ fontSize: 15, letterSpacing: "-0.02em", color: "#111318" }}>
          {heading}
        </h2>
      </div>
      {children}
    </section>
  );
}

// ── Light Sidebar (Feature C) ─────────────────────────────────────────────────
// Right-side (RTL-start) sidebar with category nav + site links.
// White/#FBFBF9 bg, hairline borders, active item in grade-A green tint.
// Coexists with the standard SiteHeader — NOT a nav replacement.

interface SidebarProps {
  categories: InventorySummaryVM["topCategories"];
  activeCategoryId: string;
  onCategorySelect: (id: string) => void;
}

function CatalogSidebar({ categories, activeCategoryId, onCategorySelect }: SidebarProps) {
  return (
    <aside
      aria-label="ניווט קטלוג"
      className="hidden lg:flex flex-col gap-0"
      style={{
        width: 220,
        flexShrink: 0,
        background: "#FFFFFF",
        border: "1px solid rgba(17,19,24,0.08)",
        borderRadius: 18,
        boxShadow: "0 2px 12px -6px rgba(17,19,24,0.06)",
        height: "fit-content",
        position: "sticky",
        // Header-relative offset (was a hardcoded 80px) so the sidebar sticks a
        // consistent gap below the real SiteHeader height at any breakpoint.
        top: "calc(var(--site-header-height-sm, 4.25rem) + 16px)",
      }}
    >
      {/* Sidebar header */}
      <div
        style={{
          padding: "14px 16px 10px",
          borderBottom: "1px solid rgba(17,19,24,0.07)",
        }}
      >
        <p
          style={{
            fontFamily: "var(--font-mono, monospace)",
            fontSize: "10px",
            fontWeight: 700,
            letterSpacing: "0.18em",
            textTransform: "uppercase",
            color: "var(--fg3, #5E6560)",
          }}
        >
          קטגוריות
        </p>
      </div>

      {/* Category nav */}
      <nav aria-label="קטגוריות מוצרים" style={{ padding: "6px 0" }}>
        <ul role="list">
          {/* "All" option */}
          <li>
            <button
              type="button"
              onClick={() => onCategorySelect("")}
              aria-pressed={activeCategoryId === ""}
              className="w-full text-right transition-colors"
              style={{
                display: "flex",
                alignItems: "center",
                padding: "7px 16px",
                fontSize: 13,
                fontWeight: activeCategoryId === "" ? 700 : 500,
                color: activeCategoryId === "" ? "#155C3C" : "var(--fg2, #4E5663)",
                background: activeCategoryId === "" ? "rgba(21,92,60,0.06)" : "transparent",
                border: "none",
                cursor: "pointer",
                borderRadius: 0,
              }}
            >
              {activeCategoryId === "" && (
                <span
                  style={{
                    display: "inline-block",
                    width: 3,
                    height: 14,
                    borderRadius: 2,
                    background: "#1F8F6A",
                    marginInlineEnd: 10,
                    flexShrink: 0,
                  }}
                  aria-hidden
                />
              )}
              {activeCategoryId !== "" && (
                <span style={{ display: "inline-block", width: 3, marginInlineEnd: 10, flexShrink: 0 }} aria-hidden />
              )}
              כל הקטגוריות
            </button>
          </li>
          {categories.map((cat) => {
            const isActive = activeCategoryId === cat.categoryId;
            return (
              <li key={cat.categoryId}>
                <button
                  type="button"
                  onClick={() => onCategorySelect(isActive ? "" : cat.categoryId)}
                  aria-pressed={isActive}
                  className="w-full text-right transition-colors"
                  style={{
                    display: "flex",
                    alignItems: "center",
                    padding: "7px 16px",
                    fontSize: 13,
                    fontWeight: isActive ? 700 : 400,
                    color: isActive ? "#155C3C" : "var(--fg2, #4E5663)",
                    background: isActive ? "rgba(21,92,60,0.06)" : "transparent",
                    border: "none",
                    cursor: "pointer",
                    width: "100%",
                  }}
                >
                  {/* Active indicator bar */}
                  <span
                    style={{
                      display: "inline-block",
                      width: 3,
                      height: 14,
                      borderRadius: 2,
                      background: isActive ? "#1F8F6A" : "transparent",
                      marginInlineEnd: 10,
                      flexShrink: 0,
                      transition: "background 0.15s",
                    }}
                    aria-hidden
                  />
                  <span className="truncate">{cat.nameHe}</span>
                  {/* Product count pill */}
                  <span
                    style={{
                      marginInlineStart: "auto",
                      paddingInlineStart: 6,
                      fontSize: 11,
                      fontFamily: "var(--font-mono, monospace)",
                      fontWeight: 600,
                      color: isActive ? "#1F8F6A" : "var(--fg4, #888C88)",
                      flexShrink: 0,
                    }}
                  >
                    {cat.count}
                  </span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Site navigation links */}
      <div
        style={{
          borderTop: "1px solid rgba(17,19,24,0.07)",
          padding: "10px 0 6px",
        }}
      >
        <p
          style={{
            padding: "6px 16px 4px",
            fontFamily: "var(--font-mono, monospace)",
            fontSize: "10px",
            fontWeight: 700,
            letterSpacing: "0.18em",
            textTransform: "uppercase",
            color: "var(--fg3, #5E6560)",
          }}
        >
          ניווט
        </p>
        <nav aria-label="קישורי אתר">
          <ul role="list">
            {[
              { href: "/hashvaot", label: "השוואות" },
              { href: "/blog", label: "בלוג" },
              { href: "/methodology", label: "מדדים ושיטה" },
            ].map(({ href, label }) => (
              <li key={href}>
                <a
                  href={href}
                  className="flex items-center transition-colors"
                  style={{
                    padding: "7px 16px",
                    fontSize: 13,
                    fontWeight: 400,
                    color: "var(--fg2, #4E5663)",
                    textDecoration: "none",
                  }}
                  onMouseEnter={(e) => {
                    (e.currentTarget as HTMLElement).style.color = "#167A58";
                    (e.currentTarget as HTMLElement).style.background = "rgba(22,122,88,0.04)";
                  }}
                  onMouseLeave={(e) => {
                    (e.currentTarget as HTMLElement).style.color = "var(--fg2, #4E5663)";
                    (e.currentTarget as HTMLElement).style.background = "transparent";
                  }}
                >
                  <span style={{ display: "inline-block", width: 3, marginInlineEnd: 10 }} aria-hidden />
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </aside>
  );
}

// ── Mobile category strip (Feature C mobile) ──────────────────────────────────
// Replaces the hidden sidebar on mobile: horizontal scroll strip of category pills.

function MobileCategoryStrip({
  categories,
  activeCategoryId,
  onCategorySelect,
}: SidebarProps) {
  return (
    <nav
      aria-label="סינון לפי קטגוריה"
      className="relative lg:hidden"
    >
      <div
        className="flex gap-2 overflow-x-auto pb-1"
        style={{ scrollSnapType: "x mandatory", WebkitOverflowScrolling: "touch" }}
        dir="rtl"
      >
        <button
          type="button"
          onClick={() => onCategorySelect("")}
          className="shrink-0 rounded-full px-3 py-1.5 text-xs font-semibold whitespace-nowrap transition-colors"
          style={{
            background: activeCategoryId === "" ? "rgba(21,92,60,0.10)" : "rgba(17,19,24,0.05)",
            color: activeCategoryId === "" ? "#155C3C" : "var(--fg2, #4E5663)",
            border: activeCategoryId === "" ? "1px solid rgba(21,92,60,0.22)" : "1px solid transparent",
          }}
        >
          הכל
        </button>
        {categories.map((cat) => {
          const isActive = activeCategoryId === cat.categoryId;
          return (
            <button
              key={cat.categoryId}
              type="button"
              onClick={() => onCategorySelect(isActive ? "" : cat.categoryId)}
              className="shrink-0 rounded-full px-3 py-1.5 text-xs whitespace-nowrap transition-colors"
              style={{
                fontWeight: isActive ? 700 : 400,
                background: isActive ? "rgba(21,92,60,0.10)" : "rgba(17,19,24,0.05)",
                color: isActive ? "#155C3C" : "var(--fg2, #4E5663)",
                border: isActive ? "1px solid rgba(21,92,60,0.22)" : "1px solid transparent",
              }}
            >
              {cat.nameHe}
            </button>
          );
        })}
      </div>
      {/* Scroll hint: fade on the inline-end (left in RTL) edge signals more categories scroll off-screen. */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-y-0 left-0 w-8"
        style={{ background: "linear-gradient(to left, rgba(247,247,242,0), #F7F7F2)" }}
      />
    </nav>
  );
}

// ── CatalogClient ─────────────────────────────────────────────────────────────

export function CatalogClient({ summary, initialRows, detailsById }: CatalogClientProps) {
  const [selectedCategory, setSelectedCategory] = useState("");

  const handleCategorySelect = useCallback((categoryId: string) => {
    setSelectedCategory(categoryId);
    // On mobile: scroll to the product table so the filtered results are visible.
    if (categoryId) {
      const el = document.getElementById("product-table-root");
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, []);

  return (
    // Two-column layout on desktop: sidebar (right/start in RTL) + main content
    <div className="flex gap-6 items-start" dir="rtl">

      {/* ── Feature C: Light sidebar (desktop only; hidden on mobile) ──────── */}
      <CatalogSidebar
        categories={summary.topCategories}
        activeCategoryId={selectedCategory}
        onCategorySelect={handleCategorySelect}
      />

      {/* ── Main content column ─────────────────────────────────────────────── */}
      <div className="flex-1 min-w-0 space-y-5" dir="rtl">

        {/* ── Page title (+ OLI top-left) ────────────────────────────────── */}
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#167A58]">
              BARI CATALOG
            </p>
            <h1
              className="mt-2 font-extrabold tracking-tight"
              style={{ fontSize: "clamp(24px, 4vw, 32px)", letterSpacing: "-0.045em", color: "#111318" }}
            >
              קטלוג המוצרים
            </h1>
            <p className="mt-1.5 text-sm font-medium" style={{ color: "var(--fg3, #5E6560)" }}>
              {summary.totalProducts.toLocaleString("he-IL")} מוצרים ·{" "}
              {summary.categoryCount.toLocaleString("he-IL")} קטגוריות פעילות ·{" "}
              <span style={{ color: "var(--bari-green-deep, #176F53)" }}>עודכן השבוע</span>
            </p>
          </div>

          {/* OLI — the olive, Bari's Healthy Guide, reading the catalog. Decorative. */}
          <Image
            src="/mascots/mascot-oli-catalog.png"
            alt=""
            width={OLI_CATALOG_W}
            height={OLI_CATALOG_H}
            aria-hidden
            className="pointer-events-none -mt-3 -mb-6 hidden h-auto w-50 shrink-0 select-none md:block lg:w-60"
            priority
          />
        </div>

        {/* ── Feature C: Mobile category strip ──────────────────────────── */}
        <MobileCategoryStrip
          categories={summary.topCategories}
          activeCategoryId={selectedCategory}
          onCategorySelect={handleCategorySelect}
        />

        {/* ── Two-column summary cards ───────────────────────────────────── */}
        <div className="grid gap-5 lg:grid-cols-2">
          <CardShell heading="פילוח לפי ציון">
            <GradeDonut gradeDistribution={summary.gradeDistribution} />
          </CardShell>

          <CardShell heading="קטגוריות מובילות">
            <TopCategoriesCard
              categories={summary.topCategories}
              activeCategoryId={selectedCategory}
              onCategorySelect={handleCategorySelect}
            />
          </CardShell>
        </div>

        {/* ── Product table (search + filters live in its own filter row) ──── */}
        <section
          className="rounded-[18px] border bg-white p-5"
          style={{
            borderColor: "var(--hairline, rgba(17,19,24,0.08))",
            boxShadow: "var(--shadow-card, 0 2px 12px -6px rgba(17,19,24,0.08))",
          }}
        >
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-bold" style={{ fontSize: 15, letterSpacing: "-0.02em", color: "#111318" }}>
              כל המוצרים
            </h2>
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
            rows={initialRows}
            variant="public"
            externalCategory={selectedCategory}
            detailsById={detailsById}
          />
        </section>

      </div>
    </div>
  );
}
