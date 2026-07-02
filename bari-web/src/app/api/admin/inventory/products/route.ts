/**
 * GET /api/admin/inventory/products
 *
 * Returns a paginated, filterable list of InventoryProductRowVM covering the
 * entire Bari corpus across all registry categories. Auth-gated.
 *
 * Query parameters (all optional):
 *   category   ComparisonCategoryId — filter to one category
 *   retailer   BariRetailerRefVM.id — filter by canonical retailer id
 *   grade      BariGrade (A|B|C|D|E) — filter by grade; "unscored" = score null
 *   q          string — case-insensitive substring match on name or brand
 *   page       integer >= 1 (default: 1)
 *   pageSize   integer 1–100 (default: 50)
 *
 * Response: { rows: InventoryProductRowVM[]; total: number; page: number }
 * Auth: requires a valid admin session cookie (isAuthed).
 * Returns 401 without an admin session.
 */

import { NextRequest, NextResponse } from "next/server";

import { isAuthed } from "@/lib/admin/auth";
import type { BariGrade } from "@/lib/view-models";
import type { ComparisonCategoryId } from "@/lib/comparisons/registry/types";
import { listComparisonCategoryIds } from "@/lib/comparisons/registry";
import { buildInventoryRows } from "@/lib/inventory/loader";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const ALL_GRADES = new Set<string>(["A", "B", "C", "D", "E"]);
const PAGE_SIZE_DEFAULT = 50;
const PAGE_SIZE_MAX = 100;

export async function GET(request: NextRequest) {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  const { searchParams } = request.nextUrl;

  // ── Parse query params ───────────────────────────────────────────────────
  const rawCategory = searchParams.get("category") ?? "";
  const rawRetailer = searchParams.get("retailer") ?? "";
  const rawGrade = searchParams.get("grade") ?? "";
  const rawQ = searchParams.get("q") ?? "";
  const rawPage = searchParams.get("page") ?? "1";
  const rawPageSize = searchParams.get("pageSize") ?? String(PAGE_SIZE_DEFAULT);

  const page = Math.max(1, parseInt(rawPage, 10) || 1);
  const pageSize = Math.min(
    PAGE_SIZE_MAX,
    Math.max(1, parseInt(rawPageSize, 10) || PAGE_SIZE_DEFAULT)
  );

  // Validate category against the live registry (zero hardcoding)
  const validCategoryIds = new Set<string>(listComparisonCategoryIds());
  const categoryFilter: ComparisonCategoryId | null =
    rawCategory && validCategoryIds.has(rawCategory)
      ? (rawCategory as ComparisonCategoryId)
      : null;

  // Canonical retailer id filter
  const retailerFilter = rawRetailer.trim().toLowerCase() || null;

  // Grade filter: "unscored" is a valid pseudo-grade (score===null)
  const gradeFilterRaw = rawGrade.trim().toUpperCase();
  const gradeFilter: BariGrade | "unscored" | null =
    ALL_GRADES.has(gradeFilterRaw)
      ? (gradeFilterRaw as BariGrade)
      : gradeFilterRaw === "UNSCORED"
        ? "unscored"
        : null;

  // Search term
  const qTerm = rawQ.trim().toLowerCase();

  // ── Build and filter rows ────────────────────────────────────────────────
  let rows = buildInventoryRows();

  if (categoryFilter) {
    rows = rows.filter((r) => r.categoryId === categoryFilter);
  }

  if (retailerFilter) {
    rows = rows.filter((r) => r.retailer.id === retailerFilter);
  }

  if (gradeFilter === "unscored") {
    rows = rows.filter((r) => r.score === null);
  } else if (gradeFilter !== null) {
    rows = rows.filter((r) => r.grade === gradeFilter);
  }

  if (qTerm) {
    rows = rows.filter(
      (r) =>
        r.name.toLowerCase().includes(qTerm) ||
        (r.brand?.toLowerCase().includes(qTerm) ?? false)
    );
  }

  const total = rows.length;

  // ── Paginate ─────────────────────────────────────────────────────────────
  const offset = (page - 1) * pageSize;
  const pageRows = rows.slice(offset, offset + pageSize);

  return NextResponse.json({ rows: pageRows, total, page });
}
