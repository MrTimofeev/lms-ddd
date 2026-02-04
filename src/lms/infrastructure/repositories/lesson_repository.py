from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from lms.domain.repositories import LessonRepository
from lms.domain.lesson import Lesson, LessonId
from lms.domain.course import CourseId
from lms.infrastructure.database.models import LessonDB


class SQLAlchemyLessonRepository(LessonRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        
    async def get_by_id(self, lesson_id: LessonId) -> Optional[Lesson]:
        query = select(LessonDB).where(LessonDB.id == lesson_id)
        result = await self._session.execute(query)
        db_lesson = result.scalar_one_or_none()
        
        if db_lesson is None:
            return None
        
        return Lesson(
            id=LessonId(str(db_lesson.id)),
            course_id=CourseId(str(db_lesson.corse_id)),
            title=db_lesson.title,
            order=db_lesson.order,
        )
        
    