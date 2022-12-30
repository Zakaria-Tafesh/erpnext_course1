import datetime
import json

from db import select
from cmd_interact.utils import convert_delta_to_time


def get_columns_names(table_name):
    statement = f'show columns from {table_name}'
    columns = select(statement, multi_row=True)
    columns = [column[0] for column in columns]
    print(columns)
    return columns


def convert_lists_to_dict(name: str, header: list, lists: list):
    """
    name : name of the first key name
    headers : a list of columns name ( keys name )
    lists : list of lists ( or list of tuples), contains the data value
    :return:
    dictionary with the list of sub dictionaries

    """
    list_of_dicts = []
    res_dict = {name: list_of_dicts,
                'header': header}
    for line in lists:
        sub_dict = dict(zip(header, line))
        list_of_dicts.append(sub_dict)

    return res_dict


def get_response_courses():
    def get_all_courses():
        statement = 'select * from courses'
        courses_s = select(statement, multi_row=True)
        print(courses_s)
        return courses_s

    courses = get_all_courses()
    header = get_columns_names('courses')
    res_courses = convert_lists_to_dict('courses', header, courses)
    print(res_courses)
    # res_courses = json.dumps(res_courses, default=json_serial)
    return res_courses


def get_response_students():
    def get_all_students():
        statement = 'select * from students'
        students_s = select(statement, multi_row=True)
        print(students_s)
        return students_s

    students = get_all_students()
    header = get_columns_names('students')
    res_students = convert_lists_to_dict('students', header, students)
    print(res_students)
    # res_students = json.dumps(res_students, default=json_serial)
    return res_students


def get_response_schedules():
    def get_all_schedules():
        statement = 'select c.course_name, cs.day_of_week, cs.start_time, cs.duration ' \
                    'from course_schedule cs join courses c on c.course_id = cs.course_id'
        schedules_s = select(statement, multi_row=True)
        print(schedules_s)
        return schedules_s

    schedules = get_all_schedules()
    schedules = convert_list_tuples(schedules)
    header = get_columns_names('course_schedule')
    header.remove('course_schedule_id')
    header[0] = 'Course Name'
    res_schedules = convert_lists_to_dict('course_schedule', header, schedules)
    print(res_schedules)
    # res_schedules = json.dumps(res_schedules, default=json_serial, )
    return res_schedules


def convert_list_tuples(my_list):
    new_list = []
    for row in my_list:
        sub_list = []
        for item in row:
            if isinstance(item, datetime.timedelta):
                item = str(convert_delta_to_time(item))
            sub_list.append(item)
        new_list.append(sub_list)
    return new_list


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()

    raise TypeError("Type %s not serializable" % type(obj))


if __name__ == '__main__':
    get_response_students()
