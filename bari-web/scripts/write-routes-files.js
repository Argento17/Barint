const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");

function w(rel, c) {
  const a = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(a), { recursive: true });
  fs.writeFileSync(a, c, "utf8");
  console.log("wrote", rel);
}

w("src/app/api/admin/categories/route.ts", [
  'import { NextResponse } from "next/server";',
  "",
  'import { isAuthed } from "@/lib/admin/auth";',
  'import { listComparisonEntries, SITE_CONTENT_ENTRIES } from "@/lib/admin/content-registry";',
  'import { LIVE_COMPARISON_FILES } from "@/lib/admin/fields";',
  'import { getComparisonFile } from "@/lib/admin/github";',
  "",
  'export const runtime = "nodejs";',
  'export const dynamic = "force-dynamic";',
  "",
  "export async function GET() {",
  "  if (!(await isAuthed())) {",
  '    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });',
  "  }",
  "",
  "  const slugs = Object.keys(LIVE_COMPARISON_FILES).sort();",
  "  const products = await Promise.all(",
  "    slugs.map(async (slug) => {",
  "      const file = LIVE_COMPARISON_FILES[slug];",
  "      try {",
  "        const { data } = await getComparisonFile(file);",
  "        const meta = data._meta ?? {};",
  "        return {",
  "          slug,",
  "          file,",
  '          nameHe: typeof meta.name_he === "string" ? meta.name_he : slug,',
  "          productCount: (data.products ?? []).length,",
  "        };",
  "      } catch {",
  "        return { slug, file, nameHe: slug, productCount: 0, unavailable: true };",
  "      }",
  "    }),",
  "  );",
  "",
  "  const site = SITE_CONTENT_ENTRIES.map((entry) => ({",
  "    id: entry.id,",
  "    file: entry.file,",
  "    labelHe: entry.labelHe,",
  "  }));",
  "",
  "  const pageChrome = listComparisonEntries();",
  "",
  "  return NextResponse.json({ sections: { products, site, pageChrome } });",
  "}",
  "",
].join("\n"));

