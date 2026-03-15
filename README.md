# SSIMS – Smart SIWES & Internship Management System <br>
A web based platform that connect students with companies for SIWES placement, tracking and evaluation.

![SSIMS Logo](preview/preview(7).png) 


*Connecting Computer Engineering students with SIWES and internship placements* <br>

A simple, clean web platform built for students to easily find and apply for SIWES placements.


## Project Overview
SSIMS helps students:
- View available SIWES placement locations
- Fill a quick Student Information Form
- Get matched with companies based on preferred location


## Features
- Beautiful welcome page with "Get Started" button
- Platform Features section (Student Profile, Company Offers, Progress Tracking, Supervisor Evaluation, Reports & Analytics)
- Real student testimonials ("What Our Students Say")
- About SSIMS page with mission statement
- Student Information Form (First Name, Last Name, Course of Study, Preferred Location dropdown)
- Fully responsive design (mobile + desktop) with hamburger menu


## Technologies Used
- **Backend**: FastAPI (Python web framework)
- **Database**: SQLite with SQLModel ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, Vanilla JavaScript
- Responsive design with mobile-first approach


## How to Run Locally

### Backend Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn server.main:app --reload
   ```
6. Open your browser and navigate to: http://127.0.0.1:8000

The backend will automatically:
- Create the SQLite database
- Seed initial data (companies and courses)
- Serve the frontend static files


## Screenshots
![Welcome Page](preview/preview(1).png) 
![Platform Features](preview/preview(2).png)  
![Student Testimonials](preview/preview(3).png)  
![About SSIMS](preview/preview(4).png)  
![Student Information Form](preview/preview(5).png)


## Full Documentation
**Complete Software Design Document** (with UML diagrams, team roles, Waterfall model, testing, etc.):  
[SOFTWARE_DESIGN_DOCUMENT.md](SDD.md)


## Team
- AIGBOKHABHO PEACE ODEGWUA - ENG2204369 - Frontend Developer & Documentation
- OTUYOMA OROGHENEJERE - ENG2204044 - Backend and DevOps
- UKPONG ANDINWAM - ENG2204052 -Sequence and Context Diagrams
- IYENGUNMWENA EMMANUEL OSARO - ENG2203994 - Development process and Implementation
- CHARLES JOSHUA - ENG2203968 - Requirements Engineering and Co-testing
- ONYEKA CLEVER DUMKELECHUKWU - ENG2204035 - UML Diagram and Class Diagram
- EHIMARE OSEOJE PRINCE - ENG2102762 - Testing and Validation

---

*Made for SIWES Project – University of Benin*  
© 2026 SSIMS. All rights reserved.
