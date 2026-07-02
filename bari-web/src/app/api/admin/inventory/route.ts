/**
 * GET /api/admin/inventory
 *
 * Returns InventorySummaryVM — the cross-category rollup header payload for the
 * internal inventory dashboard. Auth-gated (mirrors /api/admin/categories pattern).
 *
 * Auth: requires a valid admin session cookie (isAuthed).
 * Returns 401 without an admin session.
 */

import { NextResponse } from "next/server";

import { isAuthed } from "@/lib/admin/auth";
import { buildInventoryRows, buildInventorySummary } from "@/lib/inventory/loader";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  const rows = buildInventoryRows();
  const summary = buildInventorySummary(rows);

  return NextResponse.json(summary);
}
