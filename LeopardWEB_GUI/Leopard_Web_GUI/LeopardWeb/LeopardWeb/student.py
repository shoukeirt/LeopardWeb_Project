#Written Harljen Hill
#Updated and Fixed and Implemented by Anthony Magliozzi

import sqlite3
from user import User
import datetime
cx = sqlite3.connect("assignment3.db", timeout=5.0)
cursor = cx.cursor()

# Utility function to split a time range string (e.g., '2:30 PM - 4:00 PM') into start and end time objects
def slipt_time(time_str):
    start_time, end_time = time_str.split('-')
    start_time = datetime.datetime.strptime(start_time.strip(), '%I:%M %p')
    end_time = datetime.datetime.strptime(end_time.strip(), '%I:%M %p')
    return start_time, end_time


class Student(User):
    def __init__(self, in_firstName, in_lastName, in_id):
        super().__init__(in_firstName, in_lastName, in_id)

    def print_all_courses(self, cursor):
        sql_command = "SELECT * FROM COURSES"
        cursor.execute(sql_command)
        return cursor.fetchall()

    # Search for courses by CRN or TITLE
    def search_courses(self, Search_keyword, search_value):
        cx = sqlite3.connect("assignment3.db", timeout=5.0)
        cursor = cx.cursor()

        # Verify student exists
        cursor.execute("SELECT * FROM STUDENT WHERE ID = ? and NAME = ? and SURNAME = ?", 
                       (self.id, self.firstName, self.lastName))
        student = cursor.fetchone()
        if not student:
            print("Student not found.")
            cx.close()
            return []

        # Normalize search keyword
        if Search_keyword.upper() == "CRN":
            Search_keyword = "CRN"
        elif Search_keyword.upper() in ["COURSE NAME", "TITLE"]:
            Search_keyword = "TITLE"
        else:
            print("Invalid search keyword.")
            cx.close()
            return []

        # Execute course search
        cursor.execute(f"SELECT * FROM COURSES WHERE {Search_keyword} = ?", (search_value,))
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        cx.close()
        return rows

    # Add course to student schedule and check for time conflicts
    def add_course(self, CRN, search_value):
        cx = sqlite3.connect("assignment3.db", timeout=5.0)
        cursor = cx.cursor()

        try:
            # Get course information
            cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (search_value,))
            course = cursor.fetchone()

            # Retrieve existing enrollments for the student
            cursor.execute("SELECT * FROM ENROLLMENT WHERE STUDENT_ID = ?", (self.id,))
            enrollment = cursor.fetchall()

            if not course:
                print("Course not found.")
                return

            enrolled_crns = [enr[1] for enr in enrollment]

            # If the student is enrolled in any courses, check for time conflicts
            if enrolled_crns:
                query = f"SELECT * FROM COURSES WHERE CRN IN ({','.join(['?'] * len(enrolled_crns))})"
                cursor.execute(query, enrolled_crns)
                enrolled_courses = cursor.fetchall()

                # Parse time and days from the course the student wants to add
                course_days = course[4]
                course_hour_start, course_hour_end = slipt_time(course[3])

                for enrolled_course in enrolled_courses:
                    enrolled_days = enrolled_course[4]
                    enrolled_hour_start, enrolled_hour_end = slipt_time(enrolled_course[3])

                    # Check for overlapping days and time ranges
                    if any(day in enrolled_days for day in course_days) and not (
                        course_hour_end <= enrolled_hour_start or course_hour_start >= enrolled_hour_end):
                        print(f"Time conflict with course {enrolled_course[0]}: {enrolled_course[1]}")
                        return

            # Add course to ENROLLMENT table if no conflict
            cursor.execute("INSERT INTO ENROLLMENT (STUDENT_ID, CRN) VALUES (?, ?)", (self.id, course[0]))
            cx.commit()
            print(f"Course {course[0]} added successfully.")

        except ValueError:
            print("Error parsing time format. Please ensure all course times are valid.")
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
        finally:
            cx.close()

    # Remove course from student schedule
    def remove_course(self, CRN):
        cx = sqlite3.connect("assignment3.db", timeout=5.0)
        cursor = cx.cursor()

        try:
            # Verify student exists
            cursor.execute("SELECT * FROM STUDENT WHERE ID = ? and NAME = ? and SURNAME = ?", 
                           (self.id, self.firstName, self.lastName))
            student = cursor.fetchone()
            if not student:
                print("Student not found.")
                return

            # Check if student is enrolled in the course
            cursor.execute("SELECT * FROM ENROLLMENT WHERE STUDENT_ID = ? AND CRN = ?", (self.id, CRN))
            enrollment = cursor.fetchone()

            if not enrollment:
                print("You are not enrolled in this course.")
            else:
                # Delete enrollment
                cursor.execute("DELETE FROM ENROLLMENT WHERE STUDENT_ID = ? AND CRN = ?", (self.id, CRN))
                cx.commit()
                print(f"Course with CRN {CRN} removed successfully.")

        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
        finally:
            cx.close()

      

    # Print the student's enrolled courses
    def print_courses(self):
        cx = sqlite3.connect("assignment3.db", timeout=5.0)
        cursor = cx.cursor()

        # Verify student exists
        cursor.execute("SELECT * FROM STUDENT WHERE ID = ? and NAME = ? and SURNAME = ?", 
                       (self.id, self.firstName, self.lastName))
        student = cursor.fetchone()
        if not student:
            print("Student not found.")
            cx.close()
            return []

        # Get enrolled courses
        cursor.execute("SELECT * FROM ENROLLMENT WHERE STUDENT_ID = ?", (self.id,))
        rows = cursor.fetchall()
        courses = []

        for row in rows:
            cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (row[1],))
            courses.append(cursor.fetchall())

        print("Courses enrolled:")
        for course in courses:
            print("Name:", course[0][1], "Department:", course[0][2],
                  "Time:", course[0][3], "Days:", course[0][4])

        cx.close()
        return rows