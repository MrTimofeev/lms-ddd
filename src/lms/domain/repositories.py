from abc import ABC, abstractmethod
from typing import Optional

from .course import Course, CourseId
from .enrollment import Enrollment, EnrollmentId


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