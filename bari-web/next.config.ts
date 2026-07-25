import type { NextConfig } from "next";

// Security response headers. Applied via next.config so they ship on every
// Vercel response without an edge middleware. The admin editor gets a stricter
// anti-framing posture than the public site because it holds a write-to-prod
// session (its saves commit to the repo and auto-deploy).
const baseSecurityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  {
    key: "Strict-Transport-Security",
    value: "max-age=63072000; includeSubDomains; preload",
  },
  // Public pages may be embedded by us but not cross-origin.
  { key: "X-Frame-Options", value: "SAMEORIGIN" },
];

const adminSecurityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  {
    key: "Strict-Transport-Security",
    value: "max-age=63072000; includeSubDomains; preload",
  },
  // The authenticated editor must never be framed (clickjacking defense).
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Content-Security-Policy", value: "frame-ancestors 'none'" },
];

const nextConfig: NextConfig = {
  async headers() {
    return [
      { source: "/admin/:path*", headers: adminSecurityHeaders },
      { source: "/api/admin/:path*", headers: adminSecurityHeaders },
      { source: "/:path*", headers: baseSecurityHeaders },
    ];
  },
  images: {
    // ---- Image Optimization QUOTA CONTROLS (2026-07-25) -------------------------------
    // Vercel bills one "transformation" per distinct (src x width x quality x format) on a
    // cache MISS *or* STALE — so an expiring cache re-bills the same image forever. The
    // default minimumCacheTTL is 14400s (4 hours), which re-bills one image at one width up
    // to ~6x/day (~180x/month). Against 676 distinct product image URLs in the comparison
    // corpus, that is what exhausted the 5,000/month free-tier allowance — not image volume.
    //
    // Product images are content-addressed by barcode and effectively immutable, so a long
    // TTL costs nothing. To replace an image, change its URL (or add a version query) —
    // never shorten this TTL back just to re-fetch a single asset.
    minimumCacheTTL: 2678400, // 31 days
    // Next's defaults offer 15 candidate widths (8 deviceSizes + 7 imageSizes). Every width a
    // browser can request is a SEPARATE billable transformation, so widths this site never
    // renders are pure exposure. Product thumbnails display at 48-128px (see
    // bari-product-thumbnail.tsx, guide-product-row.tsx); heroes and charts are responsive.
    // Dropping the 2048/3840 tiers and the unused 32/384 steps takes the per-image ceiling
    // from 15 widths to 9. Widen deliberately if a new surface genuinely needs a size.
    deviceSizes: [640, 828, 1200, 1920],
    imageSizes: [48, 64, 96, 128, 256],
    // Pin the single quality actually used. Already Next's default, but pinning it means a
    // future `quality={90}` prop cannot silently mint a second full set of variants across
    // every product image.
    qualities: [75],
    // NOTE: `formats` is deliberately LEFT UNSET, which means webp only. Adding
    // ["image/avif", "image/webp"] would DOUBLE the variants — and the bill — for every
    // image. Do not add AVIF while on the free tier.
    // -----------------------------------------------------------------------------------
    // Product thumbnails are optimized/proxied through Next's image endpoint so they
    // are served SAME-ORIGIN from bari.digital/_next/image (never hotlinked to the
    // retailer host by the visitor's browser). This makes images survive ad blockers,
    // VPNs, and private-DNS filters that block third-party image domains, and removes
    // the dependency on a retailer host being reachable from every visitor's network.
    //
    // Every host that appears in a product image URL MUST be listed here — an
    // unconfigured host makes <Image> throw at request time. This is an EXPLICIT
    // allowlist by design: the `/_next/image?url=` endpoint fetches the given URL
    // server-side, so a broad host pattern (e.g. a whole-TLD `**.co.il` wildcard) is
    // a server-side request-forgery vector. When a new category introduces a new image
    // host, add it here explicitly rather than widening the pattern.
    remotePatterns: [
      // Cloudinary — scoped to the single cloud actually in use.
      { protocol: "https", hostname: "res.cloudinary.com", pathname: "/shufersal/**" },
      // Israeli retailer / brand image hosts in use across live categories.
      { protocol: "https", hostname: "api.yochananof.co.il" },
      { protocol: "https", hostname: "yochananof.co.il" },
      { protocol: "https", hostname: "media.shufersal.co.il" },
      { protocol: "https", hostname: "www.shufersal.co.il" },
      { protocol: "https", hostname: "vitamins4all.co.il" },
      { protocol: "https", hostname: "www.tinc.co.il" },
      { protocol: "https", hostname: "www.teva-call.co.il" },
      { protocol: "https", hostname: "www.solgar.co.il" },
      { protocol: "https", hostname: "www.biogaya.co.il" },
      { protocol: "https", hostname: "www.altman.co.il" },
    ],
  },
};

export default nextConfig;
