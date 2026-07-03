import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    // Product thumbnails are optimized/proxied through Next's image endpoint so they
    // are served SAME-ORIGIN from bari.digital/_next/image (never hotlinked to the
    // retailer host by the visitor's browser). This makes images survive ad blockers,
    // VPNs, and private-DNS filters that block third-party image domains, and removes
    // the dependency on a retailer host being reachable from every visitor's network.
    // Every host that appears in a product image URL MUST be listed here — an
    // unconfigured host makes <Image> throw at request time. The "**.co.il" wildcard
    // future-proofs new Israeli-retailer hosts added by later categories.
    remotePatterns: [
      { protocol: "https", hostname: "res.cloudinary.com" },
      { protocol: "https", hostname: "**.co.il" },
      // Explicit entries (redundant with the wildcard, kept for clarity of what ships today):
      { protocol: "https", hostname: "api.yochananof.co.il" },
      { protocol: "https", hostname: "yochananof.co.il" },
      { protocol: "https", hostname: "media.shufersal.co.il" },
      { protocol: "https", hostname: "www.shufersal.co.il" },
      { protocol: "https", hostname: "vitamins4all.co.il" },
    ],
  },
};

export default nextConfig;
