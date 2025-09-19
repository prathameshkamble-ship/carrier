from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Colleges by branch and marks ranges
COLLEGES_BY_BRANCH_MARKS = {
    "engineering": {
        (30, 60): [
            "Aurangabad College of Engineering",
            "Deogiri Institute of Engineering & Management Studies",
            "Marathwada Institute of Technology"
        ],
        (60, 90): [
            "MIT Aurangabad",
            "P.E.S. College of Engineering",
            "Government College of Engineering Aurangabad (Mechanical, Civil, Electrical)"
        ],
        (90, 101): [  # 101 to include 100
            "Government College of Engineering Aurangabad (CSE, IT, E&TC)"
        ]
    },
    "medical": {
        (30, 60): [
            "Private BAMS / BHMS Colleges, Aurangabad"
        ],
        (60, 90): [
            "MGM Medical College & Hospital, Aurangabad",
            "Private MBBS Colleges"
        ],
        (90, 101): [
            "Government Medical College, Aurangabad"
        ]
    },
    "management": {
        (30, 60): [
            "Deogiri Institute of Management Studies",
            "Local Private MBA Colleges"
        ],
        (60, 90): [
            "MGM Institute of Management",
            "Dr. Rafiq Zakaria College of Management"
        ],
        (90, 101): [
            "MGM Institute of Management"
        ]
    },
    "arts": {
        (30, 60): [
            "Dr. Babasaheb Ambedkar Marathwada University Affiliated Arts Colleges",
            "Local Arts & Commerce Colleges"
        ],
        (60, 90): [
            "Deogiri College, Aurangabad",
            "Rafiq Zakaria College for Arts"
        ],
        (90, 101): [
            "Deogiri College (Merit Seats)",
            "Maulana Azad College of Arts, Science & Commerce"
        ]
    }
}

# Branch mapping from form selection to main category
branch_mapping = {
    "cs": "engineering", "it": "engineering", "mech": "engineering",
    "civil": "engineering", "ee": "engineering", "medical": "medical",
    "general science": "medical", "mba": "management", "arts": "arts"
}


@app.route("/", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        name = request.form["name"]
        mobile = request.form["mobile"]
        marks = int(request.form["marks"])
        branch = request.form["branch"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, mobile, marks, branch) VALUES (?, ?, ?, ?)",
                       (name, mobile, marks, branch))
        conn.commit()
        conn.close()

        return redirect(url_for("suggestions", marks=marks, branch=branch))

    return render_template("student.html")


@app.route("/suggestions")
def suggestions():
    marks = int(request.args.get("marks"))
    branch = request.args.get("branch").lower()

    main_branch = branch_mapping.get(branch)

    eligible_colleges = []

    if main_branch and marks >= 30:
        for (low, high), colleges in COLLEGES_BY_BRANCH_MARKS.get(main_branch, {}).items():
            if low <= marks < high:
                eligible_colleges = colleges
                break

    return render_template("suggestions.html",
                           branch=branch,
                           colleges=eligible_colleges)


if __name__ == "__main__":
    # Initialize database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile TEXT,
        marks INTEGER,
        branch TEXT
        )
    """)
    conn.commit()
    conn.close()

    app.run(debug=True)

