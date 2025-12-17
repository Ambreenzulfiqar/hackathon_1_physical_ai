// @ts-check
// `@ts-check` enables type checking for this file.

const {themes} = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics — Essentials',
  tagline: 'A comprehensive textbook on Physical AI and Humanoid Robotics',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-textbook-domain.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'your-organization', // Usually your GitHub org/user name.
  projectName: 'textbook-frontend', // Usually your repo name.

  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'ignore',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/your-username/textbook-frontend/edit/main/',
        },
        blog: false, // Disable blog if not needed
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI & Robotics',
        logo: {
          alt: 'Physical AI & Robotics Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'textbookSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/your-username/textbook-frontend',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Chapters',
            items: [
              {
                label: 'Introduction to Physical AI',
                to: '/docs/01-intro-to-physical-ai',
              },
              {
                label: 'Basics of Humanoid Robotics',
                to: '/docs/02-basics-humanoid-robotics',
              },
              {
                label: 'ROS 2 Fundamentals',
                to: '/docs/03-ros2-fundamentals',
              },
              {
                label: 'Digital Twin Simulation',
                to: '/docs/04-digital-twin-simulation',
              },
              {
                label: 'Vision-Language-Action Systems',
                to: '/docs/05-vision-language-action',
              },
              {
                label: 'Capstone: Simple AI-Robot Pipeline',
                to: '/docs/06-capstone-ai-robot-pipeline',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/your-username/textbook-frontend',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics — Essentials. Built with Docusaurus.`,
      },
      prism: {
        theme: themes.github,
        darkTheme: themes.dracula,
      },
    }),
};

module.exports = config;