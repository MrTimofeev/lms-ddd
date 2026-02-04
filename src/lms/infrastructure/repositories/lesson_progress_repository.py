from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from lms.domain.repositories import LessonProgressRepository
from lms.domain.lesson_progress import LessonProgress, LessonProgressId
from lms.domain.lesson import LessonId
from lms.domain.enrollment import EnrollmentID
from lms.infrastructure.database.models import LessonProgressDB


class SQLAlchemyLessonProgressRepository(LessonProgressRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        
    async def save(self, progress: LessonProgress) -> None:
        db_progress = LessonProgressDB(
            id=progress.id,
            enrollment_id=progress.enrollment_id,
            lesson_id=progress.lesson_id,
            completed_at=progress.completed_at,
        )
        self._session.add(db_progress)
        
    async def get_by_enrollment_and_lesson(
        self, enrollmetn_id: EnrollmentID, lesson_id: LessonId
    ) -> Optional[LessonProgress]:
        query = select(LessonProgressDB).where(
            LessonProgressDB.enrollment_id == enrollmetn_id,
            LessonProgressDB.lesson_id == lesson_id,
        )
        result = await self._session.execute(query)
        db_progress = result.scalar_one_or_none()
        
        if db_progress is None:
            return None
        
        return LessonProgress(
            id=LessonProgressId(str(db_progress.id)),
            enrollment_id=EnrollmentID(str(db_progress.enrollment_id)),
            lesson_id=LessonId(str(db_progress.lesson_id)),
            completed_at=db_progress.completed_at,
        )
        
    async def count_completed_by_enrollment(self, enrollment_id: EnrollmentID) -> int:
        query = select(func.count(LessonProgressDB.id)).where(
            LessonProgressDB.enrollment_id == enrollment_id
        )
        result = await self._session(query)
        return result.scalar_one() or 0