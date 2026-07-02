const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..");
const skip = new Set(["supermarket", "supplements", "personal-care", "raw-foods"]);

for (const ent of fs.readdirSync(path.join(root, "src/app/hashvaot"), { withFileTypes: true })) {
  if (!ent.isDirectory() || skip.has(ent.name)) continue;
  const p = path.join(root, "src/app/hashvaot", ent.name, "page.tsx");
  let text = fs.readFileSync(p, "utf8");
  if (!text.includes("ComparisonPageSeo")) continue;
  if (text.includes("<>\n    <ComparisonPageSeo")) continue;
  text = text.replace(
    /return \(\s*\n\s*<ComparisonPageSeo/,
    "return (\n    <>\n      <ComparisonPageSeo"
  );
  text = text.replace(/\n  \);\n\}$/, "\n    </>\n  );\n}");
  fs.writeFileSync(p, text, "utf8");
  console.log("fragment", ent.name);
}

// bread editorial articles
for (const slug of ["bread-everyday", "bread-standouts", "bread-wellness-gap"]) {
  const p = path.join(root, "src/app/blog", slug, "page.tsx");
  let text = fs.readFileSync(p, "utf8");
  if (text.includes("BlogArticleSeo")) continue;
  text = text.replace(
    /import type \{ Metadata \} from "next";\r?\n\r?\n/,
    'import type { Metadata } from "next";\n\nimport { BlogArticleSeo } from "@/components/seo/blog-article-seo";\nimport { absoluteUrl } from "@/lib/site-url";\n'
  );
  const url = `/blog/${slug}`;
  const block = `    <BlogArticleSeo\n      title={article.metaTitle}\n      description={article.metaDescription}\n      url={absoluteUrl("${url}")}\n    />\n`;
  text = text.replace(
    /return <BreadEditorialArticle article=\{article\} \/>;/,
    `return (\n    <>\n${block}      <BreadEditorialArticle article={article} />\n    </>\n  );`
  );
  fs.writeFileSync(p, text, "utf8");
  console.log("blog", slug);
}

// sugar-alcohols
const sa = path.join(root, "src/app/blog/sugar-alcohols/page.tsx");
let saText = fs.readFileSync(sa, "utf8");
if (!saText.includes("BlogArticleSeo")) {
  saText = saText.replace(
    /import type \{ Metadata \} from "next";\r?\n\r?\n/,
    'import type { Metadata } from "next";\n\nimport { BlogArticleSeo } from "@/components/seo/blog-article-seo";\nimport { absoluteUrl } from "@/lib/site-url";\n'
  );
  const block = `    <BlogArticleSeo\n      title={metadata.title as string}\n      description={metadata.description as string}\n      url={absoluteUrl("/blog/sugar-alcohols")}\n    />\n`;
  saText = saText.replace(/export default function/, "const pageTitle = metadata.title as string;\nconst pageDescription = metadata.description as string;\n\nexport default function");
  saText = saText.replace(/return (\s*)<Sugar/, `return (\n    <>\n${block}      <Sugar`);
  saText = saText.replace(/(\/>);\s*\n\}/, "$1\n    </>\n  );\n}");
  fs.writeFileSync(sa, saText, "utf8");
  console.log("sugar-alcohols");
}

// bread-analysis redirect - add seo optional skip per user list - skip is ok

console.log("fix done");
