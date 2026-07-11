// TASK-478 Phase A — fetch retailer-hosted product images, self-host as WebP.
//
// Scans the frontend data files for images hotlinked from hosts the Vercel image
// optimizer CANNOT reach (Yochananof + supplement retailers → 502), downloads each
// from THIS machine (which can reach them), validates it is a real raster image,
// converts to WebP (≤256px, EXIF stripped), and writes public/products/<key>.webp.
//
// Emits two artifacts (does NOT touch data files — that is the rewrite step):
//   scripts/.image-migration-map.json   url → "/products/<key>.webp"  (or null if discarded)
//   public/products/_provenance.json     key → {sourceUrl, host, barcode, fetchedAt, bytes}
//
// Discard-not-fabricate: an image that won't fetch/decode is dropped (page keeps its ✦
// fallback); never substituted from another source. Run from bari-web/: node scripts/migrate-images-fetch.mjs

import fs from "node:fs";
import path from "node:path";
import sharp from "sharp";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "public", "products");
const MAP_PATH = path.join(ROOT, "scripts", ".image-migration-map.json");
const PROV_PATH = path.join(OUT_DIR, "_provenance.json");

// Every third-party host we self-host product images from. Phase A covered the
// optimizer-incompatible retailer hosts; Phase B adds Shufersal's Cloudinary + CDN so
// Bari owns 100% of its product imagery and depends on no third party at request time.
// Re-running is idempotent: already-migrated images are local (/products/…), not http,
// so they are never re-matched.
const EXTERNAL_IMG_HOST =
  /(^|\.)(yochananof\.co\.il|vitamins4all\.co\.il|teva-call\.co\.il|solgar\.co\.il|biogaya\.co\.il|altman\.co\.il|tinc\.co\.il|shufersal\.co\.il|cloudinary\.com)$/i;

const DATA_DIRS = ["src/data", "src/data/comparisons", "src/lib/comparisons"];
const URL_RE = /https?:\/\/[^\s"'\\)]+?\.(?:jpe?g|png|webp|gif)/gi;

function collectFiles() {
  const files = [];
  for (const d of DATA_DIRS) {
    const abs = path.join(ROOT, d);
    if (!fs.existsSync(abs)) continue;
    for (const f of fs.readdirSync(abs)) {
      if (/\.(json|ts)$/.test(f)) files.push(path.join(abs, f));
    }
  }
  return files;
}

// url → {barcode, files:Set}. Barcode = nearest preceding barcode/id (8–14 digits).
function extractTargets(files) {
  const targets = new Map();
  for (const file of files) {
    const txt = fs.readFileSync(file, "utf8");
    let m;
    URL_RE.lastIndex = 0;
    while ((m = URL_RE.exec(txt))) {
      const url = m[0];
      let host;
      try {
        host = new URL(url).host;
      } catch {
        continue;
      }
      if (!EXTERNAL_IMG_HOST.test(host)) continue;
      const before = txt.slice(Math.max(0, m.index - 800), m.index);
      const bc = [...before.matchAll(/(?:barcode|"id"|\bid)\s*[:=]\s*"?(\d{8,14})"?/g)].pop();
      const barcode = bc ? bc[1] : null;
      if (!targets.has(url)) targets.set(url, { barcode, files: new Set() });
      targets.get(url).files.add(path.basename(file));
      if (barcode && !targets.get(url).barcode) targets.get(url).barcode = barcode;
    }
  }
  return targets;
}

// Some data URLs are a third party's OWN Next.js image-optimizer wrapper
// (e.g. yochananof.co.il/_next/image?url=<encoded real image>). Fetching the wrapper
// 400s; the real raster lives in the `url` query param. Unwrap (recursively) to the
// real source, while keeping the ORIGINAL string as the map key for the data rewrite.
function unwrap(url) {
  let cur = url;
  for (let i = 0; i < 3; i++) {
    try {
      const u = new URL(cur);
      if (/\/_next\/image$/.test(u.pathname) && u.searchParams.get("url")) {
        cur = decodeURIComponent(u.searchParams.get("url"));
        continue;
      }
    } catch {
      break;
    }
    break;
  }
  return cur;
}

function keyFor(url, barcode) {
  if (barcode) return barcode;
  // Fall back to a short stable hash of the URL when no barcode is nearby.
  let h = 0;
  for (let i = 0; i < url.length; i++) h = (Math.imul(31, h) + url.charCodeAt(i)) | 0;
  return "img" + (h >>> 0).toString(36);
}

function loadJson(p) {
  try {
    return JSON.parse(fs.readFileSync(p, "utf8"));
  } catch {
    return {};
  }
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const targets = extractTargets(collectFiles());
  console.log(`Target external product images: ${targets.size}`);

  // Merge with any prior run (e.g. Phase A already self-hosted the retailer images) so
  // the manifests accumulate every image rather than overwrite the previous phase.
  const map = loadJson(MAP_PATH);
  const provenance = loadJson(PROV_PATH);
  let ok = 0,
    discarded = 0;
  const now = new Date().toISOString();

  for (const [url, info] of targets) {
    const fetchUrl = unwrap(url);
    // Barcode: prefer the one found next to the URL in data; else recover a 12–13 digit
    // GTIN from the (unwrapped) image filename.
    let barcode = info.barcode;
    if (!barcode) {
      const fnBc = fetchUrl.match(/(\d{12,13})/);
      if (fnBc) barcode = fnBc[1];
    }
    const key = keyFor(url, barcode);
    const outRel = `/products/${key}.webp`;
    const outAbs = path.join(OUT_DIR, `${key}.webp`);
    try {
      const res = await fetch(fetchUrl, {
        headers: {
          "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
          Accept: "image/avif,image/webp,image/*,*/*;q=0.8",
          Referer: "https://bari.digital/",
        },
        signal: AbortSignal.timeout(30000),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const ct = res.headers.get("content-type") || "";
      if (!/^image\//i.test(ct)) throw new Error(`non-image content-type ${ct}`);
      const buf = Buffer.from(await res.arrayBuffer());
      // Validate + normalize: sharp throws if it is not a decodable raster image.
      const webp = await sharp(buf)
        .rotate()
        .resize({ width: 256, height: 256, fit: "inside", withoutEnlargement: true })
        .webp({ quality: 82 })
        .toBuffer();
      fs.writeFileSync(outAbs, webp);
      map[url] = outRel;
      provenance[key] = {
        sourceUrl: url,
        fetchedFrom: fetchUrl !== url ? fetchUrl : undefined,
        host: new URL(fetchUrl).host,
        barcode,
        files: [...info.files],
        fetchedAt: now,
        bytes: webp.length,
      };
      ok++;
      console.log(`  ✓ ${key}.webp  (${(webp.length / 1024).toFixed(1)}KB)  ← ${new URL(url).host}`);
    } catch (e) {
      map[url] = null; // discard-not-fabricate
      discarded++;
      console.log(`  ✗ DISCARD ${key}  ${new URL(url).host}  — ${e.message}`);
    }
  }

  fs.writeFileSync(MAP_PATH, JSON.stringify(map, null, 2));
  fs.writeFileSync(PROV_PATH, JSON.stringify(provenance, null, 2));
  console.log(`\nDone: ${ok} self-hosted, ${discarded} discarded.`);
  console.log(`map → ${path.relative(ROOT, MAP_PATH)}`);
  console.log(`provenance → ${path.relative(ROOT, PROV_PATH)}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
