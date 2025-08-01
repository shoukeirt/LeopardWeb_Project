from os import remove
import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from user import User
from student import Student
from instructor import Instructor

# Database path for SQLite database
DB_PATH = "assignment3.db"

# File written by Toufic Shoukeir
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

    def add_course(self, new_crn, new_title, new_dep, new_start_str, new_days, new_sem, new_year, credits):
        """
        Adds a new course to the COURSES table in the database.

        Args:
            new_crn (int): The CRN (Course Reference Number) of the new course.
            new_title (str): The title of the new course.
            new_dep (str): The department the new course belongs to.
            new_start_str (str): The start time of the course in "HH:MM AM/PM" format.
            new_days (str): The days of the week the course is held (e.g., "M/T/R").
            new_sem (str): The semester the course is offered (e.g., "Fall", "Spring").
            new_year (int): The year the course is offered.
            credits (int): The number of credits for the course.

        Returns:
            str: A success message if the course is added, or an error message if
                 time format is invalid, CRN already exists, or a database error occurs.
        """
        try:
            # Convert the input time string to a formatted time string for database storage
            time_start = datetime.datetime.strptime(new_start_str, "%I:%M %p").time()
            time_start_formatted = time_start.strftime("%H:%M:%S")
        except ValueError:
            return "Invalid time format. Please use HH:MM AM/PM."

        try:
            # SQL command to insert new course data
            sql_command = """INSERT INTO COURSES (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS) VALUES (?, ?, ?, ?, ?, ?, ?,?)"""
            self.cursor.execute(sql_command, (new_crn, new_title, new_dep, time_start_formatted, new_days, new_sem, new_year, credits))
            self.cx.commit() # Commit changes to the database
            return f"Course {new_title} (CRN: {new_crn}) Successfully Added!"
        except sqlite3.IntegrityError:
            # Handle case where CRN already exists (primary key constraint)
            return f"Error: Course with CRN {new_crn} already exists."
        except sqlite3.Error as e:
            # Handle other general database errors
            return f"Database error: {e}"

    def remove_course(self, remove_crn, confirm=False):
        """
        Removes a course from the COURSES table.

        Args:
            remove_crn (int): The CRN of the course to be removed.
            confirm (bool): If True, proceeds with removal; if False, returns a confirmation prompt.

        Returns:
            str: A confirmation prompt if confirm is False, a success message if
                 the course is removed, or an error message if the course is not found
                 or a database error occurs.
        """
        # Check if the course exists in the database
        self.cursor.execute("""SELECT * FROM COURSES WHERE CRN = ?""", (remove_crn,))
        rows = self.cursor.fetchall()

        if not rows:
            return f"No course found with CRN {remove_crn}."

        if not confirm:
            # Return course details for user confirmation
            course_details = "\n".join([str(row) for row in rows])
            return f"----------Are you sure you want to delete this course?----------\n{course_details}\n(Confirm 'Yes' in the next step to proceed)"
        else:
            try:
                # Execute SQL command to delete the course
                self.cursor.execute("""DELETE FROM COURSES WHERE CRN = ?""", (remove_crn,))
                self.cx.commit() # Commit changes
                return f"Course with CRN {remove_crn} Removed!"
            except sqlite3.Error as e:
                return f"Database error: {e}"

    def add_user(self, user_type, new_id, new_fname, new_lname, *args):
        """
        Adds a new user (Student, Instructor, or Admin) to the system.
        This includes adding an entry to the LOGIN table and the respective user table.

        Args:
            user_type (str): The type of user to add ("Student", "Instructor", "Admin").
            new_id (int): The ID of the new user.
            new_fname (str): The first name of the new user.
            new_lname (str): The last name of the new user.
            *args: Additional arguments specific to the user type:
                - For "Student": new_gradyear (int), new_major (str)
                - For "Instructor": new_title (str), new_hireyear (int), new_dept (str)
                - For "Admin": new_title (str), new_office (str)

        Returns:
            str: A success message if the user is added, or an error message if
                 the ID/email already exists, input is invalid, or a database error occurs.
        """
        new_email = (new_lname + new_fname[0]).lower() # Generate email from name

        try:
            # Check if ID or email already exists in the LOGIN table to prevent duplicates
            self.cursor.execute("SELECT * FROM LOGIN WHERE ID = ? OR EMAIL = ?", (new_id, new_email))
            if self.cursor.fetchone():
                return f"Error: User with ID {new_id} or email {new_email} already exists in LOGIN table."

            # Add user to the LOGIN table with a default password (e.g., 1234)
            self.cursor.execute("INSERT INTO LOGIN (ID, EMAIL, PASSWORD) VALUES (?, ?, ?)", (new_id, new_email, 1234))
            
            # Add user to their specific table based on user_type
            if user_type == "Student":
                new_gradyear = args[0]
                new_major = args[1]
                sql_command = """INSERT INTO STUDENT (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL) VALUES (?, ?, ?, ?, ?, ?)"""
                self.cursor.execute(sql_command, (new_id, new_fname, new_lname, new_gradyear, new_major, new_email))
                self.cx.commit()
                return f"New Student {new_fname} {new_lname} (ID: {new_id}) Added!"
            elif user_type == "Instructor":
                new_title = args[0]
                new_hireyear = args[1]
                new_dept = args[2]
                sql_command = """INSERT INTO INSTRUCTOR (ID, NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL) VALUES (?, ?, ?, ?, ?, ?,?)"""
                self.cursor.execute(sql_command, (new_id, new_fname, new_lname, new_title, new_hireyear, new_dept, new_email))
                self.cx.commit()
                return f"New Instructor {new_fname} {new_lname} (ID: {new_id}) Added!"
            elif user_type == "Admin":
                new_title = args[0]
                new_office = args[1]
                sql_command = """INSERT INTO ADMIN (ID, NAME, SURNAME, TITLE, OFFICE, EMAIL) VALUES (?, ?, ?, ?, ?, ?)"""
                self.cursor.execute(sql_command, (new_id, new_fname, new_lname, new_title, new_office, new_email))
                self.cx.commit()
                return f"New Admin {new_fname} {new_lname} (ID: {new_id}) Added!"
            else:
                self.cx.rollback() # Rollback the LOGIN table insert if user_type is not recognized
                return "Invalid user type specified."
        except sqlite3.IntegrityError:
            self.cx.rollback() # Rollback if there's a primary key violation (e.g., ID already exists in specific table)
            return f"Error: User with ID {new_id} already exists in the selected table."
        except sqlite3.Error as e:
            self.cx.rollback() # Rollback for any other database error
            return f"Database error: {e}"

    def remove_user(self, user_id, confirm=False):
        """
        Removes a user from the system based on their ID.
        This involves removing entries from the specific user table and the LOGIN table.
        Also cleans up related entries in ENROLLMENT and COURSE_TEACHER tables.

        Args:
            user_id (int): The ID of the user to be removed.
            confirm (bool): If True, proceeds with removal; if False, returns a confirmation prompt.

        Returns:
            str: A confirmation prompt if confirm is False, a success message if
                 the user is removed, or an error message if the user is not found
                 or a database error occurs.
        """
        user_id_str = str(user_id)
        table_name = None
        # Determine the user's table based on the ID prefix
        if user_id_str.startswith("1"):
            table_name = "STUDENT"
        elif user_id_str.startswith("2"):
            table_name = "INSTRUCTOR"
        elif user_id_str.startswith("3"):
            table_name = "ADMIN"
        
        if not table_name:
            return "Invalid User ID format."

        # Fetch user details for confirmation
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE ID = ?", (user_id,))
        user_rows = self.cursor.fetchall()

        if not user_rows:
            return f"No user found with ID {user_id} in {table_name} table."

        if not confirm:
            # Return user details for user confirmation
            user_details = "\n".join([str(row) for row in user_rows])
            return f"----------Are you sure you want to delete this user ({table_name})?----------\n{user_details}\n(Confirm 'Yes' in the next step to proceed)"
        else:
            try:
                # Remove from specific user table
                self.cursor.execute(f"DELETE FROM {table_name} WHERE ID = ?", (user_id,))
                # Remove from LOGIN table
                self.cursor.execute("DELETE FROM LOGIN WHERE ID = ?", (user_id,))
                
                # Additional cleanup for related tables (enrollments, course assignments)
                if table_name == "STUDENT":
                    self.cursor.execute("DELETE FROM ENROLLMENT WHERE STUDENT_ID = ?", (user_id,))
                    # Assuming STUDENT_SCHEDULE stores student names, use LIKE for broader match
                    self.cursor.execute("DELETE FROM STUDENT_SCHEDULE WHERE STUDENTNAME LIKE ?", (f"%{user_rows[0][1]} {user_rows[0][2]}%",))
                elif table_name == "INSTRUCTOR":
                    self.cursor.execute("DELETE FROM COURSE_TEACHER WHERE INSTRUCTOR_ID = ?", (user_id,))

                self.cx.commit() # Commit all deletions
                return f"User (ID: {user_id}) removed successfully from {table_name} and LOGIN tables."
            except sqlite3.Error as e:
                self.cx.rollback() # Rollback in case of error
                return f"Database error during user removal: {e}"

    def add_instructor(self, new_id, new_fname, new_lname, new_title, new_hireyear, new_dept):
        """
        Adds a new instructor to the INSTRUCTOR table and LOGIN table.
        This is a wrapper around the more general `add_user` method.

        Args:
            new_id (int): The ID of the new instructor.
            new_fname (str): The first name of the new instructor.
            new_lname (str): The last name of the new instructor.
            new_title (str): The title of the new instructor (e.g., "Professor").
            new_hireyear (int): The year the new instructor was hired.
            new_dept (str): The department of the new instructor.

        Returns:
            str: A success message or an error message from `add_user`.
        """
        return self.add_user("Instructor", new_id, new_fname, new_lname, new_title, new_hireyear, new_dept)
    
    def link_prof(self, prof_id, add_crn, confirm=False):
        """
        Links an instructor to a course by adding an entry to the COURSE_TEACHER table.

        Args:
            prof_id (int): The ID of the instructor to link.
            add_crn (int): The CRN of the course to link.
            confirm (bool): If True, proceeds with linking; if False, returns a confirmation prompt.

        Returns:
            str: A confirmation prompt if confirm is False, a success message if
                 the link is established, or an error message if instructor/course not found,
                 already linked, or a database error occurs.
        """
        # Fetch instructor details
        self.cursor.execute("""SELECT * FROM INSTRUCTOR WHERE ID = ?""", (prof_id,))
        prof_rows = self.cursor.fetchall()
        if not prof_rows:
            return f"No instructor found with ID {prof_id}."

        # Fetch course details
        self.cursor.execute("""SELECT * FROM COURSES WHERE CRN = ?""", (add_crn,))
        course_rows = self.cursor.fetchall()
        if not course_rows:
            return f"No course found with CRN {add_crn}."

        instructorname = f"{prof_rows[0][1]} {prof_rows[0][2]}"
        course_title = f"{course_rows[0][1]}"

        if not confirm:
            # Return details for user confirmation
            return (f"Is this the correct Instructor?\n{prof_rows[0]}\n"
                    f"Is this the correct Course?\n{course_rows[0]}\n"
                    f"(Confirm 'Yes' in the next step to link {instructorname} to {course_title})")
        else:
            try:
                # Check if the instructor is already linked to this course
                self.cursor.execute("SELECT * FROM COURSE_TEACHER WHERE INSTRUCTOR_ID = ? AND CRN = ?", (prof_id, add_crn))
                if self.cursor.fetchone():
                    return f"Instructor {instructorname} is already linked to course {course_title}."

                # Insert the link into the COURSE_TEACHER table
                sql_command = """INSERT INTO COURSE_TEACHER (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, CREDITS, INSTRUCTOR_ID, INSTRUCTOR_NAME, INSTRUCTOR_SURNAME, INSTRUCTOR_TITLE) VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
                values = (
                    course_rows[0][0], course_title, course_rows[0][2], course_rows[0][3], course_rows[0][4], course_rows[0][5], course_rows[0][7], prof_rows[0][0], prof_rows[0][1], prof_rows[0][2], prof_rows[0][3]
                )
                self.cursor.execute(sql_command, values)
                self.cx.commit() # Commit changes
                return f"You have linked {instructorname} to {course_title}."
            except sqlite3.Error as e:
                self.cx.rollback() # Rollback in case of error
                return f"Database error: {e}"

    def unlink_prof(self, prof_id, remove_crn, confirm=False):
        """
        Unlinks an instructor from a course by removing the entry from the COURSE_TEACHER table.

        Args:
            prof_id (int): The ID of the instructor to unlink.
            remove_crn (int): The CRN of the course to unlink from.
            confirm (bool): If True, proceeds with unlinking; if False, returns a confirmation prompt.

        Returns:
            str: A confirmation prompt if confirm is False, a success message if
                 the link is removed, or an error message if instructor/course not found,
                 not linked, or a database error occurs.
        """
        # Fetch instructor details
        self.cursor.execute("""SELECT * FROM INSTRUCTOR WHERE ID = ?""", (prof_id,))
        prof_rows = self.cursor.fetchall()
        if not prof_rows:
            return f"No instructor found with ID {prof_id}."

        # Fetch course details
        self.cursor.execute("""SELECT * FROM COURSES WHERE CRN = ?""", (remove_crn,))
        course_rows = self.cursor.fetchall()
        if not course_rows:
            return f"No course found with CRN {remove_crn}."

        instructorname = f"{prof_rows[0][1]} {prof_rows[0][2]}"
        course_title = f"{course_rows[0][1]}"

        # Check if the instructor is actually linked to this course
        self.cursor.execute("SELECT * FROM COURSE_TEACHER WHERE INSTRUCTOR_ID = ? AND CRN = ?", (prof_id, remove_crn))
        if not self.cursor.fetchone():
            return f"Instructor {instructorname} is not linked to course {course_title}."

        if not confirm:
            # Return details for user confirmation
            return (f"Is this the correct Instructor?\n{prof_rows[0]}\n"
                    f"Is this the correct Course?\n{course_rows[0]}\n"
                    f"(Confirm 'Yes' in the next step to unlink {instructorname} from {course_title})")
        else:
            try:
                # Delete the link from the COURSE_TEACHER table
                sql_command = """DELETE FROM COURSE_TEACHER WHERE CRN = ? AND INSTRUCTOR_ID = ?"""
                self.cursor.execute(sql_command, (remove_crn, prof_id))
                self.cx.commit() # Commit changes
                return f"You have unlinked {instructorname} from {course_title}."
            except sqlite3.Error as e:
                self.cx.rollback() # Rollback in case of error
                return f"Database error: {e}"

    def add_to_course(self, student_id, add_crn, confirm=False):
        """
        Adds a student to a course by creating an enrollment entry in the ENROLLMENT table.

        Args:
            student_id (int): The ID of the student to add.
            add_crn (int): The CRN of the course to add the student to.
            confirm (bool): If True, proceeds with adding; if False, returns a confirmation prompt.

        Returns:
            str: A confirmation prompt if confirm is False, a success message if
                 the student is added, or an error message if student/course not found,
                 already enrolled, or a database error occurs.
        """
        # Fetch student details
        self.cursor.execute("""SELECT * FROM STUDENT WHERE ID = ? """, (student_id,))
        student_rows = self.cursor.fetchall()
        if not student_rows:
            return f"No student found with ID {student_id}."

        # Fetch course details
        self.cursor.execute("""SELECT * FROM COURSES WHERE CRN = ?""", (add_crn,))
        course_rows = self.cursor.fetchall()
        if not course_rows:
            return f"No course found with CRN {add_crn}."

        student_name = f"{student_rows[0][1]} {student_rows[0][2]}"
        course_title = f"{course_rows[0][1]}"

        # Check if the student is already enrolled in this course
        self.cursor.execute("SELECT * FROM ENROLLMENT WHERE STUDENT_ID = ? AND CRN = ?", (student_id, add_crn))
        if self.cursor.fetchone():
            return f"Student {student_name} is already enrolled in course {course_title}."

        if not confirm:
            # Return details for user confirmation
            return (f"Is this the correct Student?\n{student_rows[0]}\n"
                    f"Is this the correct Course?\n{course_rows[0]}\n"
                    f"(Confirm 'Yes' in the next step to add {student_name} to {course_title})")
        else:
            try:
                # Insert enrollment entry
                sql_command = ("""INSERT INTO ENROLLMENT (STUDENT_ID, CRN) VALUES (?, ?)""")
                self.cursor.execute(sql_command, (student_id, add_crn))
                self.cx.commit() # Commit changes
                return f"You have added {student_name} to {course_title}."
            except sqlite3.Error as e:
                self.cx.rollback() # Rollback in case of error
                return f"Database error: {e}"

    def remove_from_course(self, student_id, remove_crn, confirm=False):
        """
        Removes a student from a course by deleting their enrollment entry.

        Args:
            student_id (int): The ID of the student to remove.
            remove_crn (int): The CRN of the course to remove the student from.
            confirm (bool): If True, proceeds with removal; if False, returns a confirmation prompt.

        Returns:
            str: A confirmation prompt if confirm is False, a success message if
                 the student is removed, or an error message if student/course not found,
                 not enrolled, or a database error occurs.
        """
        # Fetch student details
        self.cursor.execute("""SELECT * FROM STUDENT WHERE ID = ? """, (student_id,))
        student_rows = self.cursor.fetchall()
        if not student_rows:
            return f"No student found with ID {student_id}."

        # Fetch course details
        self.cursor.execute("""SELECT * FROM COURSES WHERE CRN = ?""", (remove_crn,))
        course_rows = self.cursor.fetchall()
        if not course_rows:
            return f"No course found with CRN {remove_crn}."

        student_name = f"{student_rows[0][1]} {student_rows[0][2]}"
        course_title = f"{course_rows[0][1]}"

        # Check if the student is actually enrolled in this course
        self.cursor.execute("SELECT * FROM ENROLLMENT WHERE STUDENT_ID = ? AND CRN = ?", (student_id, remove_crn))
        if not self.cursor.fetchone():
            return f"Student {student_name} is not enrolled in course {course_title}."

        if not confirm:
            # Return details for user confirmation
            return (f"Is this the correct Student?\n{student_rows[0]}\n"
                    f"Is this the correct Course?\n{course_rows[0]}\n"
                    f"(Confirm 'Yes' in the next step to remove {student_name} from {course_title})")
        else:
            try:
                # Delete enrollment entry
                sql_command = ("""DELETE FROM ENROLLMENT WHERE STUDENT_ID = ? AND CRN = ? """)
                self.cursor.execute(sql_command, (student_id, remove_crn))
                self.cx.commit() # Commit changes
                return f"You have removed {student_name} from {course_title}."
            except sqlite3.Error as e:
                self.cx.rollback() # Rollback in case of error
                return f"Database error: {e}"

    def search_courses(self, search_keyword='CRN', search_value=None):
        """
        Searches for courses based on a keyword (CRN or TITLE) and a search value.

        Args:
            search_keyword (str): The keyword to search by ("CRN" or "TITLE").
            search_value (str or int): The value to search for.

        Returns:
            str: A formatted string of search results, or a message indicating no courses found,
                 or an error message for invalid keyword/SQL error.
        """
        if search_keyword.upper() == "CRN":
            search_keyword_col = "CRN"
        elif search_keyword.upper() in ["COURSE NAME", "TITLE"]:
            search_keyword_col = "TITLE"
        else:
            return "Invalid search keyword."

        try:
            # Execute the search query
            query = f"SELECT * FROM COURSES WHERE {search_keyword_col} = ?"
            self.cursor.execute(query, (search_value,))
            rows = self.cursor.fetchall()
            
            if rows:
                # Format the results into a readable string
                result_str = "Search Results:\n"
                for row in rows:
                    result_str += f"CRN: {row[0]}, Title: {row[1]}, Dept: {row[2]}, Time: {row[3]}, Days: {row[4]}, Semester: {row[5]}, Year: {row[6]}, Credits: {row[7]}\n"
                return result_str
            else:
                return "No courses found matching your criteria."
        except sqlite3.Error as e:
            return f"SQL Error: {e}"


class AdminMenu(tk.Toplevel):
    """
    The AdminMenu class provides the Graphical User Interface (GUI) for the Admin functionalities.
    It allows an admin to interact with the system through a user-friendly window.
    """
    def __init__(self, master, admin_obj):
        """
        Initializes the AdminMenu GUI window.
        
        Args:
            master (tk.Tk or tk.Toplevel): The parent Tkinter window (e.g., the login window).
            admin_obj (Admin): An instance of the Admin class, containing the administrative logic.
        """
        super().__init__(master)
        self.master = master
        self.admin = admin_obj
        self.title(f"Admin Menu - {self.admin.firstName} {self.admin.lastName}")
        self.geometry("700x600") # Set a default size for the window
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges the main GUI widgets for the admin menu.
        This method is called initially and whenever the user returns to the main menu.
        """
        # Clear any existing widgets from the frame to prepare for new content
        for widget in self.winfo_children():
            widget.destroy()

        self.main_frame = tk.Frame(self, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill="both")

        welcome_label = tk.Label(self.main_frame, text=f"Welcome, Admin {self.admin.firstName} {self.admin.lastName}!", font=("Arial", 16, "bold"))
        welcome_label.pack(pady=10)

        # Buttons for various admin actions, each linked to a specific menu display function
        btn_add_course = tk.Button(self.main_frame, text="Add Course", command=self.show_add_course_menu, width=30, height=2)
        btn_add_course.pack(pady=5)

        btn_remove_course = tk.Button(self.main_frame, text="Remove Course", command=self.show_remove_course_menu, width=30, height=2)
        btn_remove_course.pack(pady=5)

        btn_add_user = tk.Button(self.main_frame, text="Add User (Student/Instructor/Admin)", command=self.show_add_user_menu, width=30, height=2)
        btn_add_user.pack(pady=5)

        btn_remove_user = tk.Button(self.main_frame, text="Remove User", command=self.show_remove_user_menu, width=30, height=2)
        btn_remove_user.pack(pady=5)

        btn_link_prof = tk.Button(self.main_frame, text="Link Instructor to Course", command=self.show_link_prof_menu, width=30, height=2)
        btn_link_prof.pack(pady=5)
        
        btn_unlink_prof = tk.Button(self.main_frame, text="Unlink Instructor from Course", command=self.show_unlink_prof_menu, width=30, height=2)
        btn_unlink_prof.pack(pady=5)

        btn_add_student_to_course = tk.Button(self.main_frame, text="Add Student to Course", command=self.show_add_student_to_course_menu, width=30, height=2)
        btn_add_student_to_course.pack(pady=5)

        btn_remove_student_from_course = tk.Button(self.main_frame, text="Remove Student from Course", command=self.show_remove_student_from_course_menu, width=30, height=2)
        btn_remove_student_from_course.pack(pady=5)

        btn_search_courses = tk.Button(self.main_frame, text="Search Courses", command=self.show_search_courses_menu, width=30, height=2)
        btn_search_courses.pack(pady=5)

        # Logout button, styled differently for emphasis
        btn_logout = tk.Button(self.main_frame, text="Logout", command=self.logout, width=30, height=2, bg="red", fg="white")
        btn_logout.pack(pady=20)

    def clear_main_frame(self):
        """
        Clears all widgets from the main frame. This is used when switching between different
        sub-menus to ensure only the relevant widgets are displayed.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def logout(self):
        """
        Handles the admin logout process. It prompts for confirmation, closes the admin menu
        window, and re-displays the main login window.
        """
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.destroy() # Close the current admin menu window
            self.master.deiconify() # Show the parent (login) window again
            messagebox.showinfo("Logout", "Logged out successfully.")

    def show_add_course_menu(self):
        """
        Displays the GUI for adding a new course.
        Includes input fields for course details and buttons to add or go back.
        """
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Add New Course", font=("Arial", 14, "bold")).pack(pady=10)

        labels = ["CRN:", "Title:", "Department:", "Start Time (HH:MM AM/PM):", "Days (M/T/R Format):", "Semester:", "Year:", "Credits:"]
        entries = {} # Dictionary to store references to entry widgets
        for i, text in enumerate(labels):
            tk.Label(self.main_frame, text=text).pack(pady=2, anchor="w")
            entry = tk.Entry(self.main_frame, width=40)
            entry.pack(pady=2, anchor="w")
            entries[text.split(':')[0].strip().lower()] = entry # Store entry by its label text (lowercase)

        def perform_add_course():
            """
            Retrieves input from the entry fields, validates it, and calls the admin's add_course method.
            Displays the result using a messagebox.
            """
            try:
                # Get values from entry widgets and convert to appropriate types
                crn = int(entries["crn"].get())
                title = entries["title"].get().strip()
                dep = entries["department"].get().strip()
                start_time = entries["start time"].get().strip()
                days = entries["days"].get().strip()
                semester = entries["semester"].get().strip()
                year = int(entries["year"].get())
                credits = int(entries["credits"].get())

                # Basic input validation
                if not all([title, dep, start_time, days, semester]):
                    messagebox.showwarning("Input Error", "All fields must be filled.")
                    return

                # Call the core admin method
                result = self.admin.add_course(crn, title, dep, start_time, days, semester, year, credits)
                messagebox.showinfo("Add Course Result", result)
                if "Successfully Added" in result:
                    self.create_widgets() # Return to main menu on success
            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid input: {e}. Please check CRN, Year, and Credits are numbers, and time format is correct.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        # Buttons for action and navigation
        tk.Button(self.main_frame, text="Add Course", command=perform_add_course, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=5)

    def show_remove_course_menu(self):
        """
        Displays the GUI for removing a course.
        Includes an input field for CRN and a confirmation process.
        """
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Remove Course", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Enter CRN of course to remove:").pack(pady=5)
        crn_entry = tk.Entry(self.main_frame, width=20)
        crn_entry.pack(pady=5)

        # Text widget to display initial confirmation details (read-only)
        current_result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=5, wrap=tk.WORD)
        current_result_text.pack(pady=5)
        current_result_text.config(state=tk.DISABLED) # Make it read-only

        def confirm_remove_course(crn_val):
            """Confirms and performs the actual course removal."""
            result = self.admin.remove_course(crn_val, confirm=True)
            messagebox.showinfo("Remove Course Result", result)
            self.create_widgets() # Return to main menu after action

        def perform_remove_course_initial():
            """
            Initiates the course removal process, first showing details for confirmation.
            """
            try:
                crn = int(crn_entry.get())
                # Call admin method with confirm=False to get initial details/prompt
                initial_result = self.admin.remove_course(crn, confirm=False)
                current_result_text.config(state=tk.NORMAL) # Enable editing to update text
                current_result_text.delete(1.0, tk.END)
                current_result_text.insert(tk.END, initial_result)
                current_result_text.config(state=tk.DISABLED) # Disable editing again

                if "Are you sure" in initial_result:
                    # If the result is a confirmation prompt, ask the user
                    if messagebox.askyesno("Confirm Removal", initial_result):
                        confirm_remove_course(crn) # Proceed with actual removal
                else:
                    # If not a confirmation, it's likely an error or "not found" message
                    messagebox.showinfo("Remove Course Result", initial_result)
                    self.create_widgets() # Return to main menu
            except ValueError:
                messagebox.showerror("Input Error", "CRN must be an integer.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        # Buttons for action and navigation
        tk.Button(self.main_frame, text="Remove Course", command=perform_remove_course_initial, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=5)

    def show_add_user_menu(self):
        """
        Displays the GUI for adding a new user (Student, Instructor, or Admin).
        Dynamically adjusts input fields based on the selected user type.
        """
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Add New User", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="User Type:").pack(pady=2, anchor="w")
        user_type_var = tk.StringVar(self.main_frame)
        user_type_var.set("Student") # Set default user type
        user_type_option = tk.OptionMenu(self.main_frame, user_type_var, "Student", "Instructor", "Admin")
        user_type_option.pack(pady=2, anchor="w")

        # Labels for common user details
        common_labels = ["ID:", "First Name:", "Last Name:"]
        # Labels for specific user types
        student_labels = ["Graduation Year:", "Major (e.g., BSAS):"]
        instructor_labels = ["Title (e.g., Professor):", "Hire Year:", "Department (e.g., BSCO):"]
        admin_labels = ["Title (e.g., President):", "Office:"]

        entries = {} # Dictionary to store references to all entry widgets
        frames = {} # Dictionary to store references to dynamic frames

        # Create common entry widgets
        for text in common_labels:
            tk.Label(self.main_frame, text=text).pack(pady=2, anchor="w")
            entry = tk.Entry(self.main_frame, width=40)
            entry.pack(pady=2, anchor="w")
            entries[text.split(':')[0].strip().lower()] = entry

        # Define buttons here so they are accessible by create_dynamic_entries
        add_button = tk.Button(self.main_frame, text=f"Add {user_type_var.get()}", command=lambda: perform_add_user(), width=20)
        back_button = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)


        def create_dynamic_entries():
            """
            Dynamically creates and destroys input fields based on the selected user type.
            """
            # Destroy existing dynamic frames and clear their entries
            for frame in frames.values():
                frame.destroy()
            frames.clear()
            
            # Remove type-specific entries from the 'entries' dictionary
            for key in ["graduation year", "major", "title", "hire year", "department", "office"]:
                if key in entries:
                    del entries[key]

            current_type = user_type_var.get()
            
            dynamic_frame = tk.Frame(self.main_frame)
            dynamic_frame.pack(pady=5, fill="x")
            frames["dynamic"] = dynamic_frame # Store reference to the dynamic frame
            
            # Create type-specific entry widgets
            if current_type == "Student":
                for text in student_labels:
                    tk.Label(dynamic_frame, text=text).pack(pady=2, anchor="w")
                    entry = tk.Entry(dynamic_frame, width=40)
                    entry.pack(pady=2, anchor="w")
                    entries[text.split(':')[0].strip().lower()] = entry
            elif current_type == "Instructor":
                for text in instructor_labels:
                    tk.Label(dynamic_frame, text=text).pack(pady=2, anchor="w")
                    entry = tk.Entry(dynamic_frame, width=40)
                    entry.pack(pady=2, anchor="w")
                    entries[text.split(':')[0].strip().lower()] = entry
            elif current_type == "Admin":
                for text in admin_labels:
                    tk.Label(dynamic_frame, text=text).pack(pady=2, anchor="w")
                    entry = tk.Entry(dynamic_frame, width=40)
                    entry.pack(pady=2, anchor="w")
                    entries[text.split(':')[0].strip().lower()] = entry
            
            # Update the text of the add button based on the selected user type
            add_button.config(text=f"Add {current_type}")
            # Re-pack the buttons to ensure they are at the bottom after dynamic content
            add_button.pack_forget() # Remove from current packing geometry
            back_button.pack_forget() # Remove from current packing geometry
            add_button.pack(pady=10) # Re-pack
            back_button.pack(pady=5) # Re-pack

        # Trace changes to the user type variable to dynamically update entries
        user_type_var.trace_add("write", lambda *args: create_dynamic_entries())
        create_dynamic_entries() # Initial call to set up entries based on default user type

        def perform_add_user():
            """
            Retrieves input for adding a user, validates it, and calls the admin's add_user method.
            Displays the result using a messagebox.
            """
            try:
                user_type = user_type_var.get()
                new_id = int(entries["id"].get())
                new_fname = entries["first name"].get().strip()
                new_lname = entries["last name"].get().strip()

                # Basic validation for common fields
                if not all([new_fname, new_lname]):
                    messagebox.showwarning("Input Error", "First Name and Last Name cannot be empty.")
                    return

                args_list = []
                # Collect type-specific arguments
                if user_type == "Student":
                    new_gradyear = int(entries["graduation year"].get())
                    new_major = entries["major"].get().strip()
                    if not new_major: raise ValueError("Major cannot be empty.")
                    args_list = [new_gradyear, new_major]
                elif user_type == "Instructor":
                    new_title = entries["title"].get().strip()
                    new_hireyear = int(entries["hire year"].get())
                    new_dept = entries["department"].get().strip()
                    if not all([new_title, new_dept]): raise ValueError("Title and Department cannot be empty.")
                    args_list = [new_title, new_hireyear, new_dept]
                elif user_type == "Admin":
                    new_title = entries["title"].get().strip()
                    new_office = entries["office"].get().strip()
                    if not all([new_title, new_office]): raise ValueError("Title and Office cannot be empty.")
                    args_list = [new_title, new_office]

                # Call the core admin method
                result = self.admin.add_user(user_type, new_id, new_fname, new_lname, *args_list)
                messagebox.showinfo("Add User Result", result)
                if "Added!" in result:
                    self.create_widgets() # Return to main menu on success
            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid input: {e}. Please check ID, year, and ensure all fields are filled correctly.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        # The buttons are now defined outside create_dynamic_entries and can be packed here.
        # They will be re-packed by create_dynamic_entries when the user type changes.
        add_button.pack(pady=10)
        back_button.pack(pady=5)

    def show_remove_user_menu(self):
        """
        Displays the GUI for removing a user.
        Includes an input field for User ID and a confirmation process.
        """
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Remove User", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Enter User ID to remove:").pack(pady=5)
        user_id_entry = tk.Entry(self.main_frame, width=20)
        user_id_entry.pack(pady=5)

        current_result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=5, wrap=tk.WORD)
        current_result_text.pack(pady=5)
        current_result_text.config(state=tk.DISABLED) # Read-only

        def confirm_remove_user(user_id_val):
            """Confirms and performs the actual user removal."""
            result = self.admin.remove_user(user_id_val, confirm=True)
            messagebox.showinfo("Remove User Result", result)
            self.create_widgets() # Return to main menu after action

        def perform_remove_user_initial():
            """
            Initiates the user removal process, first showing details for confirmation.
            """
            try:
                user_id = int(user_id_entry.get())
                # Call admin method with confirm=False to get initial details/prompt
                initial_result = self.admin.remove_user(user_id, confirm=False)
                current_result_text.config(state=tk.NORMAL) # Enable editing to update text
                current_result_text.delete(1.0, tk.END)
                current_result_text.insert(tk.END, initial_result)
                current_result_text.config(state=tk.DISABLED) # Disable editing again

                if "Are you sure" in initial_result:
                    # If the result is a confirmation prompt, ask the user
                    if messagebox.askyesno("Confirm Removal", initial_result):
                        confirm_remove_user(user_id) # Proceed with actual removal
                else:
                    # If not a confirmation, it's likely an error or "not found" message
                    messagebox.showinfo("Remove User Result", initial_result)
                    self.create_widgets() # Return to main menu
            except ValueError:
                messagebox.showerror("Input Error", "User ID must be an integer.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        # Buttons for action and navigation
        tk.Button(self.main_frame, text="Remove User", command=perform_remove_user_initial, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=5)

    def show_link_prof_menu(self):
        """
        Displays the GUI for linking an instructor to a course.
        Includes input fields for instructor ID and course CRN, and a confirmation process.
        """
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Link Instructor to Course", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Instructor ID:").pack(pady=2, anchor="w")
        prof_id_entry = tk.Entry(self.main_frame, width=20)
        prof_id_entry.pack(pady=2, anchor="w")

        tk.Label(self.main_frame, text="Course CRN:").pack(pady=2, anchor="w")
        crn_entry = tk.Entry(self.main_frame, width=20)
        crn_entry.pack(pady=2, anchor="w")

        current_result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=7, wrap=tk.WORD)
        current_result_text.pack(pady=5)
        current_result_text.config(state=tk.DISABLED) # Read-only

        def confirm_link_prof(prof_id_val, crn_val):
            """Confirms and performs the actual instructor-course linking."""
            result = self.admin.link_prof(prof_id_val, crn_val, confirm=True)
            messagebox.showinfo("Link Instructor Result", result)
            self.create_widgets() # Return to main menu after action

        def perform_link_prof_initial():
            """
            Initiates the linking process, first showing details for confirmation.
            """
            try:
                prof_id = int(prof_id_entry.get())
                crn = int(crn_entry.get())

                # Call admin method with confirm=False to get initial details/prompt
                initial_result = self.admin.link_prof(prof_id, crn, confirm=False)
                current_result_text.config(state=tk.NORMAL)
                current_result_text.delete(1.0, tk.END)
                current_result_text.insert(tk.END, initial_result)
                current_result_text.config(state=tk.DISABLED)

                if "Confirm 'Yes'" in initial_result:
                    # If the result is a confirmation prompt, ask the user
                    if messagebox.askyesno("Confirm Link", initial_result):
                        confirm_link_prof(prof_id, crn) # Proceed with actual linking
                else:
                    # If not a confirmation, it's likely an error or "not found" message
                    messagebox.showinfo("Link Instructor Result", initial_result)
                    self.create_widgets() # Return to main menu
            except ValueError:
                messagebox.showerror("Input Error", "Instructor ID and CRN must be integers.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        # Buttons for action and navigation
        tk.Button(self.main_frame, text="Link Instructor", command=perform_link_prof_initial, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=5)

    def show_unlink_prof_menu(self):
        """
        Displays the GUI for unlinking an instructor from a course.
        Includes input fields for instructor ID and course CRN, and a confirmation process.
        """
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Unlink Instructor from Course", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Instructor ID:").pack(pady=2, anchor="w")
        prof_id_entry = tk.Entry(self.main_frame, width=20)
        prof_id_entry.pack(pady=2, anchor="w")

        tk.Label(self.main_frame, text="Course CRN:").pack(pady=2, anchor="w")
        crn_entry = tk.Entry(self.main_frame, width=20)
        crn_entry.pack(pady=2, anchor="w")

        current_result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=7, wrap=tk.WORD)
        current_result_text.pack(pady=5)
        current_result_text.config(state=tk.DISABLED) # Read-only

        def confirm_unlink_prof(prof_id_val, crn_val):
            """Confirms and performs the actual instructor-course unlinking."""
            result = self.admin.unlink_prof(prof_id_val, crn_val, confirm=True)
            messagebox.showinfo("Unlink Instructor Result", result)
            self.create_widgets() # Return to main menu after action

        def perform_unlink_prof_initial():
            """
            Initiates the unlinking process, first showing details for confirmation.
            """
            try:
                prof_id = int(prof_id_entry.get())
                crn = int(crn_entry.get())

                # Call admin method with confirm=False to get initial details/prompt
                initial_result = self.admin.unlink_prof(prof_id, crn, confirm=False)
                current_result_text.config(state=tk.NORMAL)
                current_result_text.delete(1.0, tk.END)
                current_result_text.insert(tk.END, initial_result)
                current_result_text.config(state=tk.DISABLED)

                if "Confirm 'Yes'" in initial_result:
                    # If the result is a confirmation prompt, ask the user
                    if messagebox.askyesno("Confirm Unlink", initial_result):
                        confirm_unlink_prof(prof_id, crn) # Proceed with actual unlinking
                else:
                    # If not a confirmation, it's likely an error or "not found" message
                    messagebox.showinfo("Unlink Instructor Result", initial_result)
                    self.create_widgets() # Return to main menu
            except ValueError:
                messagebox.showerror("Input Error", "Instructor ID and CRN must be integers.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        # Buttons for action and navigation
        tk.Button(self.main_frame, text="Unlink Instructor", command=perform_unlink_prof_initial, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=5)

    def show_add_student_to_course_menu(self):
        """
        Displays the GUI for adding a student to a course.
        Includes input fields for student ID and course CRN, and a confirmation process.
        """
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Add Student to Course", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Student ID:").pack(pady=2, anchor="w")
        student_id_entry = tk.Entry(self.main_frame, width=20)
        student_id_entry.pack(pady=2, anchor="w")

        tk.Label(self.main_frame, text="Course CRN:").pack(pady=2, anchor="w")
        crn_entry = tk.Entry(self.main_frame, width=20)
        crn_entry.pack(pady=2, anchor="w")

        current_result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=7, wrap=tk.WORD)
        current_result_text.pack(pady=5)
        current_result_text.config(state=tk.DISABLED) # Read-only

        def confirm_add_student_to_course(student_id_val, crn_val):
            """Confirms and performs the actual student-course addition."""
            result = self.admin.add_to_course(student_id_val, crn_val, confirm=True)
            messagebox.showinfo("Add Student Result", result)
            self.create_widgets() # Return to main menu after action

        def perform_add_student_to_course_initial():
            """
            Initiates the student addition process, first showing details for confirmation.
            """
            try:
                student_id = int(student_id_entry.get())
                crn = int(crn_entry.get())

                # Call admin method with confirm=False to get initial details/prompt
                initial_result = self.admin.add_to_course(student_id, crn, confirm=False)
                current_result_text.config(state=tk.NORMAL)
                current_result_text.delete(1.0, tk.END)
                current_result_text.insert(tk.END, initial_result)
                current_result_text.config(state=tk.DISABLED)

                if "Confirm 'Yes'" in initial_result:
                    # If the result is a confirmation prompt, ask the user
                    if messagebox.askyesno("Confirm Add Student", initial_result):
                        confirm_add_student_to_course(student_id, crn) # Proceed with actual addition
                else:
                    # If not a confirmation, it's likely an error or "not found" message
                    messagebox.showinfo("Add Student Result", initial_result)
                    self.create_widgets() # Return to main menu
            except ValueError:
                messagebox.showerror("Input Error", "Student ID and CRN must be integers.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        # Buttons for action and navigation
        tk.Button(self.main_frame, text="Add Student", command=perform_add_student_to_course_initial, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=5)

    def show_remove_student_from_course_menu(self):
        """
        Displays the GUI for removing a student from a course.
        Includes input fields for student ID and course CRN, and a confirmation process.
        """
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Remove Student from Course", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Student ID:").pack(pady=2, anchor="w")
        student_id_entry = tk.Entry(self.main_frame, width=20)
        student_id_entry.pack(pady=2, anchor="w")

        tk.Label(self.main_frame, text="Course CRN:").pack(pady=2, anchor="w")
        crn_entry = tk.Entry(self.main_frame, width=20)
        crn_entry.pack(pady=2, anchor="w")

        current_result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=7, wrap=tk.WORD)
        current_result_text.pack(pady=5)
        current_result_text.config(state=tk.DISABLED) # Read-only

        def confirm_remove_student_from_course(student_id_val, crn_val):
            """Confirms and performs the actual student-course removal."""
            result = self.admin.remove_from_course(student_id_val, crn_val, confirm=True)
            messagebox.showinfo("Remove Student Result", result)
            self.create_widgets() # Return to main menu after action

        def perform_remove_student_from_course_initial():
            """
            Initiates the student removal process, first showing details for confirmation.
            """
            try:
                student_id = int(student_id_entry.get())
                crn = int(crn_entry.get())

                # Call admin method with confirm=False to get initial details/prompt
                initial_result = self.admin.remove_from_course(student_id, crn, confirm=False)
                current_result_text.config(state=tk.NORMAL)
                current_result_text.delete(1.0, tk.END)
                current_result_text.insert(tk.END, initial_result)
                current_result_text.config(state=tk.DISABLED)

                if "Confirm 'Yes'" in initial_result:
                    # If the result is a confirmation prompt, ask the user
                    if messagebox.askyesno("Confirm Remove Student", initial_result):
                        confirm_remove_student_from_course(student_id, crn) # Proceed with actual removal
                else:
                    # If not a confirmation, it's likely an error or "not found" message
                    messagebox.showinfo("Remove Student Result", initial_result)
                    self.create_widgets() # Return to main menu
            except ValueError:
                messagebox.showerror("Input Error", "Student ID and CRN must be integers.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        # Buttons for action and navigation
        tk.Button(self.main_frame, text="Remove Student", command=perform_remove_student_from_course_initial, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20).pack(pady=5)

    def show_search_courses_menu(self):
        """
        Displays the GUI for searching courses.
        Allows searching by CRN or Title and displays results in a scrolled text area.
        """
        self.clear_main_frame()
        
        tk.Label(self.main_frame, text="Search Courses", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Search by:").pack()
        self.search_by_var = tk.StringVar(self.main_frame)
        self.search_by_var.set("CRN") # Default search criteria
        search_by_option = tk.OptionMenu(self.main_frame, self.search_by_var, "CRN", "TITLE")
        search_by_option.pack(pady=5)

        tk.Label(self.main_frame, text="Search Value:").pack()
        self.search_value_entry = tk.Entry(self.main_frame, width=40)
        self.search_value_entry.pack(pady=5)

        btn_search = tk.Button(self.main_frame, text="Search", command=self.perform_search_courses, width=20)
        btn_search.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=10, wrap=tk.WORD)
        self.result_text.pack(pady=10)

        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def perform_search_courses(self):
        """
        Performs the course search based on user input from the GUI and displays results.
        """
        search_keyword = self.search_by_var.get()
        search_value = self.search_value_entry.get().strip()

        if not search_value:
            messagebox.showwarning("Input Error", "Please enter a search value.")
            return

        # Convert search value to integer if searching by CRN
        if search_keyword == "CRN":
            try:
                search_value = int(search_value)
            except ValueError:
                messagebox.showerror("Input Error", "CRN must be a number.")
                return

        # Call the core admin method to perform the search
        result = self.admin.search_courses(search_keyword, search_value)
        self.result_text.delete(1.0, tk.END) # Clear previous results
        self.result_text.insert(tk.END, result) # Display new results

