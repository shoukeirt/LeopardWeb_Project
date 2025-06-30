import sqlite3
from user import User

class Instructor(User):
    def __init__(self, in_firstName, in_lastName, in_id, in_title, in_hireyear, in_dept, in_email):
        super().__init__(in_firstName, in_lastName, in_id)
        self.title = in_title
        self.hireyear = in_hireyear
        self.dept = in_dept
        self.email = in_email

    def search_courses(self, Search_keyword='CRN', search_value=None):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()
        if Search_keyword.upper() == "CRN":
            Search_keyword = "CRN"
        elif Search_keyword.upper() in ["COURSE NAME", "TITLE"]:
            Search_keyword = "TITLE"
        else:
            print("Invalid search keyword.")
            return
        if isinstance(search_value, int):
            search_value = str(search_value)
        else:
            search_value = f"'{search_value}'"
        query = f"SELECT * FROM COURSES WHERE {Search_keyword} = {search_value}"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cx.close()

    def print_schedule(self):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()
        try:
            query = """
            SELECT COURSE_TEACHER.CRN, COURSE_TEACHER.TITLE, COURSE_TEACHER.DEPARTMENT,
                   COURSE_TEACHER.TIME, COURSE_TEACHER.DAYS, COURSE_TEACHER.SEMESTER, COURSE_TEACHER.CREDITS
            FROM COURSE_TEACHER
            WHERE INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ?
            """
            cursor.execute(query, (self.firstName, self.lastName))
            rows = cursor.fetchall()
            if rows:
                print("\nYour Teaching Schedule:")
                for row in rows:
                    print(f"CRN: {row[0]}, Title: {row[1]}, Dept: {row[2]}, Time: {row[3]}, Days: {row[4]}, Semester: {row[5]}, Credits: {row[6]}")
            else:
                print("\nYou are not assigned to any courses.")
        except sqlite3.OperationalError as e:
            print(f"SQL Error: {e}")
        finally:
            cx.close()

    def search_roster(self, crn):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()
        try:
            cursor.execute("SELECT * FROM COURSE_TEACHER WHERE INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ? AND CRN = ?",
                           (self.firstName, self.lastName, crn))
            if not cursor.fetchone():
                print(f"\nYou are not assigned to teach the course with CRN {crn}. Access denied.")
                return

            cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (crn,))
            course = cursor.fetchone()
            if not course:
                print("Course not found.")
                return
            print(f"Course found: {course[1]}")

            first = input("Enter the student's FIRST name: ").strip()
            last = input("Enter the student's LAST name: ").strip()
            full_name = f"{first} {last}"

            cursor.execute("SELECT * FROM Student_Schedule LIMIT 1")
            col_names = [desc[0] for desc in cursor.description]
            name_column = next((col for col in col_names if col.lower() in ['studentname', 'name', 'fullname', 'student', 'student name']), None)
            if not name_column:
                print("Error: Could not find student name column.")
                return

            crn_columns = [col for col in col_names if col.startswith('CRN')]
            enrolled = False
            for crn_col in crn_columns:
                cursor.execute(f'SELECT * FROM Student_Schedule WHERE "{name_column}" = ? AND "{crn_col}" = ?', (full_name, crn))
                if cursor.fetchone():
                    enrolled = True
                    break

            if enrolled:
                print(f"{full_name} is enrolled in CRN {crn}")
            else:
                print(f"{full_name} is NOT enrolled in CRN {crn}")
        except sqlite3.Error as e:
            print(f"SQL Error: {e}")
        finally:
            cx.close()

    def print_roster(self, crn):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()
        try:
            cursor.execute("SELECT * FROM COURSE_TEACHER WHERE INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ? AND CRN = ?",
                           (self.firstName, self.lastName, crn))
            if not cursor.fetchone():
                print(f"\nYou are not assigned to teach the course with CRN {crn}. Access denied.")
                return

            cursor.execute("SELECT * FROM Student_Schedule LIMIT 1")
            col_names = [desc[0] for desc in cursor.description]
            name_column = next((col for col in col_names if col.lower() in ['studentname', 'name', 'fullname', 'student', 'student name']), None)
            if not name_column:
                print("Error: Could not find student name column.")
                return

            crn_columns = [col for col in col_names if col.startswith('CRN')]
            enrolled_students = set()
            for crn_col in crn_columns:
                cursor.execute(f'SELECT "{name_column}" FROM Student_Schedule WHERE "{crn_col}" = ?', (crn,))
                for result in cursor.fetchall():
                    enrolled_students.add(result[0])

            print(f"\nClass Roster for CRN {crn}:")
            if enrolled_students:
                for student in sorted(enrolled_students):
                    print(student)
            else:
                print("No students enrolled.")
        except sqlite3.Error as e:
            print(f"SQL Error: {e}")
        finally:
            cx.close()
