# 🎓 Student Result Management System (SRMS)

A web-based Student Result Management System built using **Python Flask**, **HTML/CSS/Bootstrap**, **JavaScript**, and **SQL Server**.  
The system helps automate student registration, course enrollment, and result generation for educational institutes or training centers.

---

## 🚀 Features

### 👨‍🎓 Student Module
- Student Registration & Login
- View Available Free Courses (with YouTube links)
- Join Paid Courses (with price and enrollment form)
- View Results for enrolled courses
- Clean, user-friendly dashboard

### 🛠️ Admin Module
- Admin Login
- Manage Courses  
  - Add free and paid courses  
  - Edit course details (including price and YouTube link)  
- View Total Students (Free + Paid)
- Add or Update Student Results
- Manage Enrollments and Course Data

---

## 🗂️ Database Design

The system uses **SQL Server** with the following main tables:

- **Student**  
- **Admin**  
- **Course**  
- **Enrollment**  
- **Result**

### 🔗 ER Diagram (Conceptual Overview)


---

## 🛠️ Technologies Used

### Frontend
- HTML  
- CSS  
- Bootstrap  
- JavaScript  

### Backend
- Python  
- Flask Framework  
- Jinja2 Templates  

### Database
- SQL Server  
- SQLAlchemy ORM  
- pyodbc Driver  

### Tools
- Visual Studio Code  
- Git & GitHub  
- Browser (Chrome/Edge)

---

## ⚙️ Installation & Setup

### 📥 1. Clone the Repository
```bash
git clone https://github.com/yourusername/student-result-management-system.git

### 2.Installation Required python libraries
pip install flask flask_sqlalchemy pyodbc

###3.Configure SQL Server Connection

### 4.Run the application
--python app.py

###5. Then Open
---http://localhost:5000

<img width="1920" height="1080" alt="Dashboard" src="https://github.com/user-attachments/assets/130ea377-6aa1-4db5-94ca-f6e64c60e310" />

