from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
import logging
from datetime import datetime

from ..models.textbook_chapter import TextbookChapter
from ..config.settings import settings

logger = logging.getLogger(__name__)

class ContentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_chapters(self) -> List[TextbookChapter]:
        """Retrieve all textbook chapters ordered by their sequence"""
        try:
            # Query all chapters ordered by sequence
            query = select(TextbookChapter).order_by(TextbookChapter.order)
            result = await self.db.execute(query)
            chapters = result.scalars().all()
            return chapters
        except Exception as e:
            logger.error(f"Error retrieving all chapters: {e}")
            raise

    async def get_chapter_by_id(self, chapter_id: str) -> Optional[TextbookChapter]:
        """Retrieve a specific chapter by its ID"""
        try:
            query = select(TextbookChapter).where(TextbookChapter.id == chapter_id)
            result = await self.db.execute(query)
            chapter = result.scalar_one_or_none()
            return chapter
        except Exception as e:
            logger.error(f"Error retrieving chapter by ID {chapter_id}: {e}")
            raise

    async def get_chapter_by_slug(self, slug: str) -> Optional[TextbookChapter]:
        """Retrieve a specific chapter by its slug"""
        try:
            query = select(TextbookChapter).where(TextbookChapter.slug == slug)
            result = await self.db.execute(query)
            chapter = result.scalar_one_or_none()
            return chapter
        except Exception as e:
            logger.error(f"Error retrieving chapter by slug {slug}: {e}")
            raise

    async def create_chapter(self, title: str, slug: str, content: str, order: int) -> TextbookChapter:
        """Create a new textbook chapter"""
        try:
            # Calculate word count and estimated reading time
            word_count = len(content.split())
            estimated_reading_time = max(1, word_count // 200)  # 200 words per minute

            # Create new chapter
            chapter = TextbookChapter(
                title=title,
                slug=slug,
                content=content,
                order=order,
                word_count=word_count,
                estimated_reading_time=estimated_reading_time
            )

            self.db.add(chapter)
            await self.db.commit()
            await self.db.refresh(chapter)

            logger.info(f"Created new chapter: {title} (ID: {chapter.id})")
            return chapter
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating chapter: {e}")
            raise

    async def update_chapter(self, chapter_id: str, **kwargs) -> Optional[TextbookChapter]:
        """Update an existing textbook chapter"""
        try:
            # Get the chapter to update
            chapter = await self.get_chapter_by_id(chapter_id)
            if not chapter:
                return None

            # Update provided fields
            for key, value in kwargs.items():
                if hasattr(chapter, key) and key in ['title', 'content', 'order', 'slug']:
                    if key == 'content':
                        # If content is being updated, recalculate word count and reading time
                        word_count = len(value.split())
                        estimated_reading_time = max(1, word_count // 200)
                        setattr(chapter, 'word_count', word_count)
                        setattr(chapter, 'estimated_reading_time', estimated_reading_time)

                    setattr(chapter, key, value)

            # Update the updated_at timestamp
            chapter.updated_at = datetime.now()

            await self.db.commit()
            await self.db.refresh(chapter)

            logger.info(f"Updated chapter: {chapter_id}")
            return chapter
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating chapter {chapter_id}: {e}")
            raise

    async def delete_chapter(self, chapter_id: str) -> bool:
        """Delete a textbook chapter"""
        try:
            chapter = await self.get_chapter_by_id(chapter_id)
            if not chapter:
                return False

            await self.db.delete(chapter)
            await self.db.commit()

            logger.info(f"Deleted chapter: {chapter_id}")
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting chapter {chapter_id}: {e}")
            raise

    async def get_chapters_by_range(self, start: int, end: int) -> List[TextbookChapter]:
        """Retrieve chapters within a specific order range"""
        try:
            query = select(TextbookChapter).where(
                TextbookChapter.order >= start,
                TextbookChapter.order <= end
            ).order_by(TextbookChapter.order)

            result = await self.db.execute(query)
            chapters = result.scalars().all()
            return chapters
        except Exception as e:
            logger.error(f"Error retrieving chapters by range {start}-{end}: {e}")
            raise

    async def get_next_chapter(self, current_order: int) -> Optional[TextbookChapter]:
        """Get the next chapter after the current one"""
        try:
            query = select(TextbookChapter).where(
                TextbookChapter.order > current_order
            ).order_by(TextbookChapter.order).limit(1)

            result = await self.db.execute(query)
            next_chapter = result.scalar_one_or_none()
            return next_chapter
        except Exception as e:
            logger.error(f"Error retrieving next chapter after order {current_order}: {e}")
            raise

    async def get_previous_chapter(self, current_order: int) -> Optional[TextbookChapter]:
        """Get the previous chapter before the current one"""
        try:
            query = select(TextbookChapter).where(
                TextbookChapter.order < current_order
            ).order_by(TextbookChapter.order.desc()).limit(1)

            result = await self.db.execute(query)
            prev_chapter = result.scalar_one_or_none()
            return prev_chapter
        except Exception as e:
            logger.error(f"Error retrieving previous chapter before order {current_order}: {e}")
            raise