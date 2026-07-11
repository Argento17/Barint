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

// TASK-557 visual pass: the sweeteners guide draft embeds a youtube-nocookie.com video
// slot (build brief item 6). Scoped to that one route rather than widened into
// baseSecurityHeaders — no other page embeds an iframe today, so the allowance should not
// have a broader blast radius than the feature that needs it. `frame-src` governs iframes
// THIS page embeds; it does not affect whether this page itself can be framed (that's
// `frame-ancestors`, already covered by X-Frame-Options, which the catch-all `/:path*`
// rule below still applies to this route — headers from multiple matching sources merge,
// so this array only needs to ADD the CSP, not repeat the base set).
const sweetenerGuideSecurityHeaders = [
  {
    key: "Content-Security-Policy",
    value: "frame-src 'self' https://www.youtube-nocookie.com",
  },
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
      { source: "/madrichim/sweeteners", headers: sweetenerGuideSecurityHeaders },
      { source: "/:path*", headers: baseSecurityHeaders },
    ];
  },
  images: {
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
