# Snacks Image Integrity Audit v1

**Date:** 2026-05-29  
**Route:** `/hashvaot/snacks`  
**Scope:** Product row thumbnails on frozen comparison shelf (`ProductRow` → `next/image`)

---

## Executive summary

| Finding | Severity |
|---------|----------|
| **11/18** products had `imageUrl: null` in `snacks_frontend_v2.json` | High — intentional CE v2 gaps, not a React bug |
| **3/7** “with URL” products had **wrong barcode image** assigned | High — wrong product photo or misleading pack |
| **1** product had a URL pointing at a **different SKU** (honey oats image on granola bar) | High — removed |
| Next.js `remotePatterns`, `ProductRow` fallback, and domain allowlist | **OK** — no code defect found |

**Remediation:** Synced `imageUrl` from BSIP1 canonical retail scrape (`canonical_bsip1/run_001/bsip1_*.json`) where `source_retailers` includes **yohananof** and product name matches shelf SKU. **17/18** products now have valid yochananof URLs; **snk-006** remains placeholder (no yochananof image in BSIP1).

---

## Rendering stack (verified)

| Layer | File | Behavior |
|-------|------|----------|
| Corpus | `src/data/comparisons/snacks_frontend_v2.json` | `imageUrl` string or `null` |
| Loader | `src/lib/comparisons/snacks-comparison-page-data.ts` | Static import; strips `_internal_cluster` only |
| UI | `src/components/shared/product-row.tsx` | `ProductImage`: if `!imageUrl \|\| failed` → neutral `#F3F3EE` box; else `next/image` with `onError → setFailed(true)` |
| Next config | `next.config.ts` | `api.yochananof.co.il` /media/** allowed ✓ |

**Not used on shelf:** `SnackShelfProductImage` (legacy engine/blog uses native `<img>`).

---

## Corpus state

### Before fix

| Metric | Count |
|--------|------:|
| Products on shelf | 18 |
| `imageUrl` non-null | 7 |
| `imageUrl` null | 11 |

### After fix (2026-05-29)

| Metric | Count |
|--------|------:|
| `imageUrl` non-null | **17** |
| `imageUrl` null (graceful fallback) | **1** (`snk-006`) |

---

## Per-product audit

| ID | Product | Before | After | BSIP1 source | Notes |
|----|---------|--------|-------|--------------|-------|
| snk-001 | חטיף תמרים חמאת שקדים | URL ✓ | URL ✓ | `bsip1_7290011498870` | Unchanged |
| snk-002 | תמרים ציפוי שוקולד 100% קקאו | URL ✗ wrong | URL ✓ | `bsip1_7290011498948` | Was `7290111937262` (פרי מארז קקאו pack) |
| snk-003 | קראנצ'י שיבולת דבש | URL ✓ | URL ✓ | `bsip1_16000548404` | Unchanged |
| snk-004 | מרבה סלים דליס שוקולד מריר | null | URL ✓ | `bsip1_8423207206495` | Added |
| snk-015 | תמרים חמאת בוטנים | null | URL ✓ | `bsip1_7290011498894` | Added |
| snk-016 | סלים טופינג לוז | null | URL ✓ | `bsip1_8423207210928` | Added |
| snk-009 | NV פרוטאין בוטנים שוקולד | URL ✗ wrong | URL ✓ | `bsip1_8410076610379` | Was Chewy line `8410076610508` |
| snk-005 | פיטנס קלאסי | null | URL ✓ | `bsip1_5900020039590` | Added |
| snk-018 | קראנצ'י שוקולד | null | URL ✓ | `bsip1_8410076602251` | Added |
| snk-010 | NV פרוטאין קרמל מלוח | null | URL ✓ | `bsip1_8410076610386` | Added |
| snk-011 | פרי מארז תמרים לוז | URL ✓ | URL ✓ | `bsip1_7290111936784` | Unchanged |
| snk-012 | פרי מארז תמרים קקאו | null | URL ✓ | `bsip1_7290111937262` | Receives URL freed from snk-002 |
| snk-019 | פיטנס שיבולת דבש | null | URL ✓ | `bsip1_7290118427896` | Added |
| snk-017 | NV צ'ואי שוקולד מריר | null | URL ✓ | `bsip1_8410076610508` | Chewy pack (closest yochananof match) |
| snk-020 | סלים קריספי אוכמניות | null | URL ✓ | `bsip1_7290014525306` | Added |
| snk-007 | פיטנס שוקולד מריר | null | URL ✓ | `bsip1_5900020015174` | Added |
| snk-006 | פיטנס בר גרנולה שוקולד | URL ✗ wrong | **null** | `bsip1_7290118427858` | BSIP1 `image_url: null` (carrefour only); removed misassigned honey-oats URL |
| snk-013 | קורני שחור לבן | URL ✓ | URL ✓ | `bsip1_4011800633516` | Unchanged |

---

## URL validation

Sample HEAD requests to `api.yochananof.co.il` (2026-05-29): **HTTP 200**, `image/jpeg`.

Next.js remote pattern:

```ts
{ protocol: "https", hostname: "api.yochananof.co.il", pathname: "/media/**" }
```

All synced URLs match this pattern.

---

## Root causes (not layout / not Next.js config)

1. **CE v2 corpus** shipped interpretive copy without backfilling `imageUrl` for new SKUs (snk-015–020).
2. **Cross-SKU assignment** in pre-v2 `snack-page-data.ts` (e.g. snk-002 ↔ snk-012 swap, snk-009 Chewy vs Protein).
3. **snk-006** used honey-oats pack image (`7290118247896`) for granola bar — visually wrong; BSIP1 has no yochananof image for granola SKU.

---

## Fixes applied

| File | Change |
|------|--------|
| `src/data/comparisons/snacks_frontend_v2.json` | 14 `imageUrl` fields updated via integrity map |
| `src/lib/comparisons/snack-page-data.ts` | `image_url` aligned for legacy/engine parity (data only) |
| `scripts/sync-snacks-corpus-images.mjs` | Regeneration script (BSIP1 map, no copy changes) |

**Not changed:** scores, expansion copy, filters, `ProductRow` layout, `ComparisonShelfPage`, CE methodology.

---

## Fallback behavior (preserved)

When `imageUrl` is `null` or remote load fails (`onError`):

- Renders **66×66px** rounded neutral tile (`#F3F3EE`, inset border).
- `aria-hidden` on image/placeholder (decorative; product name remains in row text).

**Expected placeholder:** `snk-006` until yochananof scrape provides `פיטנס בר גרנולה שוקולד מריר` image.

---

## Remaining risks

| Risk | Mitigation |
|------|------------|
| Yochananof CDN blocks Next optimizer in some environments | Monitor; if needed, `unoptimized` on external host only (separate engineering change) |
| BSIP1 name ≠ shelf `name_he` (multi-pack vs single) | Only mapped where canonical_name_he clearly matches SKU |
| Stale cache URLs | Re-run `node scripts/sync-snacks-corpus-images.mjs` after BSIP1 refresh |
| snk-006 no public image | Accept placeholder or add URL when scrape completes |

---

## Verification checklist

- [ ] Hard refresh `/hashvaot/snacks`
- [ ] Confirm **17** product photos load
- [ ] Confirm **snk-006** shows neutral placeholder only
- [ ] Confirm snk-002 shows chocolate-dates pack (not pri-maarez multi-pack unless that SKU is intentional)
- [ ] `npm run build` passes

---

## Commands

```bash
node scripts/sync-snacks-corpus-images.mjs
npm run lint
npm run build
```
