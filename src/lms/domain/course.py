from dataclasses import dataclass
from typing import NewType
from enum import Enum

from .exceptions import DomainError


CourseId = NewType("CourseId", str)


class CourseStatus(str, Enum):
    DRAFT = 'draft'
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class Course:
    id: CourseId
    title: str
    desriprion: str
    status: "CourseStatus"
    total_lessons: int = 0

    def publish(self, total_lessons: int) -> "Course":
        if self.status != CourseStatus.DRAFT:
            raise DomainError("Only draft courses can be publushed")
        if total_lessons <= 0:
            raise DomainError("Course must have at least one lesson")
        return Course(
            id=self.id,
            title=self.title,
            desriprion=self.desriprion,
            status=CourseStatus.PUBLISHED,
            total_lessons=total_lessons,
        )

    def can_be_enrolled(self) -> bool:
        return self.status == CourseStatus.PUBLISHED
    
    def can_issue_certificate(self, completed_lesson: int) -> bool:
        if self.total_lessons == 0:
            return False
        return (completed_lesson / self.total_lessons) >= 0.8

        