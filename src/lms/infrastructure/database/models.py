import uuid

from sqlalchemy import String, DateTime, Enum as SQLEnum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from lms.infrastructure.database.session import Base
from lms.domain.course import CourseStatus


class CourseDB(Base):
    __tablename__ = "courses"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200))
    desription: Mapped[str] = mapped_column(String(1000))
    status: Mapped[CourseStatus] = mapped_column(SQLEnum(CourseStatus))


class EnrollmentDB(Base):
    __tablename__ = "enrollments"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"))
    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc))


class LessonDB(Base):
    __tablename__ = "lessons"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    corse_id: Mapped[UUID] = mapped_column(ForeignKey('courses.id'))
    title: Mapped[str] = mapped_column(String(200))
    order: Mapped[int] = mapped_column()


class LessonProgressDB(Base):
    __tablename__ = "lesson_progress"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrollment_id: Mapped[UUID] = mapped_column(ForeignKey("enrollments.id"))
    lesson_id: Mapped[UUID] = mapped_column(ForeignKey("lessons.id"))
    completed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc))

    __table_args__ = (UniqueConstraint("enrollment_id", "lesson_id"),)
