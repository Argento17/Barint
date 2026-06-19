import { NextResponse } from "next/server";

import { isAuthed } from "@/lib/admin/auth";
import { applyEdits, LIVE_COMPARISON_FILES } from "@/lib/admin/fields";
import { getComparisonFile, githubConfigured, putComparisonFile } from "@/lib/admin/github";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Body: { slug: string, edits: { [productId]: { [fieldPath]: string | string[] } } }
 *
 * Re-fetches the live file, applies only whitelisted copy edits (applyEdits
 * rejects everything else — scores can never be written), and commits. The
 * commit triggers a Vercel rebuild → live in ~2 min.
 */
export async function POST(request: Request) {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }
  if (!githubConfigured()) {
    return NextResponse.json({ ok: false, error: "github_not_configured" }, { status: 503 });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ ok: false, error: "bad_request" }, { status: 400 });
  }

  if (!body || typeof body !== "object") {
    return NextResponse.json({ ok: false, error: "bad_request" }, { status: 400 });
  }
  const { slug, edits } = body as { slug?: unknown; edits?: unknown };

  if (typeof slug !== "string" || !LIVE_COMPARISON_FILES[slug]) {
    return NextResponse.json({ ok: false, error: "unknown_category" }, { status: 404 });
  }
  if (!edits || typeof edits !== "object") {
    return NextResponse.json({ ok: false, error: "no_edits" }, { status: 400 });
  }

  const file = LIVE_COMPARISON_FILES[slug];

  let data: Awaited<ReturnType<typeof getComparisonFile>>["data"];
  let sha: string;
  try {
    ({ data, sha } = await getComparisonFile(file));
  } catch (err) {
    return NextResponse.json(
      { ok: false, error: "load_failed", detail: String(err) },
      { status: 502 },
    );
  }

  const products = data.products ?? [];
  const index = new Map<string, Record<string, unknown>>();
  for (const p of products) {
    index.set(String(p.id ?? p.barcode ?? ""), p);
  }

  let applied = 0;
  let productsTouched = 0;
  const rejected: string[] = [];

  for (const [productId, rawFieldEdits] of Object.entries(edits as Record<string, unknown>)) {
    const product = index.get(productId);
    if (!product) {
      rejected.push(`product:${productId}`);
      continue;
    }
    if (!rawFieldEdits || typeof rawFieldEdits !== "object") {
      rejected.push(`product:${productId}:bad_shape`);
      continue;
    }
    const result = applyEdits(product, rawFieldEdits as Record<string, unknown>);
    applied += result.applied;
    rejected.push(...result.rejected.map((path) => `${productId}:${path}`));
    if (result.applied > 0) productsTouched += 1;
  }

  if (applied === 0) {
    return NextResponse.json({ ok: false, error: "no_valid_edits", rejected }, { status: 400 });
  }

  const message = `Admin copy edit: ${slug} — ${applied} field(s) across ${productsTouched} product(s) [TASK-340]`;
  try {
    const { commitSha } = await putComparisonFile(file, data, sha, message);
    return NextResponse.json({ ok: true, applied, productsTouched, rejected, commitSha });
  } catch (err) {
    return NextResponse.json(
      { ok: false, error: "commit_failed", detail: String(err) },
      { status: 502 },
    );
  }
}
