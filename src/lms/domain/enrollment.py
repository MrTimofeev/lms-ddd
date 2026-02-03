from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from .course import CourseId, Course
from .exceptions import CourseNotPublishedError

EnrollmentId = NewType("EnrollmentId", str)
UserId = NewType("UserId", str)


@dataclass(frozen=True)
class Enrollment:
    id: EnrollmentId
    user_id: UserId
    course_id: CourseId
    enrolled_at: datetime



def create_enrollment(
    enrollment_id: EnrollmentId,
    user_id: UserId,
    course: Course,
    enrolled_at: datetime,
) -> Enrollment:
    if not course.can_be_enrolled():
        raise CourseNotPublishedError(course.id)
    return Enrollment(
        id=enrollment_id,
        user_id=user_id,
        course_id=course.id,
        enrolled_at=enrolled_at
    )