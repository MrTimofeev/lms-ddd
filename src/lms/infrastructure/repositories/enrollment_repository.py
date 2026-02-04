from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from lms.domain.repositories import EnrollmentRepository
from lms.domain.enrollment import Enrollment, EnrollmentId, UserId, CourseId
from lms.infrastructure.database.models import EnrollmentDB


class SQLAlchemyEnrollmentRepository(EnrollmentRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        
    async def save(self, enrollment: Enrollment) -> None:
        db_enrollment = EnrollmentDB(
            id=enrollment.id,
            user_id=enrollment.user_id,
            course_id=enrollment.course_id,
            enrolled_at=enrollment.enrolled_at,
        )
        self._session.add(db_enrollment)
        
    async def get_by_id(self, enrollment_id: EnrollmentId) -> Optional[Enrollment]:
        query = select(EnrollmentDB).where(EnrollmentDB.id == enrollment_id)
        result = await self._session.execute(query)
        db_enrollment =  result.scalar_one_or_none()
        
        if db_enrollment is None:
            return None
        
        return Enrollment(
            id=EnrollmentId(str(db_enrollment.id)),
            user_id=UserId(str(db_enrollment.user_id)),
            course_id=CourseId(str(db_enrollment.course_id)),
            enrolled_at=db_enrollment.enrolled_at,
        )