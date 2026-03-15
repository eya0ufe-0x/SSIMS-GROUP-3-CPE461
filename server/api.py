from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from server.database import get_session
from server.models import Company, Course

router = APIRouter()


@router.get("/companies", response_model=List[Company])
def get_companies(
    session: Session = Depends(get_session),
    location: Optional[str] = Query(
        None, description="Filter by location (case-insensitive)"
    ),
    course: Optional[str] = Query(None, description="Filter by course name"),
):
    statement = select(Company)

    if location:
        statement = statement.where(
            func.lower(Company.location) == func.lower(location)
        )

    if course:
        # Join with courses to filter
        statement = statement.join(Company.courses).where(
            func.lower(Course.name) == course.lower()
        )

    # Use distinct to avoid duplicates if multiple courses match
    # (though unlikely with name filter)
    statement = statement.distinct()

    companies = session.exec(statement).all()
    return companies


@router.get("/companies/{company_id}", response_model=Company)
def get_company(company_id: int, session: Session = Depends(get_session)):
    company = session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
