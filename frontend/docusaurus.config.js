// @ts-check
// `@ts-check` enables type checking for this file.

const {themes} = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI Textbook',
  tagline: 'Learn Physical AI with examples and RAG chatbot',
  favicon: 'img/favicon.ico',

  url: 'https://hackathon-1-physical-ai-olive.vercel.app',
  baseUrl: '/',

  organizationName: 'Ambreenzulfiqar',
  projectName: 'hackathon_1_physical_ai',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          routeBasePath: 'docs',
          sidebarPath: require.resolve('./sidebars.js'),
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
module.exports = config;
