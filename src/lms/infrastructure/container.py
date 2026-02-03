from sqlalchemy.ext.asyncio import AsyncSession

from lms.application.enroll_in_course import EnrollInCourseUseCase
from lms.infrastructure.repositories.course_repository import SQLAlchemyCourseRepository
from lms.infrastructure.repositories.enrollment_repository import SQLAlchemyEnrollmentRepository


def get_enroll_in_course_use_case(session: AsyncSession) -> EnrollInCourseUseCase:
    course_repo = SQLAlchemyCourseRepository(session)
    enrollment_repo = SQLAlchemyEnrollmentRepository(session)
    return EnrollInCourseUseCase(course_repo, enrollment_repo)