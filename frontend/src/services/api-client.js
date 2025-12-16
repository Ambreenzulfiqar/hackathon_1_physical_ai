// API Client for Textbook Application
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  static async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Textbook-related API calls
  static async getTextbooks() {
    return this.request('/textbook/chapters');
  }

  static async getTextbookChapter(slug) {
    return this.request(`/textbook/chapters/${slug}`);
  }

  // Chat-related API calls
  static async createChatSession(userId = null) {
    return this.request('/chat/session', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId }),
    });
  }

  static async sendChatMessage(sessionId, message, context = null) {
    return this.request(`/chat/${sessionId}/message`, {
      method: 'POST',
      body: JSON.stringify({
        message: message,
        context: context
      }),
    });
  }

  // Search-related API calls
  static async search(query, limit = 5) {
    const params = new URLSearchParams({ q: query, limit: limit.toString() });
    return this.request(`/search?${params}`);
  }
}

export { ApiClient };