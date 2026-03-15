# Software Design Document – SSIMS (Smart SIWES & Internship Management System)

## 1. Software Design Document
This document provides a complete overview of the SSIMS web application.

## 2. Name of those on the software team
- AIGBOKHABHO PEACE ODEGWUA - [ENG2204369] – Frontend and Documentation <br>
- OTUYOMA OROGHENEJERE - [ENG2204044] - Backend and DevOps <br>
- UKPONG ANDINWAM [ENG2204052] – Sequence and Context Diagrams <br>
- IYENGUNMWENA EMMANUEL OSARO [ENG2203994] - Development process and immplementation <br>
- CHARLES JOSHUA [ENG2203968] - Requirements Engineering and Co-testing <br>
- ONYEKA CLEVER DUMKELECHUKWU [ENG2204035] -UML and Class Diagrams <br>
- EHIMARE OSEOJE PRINCE [ENG2102762] - Testing and Validation <br>

## 3. Roles of each member
- AIGBOKHABHO PEACE ODEGWUA – [ENG2204369] - Designed and coded the entire frontend (HTML, CSS, Bootstrap), created all pages, implemented the mobile navigation toggle menu, compiled documentation (README, SDD) for consistency and clarity across projects.  <br>
- OTUYOMA OROGHENEJERE - [ENG2204044] - Implemented backend functionality, maanaged the Github repository for version control, and oversaw deployment to ensure system was operational and accessible. <br>
- UKPONG ANDINWAM [ENG2204052] – Created sequence diagrams to illustrate system interactions and context diagrams to define system boundaries. <br>
- IYENGUNMWENA EMMANUEL OSARO [ENG2203994] - Applied the waterfall model to guide project phases which contributed to both frontend and backend. <br>
- CHARLES JOSHUA [ENG2203968] - Documented and analyzed functional and non-functional requirements. Additionally, particicpated in testing and validation confirming the application was responsive across multiple devices. <br>
- ONYEKA CLEVER DUMKELECHUKWU [ENG2204035] - Designed UML and class diagrams to represent system arcitecture and relationships. <br>
- EHIMARE OSEOJE PRINCE [ENG2102762] - Developed test cases to validate requirements and ensure system quality. <br>

## 4. Version
- SDD Version: 1.0  
- Software Version: 0.1 (Frontend and Backend)

## 5. UX Requirements
The application is a clean, responsive, mobile-friendly single-page style website.  
- Simple and intuitive navigation (Features, Reviews, About, Login links).  
- Clear form fields with placeholder text.  
- Modern design using background images and icons.  
- Fast loading (all static pages).

## 6.Screenshots
![Welcome Page](preview/preview(1).png)
![Platform Features](preview/preview(2).png)  
![Testimonials](preview/preview(3).png)  
![About SSIMS](preview/preview(4).png)  
![Student Information Form](preview/preview(5).png)


## 7.UML  Diagram 
```mermaid
graph LR
    subgraph "External Actors"
        Student["Student"]
        Companies["Companies / SIWES Hosts"]
    end
    
    subgraph "SSIMS System"
        Form["Student Information Form<br>(Name, Course, Preferred Location)"]
        PlacementDB["Job Search"]
    end

    Student -->|Submit Details| Form
    Form -->|Filters by Preferred Location| PlacementDB
    PlacementDB -->|Displays Available Placements| Student
    
    Companies -.->|Provides Placement Data| PlacementDB
```


## 8.Class Diagram  
**Entities:**
- Student (firstName, lastName, courseOfStudy, preferredLocation)
- Placement (locationName, companyName, description, slotsAvailable).
- Company (name, address)
```mermaid
classDiagram
    class Student {
        +String firstName
        +String lastName
        +String courseOfStudy
        +String preferredLocation
    }
    class Placement {
        +String locationName
        +String companyName
        +String description
        +int slotsAvailable
    }
    class Company {
        +String name
        +String address
    }

    Student "1" --> "0..*" Placement : applies for
    Placement "0..*" --> "1" Company : offered by
```  


## 9. Sequence diagram, Context diagram
**Sequence Diagram** <br>
Student fills form → submits → static placements displayed.  
```mermaid
sequenceDiagram
    participant Student
    participant SSIMS as SSIMS Web App
    participant PlacementData as Placement Data

    Student->>SSIMS: Opens Student Information Form
    Student->>SSIMS: Fills details (First Name, Last Name, Course of Study, Preferred Location)
    Student->>SSIMS: Clicks Submit
    SSIMS->>PlacementData: Filters placements by Preferred Location
    PlacementData-->>SSIMS: Returns matching SIWES placements
    SSIMS-->>Student: Displays list of available placements
```

**Context Diagram**  

Student interacts with SSIMS web app.  
    graph TD
    subgraph External_Actors ["External Actors"] <br>
        A[Student] <br>
        B[Company] <br>
        C[SIWES Coordinator] <br>
        D[Admin] <br>
    end

    E[SSIMS Web Application]

    A <--> E
    B --> E
    C <--> E
    D --> E
    E --> A

    A -. "Fills form & views placements" .-> E
    B -. "Posts offers" .-> E
    C -. "Evaluates students" .-> E
    D -. "Approves placements" .-> E

## 10. Implementation
**Programming Languages & Libraries used:**
- *HTML5* – Structure of all pages. Reason: Standard and semantic.  
- *CSS3 + Bootstrap 5* – Styling and responsiveness. Reason: Makes the site mobile-friendly and professional with minimal custom code (cards, forms, icons).  
- *JavaScript (vanilla)* – ONLY for the mobile navigation toggle menu. Reason: Lightweight, no extra framework needed for this simple prototype.  
- *Backend* - (Node.js + Express.js planned for real API and database).

Development tools: VS Code + Live Server (port 5500).


## 11. Source Code should be well documented
- All major sections have comments. Example from SSIMS.html:

```html
<!-- Mobile Navigation Toggle -->
<button onclick="scrollToLogin" class="button">Get Started</button>

<script>

    var navList = document.getElementById("navLinks");

    function showMenu() {
        navList.style.right = "0";
    }
    function hideMenu() {
        navList.style.right = "-200px";
    }

    function scrollToLogin() {
    document.getElementById("loginForm")
     }
    </script>
```

## 12. README
See `README` file in the repository root for:
- Project description
- How to run with locally (Live Server)
- All Screenshots
- Technologies used
- link to this SDD.

**[View the Full README.md](README.md)**


## 13. GitHub (Version Control)
- Repository: [GitHub link](https://github.com/eya0ufe-0x/SSIMS-GROUP-3-CPE461.git)
- Used Git with clear commit messages (e.g., “Add images and UML Diagram”, “Create student form page”).
- Frontend fully pushed and viewable.


## 14. Testing, Verification and Validation stage
- Manual testing of all pages on desktop, tablet and mobile.
- Verified mobile menu toggles correctly.
- Form fields validate.
- Tested in Chrome and Edge.


## 15. Test framework and Report
- Framework: Manual testing.
- Test cases passed: <br>
a. Mobile navigation menu opens/closes <br>
b. Form fields required validation <br>
c. All pages responsive on phone <br> 
- Report: Everything works as designed; simple scope kept testing straightforward.


## 16. SOFTWARE DEVELOPMENT PROCESS MODELS
**WATERFALL MODEL**
- This project is the development of the Smart SIWES & Internship Management System (SSIMS). The Waterfall model was selected because the requirements were very clear and the scope was deliberately kept simple.

**Why Waterfall?**
- All features (static pages + one form) were defined from day one.
- Perfect for academic projects needing full documentation.

**Phases Applied**
1. Requirements Analysis
2. System Design
3. Implementation
4. Testing
5. Deployment and Maintenance



```mermaid
graph TD
    A[1. Requirements Analysis<br/>Student form + features list] 
    --> B[2. System Design<br/>Class diagram + Bootstrap UI]
    B --> C[3. Implementation<br/>HTML/CSS + mobile menu JS]
    C --> D[4. Testing<br/>Manual form & responsiveness test]
    D --> E[5. Deployment & Maintenance<br/>GitHub + Live Server<br/>Backend]
```

**Waterfall Model Diagram adapted for SSIMS**

**REQUIREMENT ANALYSIS PHASE** <br>

**Activities:**
- Designed the student form
- listed static pages (Features, Testimonails, About). <br>

**Stakeholders:**
- Students (Main Users) <br>

**Functional Requirements:**
- Displaying Welcoming homepage with “Get Started” button.  
- Show static “Platform Features” page with cards (Student Profile, Company Offers, Progress Tracking, Supervisor Evaluation, Reports & Analytics). 
- Display “What Our Students Say” testimonials.  
- Show “About SSIMS” page with mission and logo.  
- Student Information Form: collect First Name, Last Name, Course of Study, Preferred Location (dropdown), then show available SIWES placements for that location. <br>

**Non Functional Requirements:**
- Responsive design
- fast loading


**IMPLEMENTATION PHASE**
- Built page by page in VS Code.
- Only JavaScript used was the mobile nav toggle.
- Regular Git commits.

**TESTING PHASE**
- Manual testing of every feature (especially mobile menu).
- All bugs fixed immediately.

**DEPLOYMENT PHASE**
- Local deployment via VS Code Live Server.

**Advantages:** Clear milestones and excellent documentation. <br>

**Limitations:** Changes (e.g., adding real database) require going back to earlier phase.

This Waterfall approach ensured the clean, simple frontend was completed perfectly on time.




















