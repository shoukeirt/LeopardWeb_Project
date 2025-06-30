from user import User
import sqlite3


class Instructor(User):
    def __init__(self, in_firstName, in_lastName, in_id, in_title, in_hireyear, in_dept, in_email):
        #Call the superclass constructor
        super().__init__(in_firstName, in_lastName, in_id)
        #Set additional instructor-specific attributes
        self.title = in_title
        self.hireyear = in_hireyear
        self.dept = in_dept
        self.email = in_email

    #Search for courses based on CRN or Title
    def search_courses(self, Search_keyword='CRN', search_value=None):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()

        #Search Course Based on CRN or TITLE
        if Search_keyword.upper() == "CRN":
            Search_keyword = "CRN"
        elif Search_keyword.upper() in ["COURSE NAME", "TITLE"]:
            Search_keyword = "TITLE"
        else:
            print("Invalid search keyword.")
            return

        #Format value for query
        if isinstance(search_value, int):
            search_value = str(search_value)
        else:
            search_value = f"'{search_value}'"

        #Execute SQL query to search course
        query = f"SELECT * FROM COURSES WHERE {Search_keyword} = {search_value}"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    #Print the instructor's assigned course schedule
    def print_schedule(self):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()

        try:
            #Query all courses assigned to this instructor
            query = """
            SELECT COURSES.CRN, COURSES.TITLE, COURSES.DEPARTMENT, COURSES.TIME, COURSES.DAYS, COURSES.SEMESTER, COURSES.CREDITS
            FROM COURSES
            JOIN COURSE_TEACHER ON COURSES.CRN = COURSE_TEACHER.CRN
            WHERE COURSE_TEACHER.INSTRUCTOR_NAME = ? AND COURSE_TEACHER.INSTRUCTOR_SURNAME = ?
            """
            cursor.execute(query, (self.firstName, self.lastName))
            rows = cursor.fetchall()

            #Print results if found
            if rows:
                print("\nYour Teaching Schedule:")
                for row in rows:
                    print(f"CRN: {row[0]}, Title: {row[1]}, Dept: {row[2]}, Time: {row[3]}, Days: {row[4]}, Semester: {row[5]}, Credits: {row[6]}")
            else:
                print("\nYou are not assigned to any courses.")
        except sqlite3.OperationalError as e:
            print(f"SQL Error while accessing COURSE_TEACHER: {e}")
        finally:
            cx.close()

    #Search a specific course roster for a specific student
    def search_roster(self, crn):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()

        try:
            #Verify instructor is teaching the course
            cursor.execute("""
                SELECT * FROM COURSE_TEACHER 
                WHERE INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ? AND CRN = ?
            """, (self.firstName, self.lastName, crn))
            course_assignment = cursor.fetchone()

            if not course_assignment:
                print(f"\nYou are not assigned to teach the course with CRN {crn}. Access denied.")
                return

            #Get course name if it exists
            cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (crn,))
            course = cursor.fetchone()
            if not course:
                print("Course not found.")
                return
            print(f"Course found: {course[1]}")

            #Prompt for student name
            first = input("Enter the student's FIRST name: ").strip()
            last = input("Enter the student's LAST name: ").strip()
            full_name = f"{first} {last}"

            #Find correct student name column
            cursor.execute("SELECT * FROM Student_Schedule LIMIT 1")
            col_names = [description[0] for description in cursor.description]

            name_column = None
            for possible in ['StudentName', 'NAME', 'FullName', 'Student', 'Student Name']:
                if possible in col_names:
                    name_column = possible
                    break

            if name_column is None:
                print("Error: Could not find a valid student name column in Student_Schedule.")
                print(f"Available columns: {col_names}")
                return

            #Check all CRN columns for student enrollment
            crn_columns = [col for col in col_names if col.startswith('CRN')]
            enrolled = False

            for crn_col in crn_columns:
                query = f'SELECT * FROM Student_Schedule WHERE "{name_column}" = ? AND "{crn_col}" = ?'
                cursor.execute(query, (full_name, crn))
                if cursor.fetchone():
                    enrolled = True
                    break

            #Print enrollment result
            if enrolled:
                print(f"{full_name} is enrolled in CRN {crn}")
            else:
                print(f"{full_name} is NOT enrolled in CRN {crn}")

        except sqlite3.OperationalError as e:
            print(f"SQL Error while accessing Student_Schedule: {e}")
        finally:
            cx.close()

    #Print all students enrolled in a specific course
    def print_roster(self, crn):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()

        try:
            #Verify instructor is assigned to the course
            cursor.execute("""
                SELECT * FROM COURSE_TEACHER 
                WHERE INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ? AND CRN = ?
            """, (self.firstName, self.lastName, crn))
            if not cursor.fetchone():
                print(f"\nYou are not assigned to teach the course with CRN {crn}. Access denied.")
                return

            #Get all student name column and CRN columns
            cursor.execute("SELECT * FROM Student_Schedule LIMIT 1")
            col_names = [description[0] for description in cursor.description]

            name_column = None
            for possible in ['StudentName', 'NAME', 'FullName', 'Student', 'Student Name']:
                if possible in col_names:
                    name_column = possible
                    break

            if name_column is None:
                print("Error: Could not find a valid student name column in Student_Schedule.")
                print(f"Available columns: {col_names}")
                return

            crn_columns = [col for col in col_names if col.startswith('CRN')]

            #Gather all enrolled students
            enrolled_students = set()
            for crn_col in crn_columns:
                query = f'SELECT "{name_column}" FROM Student_Schedule WHERE "{crn_col}" = ?'
                cursor.execute(query, (crn,))
                results = cursor.fetchall()
                for r in results:
                    enrolled_students.add(r[0])

            #Print class roster
            print(f"\nClass Roster for CRN {crn}:")
            if enrolled_students:
                for student in enrolled_students:
                    print(student)
            else:
                print("No students enrolled.")

        except sqlite3.OperationalError as e:
            print(f"SQL Error while accessing Student_Schedule: {e}")
        finally:
            cx.close()

    #Print all instructor info using existing methods
    def print_all_info(self):
        print("ALL INSTRUCTOR INFO:")
        return "NAME: " + self.print_name() + "\nID: " + self.print_id() + "\n"
