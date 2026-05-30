import { readFileSync, writeFileSync } from "node:fs";

const path = "src/data/comparisons/bread_frontend_v2.json";

function scoreToGrade(score) {
  if (score >= 80) return "A";
  if (score >= 65) return "B";
  if (score >= 50) return "C";
  if (score >= 35) return "D";
  return "E";
}

const corpus = JSON.parse(readFileSync(path, "utf8"));
let fixed = 0;

for (const product of corpus.products) {
  const expected = scoreToGrade(product.score);
  if (product.grade !== expected) {
    console.log(`${product.name}: ${product.grade} -> ${expected} (${product.score})`);
    product.grade = expected;
    fixed += 1;
  }
}

corpus._meta.generated = "2026-05-30T00:00:00Z";
corpus._meta.production_pass =
  (corpus._meta.production_pass ?? "") +
  " Grade audit pass 2026-05-30: score_to_grade alignment.";

writeFileSync(path, `${JSON.stringify(corpus, null, 2)}\n`, "utf8");
console.log(`Fixed ${fixed} grade fields.`);
