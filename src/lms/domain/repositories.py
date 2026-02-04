from abc import ABC, abstractmethod
from typing import Optional

from .course import Course, CourseId
from .enrollment import Enrollment, EnrollmentId
from .lesson import Lesson, LessonId
from .lesson_progress import LessonProgress, LessonProgressId


class CourseRepository(ABC):
    @abstractmethod
    async def get_by_id(self, course_id: CourseId) -> Optional[Course]:
        raise NotImplementedError


class EnrollmentRepository(ABC):
    @abstractmethod
    async def save(self, enrollment: Enrollment) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, enrollment_id: EnrollmentId) -> Optional[Enrollment]:
        raise NotImplementedError


class LessonRepository(ABC):
    @abstractmethod
    async def get_by_id(self, lesson_id: LessonId) -> Optional[Lesson]:
        ...


class LessonProgressRepository(ABC):
    @abstractmethod
    async def save(self, progress: LessonProgress) -> None:
        ...
        
    @abstractmethod
    async def get_by_enrollment_and_lesson(
        self, enrollmetn_id: EnrollmentId, lesson_id: LessonId
    ) -> Optional[LessonProgress]:
        ...
    
    
    @abstractmethod
    async def count_completed_by_enrollment(self, enrollment_id: EnrollmentId) -> int:
        ...
    