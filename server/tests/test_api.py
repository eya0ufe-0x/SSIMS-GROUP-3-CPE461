from fastapi.testclient import TestClient
from server.models import Company, Course


def test_read_companies_empty(client: TestClient):
    response = client.get("/api/companies")
    assert response.status_code == 200
    assert response.json() == []


def test_read_companies_seeded(client: TestClient, session):
    # Seed
    c = Course(name="TestCourse")
    session.add(c)
    comp = Company(
        name="TestComp",
        description="Desc",
        location="Lagos",
        slots_available=1,
        email="test@test.com",
        status="Open",
    )
    comp.courses.append(c)
    session.add(comp)
    session.commit()

    response = client.get("/api/companies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "TestComp"


def test_filter_location(client: TestClient, session):
    comp1 = Company(
        name="C1",
        description="D1",
        location="Lagos",
        slots_available=1,
        email="e1",
        status="O",
    )
    comp2 = Company(
        name="C2",
        description="D2",
        location="Abuja",
        slots_available=1,
        email="e2",
        status="O",
    )
    session.add(comp1)
    session.add(comp2)
    session.commit()

    response = client.get("/api/companies?location=lagos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "C1"


def test_filter_course(client: TestClient, session):
    c1 = Course(name="EE")
    comp1 = Company(
        name="C1",
        description="D1",
        location="L",
        slots_available=1,
        email="e1",
        status="O",
    )
    comp1.courses.append(c1)

    c2 = Course(name="CS")
    comp2 = Company(
        name="C2",
        description="D2",
        location="L",
        slots_available=1,
        email="e2",
        status="O",
    )
    comp2.courses.append(c2)

    session.add(comp1)
    session.add(comp2)
    session.commit()

    response = client.get("/api/companies?course=ee")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "C1"
