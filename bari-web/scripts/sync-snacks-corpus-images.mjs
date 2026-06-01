/**
 * Sync snacks_frontend_v2.json imageUrl from BSIP1 yochananof retailer URLs.
 * Product↔barcode matching only — no copy/score changes.
 *
 * Run: node scripts/sync-snacks-corpus-images.mjs
 */
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const corpusPath = join(root, "src/data/comparisons/snacks_frontend_v2.json");

/** Verified bsip1_*.json → yochananof image_url (2026-05-29 integrity pass). */
const IMAGE_BY_PRODUCT_ID = {
  "snk-001":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290011498870_s1_0004-09-2026_10-52-18.jpg",
  "snk-002":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290011498948_s1_1505-10-2020_23-00-27.jpg",
  "snk-003":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/0/1/016000548404_s1_1512-29-2024_06-37-26.jpg",
  "snk-004":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8423207206495_h105-15-2023_13-17-20.jpg",
  "snk-005":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/1/2/12505889_5900020039590.jpg",
  "snk-006": null,
  "snk-007":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/1/2/12506828_5900020015174.jpg",
  "snk-009":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8410076610379_s1_15_gs102-19-2024_08-41-10.jpg",
  "snk-010":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8410076610386_s1_15_gs102-19-2024_08-21-37.jpg",
  "snk-011":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290111936784_s104-01-2025_21-19-00.jpg",
  "snk-012":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290111937262_s104-01-2025_21-21-11.jpg",
  "snk-015":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290011498894_s1_0004-09-2026_11-01-01.jpg",
  "snk-016":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8423207210928_h105-15-2023_13-25-08.jpg",
  "snk-017":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8410076610508_s1_1503-02-2023_08-23-21.jpg",
  "snk-018":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8410076602251_s1_1512-29-2024_06-26-36.jpg",
  "snk-019":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/1/2/12615334_7290118247896.jpg",
  "snk-020":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290014525306_s105-31-2020_13-54-07.jpg",
  "snk-013":
    "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/4/0/4011800633516.jpg",
};

const corpus = JSON.parse(readFileSync(corpusPath, "utf-8"));
let updated = 0;

for (const product of corpus.products) {
  if (!(product.id in IMAGE_BY_PRODUCT_ID)) continue;
  const next = IMAGE_BY_PRODUCT_ID[product.id];
  if (product.imageUrl !== next) {
    product.imageUrl = next;
    updated += 1;
  }
}

corpus._meta.production_pass = `${corpus._meta.production_pass ?? ""} Image integrity pass 2026-05-29: BSIP1 yochananof URLs synced.`.trim();

writeFileSync(corpusPath, `${JSON.stringify(corpus, null, 2)}\n`, "utf-8");
const withImage = corpus.products.filter((p) => p.imageUrl).length;
console.log(`Updated ${updated} products. With imageUrl: ${withImage}/18.`);
