import unittest
import sqlite3
from student import Student
from admin import Admin
from instructor import Instructor
from login_menu import login
import datetime
##File made by Toufic Shoukeir and Anthony Magliozzi

cx = sqlite3.connect("assignment3.db")
cursor = cx.cursor()
# Setup test objects
student_user = Student("Toufic", "Shoukeir", 10015)
instructor_user = Instructor("Brad", "Stevens", 20007, "Full Prof.", 2020, "BSCO", "stevensb")
admin_user = Admin("Margaret", "Hamilton", 30001, cursor, cx)


def login_testable(email, password, cursor):
        try:
            cursor.execute("SELECT ID FROM LOGIN WHERE EMAIL = ? AND PASSWORD = ?", (email, password))
            result = cursor.fetchone()
            if not result: #failed login
                return None 
            user_id = result[0]
            user_str = str(user_id)
            if user_str.startswith("1"):
                cursor.execute("SELECT NAME, SURNAME FROM STUDENT WHERE ID = ?", (user_id,))
                name = cursor.fetchone()
                return {"type": "student", "id": user_id, "name": name}
            elif user_str.startswith("2"):
                cursor.execute("SELECT NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL FROM INSTRUCTOR WHERE ID = ?", (user_id,))
                info = cursor.fetchone()
                return {"type": "instructor", "id": user_id, "info": info}
            elif user_str.startswith("3"):
                cursor.execute("SELECT NAME, SURNAME FROM ADMIN WHERE ID = ?", (user_id,))
                name = cursor.fetchone()
                return {"type": "admin", "id": user_id, "name": name}
            else:
                return None #unknown user... this should NEVER happen. - Toufic 
        except Exception as exception:
            return {"error": str(exception)}

def logout_testable(current_user):
    # Simulate logout
    return f"User {current_user} logged out successfully."

def admin_add_course_testable(self, crn, title, dep, time_str, days, sem, year, credits):
    try:
        time_start = datetime.datetime.strptime(time_str, "%I:%M %p").time()
        time_start_str = time_start.strftime("%H:%M:%S")
    except ValueError:
        return "Invalid time format. Please use HH:MM AM/PM."

    sql = """
        INSERT INTO COURSES (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        self.cursor.execute(sql, (crn, title, dep, time_start_str, days, sem, year, credits))
        self.cx.commit()
        return "Course Successfully Added!"
    except sqlite3.IntegrityError:
        return f"Course with CRN {crn} already exists."
    except Exception as exception:
        return f"Database error: {exception}"
Admin.add_course_testable = admin_add_course_testable

def admin_remove_course_testable(self, crn):
    try:
        self.cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (crn,))
        row = self.cursor.fetchone()
        if not row:
            return "Course not found."
        self.cursor.execute("DELETE FROM COURSES WHERE CRN = ?", (crn,))
        self.cx.commit()
        return "Course Removed!"
    except Exception as exception:
        return f"Database error: {exception}"
Admin.remove_course_testable = admin_remove_course_testable



class TestLeopardWeb(unittest.TestCase):

    def test_student_print_all_courses(self):
        print("\n\n\n\n ----- THIS IS THE STUDENT PRINT ALL COURSES TEST")
        result = student_user.print_all_courses(cursor)
        self.assertIsInstance(result, list)
        for course in result:
            print(course)


    def test_student_search_courses(self):
        print("\n\n\n\n ----- THIS IS THE STUDENT SEARCHING FOR A COURSE TEST")
        result = student_user.search_courses("TITLE", "Computer Science I")
        self.assertIsInstance(result, list)

    def test_student_add_course(self):
        print("\n\n\n\n ----- THIS IS THE STUDENT ADDING COURSE TO SCHEDULE TEST")
        student_user.add_course("CRN", 2000)  

    def test_student_remove_course(self):
        print("\n\n\n\n ----- THIS IS THE STUDENT REMOVING COURSE FROM SCHEDULE TEST")
        student_user.remove_course(2000)

    def test_instructor_search_courses(self):
        print("\n\n\n\n ----- THIS IS THE INSTRUCTOR SEARCCHING FOR A COURSE TEST")
        instructor_user.search_courses("CRN", 2000)

    def test_instructor_print_roster(self):
        print("\n\n\n\n ----- THIS IS THE INSTRUCTOR PRINTING ROSTER TEST")
        instructor_user.print_roster(2000)

    def test_valid_login(self):
        print("\n\n\n\n ----- THIS IS THE LOGIN TEST")
        result = login_testable("newtoni", 1144, cursor) 
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "student") 

    def test_invalid_login(self):
        print("\n\n\n\n ----- THIS IS THE INVALID LOGIN TEST")
        result = login_testable("fakeuser", 9999, cursor)
        self.assertIsNone(result)

    def test_logout(self):
        print("\n\n\n\n ----- THIS IS THE LOGOUT TEST")
        result = logout_testable("Toufic Shoukeir (Student ID: 10015)")
        self.assertIn("logged out", result)


    def test_admin_add_course(self):
        print("\n\n\n\n ----- THIS IS THE ADMIN ADD COURSE TEST")
        result = admin_user.add_course_testable(
            crn=99999,
            title="Software Testing",
            dep="BSCO",
            time_str="9:00 AM",
            days="T/R",
            sem="Spring",
            year=2026,
            credits=3
        )
        print("Add course result:", result)
        self.assertIn("Added", result)

    def test_admin_remove_course(self):
        print("\n\n\n\n ----- THIS IS THE ADMIN REMOVE COURSE TEST")
        result = admin_user.remove_course_testable(99999)
        print("Remove course result:", result)
        self.assertIn("Removed", result)



if __name__ == "__main__":
    unittest.main()
