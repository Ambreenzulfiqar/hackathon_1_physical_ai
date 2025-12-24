import React, { JSX } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function Home(): JSX.Element {
  return (
    <Layout
      title="Physical AI Textbook"
      description="An interactive Physical AI textbook with RAG chatbot">

      <main style={{ padding: '4rem 1rem', textAlign: 'center' }}>
        <h1>📘 Physical AI Textbook</h1>

        <p style={{ fontSize: '1.2rem', maxWidth: '700px', margin: '1rem auto' }}>
          Learn Physical AI through structured chapters, examples,
          and an intelligent RAG-based chatbot.
        </p>

        <div style={{ marginTop: '2rem' }}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            📖 Start Reading
          </Link>

          <Link
            className="button button--secondary button--lg"
            style={{ marginLeft: '1rem' }}
            to="/docs/intro">
            📚 View Chapters
          </Link>
        </div>

        <section style={{ marginTop: '4rem' }}>
          <h2>✨ Features</h2>
          <ul style={{ listStyle: 'none', padding: 0, fontSize: '1.1rem' }}>
            <li>✅ Structured AI textbook</li>
            <li>✅ Physical AI concepts</li>
            <li>✅ RAG chatbot integration</li>
            <li>✅ Built with Docusaurus</li>
          </ul>
        </section>
      </main>
    </Layout>
  );
}