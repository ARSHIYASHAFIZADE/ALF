/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  devIndicators: false,
  env: {
    NEXT_PUBLIC_API_URL: "https://alf-zwtq.onrender.com",
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "https://alf-zwtq.onrender.com/api/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
