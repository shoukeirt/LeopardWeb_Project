from os import remove
from user import User
from student import Student
from instructor import Instructor
import sqlite3
import datetime

class Admin(User):
    def __init__(self, in_firstName, in_lastName, in_id, cursor, cx):
        super().__init__(in_firstName, in_lastName, in_id)
        self.cursor = cursor
        self.cx = cx

    def add_course(self):
        new_crn = int(input("What is the CRN of the new course?"))
        new_title = input("What is the title of the course?")
        new_dep = input("What department is the new course in?")
        new_start = input("Enter time in HH:MM AM/PM format: ")
        try:
            time_start = datetime.datetime.strptime(new_start, "%I:%M %p").time()
            time_start_str = time_start.strftime("%H:%M:%S")
            print(f"You entered the time: {time_start_str}")
        except ValueError:
            print("Invalid time format. Please use HH:MM AM/PM.")
        new_days = input("What days of the week? (M/T/R Format)")
        new_sem = str(input("What semester will this course be available?"))
        new_year = int(input("What year will this course be available?"))
        credits = int(input("How many credits is this course?"))
        sql_command = """INSERT INTO COURSES (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(sql_command, (new_crn, new_title, new_dep, time_start_str, new_days, new_sem, new_year, credits))
        self.cx.commit()
        return "Course Successfully Added!"

    def add_user(self):
        new_id = int(input("What is the ID of the new student?"))
        new_fname = str(input("What is the first name of the new student?"))
        new_lname = str(input("What is the surname of the new student?"))
        new_gradyear = int(input("What year does the new student graduate?"))
        new_major = str(input("What is the student's major? (BSAS format)"))
        new_email = (new_lname + new_fname[0]).lower()
        new_student = Student(new_id, new_fname, new_lname, new_gradyear, new_major, new_email)
        sql_command = """INSERT INTO STUDENT (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL) VALUES (?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(sql_command,
            (new_student.id, new_student.firstName, new_student.lastName, new_student.gradyear, new_student.major, new_student.email))
        self.cx.commit()
        print("New user added!")
        return

    def print_all_info(self):
        return super().print_all_info()

    # [Other functions like remove_course, add_instructor, remove_user, etc., remain unchanged]
