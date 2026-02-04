from typing import Optional

from lms.domain.repositories import (
    LessonRepository,
    LessonProgressRepository,
    CourseRepository,
    EnrollmentRepository,
)
from lms.domain.events import CourseCompleted
from lms.application.dto import CompletedLessonCommand
from lms.domain.enrollment import Enrollment


class ComletedLessonUseCase:
    def __init__(
        self,
        lesson_repo: LessonRepository,
        progress_repo: LessonProgressRepository,
        enrolment_repo: EnrollmentRepository,
        course_repo: CourseRepository,
    ):
        self._lesson_repo = lesson_repo
        self._progress_repo = progress_repo
        self._enollment_repo = enrolment_repo
        self._course_repo = course_repo

    async def execute(self, command: CompletedLessonCommand) -> Optional[CourseCompleted]:
        # 1. Проверяем, существует ли зачисление
        enrollment = await self._enollment_repo.get_by_id(command.lesson_id)
        
        if not enrollment:
            raise ValueError("Enrollemt not found")
        
        # 2. Проверяем, существует ли урок и принадлежит ли курcу
        lesson = await self._lesson_repo.get_by_id(command.lesson_id)
        if not lesson or lesson.course_id != enrollment.course_id:
            raise ValueError("Lesson not found or doese not belong to course")
        
        # 3. Проверяем, не завершен ли уже 
        existing = await self._progress_repo.get_by_enrollment_and_lesson(
            command.enrollment_id, command.lesson_id
        )
        
        if existing:
            return None # уже завершен
        
        # 5. Считаем общее количетсво завершенных уроков
        completed_count = await self._progress_repo.count_completed_by_enrollment(
            command.enrollment_id
        )
        
        # 6. Загружаем курс
        course = await self._course_repo.get_by_id(enrollment.course_id)
        if not course:
            raise ValueError("Course not found")
        
        # 7. Проверяем, можно ли выдать сертификат
        if course.can_issue_certificate(completed_count):
            from datetime import datetime, timezone
            return CourseCompleted(
                enrollment_id=command.enrollment_id,
                course_id=course.id,
                completed_at=datetime.now(timezone.utc)
            )
        
        return None
            