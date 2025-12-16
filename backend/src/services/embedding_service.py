import openai
from typing import List, Dict, Any, Optional
import logging
from ..config.settings import settings
from .qdrant_client import QdrantManager

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        # Initialize OpenAI client
        openai.api_key = settings.openai_api_key
        self.qdrant_manager = QdrantManager()
        self.chunk_size = settings.embedding_chunk_size
        self.overlap = settings.embedding_overlap

    async def create_embeddings(self, text: str, content_id: str, content_type: str, title: str = "", chapter_slug: str = "") -> List[Dict[str, Any]]:
        """Create embeddings for text content"""
        try:
            # Split text into chunks
            text_chunks = self._split_text(text)

            embeddings = []
            for i, chunk in enumerate(text_chunks):
                # Create embedding using OpenAI
                response = openai.embeddings.create(
                    input=chunk,
                    model=settings.embedding_model
                )

                embedding_vector = response.data[0].embedding

                # Create a unique ID for this chunk
                chunk_id = f"{content_id}_chunk_{i}"

                embedding_data = {
                    "id": chunk_id,
                    "vector": embedding_vector,
                    "content_id": content_id,
                    "content_type": content_type,
                    "text_content": chunk,
                    "title": title,
                    "chapter_slug": chapter_slug
                }

                embeddings.append(embedding_data)

            # Add embeddings to Qdrant
            await self.qdrant_manager.add_embeddings(embeddings)

            logger.info(f"Created {len(embeddings)} embeddings for content {content_id}")
            return embeddings
        except Exception as e:
            logger.error(f"Error creating embeddings: {e}")
            raise

    def _split_text(self, text: str) -> List[str]:
        """Split text into chunks of specified size with overlap"""
        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            # If this is not the last chunk, try to break at a sentence or paragraph boundary
            if end < len(text):
                # Look for a good break point (sentence end, paragraph end, or space)
                search_start = end - self.overlap
                break_point = -1

                # Look for sentence endings first
                for i in range(min(end, len(text)) - 1, search_start - 1, -1):
                    if text[i] in '.!?':
                        break_point = i + 1
                        break

                # If no sentence end found, look for paragraph breaks
                if break_point == -1:
                    for i in range(min(end, len(text)) - 1, search_start - 1, -1):
                        if text[i] == '\n' and i + 1 < len(text) and text[i + 1] == '\n':
                            break_point = i + 2
                            break

                # If no good break point found, use overlap
                if break_point == -1:
                    break_point = end - self.overlap if end - self.overlap > start else end

                end = break_point

            chunk = text[start:end].strip()
            if chunk:  # Only add non-empty chunks
                chunks.append(chunk)

            start = end

        return chunks

    async def get_relevant_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get relevant content based on query using vector search"""
        try:
            # Create embedding for the query
            response = openai.embeddings.create(
                input=query,
                model=settings.embedding_model
            )

            query_embedding = response.data[0].embedding

            # Search in Qdrant for similar content
            results = await self.qdrant_manager.search_similar(
                query_vector=query_embedding,
                limit=limit
            )

            return results
        except Exception as e:
            logger.error(f"Error getting relevant content: {e}")
            raise

    async def delete_content_embeddings(self, content_id: str):
        """Delete all embeddings for a specific content ID"""
        try:
            await self.qdrant_manager.delete_embeddings([content_id])
        except Exception as e:
            logger.error(f"Error deleting content embeddings: {e}")
            raise

    async def process_textbook_chapter(self, chapter_id: str, title: str, content: str, slug: str):
        """Process a textbook chapter to create embeddings"""
        try:
            # Create embeddings for the chapter content
            embeddings = await self.create_embeddings(
                text=content,
                content_id=chapter_id,
                content_type="chapter",
                title=title,
                chapter_slug=slug
            )

            logger.info(f"Processed chapter {chapter_id} with {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Error processing textbook chapter: {e}")
            raise