from pydantic import BaseModel, Field
from uuid import UUID


class EnrollInCourseRequest(BaseModel):
    user_id: UUID = Field(..., description="ID пользователя")
    course_id: UUID = Field(..., description="ID курса")
    
    
class EnrollmentResponse(BaseModel):
    enrollment_id: UUID