from os import remove
import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from user import User
import random # Added for password generation in add_user

# Database path for SQLite database connection
DB_PATH = "assignment3.db"

# --- Classes for Database Interaction (for Admin context) ---
# These classes encapsulate data when interacting with the database.
# They serve as temporary or permanent data holders for database rows,
# ensuring that data is handled as objects rather than raw tuples/lists.

class Course:
    """
    Represents a course with its various attributes such as CRN, title, department,
    time, days, semester, year, and credits. This class is used to create
    course objects from user input or database queries, facilitating
    object-oriented interaction with the COURSES table.
    """
    def __init__(self, crn, title, dept, time, days, semester, year, credits):
        """
        Initializes a Course object with the provided details.

        Args:
            crn (int): Course Reference Number, a unique identifier for the course.
            title (str): The official title of the course.
            dept (str): The department offering the course (e.g., "COMP", "MATH").
            time (str): The scheduled time for the course (e.g., "10:00 AM - 11:15 AM").
            days (str): The days of the week the course meets (e.g., "M/W/F", "T/R").
            semester (str): The semester in which the course is offered (e.g., "Fall", "Spring").
            year (int): The academic year the course is offered.
            credits (int): The number of credits the course is worth.
        """
        self.crn = crn
        self.title = title
        self.dept = dept
        self.time = time
        self.days = days
        self.semester = semester
        self.year = year
        self.credits = credits

    def __str__(self):
        """
        Returns a string representation of the Course object, suitable for printing.
        """
        return (f"CRN: {self.crn}, Title: {self.title}, Dept: {self.dept}, Time: {self.time}, "
                f"Days: {self.days}, Semester: {self.semester}, Year: {self.year}, Credits: {self.credits}")

class Student:
    """
    Represents a student in the system. Used for managing student data.
    """
    def __init__(self, s_id, name, surname, gradyear, major, email):
        self.id = s_id
        self.name = name
        self.surname = surname
        self.gradyear = gradyear
        self.major = major
        self.email = email

    def __str__(self):
        return (f"ID: {self.id}, Name: {self.name} {self.surname}, Grad Year: {self.gradyear}, "
                f"Major: {self.major}, Email: {self.email}")

class Instructor:
    """
    Represents an instructor in the system. Used for managing instructor data.
    """
    def __init__(self, i_id, name, surname, title, hireyear, dept, email):
        self.id = i_id
        self.name = name
        self.surname = surname
        self.title = title
        self.hireyear = hireyear
        self.dept = dept
        self.email = email

    def __str__(self):
        return (f"ID: {self.id}, Name: {self.name} {self.surname}, Title: {self.title}, "
                f"Hire Year: {self.hireyear}, Department: {self.dept}, Email: {self.email}")

class AdminUser:
    """
    Represents an administrator in the system. Used for managing admin user data.
    """
    def __init__(self, a_id, name, surname):
        self.id = a_id
        self.name = name
        self.surname = surname
    
    def __str__(self):
        return f"ID: {self.id}, Name: {self.name} {self.surname}"


class Admin(User):
    """
    The Admin class inherits from the User class and provides administrative functionalities
    for managing courses, users (students, instructors, admins), and course enrollments/assignments
    within the university system.
    """
    def __init__(self, in_firstName, in_lastName, in_id, cursor, cx):
        """
        Initializes an Admin object.

        Args:
            in_firstName (str): The first name of the admin.
            in_lastName (str): The last name of the admin.
            in_id (int): The ID of the admin.
            cursor (sqlite3.Cursor): The database cursor object for executing SQL queries.
            cx (sqlite3.Connection): The database connection object for committing changes.
        """
        super().__init__(in_firstName, in_lastName, in_id)
        self.cursor = cursor
        self.cx = cx

    def add_course(self, new_crn, new_title, new_dep, new_time, new_days, new_sem, new_year, credits):
        """
        Adds a new course to the COURSES table in the database.

        Args:
            new_crn (int): CRN for the new course.
            new_title (str): Title of the new course.
            new_dep (str): Department of the new course.
            new_time (str): Time of the new course.
            new_days (str): Days of the new course.
            new_sem (str): Semester of the new course.
            new_year (int): Year of the new course.
            credits (int): Credits for the new course.

        Returns:
            str: Success or error message.
        """
        try:
            # Check if CRN already exists
            self.cursor.execute("SELECT CRN FROM COURSES WHERE CRN = ?", (new_crn,))
            if self.cursor.fetchone():
                return f"Error: Course with CRN {new_crn} already exists."

            # Insert new course into the COURSES table
            self.cursor.execute(
                "INSERT INTO COURSES (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (new_crn, new_title, new_dep, new_time, new_days, new_sem, new_year, credits)
            )
            self.cx.commit()
            return f"Course '{new_title}' (CRN: {new_crn}) added successfully."
        except sqlite3.Error as e:
            self.cx.rollback()
            return f"SQL Error: {e}"

    def update_course(self, crn, field, new_value):
        """
        Updates a specific field for a given course in the COURSES table.

        Args:
            crn (int): CRN of the course to update.
            field (str): The field/column to update (e.g., 'TITLE', 'DEPARTMENT').
            new_value (str or int): The new value for the field.

        Returns:
            str: Success or error message.
        """
        try:
            # Validate if the course exists
            self.cursor.execute("SELECT CRN FROM COURSES WHERE CRN = ?", (crn,))
            if not self.cursor.fetchone():
                return f"Error: Course with CRN {crn} not found."

            # Basic validation for allowed fields to prevent SQL injection or invalid updates
            allowed_fields = ['TITLE', 'DEPARTMENT', 'TIME', 'DAYS', 'SEMESTER', 'YEAR', 'CREDITS']
            if field.upper() not in allowed_fields:
                return f"Error: Cannot update '{field}'. Allowed fields are: {', '.join(allowed_fields)}"

            # Update the specified field for the course
            query = f"UPDATE COURSES SET {field.upper()} = ? WHERE CRN = ?"
            self.cursor.execute(query, (new_value, crn))
            self.cx.commit()
            return f"Course CRN {crn} updated: {field} set to '{new_value}'."
        except sqlite3.Error as e:
            self.cx.rollback()
            return f"SQL Error: {e}"

    def remove_course(self, crn):
        """
        Removes a course from the COURSES table and associated entries in COURSE_TEACHER
        and Student_Schedule tables.

        Args:
            crn (int): CRN of the course to remove.

        Returns:
            str: Success or error message.
        """
        try:
            self.cursor.execute("SELECT CRN FROM COURSES WHERE CRN = ?", (crn,))
            if not self.cursor.fetchone():
                return f"Error: Course with CRN {crn} not found."

            # Remove from COURSES table
            self.cursor.execute("DELETE FROM COURSES WHERE CRN = ?", (crn,))
            
            # Remove from COURSE_TEACHER table (instructor assignments)
            self.cursor.execute("DELETE FROM COURSE_TEACHER WHERE CRN = ?", (crn,))

            # Remove CRN from all students' schedules in Student_Schedule table
            self.cursor.execute("PRAGMA table_info(Student_Schedule)")
            columns = [col[1] for col in self.cursor.fetchall()]
            
            # Find all CRN columns in Student_Schedule
            crn_columns = [col for col in columns if col.startswith('CRN')]
            
            for crn_col in crn_columns:
                self.cursor.execute(f"UPDATE Student_Schedule SET {crn_col} = NULL WHERE {crn_col} = ?", (crn,))

            self.cx.commit()
            return f"Course CRN {crn} and all associated data removed successfully."
        except sqlite3.Error as e:
            self.cx.rollback()
            return f"SQL Error: {e}"

    def add_user(self, user_type, user_data):
        """
        Adds a new user (student, instructor, or admin) to the respective table
        and creates a login entry.

        Args:
            user_type (str): Type of user ('student', 'instructor', 'admin').
            user_data (dict): Dictionary containing user details.
                              For student: id, name, surname, gradyear, major, email.
                              For instructor: id, name, surname, title, hireyear, dept, email.
                              For admin: id, name, surname, title, office, email.

        Returns:
            str: Success or error message.
        """
        try:
            user_id = user_data['id']
            # Check if user ID already exists in LOGIN table
            self.cursor.execute("SELECT ID FROM LOGIN WHERE ID = ?", (user_id,))
            if self.cursor.fetchone():
                return f"Error: User with ID {user_id} already exists in login system."

            # Generate a password (you might want a more sophisticated password generation/handling)
            password = str(random.randint(1000, 9999)) # Example: 4-digit numeric password

            # Insert into LOGIN table
            self.cursor.execute("INSERT INTO LOGIN (ID, EMAIL, PASSWORD) VALUES (?, ?, ?)",
                                (user_id, user_data['email'], password))

            # Insert into specific user table
            if user_type.lower() == 'student':
                self.cursor.execute(
                    "INSERT INTO STUDENT (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_data['id'], user_data['name'], user_data['surname'], user_data['gradyear'], user_data['major'], user_data['email'])
                )
                message = f"Student '{user_data['name']} {user_data['surname']}' (ID: {user_data['id']}) added successfully."
            elif user_type.lower() == 'instructor':
                self.cursor.execute(
                    "INSERT INTO INSTRUCTOR (ID, NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (user_data['id'], user_data['name'], user_data['surname'], user_data['title'], user_data['hireyear'], user_data['dept'], user_data['email'])
                )
                message = f"Instructor '{user_data['name']} {user_data['surname']}' (ID: {user_data['id']}) added successfully."
            elif user_type.lower() == 'admin':
                self.cursor.execute(
                    "INSERT INTO ADMIN (ID, NAME, SURNAME, TITLE, OFFICE, EMAIL) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_data['id'], user_data['name'], user_data['surname'], user_data['title'], user_data['office'], user_data['email'])
                )
                message = f"Admin '{user_data['name']} {user_data['surname']}' (ID: {user_data['id']}) added successfully."
            else:
                self.cx.rollback()
                return "Error: Invalid user type specified."
            
            self.cx.commit()
            return f"{message}\nGenerated Password: {password}"
        except sqlite3.Error as e:
            self.cx.rollback()
            return f"SQL Error: {e}"
        except KeyError as e:
            self.cx.rollback()
            return f"Error: Missing data for user type '{user_type}'. Missing field: {e}"

    def remove_user(self, user_id):
        """
        Removes a user (student, instructor, or admin) from the system.
        This includes removing them from the LOGIN table and their specific table.
        For instructors, it also unassigns them from courses.
        For students, it removes them from courses they are enrolled in.

        Args:
            user_id (int): The ID of the user to remove.

        Returns:
            str: Success or error message.
        """
        try:
            # Check if user exists in LOGIN table
            self.cursor.execute("SELECT ID FROM LOGIN WHERE ID = ?", (user_id,))
            if not self.cursor.fetchone():
                return f"Error: User with ID {user_id} not found."

            # Determine user type to delete from the correct table
            user_type_prefix = str(user_id)[0]
            if user_type_prefix == '1': # Student
                # Remove from Student_Schedule table
                self.cursor.execute("PRAGMA table_info(Student_Schedule)")
                col_names = [desc[1] for desc in self.cursor.fetchall()]
                name_column = next((col for col in col_names if col.lower() in ['studentname', 'name', 'fullname', 'student', 'student name']), None)
                if name_column:
                     # Get student name to remove their row from Student_Schedule
                    self.cursor.execute("SELECT NAME, SURNAME FROM STUDENT WHERE ID = ?", (user_id,))
                    student_name_data = self.cursor.fetchone()
                    if student_name_data:
                        full_name = f"{student_name_data[0]} {student_name_data[1]}"
                        self.cursor.execute(f"DELETE FROM Student_Schedule WHERE \"{name_column}\" = ?", (full_name,))

                self.cursor.execute("DELETE FROM STUDENT WHERE ID = ?", (user_id,))
                message = f"Student with ID {user_id} removed successfully."
            elif user_type_prefix == '2': # Instructor
                # Remove from COURSE_TEACHER table (unassign from courses)
                self.cursor.execute("SELECT NAME, SURNAME FROM INSTRUCTOR WHERE ID = ?", (user_id,))
                instructor_name_data = self.cursor.fetchone()
                if instructor_name_data:
                    self.cursor.execute("DELETE FROM COURSE_TEACHER WHERE INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ?", 
                                        (instructor_name_data[0], instructor_name_data[1]))
                self.cursor.execute("DELETE FROM INSTRUCTOR WHERE ID = ?", (user_id,))
                message = f"Instructor with ID {user_id} removed successfully."
            elif user_type_prefix == '3': # Admin
                self.cursor.execute("DELETE FROM ADMIN WHERE ID = ?", (user_id,))
                message = f"Admin with ID {user_id} removed successfully."
            else:
                return "Error: Invalid user ID type."

            # Remove from LOGIN table (final step)
            self.cursor.execute("DELETE FROM LOGIN WHERE ID = ?", (user_id,))
            self.cx.commit()
            return message
        except sqlite3.Error as e:
            self.cx.rollback()
            return f"SQL Error: {e}"

    def assign_instructor_to_course(self, instructor_id, crn):
        """
        Assigns an instructor to teach a specific course in the COURSE_TEACHER table.

        Args:
            instructor_id (int): ID of the instructor.
            crn (int): CRN of the course.

        Returns:
            str: Success or error message.
        """
        try:
            # Check if instructor exists
            self.cursor.execute("SELECT NAME, SURNAME FROM INSTRUCTOR WHERE ID = ?", (instructor_id,))
            instructor_data = self.cursor.fetchone()
            if not instructor_data:
                return f"Error: Instructor with ID {instructor_id} not found."
            
            # Check if course exists
            self.cursor.execute("SELECT TITLE, DEPARTMENT, TIME, DAYS, SEMESTER FROM COURSES WHERE CRN = ?", (crn,))
            course_data = self.cursor.fetchone()
            if not course_data:
                return f"Error: Course with CRN {crn} not found."
            
            # Check if instructor is already assigned to this course
            self.cursor.execute("SELECT * FROM COURSE_TEACHER WHERE CRN = ? AND INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ?",
                                (crn, instructor_data[0], instructor_data[1]))
            if self.cursor.fetchone():
                return f"Error: Instructor {instructor_data[0]} {instructor_data[1]} is already assigned to CRN {crn}."

            # Insert assignment into COURSE_TEACHER table
            self.cursor.execute(
                "INSERT INTO COURSE_TEACHER (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, INSTRUCTOR_NAME, INSTRUCTOR_SURNAME) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (crn, course_data[0], course_data[1], course_data[2], course_data[3], course_data[4], instructor_data[0], instructor_data[1])
            )
            self.cx.commit()
            return f"Instructor {instructor_data[0]} {instructor_data[1]} assigned to CRN {crn} successfully."
        except sqlite3.Error as e:
            self.cx.rollback()
            return f"SQL Error: {e}"

    def unassign_instructor_from_course(self, instructor_id, crn):
        """
        Unassigns an instructor from a course in the COURSE_TEACHER table.

        Args:
            instructor_id (int): ID of the instructor.
            crn (int): CRN of the course.

        Returns:
            str: Success or error message.
        """
        try:
            # Get instructor name
            self.cursor.execute("SELECT NAME, SURNAME FROM INSTRUCTOR WHERE ID = ?", (instructor_id,))
            instructor_data = self.cursor.fetchone()
            if not instructor_data:
                return f"Error: Instructor with ID {instructor_id} not found."

            # Check if the assignment exists
            self.cursor.execute("SELECT * FROM COURSE_TEACHER WHERE CRN = ? AND INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ?",
                                (crn, instructor_data[0], instructor_data[1]))
            if not self.cursor.fetchone():
                return f"Error: Instructor {instructor_data[0]} {instructor_data[1]} is not assigned to CRN {crn}."

            # Delete the assignment
            self.cursor.execute("DELETE FROM COURSE_TEACHER WHERE CRN = ? AND INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ?",
                                (crn, instructor_data[0], instructor_data[1]))
            self.cx.commit()
            return f"Instructor {instructor_data[0]} {instructor_data[1]} unassigned from CRN {crn} successfully."
        except sqlite3.Error as e:
            self.cx.rollback()
            return f"SQL Error: {e}"

    def add_student_to_course(self, student_id, crn):
        """
        Adds a student to a course in the Student_Schedule table.
        Each student can enroll in up to 4 courses (CRN1-CRN4).

        Args:
            student_id (int): ID of the student.
            crn (int): CRN of the course to enroll in.

        Returns:
            str: Success or error message.
        """
        try:
            # Check if student exists and get their name
            self.cursor.execute("SELECT NAME, SURNAME FROM STUDENT WHERE ID = ?", (student_id,))
            student_data = self.cursor.fetchone()
            if not student_data:
                return f"Error: Student with ID {student_id} not found."
            student_full_name = f"{student_data[0]} {student_data[1]}"

            # Check if course exists and retrieve its details using the correct 'DAYS' column name
            self.cursor.execute("SELECT Title, DAYS, TIME FROM COURSES WHERE CRN = ?", (crn,))
            course_data = self.cursor.fetchone()
            if not course_data:
                return f"Error: Course with CRN {crn} not found."
        
            course_title, course_days, course_time = course_data

            # Check if student is already in Student_Schedule or needs a new entry
            self.cursor.execute("SELECT CRN1, CRN2, CRN3, CRN4 FROM Student_Schedule WHERE StudentName = ?", (student_full_name,))
            student_schedule = self.cursor.fetchone()

            if student_schedule:
                # Check for available slot and if already enrolled
                for i in range(4): 
                    # Check for existing enrollment by CRN
                    if student_schedule[i] == crn:
                        return f"Error: Student {student_full_name} is already enrolled in CRN {crn}."
                
                    # Found an empty slot based on CRN being NULL
                    if student_schedule[i] is None:
                        # Enroll student with full details, updating the correct columns
                        update_query = f"""
                            UPDATE Student_Schedule 
                            SET CRN{i+1} = ?, COURSE{i+1} = ?, DOW{i+1} = ?, TIME{i+1} = ? 
                            WHERE StudentName = ?
                        """
                        self.cursor.execute(update_query, (crn, course_title, course_days, course_time, student_full_name))
                        self.cx.commit()
                        return f"Student {student_full_name} enrolled in CRN {crn} successfully."
            
                return f"Error: Student {student_full_name} is already enrolled in 4 courses and cannot add more."
            else:
                # New student entry with full course details
                self.cursor.execute("""
                    INSERT INTO Student_Schedule (StudentName, CRN1, COURSE1, DOW1, TIME1) 
                    VALUES (?, ?, ?, ?, ?)
                """, (student_full_name, crn, course_title, course_days, course_time))
                self.cx.commit()
                return f"Student {student_full_name} enrolled in CRN {crn} successfully (new schedule created)."
        except sqlite3.Error as e:
            self.cx.rollback()
            return f"SQL Error: {e}"

    def remove_student_from_course(self, crn, student_id):
        """
        Removes a student from a specific course in the Student_Schedule table.

        Args:
            crn (int): CRN of the course to remove the student from.
            student_id (int): ID of the student to remove.

        Returns:
            str: Success or error message.
        """
        try:
            # Check if student exists and get name
            self.cursor.execute("SELECT NAME, SURNAME FROM STUDENT WHERE ID = ?", (student_id,))
            student_data = self.cursor.fetchone()
            if not student_data:
                return f"Error: Student with ID {student_id} not found."
            student_full_name = f"{student_data[0]} {student_data[1]}"

            # Find student's schedule entry
            self.cursor.execute("SELECT CRN1, CRN2, CRN3, CRN4 FROM Student_Schedule WHERE StudentName = ?", (student_full_name,))
            schedule = self.cursor.fetchone()

            if schedule:
                # Check if the student is enrolled in the given CRN
                found_and_removed = False
                for i in range(5): # Iterate through CRN1 to CRN4 columns
                    if schedule[i] == crn:
                        # Set the CRN slot to NULL
                        self.cursor.execute(f"""
                        UPDATE Student_Schedule 
                        SET CRN{i+1} = NULL, COURSE{i+1} = NULL, DOW{i+1} = NULL, TIME{i+1} = NULL
                        WHERE StudentName = ?
                    """, (student_full_name,))
                        found_and_removed = True
                        break
                
                if found_and_removed:
                    self.cx.commit()
                    return f"Student {student_full_name} removed from CRN {crn} successfully."
                else:
                    return f"Error: Student {student_full_name} is not enrolled in CRN {crn}."
            else:
                return f"Error: Student {student_full_name} has no schedule entries."
        except sqlite3.Error as e:
            self.cx.rollback()
            return f"SQL Error: {e}"

    def print_all_users(self, user_type):
        """
        Retrieves and formats a string of all users of a specific type.

        Args:
            user_type (str): The type of user to print ('student', 'instructor', 'admin').

        Returns:
            str: A formatted string of user information or an error message.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            if user_type.lower() == 'student':
                cursor.execute("SELECT ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL FROM STUDENT")
                rows = cursor.fetchall()
                if rows:
                    users_str = "All Students:\n"
                    for row in rows:
                        student_obj = Student(row[0], row[1], row[2], row[3], row[4], row[5])
                        users_str += str(student_obj) + "\n\n" # Added extra newline
                    return users_str
                else:
                    return "No students found."
            elif user_type.lower() == 'instructor':
                cursor.execute("SELECT ID, NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL FROM INSTRUCTOR")
                rows = cursor.fetchall()
                if rows:
                    users_str = "All Instructors:\n"
                    for row in rows:
                        instructor_obj = Instructor(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                        users_str += str(instructor_obj) + "\n\n" # Added extra newline
                    return users_str
                else:
                    return "No instructors found."
            elif user_type.lower() == 'admin':
                cursor.execute("SELECT ID, NAME, SURNAME FROM ADMIN") # Assuming ADMIN table structure
                rows = cursor.fetchall()
                if rows:
                    users_str = "All Admins:\n"
                    for row in rows:
                        admin_obj = AdminUser(row[0], row[1], row[2]) # Use AdminUser for consistency
                        users_str += str(admin_obj) + "\n\n" # Added extra newline
                    return users_str
                else:
                    return "No admins found."
            else:
                return "Invalid user type specified. Choose 'student', 'instructor', or 'admin'."
        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        finally:
            conn.close()

    def print_all_courses(self):
        """
        Retrieves all available courses from the COURSES table in the database
        and formats them into a readable string with an empty line between courses.

        Returns:
            str: A formatted string listing all courses, or a message if no courses are found.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            sql_command = "SELECT CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS FROM COURSES"
            cursor.execute(sql_command)
            rows = cursor.fetchall()

            if rows:
                result_str = "All Available Courses:\n"
                for row in rows:
                    # Instantiate a Course object for each row for consistent formatting
                    course_obj = Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    result_str += str(course_obj) + "\n\n" # Added extra newline here
                return result_str
            else:
                return "No courses found in the system."
        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        finally:
            conn.close()

    def print_all_course_assignments(self):
        """
        Retrieves all course assignments (instructor to course) from the COURSE_TEACHER table.

        Returns:
            str: A formatted string listing all course assignments, or a message if none are found.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT CRN, TITLE, INSTRUCTOR_NAME, INSTRUCTOR_SURNAME FROM COURSE_TEACHER")
            rows = cursor.fetchall()
            if rows:
                assignments_str = "All Course Assignments:\n"
                for row in rows:
                    assignments_str += f"CRN: {row[0]}, Course: {row[1]}, Instructor: {row[2]} {row[3]}\n\n" # Added extra newline
                return assignments_str
            else:
                return "No course assignments found."
        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        finally:
            conn.close()

    def print_all_student_schedules(self):
        """
        Retrieves and formats all student schedules from the Student_Schedule table.

        Returns:
            str: A formatted string of all student schedules or a message if none are found.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT StudentName, CRN1, CRN2, CRN3, CRN4 FROM Student_Schedule")
            rows = cursor.fetchall()
            if rows:
                schedules_str = "All Student Schedules:\n"
                for row in rows:
                    student_name = row[0]
                    courses = [crn for crn in row[1:] if crn is not None]
                    schedules_str += f"Student: {student_name}, Enrolled CRNs: {', '.join(map(str, courses)) if courses else 'None'}\n\n" # Added extra newline
                return schedules_str
            else:
                return "No student schedules found."
        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        finally:
            conn.close()


class AdminMenu(tk.Toplevel):
    """
    Implements the graphical user interface (GUI) for the administrator menu.
    This class handles displaying administrative options and managing user input
    to perform various database operations via the Admin class.
    It now includes a scrollbar for better usability with many buttons,
    and ensures buttons are horizontally centered.
    """
    def __init__(self, master, admin_obj):
        """
        Initializes the AdminMenu GUI window with a scrollable frame.
        
        Args:
            master: The parent Tkinter window (e.g., the login window).
            admin_obj: An instance of the Admin class.
        """
        super().__init__(master)
        self.master = master
        self.admin = admin_obj
        self.title(f"Admin Menu - {self.admin.firstName} {self.admin.lastName}")
        self.geometry("800x600") # Set a default larger size for the window

        # Create a main frame to hold the canvas and scrollbar
        self.main_container = tk.Frame(self)
        self.main_container.pack(fill="both", expand=True)

        # Create a Canvas widget
        self.canvas = tk.Canvas(self.main_container)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a Scrollbar and link it to the canvas
        self.scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a frame inside the canvas to hold the actual content (buttons, labels etc.)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        # Create a window in the canvas to hold the scrollable_frame
        # anchor="nw" is correct for positioning the frame at the top-left of the scrollable area
        self.canvas_window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bind the scrollable_frame's size changes to update the canvas scroll region
        # This makes the scrollbar appear/disappear based on content height
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        # Bind the canvas's <Configure> event to resize the inner frame's width
        # to match the canvas's width. This is crucial for horizontal centering.
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        # Enable mousewheel scrolling (for Windows/Linux)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # For macOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        self.create_widgets()

    def _on_mousewheel(self, event):
        """Handles mouse wheel scrolling."""
        # For Windows/Linux, event.delta is typically +/- 120 per scroll "click"
        if event.num == 4: # macOS scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5: # macOS scroll down
            self.canvas.yview_scroll(1, "units")
        else: # Windows/Linux
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_canvas_configure(self, event):
        """
        Resizes the scrollable_frame's width to match the canvas's width,
        and updates the canvas's scrollregion.
        This ensures that content within the scrollable_frame is centered
        horizontally within the canvas's visible area if packed without 'side'/'fill'.
        """
        canvas_width = event.width
        # Update the width of the window created by the canvas
        self.canvas.itemconfig(self.canvas_window_id, width=canvas_width)
        
        # Additionally, explicitly configure the width of the scrollable_frame itself
        # This helps ensure `pack()` within the frame centers content correctly.
        self.scrollable_frame.update_idletasks() # Important: ensures geometry calculations are up-to-date
        self.scrollable_frame.config(width=canvas_width)

        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_widgets(self):
        """
        Creates and arranges the GUI widgets for the admin main menu.
        All widgets are placed within the `scrollable_frame`.
        """
        # Clear any existing widgets from the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        welcome_label = tk.Label(self.scrollable_frame, text=f"Welcome, {self.admin.firstName} {self.admin.lastName}!", font=("Arial", 16, "bold"))
        welcome_label.pack(pady=10)

        # Course Management Buttons
        tk.Label(self.scrollable_frame, text="Course Management", font=("Arial", 14, "underline")).pack(pady=5)
        btn_add_course = tk.Button(self.scrollable_frame, text="Add Course", command=self.show_add_course_menu, width=40, height=2)
        btn_add_course.pack(pady=2)
        btn_update_course = tk.Button(self.scrollable_frame, text="Update Course", command=self.show_update_course_menu, width=40, height=2)
        btn_update_course.pack(pady=2)
        btn_remove_course = tk.Button(self.scrollable_frame, text="Remove Course", command=self.show_remove_course_menu, width=40, height=2)
        btn_remove_course.pack(pady=2)
        btn_print_all_courses = tk.Button(self.scrollable_frame, text="Print All Courses", command=self.display_all_courses, width=40, height=2)
        btn_print_all_courses.pack(pady=2)

        # User Management Buttons
        tk.Label(self.scrollable_frame, text="User Management", font=("Arial", 14, "underline")).pack(pady=10)
        btn_add_user = tk.Button(self.scrollable_frame, text="Add User", command=self.show_add_user_menu, width=40, height=2)
        btn_add_user.pack(pady=2)
        btn_remove_user = tk.Button(self.scrollable_frame, text="Remove User", command=self.show_remove_user_menu, width=40, height=2)
        btn_remove_user.pack(pady=2)
        btn_print_all_students = tk.Button(self.scrollable_frame, text="Print All Students", command=lambda: self.display_all_users('student'), width=40, height=2)
        btn_print_all_students.pack(pady=2)
        btn_print_all_instructors = tk.Button(self.scrollable_frame, text="Print All Instructors", command=lambda: self.display_all_users('instructor'), width=40, height=2)
        btn_print_all_instructors.pack(pady=2)
        btn_print_all_admins = tk.Button(self.scrollable_frame, text="Print All Admins", command=lambda: self.display_all_users('admin'), width=40, height=2)
        btn_print_all_admins.pack(pady=2)

        # Assignment Management Buttons
        tk.Label(self.scrollable_frame, text="Enrollment/Assignment Management", font=("Arial", 14, "underline")).pack(pady=10)
        btn_assign_instructor = tk.Button(self.scrollable_frame, text="Assign Instructor to Course", command=self.show_assign_instructor_menu, width=40, height=2)
        btn_assign_instructor.pack(pady=2)
        btn_unassign_instructor = tk.Button(self.scrollable_frame, text="Unassign Instructor from Course", command=self.show_unassign_instructor_menu, width=40, height=2)
        btn_unassign_instructor.pack(pady=2)
        btn_add_student_to_course = tk.Button(self.scrollable_frame, text="Add Student to Course", command=self.show_add_student_to_course_menu, width=40, height=2)
        btn_add_student_to_course.pack(pady=2)
        btn_remove_student_from_course = tk.Button(self.scrollable_frame, text="Remove Student from Course", command=self.show_remove_student_from_course_menu, width=40, height=2)
        btn_remove_student_from_course.pack(pady=2)
        btn_print_all_assignments = tk.Button(self.scrollable_frame, text="Print All Course Assignments", command=self.display_all_course_assignments, width=40, height=2)
        btn_print_all_assignments.pack(pady=2)
        btn_print_all_student_schedules = tk.Button(self.scrollable_frame, text="Print All Student Schedules", command=self.display_all_student_schedules, width=40, height=2)
        btn_print_all_student_schedules.pack(pady=2)

        # Logout Button
        btn_logout = tk.Button(self.scrollable_frame, text="Logout", command=self.logout, width=40, height=2, bg="red", fg="white")
        btn_logout.pack(pady=20)

    def clear_scrollable_frame(self):
        """
        Clears all widgets from the `scrollable_frame` to switch views.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    # --- Course Management Menus ---
    def show_add_course_menu(self):
        """Displays menu for adding a new course."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="Add New Course", font=("Arial", 14, "bold")).pack(pady=10)

        fields = [
            ("CRN (int):", "crn_entry"), ("Title (str):", "title_entry"), ("Department (str):", "dep_entry"),
            ("Time (str, HH:MM AM/PM - HH:MM AM/PM):", "time_entry"), ("Days (str, M/T/W/R/F):", "days_entry"),
            ("Semester (str, e.g., Fall):", "sem_entry"), ("Year (int):", "year_entry"), ("Credits (int):", "credits_entry")
        ]
        self.entries = {}
        for text, entry_name in fields:
            tk.Label(self.scrollable_frame, text=text).pack(anchor="w", padx=10)
            entry = tk.Entry(self.scrollable_frame, width=50)
            entry.pack(pady=2, padx=10)
            self.entries[entry_name] = entry

        tk.Button(self.scrollable_frame, text="Add Course", command=self.perform_add_course, width=20).pack(pady=10)
        self.result_label = tk.Label(self.scrollable_frame, text="", wraplength=400)
        self.result_label.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    def perform_add_course(self):
        """Retrieves data from add course form and calls admin.add_course."""
        try:
            new_crn = int(self.entries["crn_entry"].get())
            new_title = self.entries["title_entry"].get()
            new_dep = self.entries["dep_entry"].get()
            new_time = self.entries["time_entry"].get()
            new_days = self.entries["days_entry"].get()
            new_sem = self.entries["sem_entry"].get()
            new_year = int(self.entries["year_entry"].get())
            credits = int(self.entries["credits_entry"].get())

            if not all([new_title, new_dep, new_time, new_days, new_sem]):
                messagebox.showwarning("Input Error", "Please fill in all text fields.")
                return

            result = self.admin.add_course(new_crn, new_title, new_dep, new_time, new_days, new_sem, new_year, credits)
            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Input Error", "CRN, Year, and Credits must be numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def show_update_course_menu(self):
        """Displays menu for updating an existing course."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="Update Course", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.scrollable_frame, text="Course CRN:").pack(anchor="w", padx=10)
        self.update_crn_entry = tk.Entry(self.scrollable_frame, width=20)
        self.update_crn_entry.pack(pady=2, padx=10)

        tk.Label(self.scrollable_frame, text="Field to Update (e.g., TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS):").pack(anchor="w", padx=10)
        self.update_field_entry = tk.Entry(self.scrollable_frame, width=30)
        self.update_field_entry.pack(pady=2, padx=10)

        tk.Label(self.scrollable_frame, text="New Value:").pack(anchor="w", padx=10)
        self.update_value_entry = tk.Entry(self.scrollable_frame, width=50)
        self.update_value_entry.pack(pady=2, padx=10)

        tk.Button(self.scrollable_frame, text="Update Course", command=self.perform_update_course, width=20).pack(pady=10)
        self.result_label = tk.Label(self.scrollable_frame, text="", wraplength=400)
        self.result_label.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    def perform_update_course(self):
        """Retrieves data from update course form and calls admin.update_course."""
        try:
            crn = int(self.update_crn_entry.get())
            field = self.update_field_entry.get().strip()
            new_value = self.update_value_entry.get().strip()

            if not all([field, new_value]):
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            # Special handling for integer fields like YEAR and CREDITS
            if field.upper() in ['YEAR', 'CREDITS']:
                try:
                    new_value = int(new_value)
                except ValueError:
                    messagebox.showerror("Input Error", f"'{field}' must be a number.")
                    return

            result = self.admin.update_course(crn, field, new_value)
            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Input Error", "CRN must be a number.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def show_remove_course_menu(self):
        """Displays menu for removing a course."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="Remove Course", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.scrollable_frame, text="Course CRN:").pack(anchor="w", padx=10)
        self.remove_crn_entry = tk.Entry(self.scrollable_frame, width=20)
        self.remove_crn_entry.pack(pady=5, padx=10)

        tk.Button(self.scrollable_frame, text="Remove Course", command=self.perform_remove_course, width=20).pack(pady=10)
        self.result_label = tk.Label(self.scrollable_frame, text="", wraplength=400)
        self.result_label.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    def perform_remove_course(self):
        """Retrieves CRN from remove course form and calls admin.remove_course."""
        try:
            crn = int(self.remove_crn_entry.get())
            result = self.admin.remove_course(crn)
            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Input Error", "CRN must be a number.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def display_all_courses(self):
        """Displays all courses in a scrolled text area."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="All Courses", font=("Arial", 14, "bold")).pack(pady=10)
        result_text_widget = scrolledtext.ScrolledText(self.scrollable_frame, width=80, height=20, wrap=tk.WORD)
        result_text_widget.pack(pady=10)
        result_text_widget.insert(tk.END, self.admin.print_all_courses())
        result_text_widget.config(state=tk.DISABLED)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    # --- User Management Menus ---
    def show_add_user_menu(self):
        """Displays menu for adding a new user (student, instructor, or admin)."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="Add New User", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.scrollable_frame, text="User Type:").pack(anchor="w", padx=10)
        self.user_type_var = tk.StringVar(self.scrollable_frame)
        self.user_type_var.set("student") # Default
        user_type_option = tk.OptionMenu(self.scrollable_frame, self.user_type_var, "student", "instructor", "admin", command=self.on_user_type_change)
        user_type_option.pack(pady=5, padx=10)

        # Frame to hold dynamic fields based on user type
        self.dynamic_fields_frame = tk.Frame(self.scrollable_frame)
        self.dynamic_fields_frame.pack(pady=10)
        self.entries = {} # Store entries for current user type

        self.on_user_type_change("student") # Initial display for student

        tk.Button(self.scrollable_frame, text="Add User", command=self.perform_add_user, width=20).pack(pady=10)
        self.result_label = tk.Label(self.scrollable_frame, text="", wraplength=400)
        self.result_label.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    def on_user_type_change(self, user_type):
        """Dynamically updates fields when user type selection changes."""
        for widget in self.dynamic_fields_frame.winfo_children():
            widget.destroy()
        self.entries = {}

        common_fields = [
            ("ID (int):", "id_entry"), ("First Name (str):", "name_entry"), 
            ("Last Name (str):", "surname_entry"), ("Email (str):", "email_entry")
        ]
        
        type_specific_fields = {
            "student": [("Graduation Year (int):", "gradyear_entry"), ("Major (str):", "major_entry")],
            "instructor": [("Title (str):", "title_entry"), ("Hire Year (int):", "hireyear_entry"), ("Department (str):", "dept_entry")],
            "admin": [("Title (str):", "title_entry"), ("Office (str):", "office_entry")]
        }

        all_fields = common_fields + type_specific_fields.get(user_type, [])

        for text, entry_name in all_fields:
            tk.Label(self.dynamic_fields_frame, text=text).pack(anchor="w", padx=10)
            entry = tk.Entry(self.dynamic_fields_frame, width=50)
            entry.pack(pady=2, padx=10)
            self.entries[entry_name] = entry
        
        # Update canvas scroll region after adding/removing fields
        self.canvas.update_idletasks() # Ensure widgets are rendered before bbox calculation
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def perform_add_user(self):
        """Retrieves data from add user form and calls admin.add_user."""
        user_type = self.user_type_var.get()
        user_data = {}
        try:
            user_data['id'] = int(self.entries["id_entry"].get())
            user_data['name'] = self.entries["name_entry"].get()
            user_data['surname'] = self.entries["surname_entry"].get()
            user_data['email'] = self.entries["email_entry"].get()

            if user_type == "student":
                user_data['gradyear'] = int(self.entries["gradyear_entry"].get())
                user_data['major'] = self.entries["major_entry"].get()
            elif user_type == "instructor":
                user_data['title'] = self.entries["title_entry"].get()
                user_data['hireyear'] = int(self.entries["hireyear_entry"].get())
                user_data['dept'] = self.entries["dept_entry"].get()
            elif user_type == "admin":
                user_data['title'] = self.entries["title_entry"].get()
                user_data['office'] = self.entries["office_entry"].get()
            
            # Basic validation for non-empty string fields
            for key, value in user_data.items():
                if isinstance(value, str) and not value.strip():
                    messagebox.showwarning("Input Error", f"Please fill in all text fields for {key}.")
                    return

            result = self.admin.add_user(user_type, user_data)
            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Input Error", "ID, Graduation Year, Hire Year must be numbers.")
        except KeyError as e:
            messagebox.showerror("Input Error", f"Missing field: {e}. Please ensure all required fields for {user_type} are filled.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def show_remove_user_menu(self):
        """Displays menu for removing a user."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="Remove User", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.scrollable_frame, text="User ID:").pack(anchor="w", padx=10)
        self.remove_user_id_entry = tk.Entry(self.scrollable_frame, width=20)
        self.remove_user_id_entry.pack(pady=5, padx=10)

        tk.Button(self.scrollable_frame, text="Remove User", command=self.perform_remove_user, width=20).pack(pady=10)
        self.result_label = tk.Label(self.scrollable_frame, text="", wraplength=400)
        self.result_label.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    def perform_remove_user(self):
        """Retrieves user ID from remove user form and calls admin.remove_user."""
        try:
            user_id = int(self.remove_user_id_entry.get())
            result = self.admin.remove_user(user_id)
            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Input Error", "User ID must be a number.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def display_all_users(self, user_type):
        """Displays all users of a specific type in a scrolled text area."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text=f"All {user_type.capitalize()}s", font=("Arial", 14, "bold")).pack(pady=10)
        result_text_widget = scrolledtext.ScrolledText(self.scrollable_frame, width=80, height=20, wrap=tk.WORD)
        result_text_widget.pack(pady=10)
        result_text_widget.insert(tk.END, self.admin.print_all_users(user_type))
        result_text_widget.config(state=tk.DISABLED)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    # --- Assignment Management Menus ---
    def show_assign_instructor_menu(self):
        """Displays menu for assigning an instructor to a course."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="Assign Instructor to Course", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.scrollable_frame, text="Instructor ID:").pack(anchor="w", padx=10)
        self.assign_instructor_id_entry = tk.Entry(self.scrollable_frame, width=20)
        self.assign_instructor_id_entry.pack(pady=2, padx=10)

        tk.Label(self.scrollable_frame, text="Course CRN:").pack(anchor="w", padx=10)
        self.assign_crn_entry = tk.Entry(self.scrollable_frame, width=20)
        self.assign_crn_entry.pack(pady=2, padx=10)

        tk.Button(self.scrollable_frame, text="Assign Instructor", command=self.perform_assign_instructor, width=20).pack(pady=10)
        self.result_label = tk.Label(self.scrollable_frame, text="", wraplength=400)
        self.result_label.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    def perform_assign_instructor(self):
        """Retrieves data from assign instructor form and calls admin.assign_instructor_to_course."""
        try:
            instructor_id = int(self.assign_instructor_id_entry.get())
            crn = int(self.assign_crn_entry.get())
            result = self.admin.assign_instructor_to_course(instructor_id, crn)
            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Input Error", "Instructor ID and CRN must be numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def show_unassign_instructor_menu(self):
        """Displays menu for unassigning an instructor from a course."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="Unassign Instructor from Course", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.scrollable_frame, text="Instructor ID:").pack(anchor="w", padx=10)
        self.unassign_instructor_id_entry = tk.Entry(self.scrollable_frame, width=20)
        self.unassign_instructor_id_entry.pack(pady=2, padx=10)

        tk.Label(self.scrollable_frame, text="Course CRN:").pack(anchor="w", padx=10)
        self.unassign_crn_entry = tk.Entry(self.scrollable_frame, width=20)
        self.unassign_crn_entry.pack(pady=2, padx=10)

        tk.Button(self.scrollable_frame, text="Unassign Instructor", command=self.perform_unassign_instructor, width=20).pack(pady=10)
        self.result_label = tk.Label(self.scrollable_frame, text="", wraplength=400)
        self.result_label.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    def perform_unassign_instructor(self):
        """Retrieves data from unassign instructor form and calls admin.unassign_instructor_from_course."""
        try:
            instructor_id = int(self.unassign_instructor_id_entry.get())
            crn = int(self.unassign_crn_entry.get())
            result = self.admin.unassign_instructor_from_course(instructor_id, crn)
            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Input Error", "Instructor ID and CRN must be numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def show_add_student_to_course_menu(self):
        """Displays menu for adding a student to a course."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="Add Student to Course", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.scrollable_frame, text="Student ID:").pack(anchor="w", padx=10)
        self.enroll_student_id_entry = tk.Entry(self.scrollable_frame, width=20)
        self.enroll_student_id_entry.pack(pady=2, padx=10)

        tk.Label(self.scrollable_frame, text="Course CRN:").pack(anchor="w", padx=10)
        self.enroll_crn_entry = tk.Entry(self.scrollable_frame, width=20)
        self.enroll_crn_entry.pack(pady=2, padx=10)

        tk.Button(self.scrollable_frame, text="Enroll Student", command=self.perform_add_student_to_course, width=20).pack(pady=10)
        self.result_label = tk.Label(self.scrollable_frame, text="", wraplength=400)
        self.result_label.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    def perform_add_student_to_course(self):
        """Retrieves data from add student to course form and calls admin.add_student_to_course."""
        try:
            student_id = int(self.enroll_student_id_entry.get())
            crn = int(self.enroll_crn_entry.get())
            result = self.admin.add_student_to_course(student_id, crn)
            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Input Error", "Student ID and CRN must be numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def show_remove_student_from_course_menu(self):
        """Displays menu for removing a student from a course."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="Remove Student from Course", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.scrollable_frame, text="Student ID:").pack(anchor="w", padx=10)
        self.unenroll_student_id_entry = tk.Entry(self.scrollable_frame, width=20)
        self.unenroll_student_id_entry.pack(pady=2, padx=10)

        tk.Label(self.scrollable_frame, text="Course CRN:").pack(anchor="w", padx=10)
        self.unenroll_crn_entry = tk.Entry(self.scrollable_frame, width=20)
        self.unenroll_crn_entry.pack(pady=2, padx=10)

        tk.Button(self.scrollable_frame, text="Unenroll Student", command=self.perform_remove_student_from_course, width=20).pack(pady=10)
        self.result_label = tk.Label(self.scrollable_frame, text="", wraplength=400)
        self.result_label.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    def perform_remove_student_from_course(self):
        """
        Retrieves course CRN and student ID from the form, validates them,
        and calls the `admin.remove_student_from_course` method.
        Displays success or error messages.
        """
        try:
            crn = int(self.unenroll_crn_entry.get())
            student_id = int(self.unenroll_student_id_entry.get())
            result = self.admin.remove_student_from_course(crn, student_id)
            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Input Error", "CRN and Student ID must be numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def display_all_course_assignments(self):
        """Displays all course assignments in a scrolled text area."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="All Course Assignments", font=("Arial", 14, "bold")).pack(pady=10)
        result_text_widget = scrolledtext.ScrolledText(self.scrollable_frame, width=80, height=20, wrap=tk.WORD)
        result_text_widget.pack(pady=10)
        result_text_widget.insert(tk.END, self.admin.print_all_course_assignments())
        result_text_widget.config(state=tk.DISABLED)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    def display_all_student_schedules(self):
        """Displays all student schedules in a scrolled text area."""
        self.clear_scrollable_frame()
        tk.Label(self.scrollable_frame, text="All Student Schedules", font=("Arial", 14, "bold")).pack(pady=10)
        result_text_widget = scrolledtext.ScrolledText(self.scrollable_frame, width=80, height=20, wrap=tk.WORD)
        result_text_widget.pack(pady=10)
        result_text_widget.insert(tk.END, self.admin.print_all_student_schedules())
        result_text_widget.config(state=tk.DISABLED)
        tk.Button(self.scrollable_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=10)

    def logout(self):
        """
        Handles the logout process. Asks for user confirmation, closes the admin menu window,
        and re-displays the main login window.
        """
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.destroy() # Close the admin menu window
            self.master.deiconify() # Show the login window again
            messagebox.showinfo("Logout", "Logged out successfully.")
