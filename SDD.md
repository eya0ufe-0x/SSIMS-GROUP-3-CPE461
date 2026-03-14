# Software Design Document – SSIMS (Smart SIWES & Internship Management System)

## 1. Software Design Document
This document provides a complete overview of the SSIMS web application.

## 2. Name of those on the software team
-AIGBOKHABHO PEACE ODEGWUA - [ENG2204369] – Frontend + Documentation <br>
-OTUYOMA OROGHENEJERE - [ENG2204044] - Backend <br>
-UKPONG ANDINWAM [ENG2204052] –   <br>
-IYENGUNMWENA EMMANUEL OSARO [ENG2203994] - <br>
-CHARLES JOSHUA [ENG2203968] -<br>
-ONYEKA CLEVER DUMKELECHUKWU [ENG2204035] -<br>
-EHIMARE OSEOJE PRINCE [ENG2102762] -<br>

## 3. Roles of each member
-AIGBOKHABHO PEACE ODEGWUA – Designed and coded the entire frontend (HTML, CSS, Bootstrap), created all pages, implemented the mobile navigation toggle menu, wrote this documentation, and managed the GitHub repository.  <br>
-OTUYOMA OROGHENEJERE - [ENG2204044] - <br>
-UKPONG ANDINWAM [ENG2204052] –   <br>
-IYENGUNMWENA EMMANUEL OSARO [ENG2203994] -<br>
-CHARLES JOSHUA [ENG2203968] -<br>
-ONYEKA CLEVER DUMKELECHUKWU [ENG2204035] - <br>
-EHIMARE OSEOJE PRINCE [ENG2102762] - <br>

## 4. Functional Requirements
- Displaying Welcoming homepage with “Get Started” button.  
- Show static “Platform Features” page with cards (Student Profile, Company Offers, Progress Tracking, Supervisor Evaluation, Reports & Analytics). 
- Display “What Our Students Say” testimonials.  
- Show “About SSIMS” page with mission and logo.  
- Student Information Form: collect First Name, Last Name, Course of Study, Preferred Location (dropdown), then show available SIWES placements for that location.

## 5. Version
- SDD Version: 1.0  
- Software Version: 0.1 (Frontend and Backend)

## 6. UX Requirements
The application is a clean, responsive, mobile-friendly single-page style website.  
- Simple and intuitive navigation (Features, Reviews, About, Login links).  
- Clear form fields with placeholder text.  
- Modern design using background images and icons.  
- Fast loading (all static pages).

![Welcome Page](preview/preview(1).png)  
![Platform Features](preview/preview(2).png)  
![Testimonials](preview/preview(3).png)  
![About SSIMS](preview/preview(4).png)  
![Student Information Form](preview/preview(5).png)

## 8.*Class Diagram*  
Entities: Student (firstName, lastName, courseOfStudy, preferredLocation), Placement (locationName, companyName, description).  
![Class Diagram](img/class-diagram.png) (create in draw.io and add to img folder)

## 9. Sequence diagram, Context diagram
*Sequence Diagram*  
Student fills form → submits → static placements displayed.  
![Sequence Diagram](img/sequence-diagram.png)

*Context Diagram*  
Student interacts with SSIMS web app.  
![Context Diagram](img/context-diagram.png)

## 10. Implementation  
- *HTML5* – Core structure. Reason: Standard.  
- *CSS3 + Bootstrap 5* – Styling and responsiveness. Reason: Professional and mobile-ready.  
- *JavaScript (vanilla)* – ONLY for the mobile navigation toggle menu. Reason: Lightweight.  
- Backend: In progress (Node.js + Express planned).

## 11. Source Code should be well documented
Example of the only JavaScript used (mobile menu):
```html
<!-- Mobile Navigation Toggle -->
<button class="navbar-toggler" ...>
<script>
// Bootstrap handles the toggle
</script>
