import React, { useState, useEffect } from 'react';
import { useLocation, useParams } from '@docusaurus/router';
import { useBaseUrlUtils } from '@docusaurus/useBaseUrl';
import { ApiClient } from '../../services/api-client';
import clsx from 'clsx';

const TextbookViewer = () => {
  const { slug } = useParams();
  const location = useLocation();
  const { withBaseUrl } = useBaseUrlUtils();
  const [chapter, setChapter] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showChat, setShowChat] = useState(false);
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    const fetchChapter = async () => {
      try {
        setLoading(true);
        const response = await ApiClient.getTextbookChapter(slug);
        setChapter(response);
        setError(null);
      } catch (err) {
        setError('Failed to load chapter content');
        console.error('Error fetching chapter:', err);
      } finally {
        setLoading(false);
      }
    };

    if (slug) {
      fetchChapter();
    }
  }, [slug]);

  // Function to handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText.length > 0) {
        setSelectedText(selectedText);
        // Show chat interface when text is selected
        setShowChat(true);
      } else {
        setSelectedText('');
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  if (loading) {
    return (
      <div className="textbook-content">
        <div className="text-center py-5">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="textbook-content">
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      </div>
    );
  }

  if (!chapter) {
    return (
      <div className="textbook-content">
        <div className="alert alert-info" role="alert">
          Chapter not found
        </div>
      </div>
    );
  }

  return (
    <div className="textbook-content">
      <article className="textbook-chapter">
        <header>
          <h1>{chapter.title}</h1>
          <p className="text-muted">
            Chapter {chapter.order} • {chapter.estimated_reading_time} min read • {chapter.word_count} words
          </p>
        </header>

        <div
          className="chapter-content"
          dangerouslySetInnerHTML={{ __html: chapter.content }}
        />

        <nav className="textbook-nav">
          <a href="#" className="btn btn-outline-primary">Previous Chapter</a>
          <a href="#" className="btn btn-primary">Next Chapter</a>
        </nav>
      </article>

      {/* Chat Interface - appears when text is selected */}
      {showChat && selectedText && (
        <div className="chat-interface">
          <div className="chat-header">
            <h5>Ask AI about selected text</h5>
          </div>
          <div className="chat-messages">
            <div className="message-assistant">
              <div className="message-bubble">
                You selected: "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
              </div>
            </div>
          </div>
          <div className="chat-input-area">
            <input
              type="text"
              className="chat-input"
              placeholder="Ask a question about the selected text..."
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  // Handle chat submission
                }
              }}
            />
            <button className="chat-button">Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TextbookViewer;