import { NextResponse } from "next/server";

import { isAuthed } from "@/lib/admin/auth";
import { extractEditableFields, LIVE_COMPARISON_FILES } from "@/lib/admin/fields";
import { getComparisonFile } from "@/lib/admin/github";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  const slug = new URL(request.url).searchParams.get("slug") ?? "";
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
    return NextResponse.json({ ok: true, slug, file, sha, nameHe, products });
  } catch (err) {
    return NextResponse.json(
      { ok: false, error: "load_failed", detail: String(err) },
      { status: 502 },
    );
  }
}
