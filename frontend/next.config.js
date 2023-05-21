/** @type {import('next').NextConfig} */
const nextTranslate = require("next-translate-plugin");

const nextConfig = {
  ...nextTranslate(),
  reactStrictMode: true,
  publicRuntimeConfig: {
    APP_NAME: "OAuth Profile",
    API_BASE_URL: process.env.API_BASE_URL,
  },
}

module.exports = nextConfig;
