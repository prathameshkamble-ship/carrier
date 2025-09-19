from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mobile TEXT,
            marks INTEGER,
            branch TEXT
        )
    """)
    conn.commit()
    conn.close()

ENGINEERING_COLLEGES = [
    "IIT Bombay", "IIT Delhi", "IIT Madras", "IIT Kharagpur", "IIT Kanpur",
    "IIT Roorkee", "IIT Guwahati", "IIT Hyderabad", "IIT Gandhinagar", "IIT Ropar",
    "NIT Trichy", "NIT Warangal", "NIT Surathkal", "NIT Calicut", "NIT Patna",
    "NIT Rourkela", "NIT Jaipur", "NIT Bhopal", "BITS Pilani", "VIT Vellore",
    "MIT Manipal", "DTU Delhi", "Thapar Institute", "Shiv Nadar University"
]

MEDICAL_COLLEGES = [
    "AIIMS New Delhi", "AIIMS Bhopal", "AIIMS Bhubaneswar", "AIIMS Jodhpur",
    "AIIMS Patna", "AIIMS Raipur", "AIIMS Rishikesh", "Maulana Azad Medical College",
    "KGMU Lucknow", "Grant Medical College Mumbai", "Madras Medical College Chennai",
    "Bangalore Medical College", "Lady Hardinge Medical College", "St. John's Medical College"
]

@app.route("/", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        name = request.form["name"]
        mobile = request.form["mobile"]
        marks = int(request.form["marks"])
        branch = request.form["branch"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, mobile, marks, branch) VALUES (?, ?, ?, ?)",
            (name, mobile, marks, branch)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("suggestions", marks=marks, branch=branch))

    return render_template("student.html")


@app.route("/suggestions")
def suggestions():
    marks = int(request.args.get("marks"))
    branch = request.args.get("branch")

    engineering_branches = ["cs", "it", "mech", "civil", "ee"]
    medical_branches = ["medical", "general science"]

    if branch.lower() in medical_branches:
        eligible_colleges = [c for c in MEDICAL_COLLEGES if marks >= 50]
    elif branch.lower() in engineering_branches:
        eligible_colleges = [c for c in ENGINEERING_COLLEGES if marks >= 60]
    else:
        eligible_colleges = []

    return render_template("suggestions.html", branch=branch, colleges=eligible_colleges)


if __name__ == "__main__":
    init_db()
    print("✅ Database ready. Open http://127.0.0.1:5000/")
    app.run(debug=True)
