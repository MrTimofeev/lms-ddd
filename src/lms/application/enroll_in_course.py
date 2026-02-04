from typing import Optional

from lms.domain.course import Course
from lms.domain.enrollment import create_enrollment, EnrollmentId
from lms.domain.repositories import CourseRepository, EnrollmentRepository
from lms.application.dto import EnrollInCourseCommand


class EnrollInCourseUseCase:
    def __init__(
        self,
        course_repository: CourseRepository,
        enrollment_repository: EnrollmentRepository,
    ):
        self._course_repo = course_repository
        self._enrollment_repo = enrollment_repository
        
    
    async def execute(self, command: EnrollInCourseCommand) -> EnrollmentId:
        # 1. Загружаем курс
        course: Optional[Course] = await self._course_repo.get_by_id(command.course_id)
        
        if course is None:
            raise ValueError(f"Course {command.course_id} not found")
        
        # 2. пытаемся создать зачисление (фабрика проверит статус)
        from datetime import datetime, timezone
        import uuid
        enrollment = create_enrollment(
            enrollment_id=EnrollmentId(str(uuid.uuid4())),
            user_id=command.user_id,
            course=course,
            enrolled_at=datetime.now(timezone.utc),
        )
        
        # 3. Сохраняем
        await self._enrollment_repo.save(enrollment)
        
        # 4. Возвращаем ID
        return enrollment.id