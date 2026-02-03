from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from lms.interfaces.schemas import EnrollInCourseRequest, EnrollmentResponse
from lms.infrastructure.container import get_enroll_in_course_use_case
from lms.infrastructure.database.session import AsyncSessionLocal
from lms.application.dto import EnrollInCourseCommand
from lms.domain.exceptions import CourseNotPublishedError
from lms.domain.course import CourseId
from lms.domain.enrollment import UserId


router = APIRouter(prefix="/enrollments", tags=["Erollments"])

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
        

@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_in_course(
    request: EnrollInCourseRequest,
    session: AsyncSession =  Depends(get_db_session),
):
    try:
        # Преобразуем Pydantic-модель -> доменнтые типы
        command = EnrollInCourseCommand(
            user_id=UserId(str(request.user_id)),
            course_id=CourseId(str(request.course_id)),
        )
        
        # получаем use casa с внедренными репозиториями
        use_case = get_enroll_in_course_use_case(session)
        
        # Выполянем бизнес-логику
        enrollment_id = await use_case.execute(command)
        
        return EnrollmentResponse(enrollment_id=enrollment_id)
        
    except CourseNotPublishedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot enroll in unpublished course: {e.course_id}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )