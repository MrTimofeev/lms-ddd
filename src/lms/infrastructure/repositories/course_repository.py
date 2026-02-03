from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from lms.domain.repositories import CourseRepository
from lms.domain.course import Course, CourseId, CourseStatus
from lms.infrastructure.database.model import CourseDB

class SQLAlchemyCourseRepository(CourseRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def get_by_id(self, course_id: CourseId) -> Optional[Course]:
        query = select(CourseDB).where(CourseDB.id == course_id)
        result = await self._session.execute(query)
        db_course = result.scalar_one_or_none()
        
        if db_course is None:
            return None
        
        return Course(
            id=CourseId(str(db_course.id)),
            title=db_course.title,
            desriprion=db_course.desription,
            status=db_course.status,
        )
        