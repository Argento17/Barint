import { writeFileSync } from "fs";

const slugs = [
  ["bread", "bread-comparison-page-data"],
  ["brined_cheeses", "brined-cheeses-page-data"],
  ["cereals", "cereals-page-data"],
  ["cheese", "cheese-page-data"],
  ["cookies_coffee", "cookies-coffee-page-data"],
  ["granola", "granola-page-data"],
  ["hard_cheeses", "hard-cheeses-page-data"],
  ["hummus", "hummus-comparison-page-data"],
  ["juices", "juices-page-data"],
  ["milk", "milk-page-data"],
  ["snacks", "snacks-comparison-page-data"],
  ["cakes_hard_cookies", "cakes-hard-cookies-page-data"],
  ["chocolate_bars", "chocolate-bars-comparison-page-data"],
  ["chocolate_tablets", "chocolate-tablets-comparison-page-data"],
  ["protein_bars", "protein-bars-comparison-page-data"],
];

const out = {};
for (const [slug, mod] of slugs) {
  const m = await import(`../src/lib/comparisons/${mod}.ts`);
  const prefix = slug.replace(/_([a-z])/g, (_, c) => c.toUpperCase()).replace(/^./, (c) => c);
  // find hero key
  const heroKey = Object.keys(m).find((k) => k.endsWith("Hero") && typeof m[k] === "object");
  const prologueKey = Object.keys(m).find((k) => k.includes("Prologue"));
  const methodologyKey = Object.keys(m).find((k) => k.includes("Methodology"));
  const categoryNoteKey = Object.keys(m).find((k) => k.includes("CategoryNote"));
  const metadataKey = Object.keys(m).find((k) => k.includes("ComparisonMetadata") || k.endsWith("Metadata"));
  if (!heroKey || !prologueKey) { console.warn("skip", slug); continue; }
  out[slug] = {
    hero: m[heroKey],
    prologue: [...(m[prologueKey] ?? [])],
    methodology: methodologyKey ? [...(m[methodologyKey] ?? [])] : [],
  };
  if (categoryNoteKey && m[categoryNoteKey]) out[slug].categoryNote = m[categoryNoteKey];
  if (metadataKey && m[metadataKey]) {
    const md = m[metadataKey];
    out[slug].metadata = { title: md.title ?? "", description: md.description ?? "" };
  }
}
writeFileSync("src/data/site-content/comparison-pages.json", JSON.stringify(out, null, 2), "utf8");
console.log("wrote", Object.keys(out).length, "pages");
