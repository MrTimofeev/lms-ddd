from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from lms.interfaces.schemas import CompletedLessonRequest, CourseCompletedResponse
from lms.application.dto import CompletedLessonCommand
from lms.infrastructure.container import get_complete_lesson_use_case
from lms.infrastructure.database.session import AsyncSessionLocal
from lms.domain.lesson_progress import EnrollmentId, LessonId

router = APIRouter(prefix="/progress", tags=["Progress"])


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
        
        
@router.post('/complete')
async def complete_lesson(
    request: CompletedLessonRequest,
    sessiom: AsyncSession = Depends(get_db_session),
):
    command = CompletedLessonCommand(
        enrollment_id=EnrollmentId(str(request.enrollment_id)),
        lesson_id=LessonId(str(request.lesson_id)),
    )
    
    use_case = get_complete_lesson_use_case(sessiom)
    event = await use_case.execute(command)
    
    if event is None:
        return {"Message": "Lesson marked as completed"}
    
    return CourseCompletedResponse(
        enrollment_id=event.enrollment_id,
        course_id=event.course_id,
        completed_at=event.completed_at,
    )