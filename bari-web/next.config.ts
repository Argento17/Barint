import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "api.yochananof.co.il",
        pathname: "/media/**",
      },
      {
        protocol: "https",
        hostname: "res.cloudinary.com",
        pathname: "/shufersal/**",
      },
      {
        protocol: "https",
        hostname: "media.shufersal.co.il",
      },
    ],
  },
};

export default nextConfig;
