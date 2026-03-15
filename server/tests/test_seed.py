from sqlmodel import Session, select
from server.seed import seed_data
from server.models import Company, Course


def test_seed_populates_db(session: Session):
    # Verify empty start
    assert session.exec(select(Company)).first() is None

    # Run seed
    seed_data(session)

    # Verify companies populated
    companies = session.exec(select(Company)).all()
    assert len(companies) > 0

    # Verify courses populated
    courses = session.exec(select(Course)).all()
    assert len(courses) > 0

    # Verify linking
    company_with_course = next((c for c in companies if c.courses), None)
    assert company_with_course is not None
    assert len(company_with_course.courses) > 0


def test_seed_idempotency(session: Session):
    seed_data(session)
    count_1 = len(session.exec(select(Company)).all())

    seed_data(session)
    count_2 = len(session.exec(select(Company)).all())

    assert count_1 == count_2
