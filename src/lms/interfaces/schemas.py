from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class EnrollInCourseRequest(BaseModel):
    user_id: UUID = Field(..., description="ID пользователя")
    course_id: UUID = Field(..., description="ID курса")
    
    
class EnrollmentResponse(BaseModel):
    enrollment_id: UUID
    
    
class CompletedLessonRequest(BaseModel):
    enrollment_id: UUID
    lesson_id: UUID
    
class CourseCompletedResponse(BaseModel):
    message: str = "Course completed!"
    enrollment_id: UUID
    course_id: UUID
    completed_at: datetime