from dataclasses import dataclass
from .enrollment import EnrollmentId
from .course import CourseId

@dataclass(frozen=True)
class CourseCompleted:
    enrollment_id: EnrollmentId
    course_id: CourseId
    completed_at: "datetime"