from dataclasses import dataclass
from typing import NewType

from lms.domain.course import CourseId
from lms.domain.enrollment import UserId, EnrollmentId
from lms.domain.lesson import LessonId

@dataclass(frozen=True)
class EnrollInCourseCommand:
    user_id: UserId
    course_id: CourseId
    
    
@dataclass(frozen=True)
class CompletedLessonCommand:
    enrollment_id: EnrollmentId
    lesson_id: LessonId