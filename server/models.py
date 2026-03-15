from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class CompanyCourseLink(SQLModel, table=True):
    company_id: Optional[int] = Field(
        default=None, foreign_key="company.id", primary_key=True
    )
    course_id: Optional[int] = Field(
        default=None, foreign_key="course.id", primary_key=True
    )


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    companies: List["Company"] = Relationship(
        back_populates="courses", link_model=CompanyCourseLink
    )


class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    location: str = Field(index=True)
    slots_available: int
    email: str
    status: str
    courses: List[Course] = Relationship(
        back_populates="companies", link_model=CompanyCourseLink
    )
