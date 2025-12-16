from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from ...config.database import get_async_db
from ...models.textbook_chapter import TextbookChapter
from ...services.content_service import ContentService

router = APIRouter(prefix="/textbook", tags=["textbook"])

@router.get("/chapters")
async def get_all_chapters(
    db: AsyncSession = Depends(get_async_db)
) -> List[dict]:
    """
    Retrieve list of all textbook chapters
    """
    try:
        content_service = ContentService(db)
        chapters = await content_service.get_all_chapters()

        return {
            "chapters": [
                {
                    "id": chapter.id,
                    "title": chapter.title,
                    "slug": chapter.slug,
                    "order": chapter.order,
                    "word_count": chapter.word_count,
                    "estimated_reading_time": chapter.estimated_reading_time
                }
                for chapter in chapters
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chapters: {str(e)}")


@router.get("/chapters/{slug}")
async def get_chapter_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_async_db)
) -> dict:
    """
    Retrieve content of a specific chapter by slug
    """
    try:
        content_service = ContentService(db)
        chapter = await content_service.get_chapter_by_slug(slug)

        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        # For now, returning sections as empty - we'll implement section parsing later
        return {
            "id": chapter.id,
            "title": chapter.title,
            "slug": chapter.slug,
            "content": chapter.content,
            "order": chapter.order,
            "sections": []  # Will be implemented later with proper section parsing
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chapter: {str(e)}")