/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
    formats: ['image/avif', 'image/webp'],
  },
  // Production optimizations
  compress: true,
  poweredByHeader: false,
  // API proxy for development
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api'}/:path*`,
      },
    ];
  },
  // Environment variables
  env: {
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1',
  },
};

module.exports = nextConfig;
