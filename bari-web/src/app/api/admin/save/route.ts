import { NextResponse } from "next/server";

import { isAuthed } from "@/lib/admin/auth";
import { applyProse, BLOG_DIR, blogDoc } from "@/lib/admin/blog";
import { getSiteContentEntry, PAGE_CHROME_FILE } from "@/lib/admin/content-registry";
import { applyEdits, LIVE_COMPARISON_FILES } from "@/lib/admin/fields";
import { applySiteEdits, extractPageChromeFields, extractSiteFields } from "@/lib/admin/site-fields";
import {
  getComparisonFile,
  getRepoJson,
  githubConfigured,
  putComparisonFile,
  putRepoJson,
  getSiteContentFile,
  putSiteContentFile,
} from "@/lib/admin/github";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Body: { kind?: "comparison" | "blog" | "page_chrome" | "site", slug, edits: { [itemId]: { [path]: value } } }
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

  const { slug, edits, kind } = body as { slug?: unknown; edits?: unknown; kind?: unknown };
  if (typeof slug !== "string") {
    return NextResponse.json({ ok: false, error: "bad_request" }, { status: 400 });
  }
  if (!edits || typeof edits !== "object") {
    return NextResponse.json({ ok: false, error: "no_edits" }, { status: 400 });
  }

  const docKind = typeof kind === "string" ? kind : "comparison";

  if (docKind === "blog") return saveBlog(slug, edits as Record<string, unknown>);
  if (docKind === "site") return saveSite(slug, edits as Record<string, unknown>);
  if (docKind === "page_chrome") return savePageChrome(slug, edits as Record<string, unknown>);
  return saveComparison(slug, edits as Record<string, unknown>);
}

async function saveBlog(slug: string, edits: Record<string, unknown>) {
  const doc = blogDoc(slug);
  if (!doc) {
    return NextResponse.json({ ok: false, error: "unknown_blog_doc" }, { status: 404 });
  }
  const repoPath = `${BLOG_DIR}/${doc.file}`;

  let data: Record<string, unknown>;
  let sha: string;
  try {
    ({ data, sha } = await getRepoJson(repoPath));
  } catch (err) {
    return NextResponse.json({ ok: false, error: "load_failed", detail: String(err) }, { status: 502 });
  }

  const fieldEdits = edits[slug];
  if (!fieldEdits || typeof fieldEdits !== "object") {
    return NextResponse.json({ ok: false, error: "no_edits" }, { status: 400 });
  }
  const result = applyProse(data, fieldEdits as Record<string, unknown>);
  if (result.applied === 0) {
    return NextResponse.json({ ok: false, error: "no_valid_edits", rejected: result.rejected }, { status: 400 });
  }

  const message = `Admin blog edit: ${slug} — ${result.applied} field(s) [TASK-350]`;
  try {
    const { commitSha } = await putRepoJson(repoPath, data, sha, message);
    return NextResponse.json({ ok: true, applied: result.applied, productsTouched: 1, rejected: result.rejected, commitSha });
  } catch (err) {
    return NextResponse.json({ ok: false, error: "commit_failed", detail: String(err) }, { status: 502 });
  }
}

async function saveSite(slug: string, edits: Record<string, unknown>) {
  const entry = getSiteContentEntry(slug);
  if (!entry) {
    return NextResponse.json({ ok: false, error: "unknown_site_id" }, { status: 404 });
  }
  let data: Record<string, unknown>;
  let sha: string;
  try {
    ({ data, sha } = await getSiteContentFile(entry.file));
  } catch (err) {
    return NextResponse.json({ ok: false, error: "load_failed", detail: String(err) }, { status: 502 });
  }
  const fieldEdits = edits[slug];
  if (!fieldEdits || typeof fieldEdits !== "object") {
    return NextResponse.json({ ok: false, error: "no_edits" }, { status: 400 });
  }
  const allowed = new Set(extractSiteFields(data).map((f) => f.path));
  const result = applySiteEdits(data, fieldEdits as Record<string, unknown>, allowed);
  if (result.applied === 0) {
    return NextResponse.json({ ok: false, error: "no_valid_edits", rejected: result.rejected }, { status: 400 });
  }
  const message = `Admin site edit: ${slug} — ${result.applied} field(s)`;
  try {
    const { commitSha } = await putSiteContentFile(entry.file, data, sha, message);
    return NextResponse.json({ ok: true, applied: result.applied, productsTouched: 1, rejected: result.rejected, commitSha });
  } catch (err) {
    return NextResponse.json({ ok: false, error: "commit_failed", detail: String(err) }, { status: 502 });
  }
}

async function savePageChrome(slug: string, edits: Record<string, unknown>) {
  let data: Record<string, unknown>;
  let sha: string;
  try {
    ({ data, sha } = await getSiteContentFile(PAGE_CHROME_FILE));
  } catch (err) {
    return NextResponse.json({ ok: false, error: "load_failed", detail: String(err) }, { status: 502 });
  }
  const pages = data as Record<string, Record<string, unknown>>;
  const chrome = pages[slug];
  if (!chrome) {
    return NextResponse.json({ ok: false, error: "unknown_slug" }, { status: 404 });
  }
  const fieldEdits = edits[slug];
  if (!fieldEdits || typeof fieldEdits !== "object") {
    return NextResponse.json({ ok: false, error: "no_edits" }, { status: 400 });
  }
  const allowed = new Set(extractPageChromeFields(chrome).map((f) => f.path));
  const result = applySiteEdits(chrome, fieldEdits as Record<string, unknown>, allowed);
  if (result.applied === 0) {
    return NextResponse.json({ ok: false, error: "no_valid_edits", rejected: result.rejected }, { status: 400 });
  }
  pages[slug] = chrome;
  const message = `Admin page chrome edit: ${slug} — ${result.applied} field(s)`;
  try {
    const { commitSha } = await putSiteContentFile(PAGE_CHROME_FILE, data, sha, message);
    return NextResponse.json({ ok: true, applied: result.applied, productsTouched: 1, rejected: result.rejected, commitSha });
  } catch (err) {
    return NextResponse.json({ ok: false, error: "commit_failed", detail: String(err) }, { status: 502 });
  }
}

async function saveComparison(slug: string, edits: Record<string, unknown>) {
  if (!LIVE_COMPARISON_FILES[slug]) {
    return NextResponse.json({ ok: false, error: "unknown_category" }, { status: 404 });
  }
  const file = LIVE_COMPARISON_FILES[slug];

  let data: Awaited<ReturnType<typeof getComparisonFile>>["data"];
  let sha: string;
  try {
    ({ data, sha } = await getComparisonFile(file));
  } catch (err) {
    return NextResponse.json({ ok: false, error: "load_failed", detail: String(err) }, { status: 502 });
  }

  const products = data.products ?? [];
  const index = new Map<string, Record<string, unknown>>();
  for (const p of products) index.set(String(p.id ?? p.barcode ?? ""), p);

  let applied = 0;
  let productsTouched = 0;
  const rejected: string[] = [];

  for (const [productId, rawFieldEdits] of Object.entries(edits)) {
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
    return NextResponse.json({ ok: false, error: "commit_failed", detail: String(err) }, { status: 502 });
  }
}
