from dataclasses import dataclass
from typing import NewType

LessonId = NewType("LessonId", str)


@dataclass(frozen=True)
class Lesson:
    id: LessonId
    course_id: "CourseId"
    title: str
    order: int
    
from .course import CourseId # чтобы избежать циклического импорта 
# TODO: узнать как это работает