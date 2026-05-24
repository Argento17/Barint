import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "api.yochananof.co.il",
        pathname: "/media/**",
      },
    ],
  },
};

export default nextConfig;
