import React, { useState, useEffect } from 'react';
import { useBaseUrlUtils } from '@docusaurus/useBaseUrl';
import { ApiClient } from '../services/api-client';

const Home = () => {
  const { withBaseUrl } = useBaseUrlUtils();
  const [chapters, setChapters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChapters = async () => {
      try {
        setLoading(true);
        const response = await ApiClient.getTextbooks();
        setChapters(response.chapters || []);
        setError(null);
      } catch (err) {
        setError('Failed to load textbook chapters');
        console.error('Error fetching chapters:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchChapters();
  }, []);

  if (loading) {
    return (
      <div className="container margin-vert--lg">
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container margin-vert--lg">
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="container margin-vert--lg">
      <div className="text-center margin-bottom--lg">
        <h1>Physical AI & Humanoid Robotics — Essentials</h1>
        <p className="hero__subtitle">
          A comprehensive textbook on Physical AI and Humanoid Robotics with integrated AI assistance
        </p>
      </div>

      <div className="row">
        <div className="col">
          <h2>Textbook Chapters</h2>

          {chapters.length > 0 ? (
            <div className="card-group">
              {chapters
                .sort((a, b) => a.order - b.order)
                .map((chapter) => (
                <div key={chapter.id} className="card margin-bottom--md">
                  <div className="card__body">
                    <h3>Chapter {chapter.order}: {chapter.title}</h3>
                    <p>
                      {chapter.word_count} words • ~{chapter.estimated_reading_time} min read
                    </p>
                    <a
                      href={withBaseUrl(`/docs/${chapter.slug}`)}
                      className="button button--primary button--outline"
                    >
                      Read Chapter
                    </a>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No chapters available yet.</p>
          )}
        </div>
      </div>

      <div className="row margin-top--lg">
        <div className="col col--6">
          <h3>About this Textbook</h3>
          <p>
            This textbook provides a comprehensive introduction to Physical AI and Humanoid Robotics.
            Each chapter builds upon the previous ones, taking you from fundamental concepts to
            advanced applications.
          </p>
        </div>
        <div className="col col--6">
          <h3>Interactive Learning</h3>
          <p>
            Use the integrated AI assistant to ask questions about the content as you read.
            Select text and click "Ask AI" to get clarifications based on the textbook content.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;

// Add CSS modules if needed