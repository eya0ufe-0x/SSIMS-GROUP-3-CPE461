from sqlmodel import Session, select
from server.models import Company, Course


def test_create_linked_company_course(session: Session):
    # Create models
    course = Course(name="Computer Engineering")
    company = Company(
        name="TechCorp",
        description="Great place",
        location="Lagos",
        slots_available=5,
        email="jobs@techcorp.com",
        status="Open",
    )
    company.courses.append(course)

    # Save to DB
    session.add(company)
    session.commit()
    session.refresh(company)
    session.refresh(course)

    # Verify IDs generated
    assert company.id is not None
    assert course.id is not None

    # Verify relationship
    assert len(company.courses) == 1
    assert company.courses[0].name == "Computer Engineering"

    # Verify reverse relationship
    assert len(course.companies) == 1
    assert course.companies[0].name == "TechCorp"


def test_course_filtering(session: Session):
    course1 = Course(name="EE")
    course2 = Course(name="CS")

    c1 = Company(
        name="C1",
        description="D1",
        location="L",
        slots_available=1,
        email="e",
        status="O",
    )
    c1.courses = [course1]

    c2 = Company(
        name="C2",
        description="D2",
        location="L",
        slots_available=1,
        email="e",
        status="O",
    )
    c2.courses = [course2]

    session.add(c1)
    session.add(c2)
    session.commit()

    # Query companies with course1
    statement = select(Company).where(Company.courses.any(Course.name == "EE"))
    results = session.exec(statement).all()

    assert len(results) == 1
    assert results[0].name == "C1"
