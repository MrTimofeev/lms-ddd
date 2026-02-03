from dataclasses import dataclass
from typing import NewType

from lms.domain.course import CourseId
from lms.domain.enrollment import UserId

@dataclass(frozen=True)
class EnrollInCourseCommand:
    user_id: UserId
    course_id: CourseId