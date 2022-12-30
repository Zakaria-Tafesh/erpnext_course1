import json
from utils import get_response_courses, get_response_students, get_response_schedules
from flask import render_template  # Remove: import Flask

import connexion


app = connexion.App(__name__, specification_dir="./")

app.add_api("swagger.yml")

# app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


# @app.route('/api/courses', methods=['GET'])
# def courses():
#     res_json = get_response_courses()
#     return res_json
#
#
# @app.route('/api/students', methods=['GET'])
# def students():
#     res_json = get_response_students()
#     return res_json
#
#
# @app.route('/api/schedules', methods=['GET'])
# def schedules():
#     res_json = get_response_schedules()
#     return res_json


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
