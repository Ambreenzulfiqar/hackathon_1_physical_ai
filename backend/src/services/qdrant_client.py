from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from typing import List, Dict, Any, Optional
import logging
from ..config.settings import settings

logger = logging.getLogger(__name__)

class QdrantManager:
    def __init__(self):
        # Initialize Qdrant client
        if settings.qdrant_api_key:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                prefer_grpc=False  # Using HTTP for simplicity
            )
        else:
            self.client = QdrantClient(url=settings.qdrant_url)

        # Collection name for textbook embeddings
        self.collection_name = "textbook_embeddings"

        # Initialize the collection if it doesn't exist
        self._init_collection()

    def _init_collection(self):
        """Initialize the Qdrant collection for textbook embeddings"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if self.collection_name not in collection_names:
                # Create collection for embeddings
                # Using 1536 dimensions for text-embedding-3-small model
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {e}")
            raise

    async def add_embeddings(self, points: List[Dict[str, Any]]):
        """Add embeddings to the collection"""
        try:
            # Prepare points for insertion
            qdrant_points = []
            for point in points:
                qdrant_points.append(
                    models.PointStruct(
                        id=point["id"],
                        vector=point["vector"],
                        payload={
                            "content_id": point["content_id"],
                            "content_type": point["content_type"],
                            "text_content": point["text_content"],
                            "title": point.get("title", ""),
                            "chapter_slug": point.get("chapter_slug", ""),
                            **point.get("metadata", {})
                        }
                    )
                )

            # Upload points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=qdrant_points
            )
            logger.info(f"Added {len(qdrant_points)} embeddings to collection")
        except Exception as e:
            logger.error(f"Error adding embeddings: {e}")
            raise

    async def search_similar(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar embeddings"""
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            results = []
            for hit in search_results:
                results.append({
                    "id": hit.id,
                    "content_id": hit.payload.get("content_id"),
                    "content_type": hit.payload.get("content_type"),
                    "text_content": hit.payload.get("text_content"),
                    "title": hit.payload.get("title", ""),
                    "chapter_slug": hit.payload.get("chapter_slug", ""),
                    "relevance_score": hit.score,
                    "metadata": {k: v for k, v in hit.payload.items()
                                if k not in ["content_id", "content_type", "text_content", "title", "chapter_slug"]}
                })

            return results
        except Exception as e:
            logger.error(f"Error searching embeddings: {e}")
            raise

    async def delete_embeddings(self, content_ids: List[str]):
        """Delete embeddings by content ID"""
        try:
            # Find points with matching content IDs
            points_to_delete = []
            for content_id in content_ids:
                # Search for points with this content_id
                search_results = self.client.search(
                    collection_name=self.collection_name,
                    query_filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="content_id",
                                match=models.MatchValue(value=content_id)
                            )
                        ]
                    ),
                    limit=1000  # Assuming max 1000 points per content_id
                )

                points_to_delete.extend([hit.id for hit in search_results])

            if points_to_delete:
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=models.PointIdsList(
                        points=points_to_delete
                    )
                )
                logger.info(f"Deleted {len(points_to_delete)} embeddings")
        except Exception as e:
            logger.error(f"Error deleting embeddings: {e}")
            raise

    async def get_embedding_by_id(self, point_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific embedding by its ID"""
        try:
            records = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[point_id]
            )

            if records:
                record = records[0]
                return {
                    "id": record.id,
                    "vector": record.vector,
                    "payload": record.payload
                }
            return None
        except Exception as e:
            logger.error(f"Error getting embedding by ID: {e}")
            raise

    def close(self):
        """Close the Qdrant client connection"""
        if hasattr(self, 'client'):
            # Qdrant client doesn't have a close method in most versions
            pass