import requests
from decouple import config


URL_COURSES = 'http://127.0.0.1:8000/api/courses'
URL_STUDENTS = 'http://127.0.0.1:8000/api/students'
URL_SCHEDULE = 'http://127.0.0.1:8000/api/schedules'


headers = {'X-API-KEY': config('API_KEY')}


def get_courses():
    res = requests.get(URL_COURSES, headers=headers)
    print(res)
    res_json = res.json()
    all_courses = res_json['courses']
    header = res_json['header']

    print(res.json())

    if res.status_code == 200:
        print('Get ALL Courses Successfully ')
        return all_courses, header
    else:
        print('ERROR Getting All Courses')
        return False


def get_students():
    res = requests.get(URL_STUDENTS, headers=headers)
    print('#'*100)
    print(res)
    res_json = res.json()
    all_students = res_json['students']
    header = res_json['header']

    print(res.json())

    if res.status_code == 200:
        print('Get all_students Successfully ')
        return all_students, header
    else:
        print('ERROR Getting all_students')
        return False


def get_schedules():
    res = requests.get(URL_SCHEDULE, headers=headers)
    print('#'*100)
    print(res)
    res_json = res.json()
    schedules = res_json['course_schedule']
    header = res_json['header']

    print(res.json())

    if res.status_code == 200:
        print('Get schedules Successfully ')
        return schedules, header
    else:
        print('ERROR schedules all_students')
        return False


if __name__ == '__main__':
    get_courses()
