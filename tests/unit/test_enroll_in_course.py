import pytest
from datetime import datetime
from unittest.mock import Mock

from lms.domain.course import Course, CourseId, CourseStatus
from lms.domain.enrollment import EnrollmentId, UserId
from lms.domain.repositories import CourseRepository, EnrollmentRepository
from lms.domain.exceptions import CourseNotPublishedError
from lms.application.dto import EnrollInCourseCommand
from lms.application.enroll_in_course import EnrollInCourseUseCase

# === In-memory реализация репозиотриев для тестов ===

class InMemoryCourseRepository(CourseRepository):
    def __init__(self):
        self._courses = {}
        
    async def get_by_id(self, course_id: CourseId) -> Course | None:
        return self._courses.get(course_id)
    
    def add(self, course: Course):
        self._courses[course.id] = course
        

class InMemoryEnrollmentRepository(EnrollmentRepository):
    def __init__(self):
        self._enrollments = {}
    
    async def save(self, enrollment) -> None:
        self._enrollments[enrollment.id] = enrollment
        
    async def get_by_id(self, enrollment_id: EnrollmentId):
        return self._enrollments.get(enrollment_id)


# === Тесты ===

async def test_enroll_in_published_course():
    course_repo = InMemoryCourseRepository()
    enrollment_repo = InMemoryEnrollmentRepository()
    
    # Создаем опубликовынный курс
    course = Course(
        id=CourseId("course-1"),
        title="Python DDD",
        desriprion="Learn DDD with Python",
        status=CourseStatus.PUBLISHED,
    )
    course_repo.add(course)
    
    use_case = EnrollInCourseUseCase(course_repo, enrollment_repo)
    
    command = EnrollInCourseCommand(
        user_id=UserId("user-1"),
        course_id=CourseId("course-1"),
    )
    
    enrollment_id = await use_case.execute(command)
    
    assert enrollment_id is not None
    saved_enrollment = await enrollment_repo.get_by_id(enrollment_id)
    assert saved_enrollment is not None
    assert saved_enrollment.user_id == UserId('user-1')
    assert saved_enrollment.course_id == CourseId("course-1")
    
    
async def test_cannot_enroll_in_unpublished_course():
    course_repo = InMemoryCourseRepository()
    enrollment_repo = InMemoryEnrollmentRepository()
    
    # Создаем курс в черновике
    course = Course(
        id=CourseId("course-2"),
        title="Secret Course",
        desriprion="Not ready yet",
        status=CourseStatus.DRAFT,
    )
    course_repo.add(course)
    
    use_case = EnrollInCourseUseCase(course_repo, enrollment_repo)
    
    command = EnrollInCourseCommand(
        user_id=UserId("user-2"),
        course_id=CourseId("course-2"),
    )
    
    
    with pytest.raises(CourseNotPublishedError):
        await use_case.execute(command)
        
    assert len(enrollment_repo._enrollments) == 0