class DomainError(Exception):
    """Базовый класс для всех доменных ошибок"""
    pass


class CourseNotPublishedError(DomainError):
    def __init__(self, course_id: "CourseId"):
        self.course_id = course_id
        super().__init__(f"Cannot enroll in published course: {course_id}")