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

    def publish(self) -> "Course":
        if self.status != CourseStatus.DRAFT:
            raise DomainError("Only draft courses can be publushed")
        
        return Course(
            id=self.id,
            title=self.title,
            desriprion=self.desriprion,
            status=CourseStatus.PUBLISHED,
        )

    def can_be_enrolled(self) -> bool:
        return self.status == CourseStatus.PUBLISHED

        