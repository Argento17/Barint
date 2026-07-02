const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const FAQ = {
  bread: "bread",
  "breakfast-cereals": "breakfast_cereals",
  "brined-cheeses": "brined_cheeses",
  "cookies-coffee": "cookies_coffee",
  granola: "granola",
  "hard-cheeses": "hard_cheeses",
  hummus: "hummus",
  juices: "juices",
};

const skip = new Set(["supermarket", "supplements", "personal-care", "raw-foods"]);

function extractComponentJsx(text) {
  const m = text.match(/<([A-Z][A-Za-z]*ComparisonPage)[\s\S]*?\/>/);
  if (!m) throw new Error("ComparisonPage jsx not found");
  return m[0];
}

function transform(slug, text) {
  if (text.includes("ComparisonPageSeo") && text.includes("</>")) {
    return null;
  }

  text = text.replace(/import \{ buildFaqScript \} from "@\/lib\/seo\/faq-schema";\r?\n/g, "");
  text = text.replace(/import rawFaqSchema from "@\/data\/seo\/[^"]+";\r?\n/g, "");
  text = text.replace(/\s*<script type="application\/ld\+json"[\s\S]*?\/>\s*/g, "\n");
  text = text.replace(/return \(\s*<>\s*/g, "return (\n    TEMP_PLACEHOLDER\n");
  text = text.replace(/\s*<\/>\s*\);/g, "\n  );");

  const productsMatch = text.match(/products=\{(\w+)\}/);
  if (!productsMatch) throw new Error(`products not found in ${slug}`);
  const products = productsMatch[1];

  let componentJsx = extractComponentJsx(text);
  if (!componentJsx.includes("initialExpandedProductId")) {
    componentJsx = componentJsx.replace(/(\n\s*)\/>$/, "$1  initialExpandedProductId={initialExpandedProductId}\n$1/>");
  }

  const fnMatch = text.match(/export default (?:async )?function (\w+)/);
  if (!fnMatch) throw new Error(`fn not found in ${slug}`);
  const fnName = fnMatch[1];

  const metaEnd = text.indexOf("export default");
  let head = text.slice(0, metaEnd);
  if (!head.includes("ComparisonPageSeo")) {
    head = head.replace(
      /import type \{ Metadata \} from "next";\r?\n\r?\n/,
      'import type { Metadata } from "next";\n\nimport { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";\n'
    );
  }

  const faq = FAQ[slug];
  const faqAttr = faq ? ` faqKey="${faq}"` : "";

  const indented = componentJsx
    .split("\n")
    .map((line) => (line.trim() ? "      " + line.trimStart() : line))
    .join("\n");

  const body = `export default async function ${fnName}({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/${slug}" products={${products}}${faqAttr} />
${indented}
    </>
  );
}
`;

  return head + body;
}

for (const ent of fs.readdirSync(path.join(root, "src/app/hashvaot"), { withFileTypes: true })) {
  if (!ent.isDirectory() || skip.has(ent.name)) continue;
  const p = path.join(root, "src/app/hashvaot", ent.name, "page.tsx");
  if (!fs.existsSync(p)) continue;
  const original = fs.readFileSync(p, "utf8");
  try {
    const next = transform(ent.name, original);
    if (next) {
      fs.writeFileSync(p, next, "utf8");
      console.log("ok", ent.name);
    } else {
      console.log("skip", ent.name);
    }
  } catch (e) {
    console.error("fail", ent.name, e.message);
  }
}
