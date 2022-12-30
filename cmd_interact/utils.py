import datetime
import traceback

from db import insert, select

MSG_MENU = '''
[1] : Register New Students.
[2] : Enroll a Course.
[3] : Create new Course.
[4] : Create new Schedule. 
[5] : Display Student Course Schedule. 
[6] : Exit :(

'''

valid_options = [1, 2, 3, 4, 5, 6]

ACCEPTED_LEVELS = dict()  # select from db


def get_levels():
    global ACCEPTED_LEVELS
    statement = 'select level_name, level_id from levels'
    levels = select(statement, multi_row=True)
    levels = {level[0]: level[1] for level in levels}
    ACCEPTED_LEVELS = levels
    print(levels, type(levels))


class CourseSchedule:

    def __init__(self):
        self.courses_id = []
        self.new_schedule_dict = dict()

    def create_new(self):
        self.courses_id = Course.get_courses_id()
        self.display_course_schedule()
        if not self.is_time_available():
            return
        self.add_schedule()

    def is_time_available(self):
        start_time = self.new_schedule_dict['start_time']
        duration = self.new_schedule_dict['duration']

        duration_delta = convert_time_to_delta(duration)
        end_time = add_time_to_delta(start_time, duration_delta)
        end_time_delta = convert_time_to_delta(end_time)
        end_time_delta_seconds = end_time_delta.seconds
        level_id = select(f'select level_id from courses where course_id = {self.new_schedule_dict["course_id"]}')[0]
        all_courses_same_level = select(f'select course_id from courses where level_id = {level_id}', multi_row=True)
        print('all_courses_same_level', all_courses_same_level)
        all_courses_same_level = [str(course[0]) for course in all_courses_same_level]
        all_courses_same_level = ','.join(all_courses_same_level)

        end_times_db = select(f'select distinct ADDTIME(start_time, duration) end_time from course_schedule where '
                              f'course_id in ({all_courses_same_level}) and '
                              f'day_of_week = \'{self.new_schedule_dict["day_of_week"]}\' and start_time = \'{start_time}\' '
                              , multi_row=True)

        print('end_times_db', end_times_db)
        print('end_time_delta_seconds', end_time_delta_seconds)
        if end_times_db:
            for end_time_db in end_times_db:
                if end_time_delta_seconds == end_time_db[0].seconds:
                    print('Sorry, Can Not schedule a course with the same level at the same time.')
                    return False
        print('Time is Available')
        return True

    def add_schedule(self):
        last_id = insert(table='course_schedule', data_dict=self.new_schedule_dict)
        return last_id

    def display_course_schedule(self):

        day_of_week = input('WeekDay eg.(Sat, Sun, Mon, ...): \n')

        course_id = input('Course Code (ID): \n')
        while int(course_id) not in self.courses_id:
            print(f'Course ID : {course_id} is NOT exist, (Current Courses Ids ={self.courses_id})')
            course_id = input('Course Code (ID): \n').upper()

        start_time = input('Start Time eg.(13:30:00): \n')
        while not self.check_str_time(start_time):
            start_time = input('Start Time eg.(13:30:00): \n')
        start_time = self.check_str_time(start_time)

        duration = input('Duration eg.(2:30:00): \n')
        while not self.check_str_time(duration):
            duration = input('Duration eg.(2:30:00): \n')
        duration = self.check_str_time(duration)

        new_schedule = {
            'day_of_week': day_of_week,
            'course_id': course_id,
            'start_time': start_time,
            'duration': duration,
        }
        self.new_schedule_dict = new_schedule

    @staticmethod
    def check_str_time(my_str):
        try:
            my_time = datetime.datetime.strptime(my_str, '%H:%M:%S').time()
            print(type(my_time))
            print(my_time)
            return my_time
        except:
            print('Error Time Format!')


class Course:
    new_course_dict = dict()
    new_enroll_dict = dict()
    courses_id = []

    @classmethod
    def create_new_course(cls):
        get_levels()
        cls.get_courses_id()

        cls.display_new_course()
        cls.add_course()

    @classmethod
    def enroll_course(cls):
        cls.get_courses_id()
        cls.display_enroll_course()

        if not cls.check_same_level():
            return

        if cls.check_enrolled():
            return

        if cls.is_full_capacity():
            return

        cls.add_enroll()

    @classmethod
    def get_max_capacity(cls):
        statement = f'select max_capacity from courses where course_id = {cls.new_enroll_dict["course_id"]}'
        max_capacity = select(statement)[0]
        return max_capacity

    @classmethod
    def get_current_capacity(cls):
        statement = f'select count(*) from enrollment_history where course_id = {cls.new_enroll_dict["course_id"]}'
        current_capacity = select(statement)[0]
        return current_capacity

    @classmethod
    def is_full_capacity(cls):
        if cls.get_max_capacity() <= cls.get_current_capacity():
            print('Sorry, This Course is Full.')
            return True
        return False

    @classmethod
    def add_course(cls):
        last_id = insert(table='courses', data_dict=cls.new_course_dict)
        return last_id

    @classmethod
    def add_enroll(cls):
        print(
            f'Enrolling course: {cls.new_enroll_dict["course_id"]} , to student_id : {cls.new_enroll_dict["student_id"]}')
        last_id = insert(table='enrollment_history', data_dict=cls.new_enroll_dict)
        return last_id

    @classmethod
    def get_courses_id(cls):
        statement = 'select distinct course_id from courses'
        courses = select(statement, multi_row=True)
        courses = [course[0] for course in courses]
        print(courses)
        cls.courses_id = courses
        return cls.courses_id

    @classmethod
    def check_enrolled(cls):

        statement = f'select enroll_id from enrollment_history where student_id = {cls.new_enroll_dict["student_id"]} ' \
                    f'and course_id = {cls.new_enroll_dict["course_id"]}'

        enroll_id = select(statement)
        print('enroll_id:', enroll_id)

        if enroll_id:
            print('This Student is Already Enrolled this Course before, Please Try again.')
            return True
        return False

    @classmethod
    def check_same_level(cls):

        statement = f'select level_id from students where student_id = {cls.new_enroll_dict["student_id"]}'
        level_student = select(statement)[0]
        print('level_student:', level_student)

        statement = f'select level_id from courses where course_id = {cls.new_enroll_dict["course_id"]}'
        level_course = select(statement)[0]
        print('level_course:', level_course)
        if level_course != level_student:
            print('This Student is Not in the Same Level with this Course, ')
            return False
        return True

    @classmethod
    def display_enroll_course(cls):
        students_id = Student.get_students_id()
        student_id = input('Student ID: \n')
        while int(student_id) not in students_id:
            print(f'Student ID : {student_id} is NOT exist, (Current Students Ids ={students_id})')
            student_id = input('Student ID: \n')

        course_id = input('Course Code (ID): \n')
        while int(course_id) not in cls.courses_id:
            print(f'Course ID : {course_id} is NOT exist, (Current Courses Ids ={cls.courses_id})')
            course_id = input('Course Code (ID): \n').upper()

        total_hours = input('Total Hours: \n')

        new_enroll_dict = {
            'student_id': student_id,
            'course_id': course_id,
            'total_hours': total_hours,
        }

        cls.new_enroll_dict = new_enroll_dict

    @classmethod
    def display_new_course(cls):

        course_id = input('Course Code (ID): \n')
        while int(course_id) in cls.courses_id:
            print(f'Course ID : {course_id} is already exist before, (Current Courses Ids ={cls.courses_id}) Please '
                  f'try a different Course ID.')
            course_id = input('Course Code (ID): \n').upper()

        course_name = input('Course Name: \n')
        max_capacity = input('Max Capacity: \n')
        rate_per_hour = input('Hour Rate (Price): \n')

        level_name = input('Level Name: \n').upper()
        while level_name not in ACCEPTED_LEVELS:
            print(f'Level should be in {list(ACCEPTED_LEVELS.keys())}')
            level_name = input('Level Name: \n').upper()

        level_id = ACCEPTED_LEVELS[level_name]

        new_course_dict = {
            'course_id': course_id,
            'course_name': course_name,
            'max_capacity': max_capacity,
            'rate_per_hour': rate_per_hour,
            'level_id': level_id,
        }

        cls.new_course_dict = new_course_dict


class Student:
    def __init__(self):
        self.student_dict = dict()

    @classmethod
    def get_students_id(cls):
        statement = 'select distinct student_id from students'
        students_id = select(statement, multi_row=True)
        students_id = [student[0] for student in students_id]
        return students_id

    def display_student_schedule(self):
        student_id = input('Student ID: \n')
        student_courses = self.get_courses_id(student_id)
        if not student_courses:
            print('Sorry this Student does NOT have any courses yet.')
            return
        print(student_courses)
        self.print_courses_schedule(student_courses)

    @staticmethod
    def print_courses_schedule(courses_id):
        courses_id = list(map(str, courses_id))
        courses_id = ','.join(courses_id)
        courses_schedule = f'select * from course_schedule where course_id in ({courses_id})'
        courses_schedule = select(courses_schedule, multi_row=True)
        # courses_id = [course[0] for course in courses]
        for course in courses_schedule:
            # print(course)
            start_time_delta = course[3]
            start_time = convert_delta_to_time(start_time_delta)
            duration_delta = course[4]

            end_time_delta = start_time_delta + duration_delta
            end_time = convert_delta_to_time(end_time_delta)

            print(f'Course ID: {course[1]} || Day: {course[2]} || From {start_time} --> {end_time}')

        return courses_schedule

    @staticmethod
    def get_courses_id(student_id):
        statement = f'select distinct course_id from enrollment_history where student_id = {student_id}'
        courses = select(statement, multi_row=True)
        courses_id = [course[0] for course in courses]
        print(courses_id)
        return courses_id

    def create_new_student(self):
        get_levels()
        self.display_new_student()

        contact_id = self.add_contact()
        print('contact_id: ', contact_id)

        address_id = self.add_address()
        print('address_id: ', address_id)

        student_id = self.add_student()
        print('student_id: ', student_id)

    def add_student(self):
        last_id = insert(table='students', data_dict=self.student_dict)
        return last_id

    def add_contact(self):
        contact_dict = dict((k, self.student_dict[k]) for k in ('mobile', 'email') if k in self.student_dict)
        last_id = insert(table='contacts', data_dict=contact_dict)

        del self.student_dict['mobile']
        del self.student_dict['email']

        self.student_dict['contact_id'] = last_id

        return last_id

    def add_address(self):
        address_dict = {'address_name': self.student_dict[
            'address_name']}  # dict((k, self.student_dict[k]) for k in ('address_name',) if k in self.student_dict)
        last_id = insert(table='addresses', data_dict=address_dict)

        del self.student_dict['address_name']

        self.student_dict['address_id'] = last_id

        return last_id

    def display_new_student(self):

        student_name = input('Student Name: \n')
        dob = input('Date Of Birth eg.(31/12/2005): \n')
        while not check_str_date(dob):
            dob = input('Date Of Birth eg.(31/12/2005): \n')
        dob = check_str_date(dob)

        level_name = input('Level Name: \n').upper()
        while level_name not in ACCEPTED_LEVELS:
            print(f'Level should be in {list(ACCEPTED_LEVELS.keys())}')
            level_name = input('Level Name: \n').upper()

        level_id = ACCEPTED_LEVELS[level_name]

        mobile = input('Mobile Number: \n')
        while not check_integer(mobile):
            mobile = input('Mobile Number: \n')

        email = input('Email: \n')
        address_name = input('Address Name: \n')

        student_dict = {
            'student_name': student_name,
            'dob': dob,
            'level_id': level_id,
            'mobile': mobile,
            'email': email,
            'address_name': address_name,
        }

        self.student_dict = student_dict


def check_str_date(my_str):
    try:
        my_date = datetime.datetime.strptime(my_str, '%d/%m/%Y')
        return my_date
    except:
        print('Error Date Format')


def check_integer(num):
    try:
        integer = int(num)
        # print(integer)
        return True
    except ValueError:
        print('The provided value is not an integer')


def check_valid_option(my_option):
    if not check_integer(my_option):
        return
    if int(my_option) not in valid_options:
        print('Please select a valid option!')
        return
    return True


def convert_delta_to_time(my_delta):
    my_time = (datetime.datetime.min + my_delta).time()
    return my_time


def convert_time_to_delta(my_time):
    my_time_delta = datetime.timedelta(hours=my_time.hour, minutes=my_time.minute, seconds=my_time.second)
    return my_time_delta


def add_time_to_delta(my_time, my_delta):
    return (datetime.datetime.combine(datetime.date(1, 1, 1), my_time) + my_delta).time()  # time object


if __name__ == '__main__':
    Course.get_courses_id()
