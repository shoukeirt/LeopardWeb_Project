#Written Harljen Hill
#Updated and Fixed and Implemented by Anthony Magliozzi

import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from user import User # Assuming User class is in user.py

# Database path
DB_PATH = "assignment3.db"

import datetime

# Utility function to split a time range string (e.g., '2:30 PM - 4:00 PM') into start and end time objects
def split_time(time_str):
    start_time, end_time = time_str.split('-')
    start_time = datetime.datetime.strptime(start_time.strip(), '%I:%M %p')
    end_time = datetime.datetime.strptime(end_time.strip(), '%I:%M %p')
    return start_time, end_time

# --- New Class for Course Representation (for consistent display) ---
class Course:
    """
    Represents a course with its various attributes such as CRN, title, department,
    time, days, semester, year, and credits. This class is used to create
    course objects from database queries, facilitating object-oriented interaction
    with course information.
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
        return (f"CRN: {self.crn}, Title: {self.title}, Dept: {self.dept}, "
                f"Time: {self.time}, Days: {self.days}, Semester: {self.semester}, "
                f"Year: {self.year}, Credits: {self.credits}")

class Student(User):
    def __init__(self, in_firstName, in_lastName, in_id):
        super().__init__(in_firstName, in_lastName, in_id)

    def print_all_courses(self): # Modified to manage its own connection
        """
        Retrieves all available courses from the COURSES table in the database
        and formats them into a readable string with an empty line between courses.

        Returns:
            str: A formatted string listing all courses, or a message if no courses are found.
        """
        with sqlite3.connect(DB_PATH) as cx: # Use with statement
            cursor = cx.cursor()
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

    # Search for courses by CRN or TITLE
    def search_courses(self, Search_keyword, search_value):
        with sqlite3.connect(DB_PATH) as cx: # Use DB_PATH constant
            cursor = cx.cursor()

            try:
                # Removed redundant student existence check as it's assumed logged in

                # Normalize search keyword
                if Search_keyword.upper() == "CRN":
                    Search_keyword = "CRN"
                elif Search_keyword.upper() in ["COURSE NAME", "TITLE"]:
                    Search_keyword = "TITLE"
                else:
                    return "Invalid search keyword."

                # Execute course search
                cursor.execute(f"SELECT CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS FROM COURSES WHERE {Search_keyword} = ?", (search_value,))
                rows = cursor.fetchall()

                if rows:
                    result_str = "Search Results:\n"
                    for row in rows:
                        course_obj = Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                        result_str += str(course_obj) + "\n\n" # Added extra newline here
                    return result_str
                else:
                    return "No courses found matching your criteria."
            except sqlite3.Error as e:
                return f"SQL Error: {e}"

    # Add course to student schedule and check for time conflicts
    def add_course(self, CRN):
        with sqlite3.connect(DB_PATH) as cx: # Use DB_PATH constant
            cursor = cx.cursor()

            try:
                # Get course information
                # Fetching all columns to ensure Course constructor has all data
                cursor.execute("SELECT CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS FROM COURSES WHERE CRN = ?", (CRN,))
                course = cursor.fetchone()

                if not course:
                    return "Course not found."

                # Retrieve existing enrollments for the student
                cursor.execute("SELECT CRN FROM ENROLLMENT WHERE STUDENT_ID = ?", (self.id,))
                enrolled_crns = [row[0] for row in cursor.fetchall()]

                if CRN in enrolled_crns:
                    return f"You are already enrolled in CRN {CRN}."
                
                # Check maximum course limit (changed from 4 to 5 as per previous fix)
                if len(enrolled_crns) >= 5:
                    return "You are already enrolled in 5 courses and cannot add more."

                # If the student is enrolled in any courses, check for time conflicts
                if enrolled_crns:
                    # Fetch details for enrolled courses to check for conflicts
                    query = f"SELECT CRN, TIME, DAYS FROM COURSES WHERE CRN IN ({','.join(['?'] * len(enrolled_crns))})"
                    cursor.execute(query, enrolled_crns)
                    enrolled_courses_details = cursor.fetchall()

                    # Parse time and days from the course the student wants to add
                    # Indexes here correspond to (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS) from the main SELECT *
                    course_days = course[4] 
                    course_hour_start, course_hour_end = split_time(course[3]) 

                    for enrolled_course_detail in enrolled_courses_details:
                        enrolled_crn, enrolled_time_str, enrolled_days = enrolled_course_detail
                        enrolled_hour_start, enrolled_hour_end = split_time(enrolled_time_str)

                        # Check for overlapping days and time ranges (logic fixed previously)
                        if any(day in enrolled_days for day in course_days) and not (
                            course_hour_end <= enrolled_hour_start or course_hour_start >= enrolled_hour_end):
                            return f"Time conflict with course {enrolled_crn}: {enrolled_course_detail[1]}"

                # Add course to ENROLLMENT table if no conflict
                cursor.execute("INSERT INTO ENROLLMENT (STUDENT_ID, CRN) VALUES (?, ?)", (self.id, course[0]))
                cx.commit()
                return f"Course {course[0]} added successfully."

            except ValueError:
                return "Error parsing time format. Please ensure all course times are valid."
            except sqlite3.Error as e:
                return f"SQL Error: {e}"

    # Remove course from student schedule
    def remove_course(self, CRN):
        with sqlite3.connect(DB_PATH) as cx: # Use DB_PATH constant
            cursor = cx.cursor()

            try:
                # Check if student is enrolled in the course
                cursor.execute("SELECT * FROM ENROLLMENT WHERE STUDENT_ID = ? AND CRN = ?", (self.id, CRN))
                enrollment = cursor.fetchone()

                if not enrollment:
                    return "You are not enrolled in this course."
                else:
                    # Delete enrollment
                    cursor.execute("DELETE FROM ENROLLMENT WHERE STUDENT_ID = ? AND CRN = ?", (self.id, CRN))
                    cx.commit()
                    return f"Course with CRN {CRN} removed successfully."

            except sqlite3.Error as e:
                return f"SQL Error: {e}"

    # Print the student's enrolled courses
    def print_courses(self):
        with sqlite3.connect(DB_PATH) as cx: # Use DB_PATH constant
            cursor = cx.cursor()

            try:
                # Removed redundant student existence check

                # Get enrolled courses
                cursor.execute("SELECT CRN FROM ENROLLMENT WHERE STUDENT_ID = ?", (self.id,))
                enrolled_crns = [row[0] for row in cursor.fetchall()]
                
                if not enrolled_crns:
                    return "You are not enrolled in any courses."

                # Ensure all columns needed by Course constructor are selected
                query = f"SELECT CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS FROM COURSES WHERE CRN IN ({','.join(['?'] * len(enrolled_crns))})"
                cursor.execute(query, enrolled_crns)
                courses = cursor.fetchall()

                schedule_str = "Your Enrolled Courses:\n"
                for course in courses:
                    # Instantiate Course object for consistent display
                    course_obj = Course(course[0], course[1], course[2], course[3], course[4], course[5], course[6], course[7])
                    schedule_str += str(course_obj) + "\n\n" # Added extra newline here
                return schedule_str

            except sqlite3.Error as e:
                return f"SQL Error: {e}"


class StudentMenu(tk.Toplevel):
    def __init__(self, master, student_obj):
        """
        Initializes the StudentMenu GUI window.
        
        Args:
            master: The parent Tkinter window (e.g., the login window).
            student_obj: An instance of the Student class.
        """
        super().__init__(master)
        self.master = master
        self.student = student_obj
        self.title(f"Student Menu - {self.student.firstName} {self.student.lastName}")
        self.geometry("600x450") # Set a default size for the window (increased slightly for new button)
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges the GUI widgets for the student menu.
        """
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        self.main_frame = tk.Frame(self, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill="both")

        welcome_label = tk.Label(self.main_frame, text=f"Welcome, {self.student.firstName} {self.student.lastName}!", font=("Arial", 16, "bold"))
        welcome_label.pack(pady=10)

        # Buttons for student actions
        btn_print_all_courses = tk.Button(self.main_frame, text="Print All Courses", command=self.display_all_courses, width=30, height=2)
        btn_print_all_courses.pack(pady=5)

        btn_search_courses = tk.Button(self.main_frame, text="Search Courses", command=self.show_search_courses_menu, width=30, height=2)
        btn_search_courses.pack(pady=5)

        btn_print_schedule = tk.Button(self.main_frame, text="Print My Schedule", command=self.display_my_schedule, width=30, height=2)
        btn_print_schedule.pack(pady=5)

        btn_ar_course = tk.Button(self.main_frame, text="Add/Remove Courses from Schedule", command=self.show_ar_course_menu, width=30, height=2)
        btn_ar_course.pack(pady=5)

        btn_logout = tk.Button(self.main_frame, text="Logout", command=self.logout, width=30, height=2, bg="red", fg="white")
        btn_logout.pack(pady=20)

    def display_all_courses(self):
        """
        Calls `student.print_all_courses` to retrieve all course information
        and displays it in a scrollable text area.
        """
        self.clear_main_frame()
        tk.Label(self.main_frame, text="All Available Courses", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Student.print_all_courses no longer needs a cursor passed
        result = self.student.print_all_courses()
        self.result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=15, wrap=tk.WORD)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)
        self.result_text.pack(pady=10)
        
        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def show_search_courses_menu(self):
        """
        Displays the menu for searching courses.
        """
        self.clear_main_frame()
        
        tk.Label(self.main_frame, text="Search Courses", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Search by:").pack()
        self.search_by_var = tk.StringVar(self.main_frame)
        self.search_by_var.set("CRN") # default value
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
        Performs the course search based on user input and displays results.
        """
        search_keyword = self.search_by_var.get()
        search_value = self.search_value_entry.get().strip()

        if not search_value:
            messagebox.showwarning("Input Error", "Please enter a search value.")
            return

        if search_keyword == "CRN":
            try:
                search_value = int(search_value)
            except ValueError:
                messagebox.showerror("Input Error", "CRN must be a number.")
                return

        result = self.student.search_courses(search_keyword, search_value)
        self.result_text.delete(1.0, tk.END) # Clear previous results
        self.result_text.insert(tk.END, result)

    def display_my_schedule(self):
        """
        Displays the student's current schedule.
        """
        self.clear_main_frame()
        tk.Label(self.main_frame, text="My Current Schedule", font=("Arial", 14, "bold")).pack(pady=10)
        
        result = self.student.print_courses()
        self.result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=15, wrap=tk.WORD)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)
        self.result_text.pack(pady=10)
        
        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def show_ar_course_menu(self):
        """
        Displays the menu for adding/removing courses.
        """
        self.clear_main_frame()
        
        tk.Label(self.main_frame, text="Add/Remove Courses", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Enter Course CRN:").pack()
        self.ar_crn_entry = tk.Entry(self.main_frame, width=20)
        self.ar_crn_entry.pack(pady=5)

        btn_add = tk.Button(self.main_frame, text="Add Course", command=self.perform_add_course, width=20)
        btn_add.pack(pady=5)

        btn_remove = tk.Button(self.main_frame, text="Remove Course", command=self.perform_remove_course, width=20)
        btn_remove.pack(pady=5)

        self.ar_result_label = tk.Label(self.main_frame, text="", wraplength=400)
        self.ar_result_label.pack(pady=10)

        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def perform_add_course(self):
        """
        Performs adding a course to the student's schedule.
        """
        crn_str = self.ar_crn_entry.get().strip()
        if not crn_str:
            messagebox.showwarning("Input Error", "Please enter a CRN.")
            return
        try:
            crn = int(crn_str)
        except ValueError:
            messagebox.showerror("Input Error", "CRN must be a number.")
            return
        
        result = self.student.add_course(crn)
        self.ar_result_label.config(text=result)

    def perform_remove_course(self):
        """
        Performs removing a course from the student's schedule.
        """
        crn_str = self.ar_crn_entry.get().strip()
        if not crn_str:
            messagebox.showwarning("Input Error", "Please enter a CRN.")
            return
        try:
            crn = int(crn_str)
        except ValueError:
            messagebox.showerror("Input Error", "CRN must be a number.")
            return
        
        result = self.student.remove_course(crn)
        self.ar_result_label.config(text=result)

    def logout(self):
        """
        Handles the logout process, closing the student menu and showing the login window.
        """
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.destroy() # Close the student menu window
            self.master.deiconify() # Show the login window again
            messagebox.showinfo("Logout", "Logged out successfully.")

    def clear_main_frame(self):
        """
        Clears all widgets from the main frame to switch views.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()
