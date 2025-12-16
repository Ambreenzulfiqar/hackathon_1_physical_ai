# Quickstart Guide: Physical AI & Humanoid Robotics — Essentials

**Feature**: 001-ai-humanoid-textbook
**Date**: 2025-12-17

## Overview
This guide provides a quick setup and deployment process for the Physical AI & Humanoid Robotics textbook with Docusaurus UI and RAG chatbot.

## Prerequisites
- Node.js 18+ (for Docusaurus frontend)
- Python 3.11+ (for FastAPI backend)
- Docker (for Qdrant vector database)
- Git

## Frontend Setup (Docusaurus)

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
Create `.env` file in the frontend directory:
```env
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
REACT_APP_TITLE=Physical AI & Humanoid Robotics — Essentials
```

### 3. Add Textbook Content
Place your textbook chapters in the `docs/` directory:
```
docs/
├── 01-intro-to-physical-ai.md
├── 02-basics-humanoid-robotics.md
├── 03-ros2-fundamentals.md
├── 04-digital-twin-simulation.md
├── 05-vision-language-action.md
└── 06-capstone-ai-robot-pipeline.md
```

### 4. Run Development Server
```bash
npm start
```
The frontend will be available at http://localhost:3000

## Backend Setup (FastAPI)

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/textbook
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key
OPENAI_API_KEY=your_openai_api_key
EMBEDDING_MODEL=text-embedding-3-small
```

### 4. Run Development Server
```bash
uvicorn src.api.main:app --reload --port 8000
```
The backend API will be available at http://localhost:8000

## Vector Database Setup (Qdrant)

### 1. Run Qdrant with Docker
```bash
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```

### 2. Configure Collection
The application will automatically create the required vector collections on first run.

## Initialize Textbook Content

### 1. Generate Embeddings
Run the content processing script to generate embeddings for your textbook:
```bash
cd backend
python -m src.services.embedding_service --process-content
```

### 2. Verify Content
Check that all 6 chapters are properly loaded:
```bash
curl http://localhost:8000/api/v1/textbook/chapters
```

## Running the Full Application

### 1. Start Services in Order
```bash
# Terminal 1: Start Qdrant
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# Terminal 2: Start Backend
cd backend
uvicorn src.api.main:app --reload --port 8000

# Terminal 3: Start Frontend
cd frontend
npm start
```

### 2. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Testing the AI Chatbot

1. Navigate to any textbook chapter
2. Select text and click "Ask AI" or use the chat interface
3. Verify that the AI responds with information from the textbook content only

## Deployment Considerations

### Free-tier Deployment
- Use Neon for PostgreSQL (free tier available)
- Deploy backend to platforms supporting Python/Free tier (e.g., Railway, Heroku)
- Deploy frontend to Netlify or Vercel (free tier available)
- Use Qdrant Cloud or self-hosted Qdrant

### Environment Variables for Production
Update your deployment environment with:
- Production database URLs
- API keys for production
- Correct API base URLs for frontend-backend communication

## Troubleshooting

### Common Issues
- **API calls failing**: Check that backend is running and API URL is correctly configured
- **AI responses not working**: Verify embedding generation completed successfully
- **Slow loading**: Check network connectivity and database connection

### Verification Commands
```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend connectivity to backend
curl http://localhost:8000/api/v1/textbook/chapters | head -20
```