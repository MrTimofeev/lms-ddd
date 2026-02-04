from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from .lesson import LessonId
from .enrollment import EnrollmentId

LessonProgressId = NewType("LessonProgressId", str)

@dataclass(frozen=True)
class LessonProgress:
    id: LessonProgressId
    enrollment_id: EnrollmentId
    lesson_id: LessonId
    completed_at: datetime
    
    @classmethod
    def create(cls, enrollment_id: EnrollmentId, lesson_id: LessonId) -> "LessonProgress":
        from uuid import uuid4
        from datetime import datetime, timezone
        return cls(
            id=LessonProgressId(str(uuid4())),
            enrollment_id=enrollment_id,
            lesson_id=lesson_id,
            completed_at=datetime.now(timezone.utc),
        )
    
