import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Lets `next dev` serve its assets through a Cloudflare quick tunnel.
  allowedDevOrigins: ["*.trycloudflare.com"],
};

export default nextConfig;
