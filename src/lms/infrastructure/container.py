from sqlalchemy.ext.asyncio import AsyncSession

from lms.application.enroll_in_course import EnrollInCourseUseCase
from lms.infrastructure.repositories.course_repository import SQLAlchemyCourseRepository
from lms.infrastructure.repositories.enrollment_repository import SQLAlchemyEnrollmentRepository

from lms.application.complete_lesson import ComletedLessonUseCase
from lms.infrastructure.repositories.lesson_repository import SQLAlchemyLessonRepository
from lms.infrastructure.repositories.lesson_progress_repository import SQLAlchemyLessonProgressRepository

def get_enroll_in_course_use_case(session: AsyncSession) -> EnrollInCourseUseCase:
    course_repo = SQLAlchemyCourseRepository(session)
    enrollment_repo = SQLAlchemyEnrollmentRepository(session)
    return EnrollInCourseUseCase(course_repo, enrollment_repo)


def get_complete_lesson_use_case(session: AsyncSession) -> ComletedLessonUseCase:
    return ComletedLessonUseCase(
        lesson_repo=SQLAlchemyLessonRepository(session),
        progress_repo=SQLAlchemyLessonProgressRepository(session),
        enrolment_repo=SQLAlchemyEnrollmentRepository(session),
        course_repo=SQLAlchemyCourseRepository(session),
    )