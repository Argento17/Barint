import { NextResponse } from "next/server";

import { isAuthed } from "@/lib/admin/auth";
import { BLOG_DIR, blogDoc, extractProse } from "@/lib/admin/blog";
import { extractEditableFields, LIVE_COMPARISON_FILES } from "@/lib/admin/fields";
import { getComparisonFile, getRepoJson } from "@/lib/admin/github";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  const params = new URL(request.url).searchParams;
  const slug = params.get("slug") ?? "";
  const kind = params.get("kind") ?? "comparison";

  if (kind === "blog") {
    const doc = blogDoc(slug);
    if (!doc) {
      return NextResponse.json({ ok: false, error: "unknown_blog_doc" }, { status: 404 });
    }
    try {
      const { data, sha } = await getRepoJson(`${BLOG_DIR}/${doc.file}`);
      return NextResponse.json({
        ok: true,
        kind: "blog",
        slug,
        sha,
        nameHe: doc.labelHe,
        products: [
          { id: slug, name: doc.labelHe, score: null, grade: null, fields: extractProse(data) },
        ],
      });
    } catch (err) {
      return NextResponse.json(
        { ok: false, error: "load_failed", detail: String(err) },
        { status: 502 },
      );
    }
  }

  const file = LIVE_COMPARISON_FILES[slug];
  if (!file) {
    return NextResponse.json({ ok: false, error: "unknown_category" }, { status: 404 });
  }

  try {
    const { data, sha } = await getComparisonFile(file);
    const products = (data.products ?? []).map((p) => ({
      id: String(p.id ?? p.barcode ?? ""),
      name: typeof p.name === "string" ? p.name : "",
      score: p.score ?? null,
      grade: p.grade ?? null,
      fields: extractEditableFields(p),
    }));
    const nameHe =
      data._meta && typeof data._meta.name_he === "string" ? data._meta.name_he : slug;
    return NextResponse.json({ ok: true, kind: "comparison", slug, file, sha, nameHe, products });
  } catch (err) {
    return NextResponse.json(
      { ok: false, error: "load_failed", detail: String(err) },
      { status: 502 },
    );
  }
}
