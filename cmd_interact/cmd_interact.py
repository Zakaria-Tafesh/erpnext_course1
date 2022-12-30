from utils import *


def display_options():
    option = input(MSG_MENU)
    is_valid_option = check_valid_option(option)
    while not is_valid_option:
        option = input(MSG_MENU)
        is_valid_option = check_valid_option(option)

    option = int(option)

    if option == 1:
        s = Student()
        s.create_new_student()

    elif option == 2:
        Course.enroll_course()

    # Create new Course
    elif option == 3:
        Course.create_new_course()

    elif option == 4:
        c = CourseSchedule()
        c.create_new()
    #
    elif option == 5:
        s = Student()
        s.display_student_schedule()

    else:
        return 'exit'



while True:

    print('#' * 30)

    status = display_options()
    if status == 'exit':
        break

print('Exiting from the System, See You soon.')
