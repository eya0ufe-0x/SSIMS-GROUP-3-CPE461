import json
from pathlib import Path
from sqlmodel import Session, select
from server.models import Company, Course


def seed_data(session: Session):
    # Check if data exists
    if session.exec(select(Company)).first():
        return

    json_path = Path("data.json")
    if not json_path.exists():
        print("data.json not found, skipping seed")
        return

    with open(json_path, "r") as f:
        data = json.load(f)

    # 1. Seed Courses
    course_map = {}  # name -> Course object
    for course_name in data.get("courses", []):
        statement = select(Course).where(Course.name == course_name)
        course = session.exec(statement).first()
        if not course:
            course = Course(name=course_name)
            session.add(course)
            session.commit()
            session.refresh(course)
        course_map[course_name] = course

    # 2. Seed Companies
    for company_data in data.get("companies", []):
        # Extract course names and find course objects
        course_names = company_data.pop("course_names", [])

        # Check if company already exists (by name)
        # to avoid duplicates if partial seed
        statement = select(Company).where(Company.name == company_data["name"])
        existing = session.exec(statement).first()
        if existing:
            continue

        company = Company(**company_data)

        for c_name in course_names:
            if c_name in course_map:
                company.courses.append(course_map[c_name])

        session.add(company)

    session.commit()
