import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  ...(process.env.DOCKER_BUILD === "true" ? { output: "standalone" } : {}),
  async rewrites() {
    const backend = process.env.BACKEND_INTERNAL_URL ?? process.env.NEXT_PUBLIC_API_URL?.replace(/\/api\/v1$/, "") ?? "http://127.0.0.1:8000";
    return [{ source: "/api/v1/:path*", destination: `${backend}/api/v1/:path*` }];
  },
};

export default nextConfig;
