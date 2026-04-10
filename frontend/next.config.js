/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  devIndicators: false,
  env: {
    NEXT_PUBLIC_API_URL: "https://api-production-6cad.up.railway.app",
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "https://api-production-6cad.up.railway.app/api/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
