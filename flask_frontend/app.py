from flask import Flask, render_template
from utils import get_courses, get_students, get_schedules

app = Flask(__name__)


@app.route("/courses")
def courses_home():
    courses, headers = get_courses()
    print(courses)
    context = {
        "title": "Courses",
        'list_dicts': courses,
        'headers': headers
    }
    return render_template("new_table.html", **context)


@app.route("/students")
def students_home():
    students, headers = get_students()
    print(students)
    context = {
        "title": "students",
        'list_dicts': students,
        'headers': headers
    }
    return render_template("new_table.html", **context)


@app.route("/schedules")
def schedules_home():
    schedules, headers = get_schedules()
    print(schedules)
    context = {
        "title": "schedules",
        'list_dicts': schedules,
        'headers': headers
    }
    return render_template("new_table.html", **context)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
