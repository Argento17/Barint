"use client";

/**
 * ProductTable — shared between /admin/inventory (variant="admin") and /catalog (variant="public").
 *
 * Public variant (default):
 *   Columns: מוצר | קטגוריה | ציון | רשת  (4 shared columns) + compact buy column
 *   SKU hidden. Dormant "צפייה ברשת" affordance (view-at-retailer, inactive, "בקרוב" tooltip).
 *
 * Admin variant:
 *   4 shared columns. SKU as subtle secondary line under retailer. No buy column.
 *   No expansion — detailsById not passed → expansion never rendered.
 *
 * Feature A: Per-product accordion expansion.
 *   Only rendered when `detailsById` prop is provided (catalog passes it; /admin/inventory
 *   passes none → no expansion, admin unchanged). Each row gets a chevron <button>
 *   (aria-expanded + aria-controls). One-open-at-a-time. Desktop: detail <tr> spanning
 *   all columns. Mobile: expansion below the list item. Uses <ExpansionSection> directly.
 *
 * Feature B: Brand in comparison style.
 *   When `detailsById` is provided (public/catalog), brand renders as
 *   `{name} · {brand}` in green #167A58 (~13px) on the same line as the name, with
 *   in-name suppression (brand already stripped from name by normalizeProductBrandDisplay
 *   at load time; we compare product.brand vs row.name to decide whether to show it).
 *   Admin variant keeps the existing grey secondary-line treatment.
 *
 * Visual spec fixes (Design Agent audit 2026-07-01):
 *   H1: cell padding 13px vertical / 22px horizontal (matching reference line 171–204)
 *   H2: table-layout:fixed + <colgroup> — 4 shared cols follow 2.2fr 1.5fr .8fr 1.5fr ratio;
 *       public variant adds compact 120px buy column keeping ratios for the 4 main cols.
 *   C1: buy button text → var(--fg3, #5E6560) — ≥4.5:1 on #FFFFFF and #FBFBF9; border+icon
 *       remain at low opacity to preserve "inert/coming-soon" feel.
 *   H5/M1/M4 tokens:
 *     #6B7280 → var(--fg3, #5E6560)
 *     #9AA0A6 text uses → var(--fg3, #5E6560) or var(--fg4, #666C67)
 *     #EEEEEA / #F2F2ED surfaces → var(--surface-neutral, #F2F2ED)
 *
 * NO import from scoring/bsip/registry/comparisons modules.
 */

import { useState, useMemo, useId } from "react";
import Link from "next/link";
import { Search, Store, ChevronUp, ChevronDown, ChevronsUpDown, ChevronRight } from "lucide-react";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import { InventoryGradeChip } from "./inventory-grade-chip";
import type { BariGrade, BariProductVM, InventoryProductRowVM } from "@/lib/view-models";
import { ExpansionSection } from "@/components/shared/expansion-section";

// ── Row type extended with optional buy URL (future-ready) ──────────────────

export type InventoryProductRowWithBuy = InventoryProductRowVM & {
  buyUrl?: string | null;
};

// ── Filter state ─────────────────────────────────────────────────────────────

interface TableFilters {
  category: string;
  retailer: string;
  grade: string;
  q: string;
}

const EMPTY_FILTERS: TableFilters = { category: "", retailer: "", grade: "", q: "" };

// ── Sort state ───────────────────────────────────────────────────────────────

type SortKey = "name" | "category" | "score" | "retailer";
interface SortState {
  key: SortKey | null;
  dir: "asc" | "desc";
}
const NO_SORT: SortState = { key: null, dir: "asc" };
// First-click direction per column: ציון = best→worst (desc); text columns = A→Z (asc).
const FIRST_DIR: Record<SortKey, "asc" | "desc"> = {
  score: "desc",
  name: "asc",
  category: "asc",
  retailer: "asc",
};
const SORT_LABELS: Record<SortKey, string> = {
  name: "מוצר",
  category: "קטגוריה",
  score: "ציון",
  retailer: "רשת",
};

const PAGE_SIZE = 20;

const GRADE_OPTIONS: Array<{ value: string; label: string }> = [
  { value: "", label: "כל הדרגות" },
  { value: "A", label: "A" },
  { value: "B", label: "B" },
  { value: "C", label: "C" },
  { value: "D", label: "D" },
  { value: "E", label: "E" },
  { value: "unscored", label: "ללא ציון" },
];

// ── Column widths (H2) ────────────────────────────────────────────────────────
// Reference proportions: 2.2fr 1.5fr .8fr 1.5fr
// Total parts = 6.0 → as percentages: 36.7% | 25% | 13.3% | 25%
// Public variant adds a 120px buy column; the 4 main cols fill the remainder.

const COL_WIDTHS_SHARED = ["36.7%", "25%", "13.3%", "25%"] as const;
const BUY_COL_WIDTH = "185px";
// Expand affordance column (public only, replaces buy col width or added separately)
const EXPAND_COL_WIDTH = "52px";

// ── Skeleton ─────────────────────────────────────────────────────────────────

function TableSkeleton({ cols }: { cols: number }) {
  return (
    <>
      {Array.from({ length: 6 }).map((_, i) => (
        <tr
          key={i}
          className="border-b border-[rgba(17,19,24,0.05)]"
          style={{ background: i % 2 === 1 ? "#FBFBF9" : "#FFFFFF" }}
        >
          {Array.from({ length: cols }).map((__, j) => (
            <td key={j} style={{ padding: "13px 22px" }}>
              <div
                className="animate-pulse rounded"
                style={{
                  height: 14,
                  width: j === 0 ? "60%" : "50%",
                  background: "var(--surface-neutral, #F2F2ED)",
                }}
              />
            </td>
          ))}
        </tr>
      ))}
    </>
  );
}

// ── Letter tile (missing image fallback) ──────────────────────────────────────

function ProductThumb({ imageUrl, name }: { imageUrl: string | null; name: string }) {
  const initial = name.trim()[0] ?? "?";

  if (imageUrl) {
    return (
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src={imageUrl}
        alt=""
        className="object-contain"
        style={{
          width: 36,
          height: 36,
          flex: "none",
          borderRadius: 10,
          background: "var(--surface-neutral, #F2F2ED)",
          border: "1px solid rgba(17,19,24,0.07)",
        }}
        onError={(e) => {
          (e.currentTarget as HTMLImageElement).style.display = "none";
        }}
      />
    );
  }

  return (
    <span
      className="inline-flex shrink-0 items-center justify-center font-extrabold"
      style={{
        width: 36,
        height: 36,
        borderRadius: 10,
        background: "var(--surface-neutral, #F2F2ED)",
        border: "1px solid rgba(17,19,24,0.07)",
        color: "var(--fg2, #4E5663)",
        fontSize: 14,
      }}
      aria-hidden="true"
    >
      {initial}
    </span>
  );
}

// ── Brand display (comparison style) ─────────────────────────────────────────
// Renders "· brand" in green #167A58 when brand is present and NOT already
// visible in the product name (in-name suppression: brand stripped from name
// by normalizeProductBrandDisplay at load time — if brand still appears in name
// we skip it to avoid duplication).

function BrandTag({ brand, productName }: { brand: string | null | undefined; productName: string }) {
  if (!brand?.trim()) return null;
  // In-name suppression: if the stripped name still contains the brand token, suppress.
  // (normalizeProductBrandDisplay already stripped brand prefix/suffix from the name, but
  // inline occurrences may remain. Case-insensitive check is the same rule comparison-row uses.)
  if (productName.toLowerCase().includes(brand.trim().toLowerCase())) return null;
  return (
    <span
      style={{
        fontSize: "13px",
        fontWeight: 500,
        color: "#167A58",
        whiteSpace: "nowrap",
      }}
      aria-label={`מותג: ${brand}`}
    >
      {" "}·{" "}{brand}
    </span>
  );
}

// ── Dormant buy affordance ────────────────────────────────────────────────────
// C1 fix: text → var(--fg3, #5E6560) which yields ≥5.9:1 on #FFFFFF and #FBFBF9.
// "Inert" feel preserved via: very light border (0.10 opacity) + icon at 40% opacity.

// "צפייה ברשת" (view at the retail chain) — NOT "buy from Bari". Bari does not sell;
// when a per-product retailer URL is wired later, this links to the product's listing
// on the chain's site. Dormant state = greyed + "בקרוב" tooltip (no inline text, to keep
// the pill from clipping in the fixed-width column).
function BuyAffordance({ buyUrl }: { buyUrl?: string | null }) {
  if (buyUrl) {
    return (
      <a
        href={buyUrl}
        target="_blank"
        rel="noopener noreferrer"
        title="צפייה במוצר באתר הרשת"
        className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-full border px-3 py-1 text-xs font-semibold transition-colors"
        style={{
          borderColor: "rgba(23,111,83,0.28)",
          color: "var(--bari-green-deep, #176F53)",
          background: "#FAFAF8",
        }}
      >
        <Store className="h-3 w-3" aria-hidden />
        צפייה ברשת
      </a>
    );
  }

  // Dormant: greyed + tooltip signal "coming soon"; text at --fg3 (≥5.9:1 on white).
  return (
    <button
      type="button"
      disabled
      aria-disabled="true"
      title="בקרוב — צפייה במוצר באתר הרשת"
      className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-full border px-3 py-1 text-xs font-semibold cursor-not-allowed select-none"
      style={{
        borderColor: "rgba(17,19,24,0.10)",
        color: "var(--fg3, #5E6560)",
        background: "transparent",
      }}
    >
      <Store className="h-3 w-3 opacity-40" aria-hidden />
      צפייה ברשת
      <span className="text-[10px] opacity-60">· בקרוב</span>
    </button>
  );
}

// ── Filter bar ────────────────────────────────────────────────────────────────

interface FilterBarProps {
  filters: TableFilters;
  onChange: (next: TableFilters) => void;
  categoryOptions: string[];
  retailerOptions: Array<{ id: string; nameHe: string }>;
}

function FilterBar({
  filters,
  onChange,
  categoryOptions,
  retailerOptions,
  appearance = "default",
}: FilterBarProps & { appearance?: "default" | "dashboard" }) {
  const isDashboard = appearance === "dashboard";
  const selectClass = isDashboard
    ? "rounded-md border border-[rgba(17,19,24,0.12)] bg-white px-2.5 py-1 text-xs font-medium text-[#111318] focus:outline-none focus:ring-2 focus:ring-[#1F8F6A]/40"
    : "rounded-full border border-[rgba(17,19,24,0.12)] bg-white px-3.5 py-1.5 text-sm text-[#111318] focus:outline-none focus:ring-2 focus:ring-[#1F8F6A]/40";
  const inputClass = isDashboard
    ? "w-full rounded-md border border-[rgba(17,19,24,0.12)] bg-white pe-8 ps-3 py-1 text-xs text-[#111318] placeholder:text-[#888C88] focus:outline-none focus:ring-2 focus:ring-[#1F8F6A]/40"
    : "w-full rounded-full border border-[rgba(17,19,24,0.12)] bg-white pe-9 ps-4 py-1.5 text-sm text-[#111318] placeholder:text-[#888C88] focus:outline-none focus:ring-2 focus:ring-[#1F8F6A]/40";

  return (
    <div
      className={
        isDashboard
          ? "flex flex-wrap items-center gap-1.5 rounded-md border p-2"
          : "flex flex-wrap items-center gap-2"
      }
      style={
        isDashboard
          ? { borderColor: "rgba(17,19,24,0.10)", background: "#FAFAF8" }
          : undefined
      }
      role="search"
      aria-label="סינון מוצרים"
    >
      <div className={isDashboard ? "relative min-w-[180px] flex-[1.4]" : "relative flex-1 min-w-[200px]"}>
        <Search
          className={`pointer-events-none absolute end-3 top-1/2 -translate-y-1/2 opacity-50 ${isDashboard ? "h-3.5 w-3.5" : "h-4 w-4"}`}
          style={{ color: "var(--fg3, #5E6560)" }}
          aria-hidden
        />
        <input
          type="search"
          value={filters.q}
          onChange={(e) => onChange({ ...filters, q: e.target.value })}
          placeholder="חיפוש שם מוצר, מותג..."
          dir="rtl"
          className={inputClass}
          aria-label="חיפוש מוצר"
        />
      </div>

      <select
        value={filters.category}
        onChange={(e) => onChange({ ...filters, category: e.target.value })}
        className={selectClass}
        aria-label="סינון לפי קטגוריה"
      >
        <option value="">כל הקטגוריות</option>
        {categoryOptions.map((cat) => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>

      <select
        value={filters.retailer}
        onChange={(e) => onChange({ ...filters, retailer: e.target.value })}
        className={selectClass}
        aria-label="סינון לפי רשת"
      >
        <option value="">כל הרשתות</option>
        {retailerOptions.map((r) => (
          <option key={r.id} value={r.id}>{r.nameHe}</option>
        ))}
      </select>

      <select
        value={filters.grade}
        onChange={(e) => onChange({ ...filters, grade: e.target.value })}
        className={selectClass}
        aria-label="סינון לפי דרגה"
      >
        {GRADE_OPTIONS.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>
    </div>
  );
}

// ── Sortable column header ─────────────────────────────────────────────────────

function SortHeader({
  label,
  sortKey,
  sort,
  onSort,
  alignEnd = false,
  compact = false,
}: {
  label: string;
  sortKey: SortKey;
  sort: SortState;
  onSort: (key: SortKey) => void;
  alignEnd?: boolean;
  compact?: boolean;
}) {
  const active = sort.key === sortKey;
  const ariaSort: React.AriaAttributes["aria-sort"] = !active
    ? "none"
    : sort.dir === "asc"
      ? "ascending"
      : "descending";

  return (
    <th scope="col" aria-sort={ariaSort} style={{ ...thStyle, padding: compact ? "10px 16px" : "13px 22px", textAlign: alignEnd ? "end" : "start" }}>
      <button
        type="button"
        onClick={() => onSort(sortKey)}
        aria-label={`מיין לפי ${label}`}
        className="inline-flex cursor-pointer select-none items-center gap-1 transition-colors hover:text-[#111318]"
        style={{
          font: "inherit",
          letterSpacing: "inherit",
          textTransform: "inherit",
          color: "inherit",
          background: "none",
          border: "none",
          padding: 0,
        }}
      >
        {label}
        {active ? (
          sort.dir === "asc" ? (
            <ChevronUp className="h-3 w-3" aria-hidden />
          ) : (
            <ChevronDown className="h-3 w-3" aria-hidden />
          )
        ) : (
          <ChevronsUpDown className="h-3 w-3 opacity-30" aria-hidden />
        )}
      </button>
    </th>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

interface ProductTableProps {
  rows: InventoryProductRowWithBuy[];
  variant?: "public" | "admin";
  /** Dashboard styling for /catalog — dense grid, sticky header, toolbar filters. */
  appearance?: "default" | "dashboard";
  loading?: boolean;
  error?: string | null;
  onRetry?: () => void;
  /**
   * External search term from the AppShell header search pill (controlled).
   * ANDs with the table's internal q. Pass "" for internal-only control.
   */
  externalQ?: string;
  /**
   * External category filter from TopCategoriesCard (controlled, by categoryId).
   * When set, overrides the internal category <select> and syncs its display.
   * Pass "" to clear and return control to the internal select.
   */
  externalCategory?: string;
  /**
   * Feature A: Full product details keyed by product ID.
   * When provided, each row renders an expand affordance (chevron button) that
   * opens an inline <ExpansionSection> with the full BariProductVM detail.
   * When absent (admin route), no expansion is rendered → admin unchanged.
   */
  detailsById?: Record<string, BariProductVM>;
}

export function ProductTable({
  rows,
  variant = "public",
  appearance = "default",
  loading = false,
  error = null,
  onRetry,
  externalQ = "",
  externalCategory = "",
  detailsById,
}: ProductTableProps) {
  const isAdmin = variant === "admin";
  const isDashboard = appearance === "dashboard" && !isAdmin;
  const hasExpansion = !isAdmin && detailsById !== undefined;
  const [filters, setFilters] = useState<TableFilters>(EMPTY_FILTERS);
  const [sort, setSort] = useState<SortState>(NO_SORT);
  const [page, setPage] = useState(0);
  // One-open-at-a-time: tracks the currently expanded product id (null = all collapsed)
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const tableId = useId();

  // Column sort: click a header → sort by it; same header again → reverse;
  // third click → clear back to default (as-passed) order.
  function handleSort(key: SortKey) {
    setSort((s) => {
      const first = FIRST_DIR[key];
      if (s.key !== key) return { key, dir: first };
      if (s.dir === first) return { key, dir: first === "asc" ? "desc" : "asc" };
      return NO_SORT;
    });
    setPage(0);
  }

  // Build a stable categoryId→nameHe map from rows for select sync
  const categoryIdToName = useMemo(() => {
    const map = new Map<string, string>();
    for (const r of rows) map.set(r.categoryId, r.categoryNameHe);
    return map;
  }, [rows]);

  // Resolved category name: externalCategory (by id) takes precedence over internal select
  const resolvedCategoryName = useMemo(() => {
    if (externalCategory) return categoryIdToName.get(externalCategory) ?? "";
    return filters.category;
  }, [externalCategory, categoryIdToName, filters.category]);

  // When externalCategory changes, reset internal category select to avoid fighting
  const [prevExtCat, setPrevExtCat] = useState(externalCategory);
  if (prevExtCat !== externalCategory) {
    setPrevExtCat(externalCategory);
    if (externalCategory && filters.category) {
      setFilters((f) => ({ ...f, category: "" }));
    }
    setPage(0);
  }

  const categoryOptions = useMemo(
    () => Array.from(new Set(rows.map((r) => r.categoryNameHe))).sort(),
    [rows],
  );
  const retailerOptions = useMemo(() => {
    const seen = new Map<string, string>();
    for (const r of rows) seen.set(r.retailer.id, r.retailer.nameHe);
    return Array.from(seen.entries()).map(([id, nameHe]) => ({ id, nameHe }));
  }, [rows]);

  const filtered = useMemo(() => {
    // externalQ (AppShell header) takes precedence over internal search field
    const rawQ = externalQ.trim() || filters.q.trim();
    const q = rawQ.toLowerCase();
    const normalizedSkuQuery = /^\d+$/.test(rawQ.replace(/\s+/g, ""))
      ? rawQ.replace(/\s+/g, "")
      : null;
    // resolvedCategoryName: externalCategory (by id→name lookup) OR internal select
    const cat = resolvedCategoryName;
    return rows.filter((r) => {
      if (cat && r.categoryNameHe !== cat) return false;
      if (filters.retailer && r.retailer.id !== filters.retailer) return false;
      if (filters.grade) {
        if (filters.grade === "unscored") {
          if (r.grade !== null) return false;
        } else {
          if (r.grade !== (filters.grade as BariGrade)) return false;
        }
      }
      if (q) {
        if (normalizedSkuQuery && r.sku?.replace(/\s+/g, "") === normalizedSkuQuery) {
          return true;
        }
        const haystack = [r.name, r.brand ?? "", r.categoryNameHe, r.retailer.nameHe, r.sku ?? ""]
          .join(" ")
          .toLowerCase();
        if (!haystack.includes(q)) return false;
      }
      return true;
    });
  }, [rows, filters, externalQ, resolvedCategoryName]);

  // Sort the filtered set. ציון sorts by numeric score (unscored always last);
  // text columns use Hebrew locale compare. Default (no key) = as-passed order.
  const sorted = useMemo(() => {
    if (!sort.key) return filtered;
    const key = sort.key;
    const factor = sort.dir === "asc" ? 1 : -1;
    const arr = [...filtered];
    arr.sort((a, b) => {
      if (key === "score") {
        const as = a.score;
        const bs = b.score;
        // Unscored (null) always sink to the bottom, regardless of direction.
        if (as === null && bs === null) return 0;
        if (as === null) return 1;
        if (bs === null) return -1;
        return (as - bs) * factor;
      }
      const av =
        key === "name" ? a.name : key === "category" ? a.categoryNameHe : a.retailer.nameHe;
      const bv =
        key === "name" ? b.name : key === "category" ? b.categoryNameHe : b.retailer.nameHe;
      return av.localeCompare(bv, "he") * factor;
    });
    return arr;
  }, [filtered, sort]);

  const totalPages = Math.max(1, Math.ceil(sorted.length / PAGE_SIZE));
  const safePage = Math.min(page, totalPages - 1);
  const pageRows = sorted.slice(safePage * PAGE_SIZE, (safePage + 1) * PAGE_SIZE);

  function handleFilterChange(next: TableFilters) {
    setFilters(next);
    setPage(0);
  }

  // Collapse expansion when the page changes (avoids stale expanded row being off-screen)
  function handlePageChange(next: number) {
    setPage(next);
    setExpandedId(null);
  }

  function toggleExpand(id: string) {
    setExpandedId((prev) => (prev === id ? null : id));
  }

  // Total columns for skeleton and colSpan
  // public with expansion: 4 shared + buy col + expand col = 6
  // public without expansion: 4 shared + buy col = 5
  // admin: 4 shared
  const colCount = isAdmin ? 4 : hasExpansion ? 6 : 5;

  // Synthesize filters for FilterBar display: show resolvedCategoryName in the category <select>
  // so it reflects the external selection without the two sources fighting.
  const displayFilters: TableFilters = {
    ...filters,
    category: resolvedCategoryName,
  };

  return (
    <div className={`flex flex-col ${isDashboard ? "gap-3" : "gap-4"}`} id="product-table-root">
      <FilterBar
        filters={displayFilters}
        onChange={(next) => {
          // If user manually changes category in the select, apply it as internal filter.
          // External category (from TopCategoriesCard) remains set in the parent —
          // externalCategory has priority in resolvedCategoryName when non-empty,
          // so the internal select is effectively decorative when external is active.
          // Clearing externalCategory is done by clicking the active category row again.
          handleFilterChange(next);
        }}
        categoryOptions={categoryOptions}
        retailerOptions={retailerOptions}
        appearance={isDashboard ? "dashboard" : "default"}
      />

      {!loading && !error && (
        <p
          className="text-xs"
          style={{ color: "var(--fg3, #5E6560)" }}
          aria-live="polite"
        >
          {filtered.length.toLocaleString("he-IL")} מוצרים
        </p>
      )}

      {/* Mobile sort control — desktop sorts via clickable column headers */}
      {!loading && !error && (
        <div className="flex items-center gap-2 sm:hidden">
          <label htmlFor="mobile-sort" className="text-xs" style={{ color: "var(--fg3, #5E6560)" }}>
            מיין לפי
          </label>
          <select
            id="mobile-sort"
            value={sort.key ?? ""}
            onChange={(e) => {
              const k = e.target.value as SortKey | "";
              setSort(k ? { key: k, dir: FIRST_DIR[k] } : NO_SORT);
              setPage(0);
            }}
            className="rounded-full border border-[rgba(17,19,24,0.12)] bg-white px-3 py-1 text-sm text-[#111318] focus:outline-none focus:ring-2 focus:ring-[#1F8F6A]/40"
          >
            <option value="">ברירת מחדל</option>
            {(["score", "name", "category", "retailer"] as SortKey[]).map((k) => (
              <option key={k} value={k}>{SORT_LABELS[k]}</option>
            ))}
          </select>
          {sort.key && (
            <button
              type="button"
              onClick={() => setSort((s) => ({ ...s, dir: s.dir === "asc" ? "desc" : "asc" }))}
              aria-label={sort.dir === "asc" ? "מיון עולה" : "מיון יורד"}
              className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-[rgba(17,19,24,0.12)] bg-white"
              style={{ color: "var(--fg2, #4E5663)" }}
            >
              {sort.dir === "asc" ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
            </button>
          )}
        </div>
      )}

      {/* Table wrapper */}
      <div className={isDashboard ? "overflow-x-auto" : "overflow-x-auto rounded-[18px] border border-[rgba(17,19,24,0.08)]"}>

        {/* Mobile: stacked list */}
        <div className="block sm:hidden">
          {loading ? (
            <div className="space-y-3 p-4" aria-busy="true">
              {Array.from({ length: 5 }).map((_, i) => (
                <div
                  key={i}
                  className="h-14 animate-pulse rounded-lg"
                  style={{ background: "var(--surface-neutral, #F2F2ED)" }}
                />
              ))}
            </div>
          ) : error ? (
            <ErrorState message={error} onRetry={onRetry} />
          ) : pageRows.length === 0 ? (
            <EmptyState />
          ) : (
            <ul role="list" className="divide-y divide-[rgba(17,19,24,0.05)]">
              {pageRows.map((row) => (
                <MobileRow
                  key={row.id}
                  row={row}
                  showBuy={!isAdmin}
                  hasExpansion={hasExpansion}
                  detail={hasExpansion ? (detailsById?.[row.id] ?? null) : null}
                  expanded={expandedId === row.id}
                  onToggle={() => toggleExpand(row.id)}
                  panelId={`${tableId}-mobile-panel-${row.id}`}
                  triggerId={`${tableId}-mobile-btn-${row.id}`}
                />
              ))}
            </ul>
          )}
        </div>

        {/* Desktop: semantic <table> with fixed layout + colgroup (H2) */}
        <table
          className="hidden w-full sm:table"
          style={{ tableLayout: "fixed" }}
          dir="rtl"
          lang="he"
          aria-label="טבלת מוצרים"
        >
          {/* H2: colgroup pins column widths */}
          <colgroup>
            {COL_WIDTHS_SHARED.map((w, i) => (
              <col key={i} style={{ width: w }} />
            ))}
            {!isAdmin && <col style={{ width: BUY_COL_WIDTH }} />}
            {hasExpansion && <col style={{ width: EXPAND_COL_WIDTH }} />}
          </colgroup>

          {/* Thead: background #FAFAF8, mono uppercase, H1 padding 13px/22px */}
          <thead className={isDashboard ? "sticky top-[var(--site-header-height-sm,4.25rem)] z-10" : undefined}>
            <tr style={{ background: "#FAFAF8", borderBottom: "1px solid rgba(17,19,24,0.08)" }}>
              <SortHeader label="מוצר" sortKey="name" sort={sort} onSort={handleSort} compact={isDashboard} />
              <SortHeader label="קטגוריה" sortKey="category" sort={sort} onSort={handleSort} compact={isDashboard} />
              <SortHeader label="ציון" sortKey="score" sort={sort} onSort={handleSort} alignEnd={isDashboard} compact={isDashboard} />
              <SortHeader label="רשת · מקור" sortKey="retailer" sort={sort} onSort={handleSort} compact={isDashboard} />
              {!isAdmin && (
                <th scope="col" style={{ ...thStyle, padding: "13px 12px", textAlign: "start" }}>
                  <span className="sr-only">צפייה ברשת</span>
                </th>
              )}
              {hasExpansion && (
                <th scope="col" style={{ ...thStyle, padding: "13px 8px", textAlign: "center" }}>
                  <span className="sr-only">פרטים</span>
                </th>
              )}
            </tr>
          </thead>

          <tbody>
            {loading ? (
              <TableSkeleton cols={colCount} />
            ) : error ? (
              <tr>
                <td colSpan={colCount} style={{ padding: "13px 22px" }}>
                  <ErrorState message={error} onRetry={onRetry} />
                </td>
              </tr>
            ) : pageRows.length === 0 ? (
              <tr>
                <td colSpan={colCount} style={{ padding: "13px 22px" }}>
                  <EmptyState />
                </td>
              </tr>
            ) : (
              pageRows.map((row, idx) => (
                <DesktopRow
                  key={row.id}
                  row={row}
                  idx={idx}
                  isAdmin={isAdmin}
                  isDashboard={isDashboard}
                  hasExpansion={hasExpansion}
                  detail={hasExpansion ? (detailsById?.[row.id] ?? null) : null}
                  expanded={expandedId === row.id}
                  onToggle={() => toggleExpand(row.id)}
                  colCount={colCount}
                  panelId={`${tableId}-panel-${row.id}`}
                  triggerId={`${tableId}-btn-${row.id}`}
                />
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {!loading && !error && totalPages > 1 && (
        <div
          className="flex items-center justify-between text-sm"
          style={{ color: "var(--fg2, #4E5663)" }}
          aria-label="עימוד"
        >
          <button
            onClick={() => handlePageChange(Math.max(0, safePage - 1))}
            disabled={safePage === 0}
            className="rounded-full border border-[rgba(17,19,24,0.12)] bg-white px-4 py-1.5 disabled:opacity-40 hover:bg-[#F7F7F2] transition-colors"
          >
            הקודם
          </button>
          <span>
            עמוד {(safePage + 1).toLocaleString("he-IL")} מתוך {totalPages.toLocaleString("he-IL")}
          </span>
          <button
            onClick={() => handlePageChange(Math.min(totalPages - 1, safePage + 1))}
            disabled={safePage >= totalPages - 1}
            className="rounded-full border border-[rgba(17,19,24,0.12)] bg-white px-4 py-1.5 disabled:opacity-40 hover:bg-[#F7F7F2] transition-colors"
          >
            הבא
          </button>
        </div>
      )}
    </div>
  );
}

// ── Shared th style (H1 padding applied inline per cell) ──────────────────────

const thStyle: React.CSSProperties = {
  fontFamily: "var(--font-mono, ui-monospace, monospace)",
  fontSize: "10.5px",
  fontWeight: 700,
  letterSpacing: "0.14em",
  textTransform: "uppercase",
  color: "var(--fg3, #5E6560)",
};

// ── Desktop row — H1: padding 13px/22px (reference lines 171–204) ─────────────

function DesktopRow({
  row,
  idx,
  isAdmin,
  isDashboard,
  hasExpansion,
  detail,
  expanded,
  onToggle,
  colCount,
  panelId,
  triggerId,
}: {
  row: InventoryProductRowWithBuy;
  idx: number;
  isAdmin: boolean;
  isDashboard: boolean;
  hasExpansion: boolean;
  detail: BariProductVM | null;
  expanded: boolean;
  onToggle: () => void;
  colCount: number;
  panelId: string;
  triggerId: string;
}) {
  const isEven = idx % 2 === 1;
  const rowBg = isEven ? "#FBFBF9" : "#FFFFFF";

  return (
    <>
      <tr
        className="border-b border-[rgba(17,19,24,0.05)] transition-colors hover:bg-[#FBFBF9]"
        style={{ background: expanded ? "#F4FAF7" : rowBg }}
      >
        {/* מוצר */}
        <td style={{ padding: isDashboard ? "10px 16px" : "13px 22px" }}>
          <div className="flex items-center gap-3 min-w-0">
            <ProductThumb imageUrl={row.imageUrl} name={row.name} />
            <div className="flex flex-col gap-0.5 min-w-0">
              {/* Feature B + name link: name is a <Link> to the category comparison page.
                  Brand tag sits beside the link (separate node — not part of the link href).
                  Admin keeps grey secondary-line treatment but also gets the name link. */}
              <span
                className="font-semibold"
                style={{ fontSize: 14, lineHeight: 1.4 }}
              >
                <Link
                  href={row.comparisonHref}
                  className="product-name-link break-words"
                  style={{ color: "var(--fg1, #111318)" }}
                  title={`לעמוד ההשוואה — ${row.categoryNameHe}`}
                >
                  {row.name}
                </Link>
                {/* Brand: comparison style on public, grey secondary on admin */}
                {isAdmin ? null : <BrandTag brand={row.brand} productName={row.name} />}
              </span>
              {/* Admin: grey secondary brand line */}
              {isAdmin && row.brand && (
                <span
                  className="truncate"
                  style={{ fontSize: 12, color: "var(--fg3, #5E6560)" }}
                >
                  {row.brand}
                </span>
              )}
            </div>
          </div>
        </td>

        {/* קטגוריה */}
        <td style={{ padding: isDashboard ? "10px 16px" : "13px 22px" }}>
          <span
            className={isDashboard ? "inline-block rounded px-2 py-0.5" : undefined}
            style={{
              fontSize: isDashboard ? 12 : 13.5,
              fontWeight: 500,
              color: "var(--fg2, #4E5663)",
              background: isDashboard ? "rgba(17,19,24,0.04)" : undefined,
              border: isDashboard ? "1px solid rgba(17,19,24,0.06)" : undefined,
            }}
          >
            {row.categoryNameHe}
          </span>
        </td>

        {/* ציון */}
        <td style={{ padding: isDashboard ? "10px 16px" : "13px 22px", textAlign: isDashboard ? "end" : "start" }}>
          <div className={isDashboard ? "inline-flex flex-col items-end gap-1" : undefined}>
            {isDashboard && row.score !== null ? (
              <span
                className="font-bold tabular-nums"
                style={{
                  fontSize: 13,
                  color: "var(--fg1, #111318)",
                  fontVariantNumeric: "tabular-nums",
                  fontFamily: "var(--font-mono, ui-monospace, monospace)",
                }}
              >
                {row.score.toLocaleString("he-IL")}
              </span>
            ) : null}
            <InventoryGradeChip grade={row.grade} />
          </div>
        </td>

        {/* רשת + optional SKU (admin only) */}
        <td style={{ padding: isDashboard ? "10px 16px" : "13px 22px" }}>
          <div className="flex flex-col gap-0.5">
            <span style={{ fontSize: 13.5, fontWeight: 500, color: "var(--fg2, #4E5663)" }}>
              {row.retailer.nameHe}
            </span>
            {isAdmin && row.sku && (
              <span
                className="tabular-nums"
                style={{
                  fontSize: 11,
                  color: "var(--fg4, #666C67)",
                  fontFamily: "var(--font-mono, ui-monospace, monospace)",
                  fontVariantNumeric: "tabular-nums",
                }}
              >
                SKU {row.sku}
              </span>
            )}
          </div>
        </td>

        {/* Buy affordance (public only) — tighter horizontal padding so the pill fits */}
        {!isAdmin && (
          <td style={{ padding: isDashboard ? "10px 8px" : "13px 12px" }}>
            <BuyAffordance buyUrl={row.buyUrl} />
          </td>
        )}

        {/* Expand affordance (public + detailsById only).
            stopPropagation on click keeps this control independent from the name <Link>. */}
        {hasExpansion && (
          <td style={{ padding: "13px 8px", textAlign: "center" }}>
            {detail ? (
              <button
                id={triggerId}
                type="button"
                onClick={(e) => { e.stopPropagation(); onToggle(); }}
                aria-expanded={expanded}
                aria-controls={panelId}
                aria-label={expanded ? `סגור פרטים עבור ${row.name}` : `הצג פרטים עבור ${row.name}`}
                className="inline-flex h-8 w-8 items-center justify-center rounded-full transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
                style={{
                  background: expanded ? "rgba(22,122,88,0.10)" : "transparent",
                  border: expanded ? "1px solid rgba(22,122,88,0.22)" : "1px solid rgba(17,19,24,0.10)",
                  color: expanded ? "#167A58" : "var(--fg3, #5E6560)",
                }}
              >
                <ChevronRight
                  className="h-4 w-4 transition-transform duration-200"
                  style={{ transform: expanded ? "rotate(90deg)" : "rotate(0deg)" }}
                  aria-hidden
                />
              </button>
            ) : null}
          </td>
        )}
      </tr>

      {/* Expansion row (desktop) — spans all columns */}
      {hasExpansion && expanded && detail && (
        <tr
          id={panelId}
          role="region"
          aria-labelledby={triggerId}
          style={{ background: "#F9FCF9" }}
        >
          <td
            colSpan={colCount}
            style={{
              padding: "0",
              borderBottom: "1px solid rgba(17,19,24,0.08)",
            }}
          >
            <div style={{ padding: "16px 16px 4px", borderTop: "1px solid rgba(22,122,88,0.12)" }}>
              {/* Product header in expansion */}
              <div
                className="mb-3 flex items-center gap-3"
                style={{ paddingInlineStart: "8px" }}
                dir="rtl"
              >
                <ProductThumb imageUrl={detail.imageUrl} name={detail.name} />
                <div>
                  <p style={{ fontWeight: 700, fontSize: 14, color: "#111318" }}>
                    {detail.name}
                    <BrandTag brand={detail.brand} productName={detail.name} />
                  </p>
                  <p style={{ fontSize: 12, color: "var(--fg3, #5E6560)" }}>
                    {row.categoryNameHe}
                  </p>
                </div>
              </div>
              <ExpansionSection
                expansion={detail.expansion}
                confidence={detail.confidence}
                confidenceLabelHe={detail.confidence_label_he}
                confidenceTooltipHe={detail.confidence_tooltip_he}
                onCollapse={onToggle}
                category={row.categoryId}
                rowVerdict={detail.rowVerdict}
                consumerExplanation={detail.expansion.consumerExplanation}
                bestUseCases={detail.bestUseCases}
                consumerTakeaway={detail.consumerTakeaway}
                bariInterpretation={detail.bariInterpretation}
                rank={detail.rank}
                categoryTotal={detail.categoryTotal}
                glassBox={detail.glassBox}
                d4Additives={detail.d4_additives}
                d3Processing={detail.d3_processing}
                productId={detail.id}
                magnesiumBadges={detail.magnesiumBadges}
              />
            </div>
          </td>
        </tr>
      )}
    </>
  );
}

// ── Mobile row ─────────────────────────────────────────────────────────────────

function MobileRow({
  row,
  showBuy,
  hasExpansion,
  detail,
  expanded,
  onToggle,
  panelId,
  triggerId,
}: {
  row: InventoryProductRowWithBuy;
  showBuy: boolean;
  hasExpansion: boolean;
  detail: BariProductVM | null;
  expanded: boolean;
  onToggle: () => void;
  panelId: string;
  triggerId: string;
}) {
  return (
    <li>
      <div className="flex items-center gap-3 px-4 py-3">
        <ProductThumb imageUrl={row.imageUrl} name={row.name} />
        <div className="flex-1 min-w-0">
          <p
            className="text-sm font-semibold"
            style={{ lineHeight: 1.4 }}
          >
            {/* Name link — navigates to category comparison page; separate from expand chevron */}
            <Link
              href={row.comparisonHref}
              className="product-name-link break-words"
              style={{ color: "var(--fg1, #111318)" }}
              title={`לעמוד ההשוואה — ${row.categoryNameHe}`}
            >
              {row.name}
            </Link>
            {/* Brand tag (comparison style on public/catalog) */}
            {hasExpansion ? (
              <BrandTag brand={row.brand} productName={row.name} />
            ) : null}
          </p>
          {/* Admin: grey secondary brand line */}
          {!hasExpansion && row.brand && (
            <p className="truncate text-xs" style={{ color: "var(--fg3, #5E6560)" }}>
              {row.brand}
            </p>
          )}
          <p className="truncate text-xs" style={{ color: "var(--fg3, #5E6560)" }}>
            {row.categoryNameHe} · {row.retailer.nameHe}
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          <InventoryGradeChip grade={row.grade} />
          {showBuy && !hasExpansion && <BuyAffordance buyUrl={row.buyUrl} />}
          {hasExpansion && detail && (
            <button
              id={triggerId}
              type="button"
              onClick={(e) => { e.stopPropagation(); onToggle(); }}
              aria-expanded={expanded}
              aria-controls={panelId}
              aria-label={expanded ? `סגור פרטים עבור ${row.name}` : `הצג פרטים עבור ${row.name}`}
              className="inline-flex h-8 w-8 items-center justify-center rounded-full transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
              style={{
                background: expanded ? "rgba(22,122,88,0.10)" : "transparent",
                border: expanded ? "1px solid rgba(22,122,88,0.22)" : "1px solid rgba(17,19,24,0.10)",
                color: expanded ? "#167A58" : "var(--fg3, #5E6560)",
              }}
            >
              <ChevronRight
                className="h-4 w-4 transition-transform duration-200"
                style={{ transform: expanded ? "rotate(90deg)" : "rotate(0deg)" }}
                aria-hidden
              />
            </button>
          )}
        </div>
      </div>

      {/* Mobile expansion panel */}
      {hasExpansion && expanded && detail && (
        <div
          id={panelId}
          role="region"
          aria-labelledby={triggerId}
          style={{
            borderTop: "1px solid rgba(22,122,88,0.12)",
            background: "#F9FCF9",
            paddingBottom: "8px",
          }}
        >
          <ExpansionSection
            expansion={detail.expansion}
            confidence={detail.confidence}
            confidenceLabelHe={detail.confidence_label_he}
            confidenceTooltipHe={detail.confidence_tooltip_he}
            onCollapse={onToggle}
            category={row.categoryId}
            rowVerdict={detail.rowVerdict}
            consumerExplanation={detail.expansion.consumerExplanation}
            bestUseCases={detail.bestUseCases}
            consumerTakeaway={detail.consumerTakeaway}
            bariInterpretation={detail.bariInterpretation}
            rank={detail.rank}
            categoryTotal={detail.categoryTotal}
            glassBox={detail.glassBox}
            d4Additives={detail.d4_additives}
            d3Processing={detail.d3_processing}
            productId={detail.id}
            magnesiumBadges={detail.magnesiumBadges}
          />
        </div>
      )}
    </li>
  );
}

// ── State components ──────────────────────────────────────────────────────────

function EmptyState() {
  return (
    <div className="py-12 text-center" role="status" aria-live="polite">
      <p className="text-sm font-medium" style={{ color: "var(--fg2, #4E5663)" }}>
        לא נמצאו מוצרים תואמים
      </p>
      <p className="mt-1 text-xs" style={{ color: "var(--fg3, #5E6560)" }}>
        נסו לשנות את הסינון, או שהמוצר עדיין לא נבדק. הקטלוג גדל כל שבוע, וכל ההשוואות המלאות נמצאות ב
        {" "}
        <a
          href="/hashvaot"
          className="font-semibold underline underline-offset-2"
          style={{ color: "var(--bari-green-deep, #176F53)" }}
        >
          השוואות
        </a>
        .
      </p>
    </div>
  );
}

function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="py-8 text-center" role="alert">
      <p className="text-sm font-medium" style={{ color: BARI_COMPARISON_TOKENS.gradePalette.D.text }}>
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-3 rounded-full border px-4 py-1.5 text-sm transition-colors hover:bg-[#FEF6F2]"
          style={{
            borderColor: `${BARI_COMPARISON_TOKENS.gradePalette.D.accent}33`,
            color: BARI_COMPARISON_TOKENS.gradePalette.D.text,
          }}
        >
          נסה שוב
        </button>
      )}
    </div>
  );
}
