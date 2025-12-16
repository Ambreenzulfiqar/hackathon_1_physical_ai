from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional

from ...config.database import get_async_db
from ...services.rag_service import RAGService

router = APIRouter(prefix="/search", tags=["search"])

class SearchResponse(BaseModel):
    class SearchResult(BaseModel):
        id: str
        title: str
        content_snippet: str
        relevance_score: float
        url: str

    results: List[SearchResult]

@router.get("", response_model=SearchResponse)
async def search_textbook_content(
    q: str = Query(..., description="Search query string", min_length=1, max_length=500),
    limit: int = Query(5, ge=1, le=10, description="Number of results to return (max 10)"),
    db: AsyncSession = Depends(get_async_db)
) -> SearchResponse:
    """
    Search textbook content using RAG
    """
    try:
        rag_service = RAGService(db)
        results = await rag_service.search_content(q, limit=limit)

        return SearchResponse(
            results=[
                SearchResponse.SearchResult(
                    id=result.get("id", ""),
                    title=result.get("title", ""),
                    content_snippet=result.get("content_snippet", ""),
                    relevance_score=result.get("relevance_score", 0.0),
                    url=result.get("url", "")
                )
                for result in results
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching content: {str(e)}")