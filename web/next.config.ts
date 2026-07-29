import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Firebase App Hosting builds this directly (Cloud Run under the hood) —
  // no `output: 'export'`, we need SSR/middleware for auth-gated routes.
  reactStrictMode: true,
};

export default nextConfig;
