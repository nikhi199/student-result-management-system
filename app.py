from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mysecretkey"

# ==============================
# SQL Server connection string
# ==============================
# CHANGE: USERNAME, PASSWORD, SERVERNAME
# Example SERVERNAME:
#   - localhost
#   - DESKTOP-ABC123\SQLEXPRESS

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc://@NIKHIL-GOLE\\SQLEXPRESS/StudentSystemDB"
    "?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
)



app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ==============================
# Database Models (Tables)
# ==============================
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # free or paid
    youtube_link = db.Column(db.String)
    price = db.Column(db.Integer)  # NEW FIELD



class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    join_date = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    marks = db.Column(db.Integer, nullable=False)


# ==============================
# Create tables + default courses
# ==============================
tables_created = False

@app.before_request
def create_tables_and_seed():
    global tables_created
    if not tables_created:
        db.create_all()

        # Add default courses only once
        if Course.query.count() == 0:
            free_courses = [
                ("Python Basics", "free", "https://www.youtube.com/results?search_query=python+tutorial"),
                ("Java Basics", "free", "https://www.youtube.com/results?search_query=java+tutorial"),
                ("C++ Basics", "free", "https://www.youtube.com/results?search_query=c++tutorial"),
                ("React", "free", "https://www.youtube.com/results?search_query=react+tutorial"),
                ("SQL", "free", "https://www.youtube.com/results?search_query=sql+tutorial"),
            ]
            paid_courses = [
                ("Advance Java", "paid", ""),
                ("Python with Flask Framework", "paid", ""),
                ("Advance JavaScript", "paid", ""),
                ("Rust", "paid", ""),
                ("PHP", "paid", ""),
                ("AWS Cloud", "paid", ""),
                ("Software Testing", "paid", "")
            ]

            for name, ctype, link in free_courses + paid_courses:
                db.session.add(Course(name=name, type=ctype, youtube_link=link))

            db.session.commit()

        tables_created = True


# ==============================
# Home Page
# ==============================
@app.route("/")
def index():
    return render_template("index.html")


# ==============================
# Student Registration
# ==============================
@app.route("/student/register", methods=["GET", "POST"])
def student_register():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        email = request.form["email"]
        password = request.form["password"]
        gender = request.form["gender"]

        # Check email already exist
        existing = Student.query.filter_by(email=email).first()
        if existing:
            flash("Email already registered!", "error")
            return redirect(url_for("student_register"))

        s = Student(name=name, age=age, email=email, password=password, gender=gender)
        db.session.add(s)
        db.session.commit()
        flash("Student registered successfully! Please login.", "success")
        return redirect(url_for("student_login"))

    return render_template("student_register.html")


# ==============================
# Student Login
# ==============================
@app.route("/student/login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        student = Student.query.filter_by(email=email, password=password).first()
        if student:
            session["student_id"] = student.id
            flash("Login successful!", "success")
            return redirect(url_for("student_dashboard"))
        else:
            flash("Invalid email or password.", "error")

    return render_template("student_login.html")


# ==============================
# Student Dashboard
# ==============================
@app.route("/student/dashboard")
def student_dashboard():
    if "student_id" not in session:
        flash("Please login as student first.", "error")
        return redirect(url_for("student_login"))

    student = Student.query.get(session["student_id"])
    free_courses = Course.query.filter_by(type="free").all()
    paid_courses = Course.query.filter_by(type="paid").all()

    return render_template(
        "student_dashboard.html",
        student=student,
        free_courses=free_courses,
        paid_courses=paid_courses
    )


# ==============================
# Student - Free Course Enrollment
# ==============================
@app.route("/student/free-course", methods=["GET", "POST"])
def student_free_course():
    if "student_id" not in session:
        flash("Please login as student.", "error")
        return redirect(url_for("student_login"))

    student = Student.query.get(session["student_id"])
    free_courses = Course.query.filter_by(type="free").all()

    if request.method == "POST":
        course_id = request.form["course_id"]
        join_date = request.form["join_date"]
        address = request.form["address"]

        enroll = Enrollment(
            student_id=student.id,
            course_id=course_id,
            join_date=join_date,
            address=address
        )
        db.session.add(enroll)
        db.session.commit()
        flash("Free course joined successfully!", "success")
        return redirect(url_for("student_dashboard"))

    return render_template("student_free_course.html", student=student, free_courses=free_courses)


# ==============================
# Student - Paid Course Enrollment
# ==============================
@app.route("/student/paid-course", methods=["GET", "POST"])
def student_paid_course():
    if "student_id" not in session:
        flash("Please login as student.", "error")
        return redirect(url_for("student_login"))

    student = Student.query.get(session["student_id"])
    paid_courses = Course.query.filter_by(type="paid").all()

    if request.method == "POST":
        course_id = request.form["course_id"]
        join_date = request.form["join_date"]
        address = request.form["address"]

        enroll = Enrollment(
            student_id=student.id,
            course_id=course_id,
            join_date=join_date,
            address=address
        )
        db.session.add(enroll)
        db.session.commit()
        flash("Paid course joined successfully!", "success")
        return redirect(url_for("student_dashboard"))

    return render_template("student_paid_course.html", student=student, paid_courses=paid_courses)


# ==============================
# Student - View Result
# ==============================
@app.route("/student/view-result", methods=["GET", "POST"])
def student_view_result():
    search_name = ""
    found_student = None
    student_results = []

    if request.method == "POST":
        search_name = request.form["search_name"].strip()

        found_student = Student.query.filter(
            Student.name.ilike(f"%{search_name}%")
        ).first()

        if found_student:
            # list of (Result, Course)
            student_results = db.session.query(Result, Course)\
                .join(Course, Result.course_id == Course.id)\
                .filter(Result.student_id == found_student.id).all()
        else:
            flash("No student found with that name.", "error")

    return render_template(
        "student_view_result.html",
        search_name=search_name,
        found_student=found_student,
        student_results=student_results
    )


# ==============================
# Admin Registration/Login
# ==============================
@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing = Admin.query.filter_by(email=email).first()
        if existing:
            flash("Admin email already registered!", "error")
            return redirect(url_for("admin_register"))

        a = Admin(name=name, email=email, password=password)
        db.session.add(a)
        db.session.commit()
        flash("Admin registered successfully! Please login.", "success")
        return redirect(url_for("admin_login"))

    return render_template("admin_register.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        admin = Admin.query.filter_by(email=email, password=password).first()
        if admin:
            session["admin_id"] = admin.id
            flash("Admin login successful!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid admin email or password!", "error")

    return render_template("admin_login.html")


# ==============================
# Admin Dashboard
# ==============================
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        flash("Please login as admin.", "error")
        return redirect(url_for("admin_login"))

    total_students = Student.query.count()
    total_courses = Course.query.count()
    free_students = Enrollment.query.join(Course).filter(Course.type == "free").count()
    paid_students = Enrollment.query.join(Course).filter(Course.type == "paid").count()

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        total_courses=total_courses,
        free_students=free_students,
        paid_students=paid_students
    )


# ==============================
# Admin - Manage Students
# ==============================
@app.route("/admin/manage-students")
def admin_manage_students():
    if "admin_id" not in session:
        flash("Please login as admin.", "error")
        return redirect(url_for("admin_login"))

    data = []

    for s in Student.query.all():
        enrollments = db.session.query(Enrollment, Course)\
            .join(Course, Enrollment.course_id == Course.id)\
            .filter(Enrollment.student_id == s.id).all()

        data.append({
            "student": s,
            "enrollments": enrollments
        })

    return render_template("admin_manage_students.html", data=data)


# ==============================
# Admin - Manage Courses
# ==============================
@app.route("/admin/manage-courses", methods=["GET", "POST"])
def admin_manage_courses():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        name = request.form.get("name")
        course_type = request.form.get("type")
        youtube_link = request.form.get("youtube_link")

        # NEW PRICE FIELD
        price = request.form.get("price")
        if price == "" or price is None:
            price = None

        new_course = Course(
            name=name,
            type=course_type,
            youtube_link=youtube_link,
            price=price
        )

        db.session.add(new_course)
        db.session.commit()

        flash("Course added successfully!", "success")
        return redirect(url_for("admin_manage_courses"))

    courses = Course.query.all()
    return render_template("admin_manage_courses.html", courses=courses)



@app.route("/admin/edit-course/<int:course_id>", methods=["GET", "POST"])
def admin_edit_course(course_id):
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    course = Course.query.get(course_id)

    if request.method == "POST":
        name = request.form.get("name")
        course_type = request.form.get("type")
        youtube_link = request.form.get("youtube_link")

        # NEW PRICE FIELD
        price = request.form.get("price")
        if price == "" or price is None:
            price = None

        # UPDATE COURSE VALUES
        course.name = name
        course.type = course_type
        course.youtube_link = youtube_link
        course.price = price    # <-- IMPORTANT LINE

        db.session.commit()

        flash("Course updated successfully!", "success")
        return redirect(url_for("admin_manage_courses"))

    return render_template("admin_edit_course.html", course=course)



# ==============================
# Admin - Add/Edit Result
# ==============================
@app.route("/admin/add-result", methods=["GET", "POST"])
def admin_add_result():
    if "admin_id" not in session:
        flash("Please login as admin.", "error")
        return redirect(url_for("admin_login"))

    students = Student.query.all()
    paid_courses = Course.query.filter_by(type="paid").all()

    if request.method == "POST":
        student_id = request.form["student_id"]
        course_id = request.form["course_id"]
        marks = request.form["marks"]

        existing = Result.query.filter_by(student_id=student_id, course_id=course_id).first()
        if existing:
            existing.marks = marks
        else:
            r = Result(student_id=student_id, course_id=course_id, marks=marks)
            db.session.add(r)

        db.session.commit()
        flash("Result saved successfully!", "success")
        return redirect(url_for("admin_add_result"))

    return render_template("admin_add_result.html", students=students, paid_courses=paid_courses)


# ==============================
# Logout
# ==============================
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
