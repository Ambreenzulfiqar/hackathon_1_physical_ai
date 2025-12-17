import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/Home',
    component: ComponentCreator('/Home', '6d6'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'f24'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'b87'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '997'),
            routes: [
              {
                path: '/docs/',
                component: ComponentCreator('/docs/', '0ee'),
                exact: true
              },
              {
                path: '/docs/basics-humanoid-robotics',
                component: ComponentCreator('/docs/basics-humanoid-robotics', 'bcb'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/capstone-ai-robot-pipeline',
                component: ComponentCreator('/docs/capstone-ai-robot-pipeline', 'b3f'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/digital-twin-simulation',
                component: ComponentCreator('/docs/digital-twin-simulation', 'bd4'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/intro-to-physical-ai',
                component: ComponentCreator('/docs/intro-to-physical-ai', '0f0'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/ros2-fundamentals',
                component: ComponentCreator('/docs/ros2-fundamentals', '3d0'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/vision-language-action',
                component: ComponentCreator('/docs/vision-language-action', '775'),
                exact: true,
                sidebar: "textbookSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
