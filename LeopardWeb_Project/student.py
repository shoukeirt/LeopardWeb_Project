#Written Harljen Hill
#Updated and Fixed and Implemented by Anthony Magliozzi

import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from user import User # Assuming User class is in user.py

# Database path
DB_PATH = "assignment3.db"

import datetime
#cx = sqlite3.connect("assignment3.db", timeout=5.0)
#cursor = cx.cursor()

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

        try:
            # Verify student exists
            cursor.execute("SELECT * FROM STUDENT WHERE ID = ? and NAME = ? and SURNAME = ?", 
                           (self.id, self.firstName, self.lastName))
            student = cursor.fetchone()
            if not student:
                return "Student not found."

            # Normalize search keyword
            if Search_keyword.upper() == "CRN":
                Search_keyword = "CRN"
            elif Search_keyword.upper() in ["COURSE NAME", "TITLE"]:
                Search_keyword = "TITLE"
            else:
                return "Invalid search keyword."

            # Execute course search
            cursor.execute(f"SELECT * FROM COURSES WHERE {Search_keyword} = ?", (search_value,))
            rows = cursor.fetchall()

            if rows:
                result_str = "Search Results:\n"
                for row in rows:
                    result_str += f"CRN: {row[0]}, Title: {row[1]}, Dept: {row[2]}, Time: {row[3]}, Days: {row[4]}, Semester: {row[5]}, Year: {row[6]}, Credits: {row[7]}\n"
                return result_str
            else:
                return "No courses found matching your criteria."
        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        finally:
            cx.close()

    # Add course to student schedule and check for time conflicts
    def add_course(self, CRN):
        cx = sqlite3.connect("assignment3.db", timeout=5.0)
        cursor = cx.cursor()

        try:
            # Get course information
            cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (CRN,))
            course = cursor.fetchone()

            if not course:
                return "Course not found."

            # Retrieve existing enrollments for the student
            cursor.execute("SELECT CRN FROM ENROLLMENT WHERE STUDENT_ID = ?", (self.id,))
            enrolled_crns = [row[0] for row in cursor.fetchall()]

            if CRN in enrolled_crns:
                return f"You are already enrolled in CRN {CRN}."

            # If the student is enrolled in any courses, check for time conflicts
            if enrolled_crns:
                query = f"SELECT CRN, TIME, DAYS FROM COURSES WHERE CRN IN ({','.join(['?'] * len(enrolled_crns))})"
                cursor.execute(query, enrolled_crns)
                enrolled_courses_details = cursor.fetchall()

                # Parse time and days from the course the student wants to add
                course_days = course[4]
                course_hour_start, course_hour_end = slipt_time(course[3])

                for enrolled_course_detail in enrolled_courses_details:
                    enrolled_crn, enrolled_time_str, enrolled_days = enrolled_course_detail
                    enrolled_hour_start, enrolled_hour_end = slipt_time(enrolled_time_str)

                    # Check for overlapping days and time ranges
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
        finally:
            cx.close()

    # Remove course from student schedule
    def remove_course(self, CRN):
        cx = sqlite3.connect("assignment3.db", timeout=5.0)
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
        finally:
            cx.close()

    # Print the student's enrolled courses
    def print_courses(self):
        cx = sqlite3.connect("assignment3.db", timeout=5.0)
        cursor = cx.cursor()

        try:
            # Verify student exists
            cursor.execute("SELECT * FROM STUDENT WHERE ID = ? and NAME = ? and SURNAME = ?", 
                           (self.id, self.firstName, self.lastName))
            student = cursor.fetchone()
            if not student:
                return "Student not found."

            # Get enrolled courses
            cursor.execute("SELECT CRN FROM ENROLLMENT WHERE STUDENT_ID = ?", (self.id,))
            enrolled_crns = [row[0] for row in cursor.fetchall()]
            
            if not enrolled_crns:
                return "You are not enrolled in any courses."

            query = f"SELECT CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, CREDITS FROM COURSES WHERE CRN IN ({','.join(['?'] * len(enrolled_crns))})"
            cursor.execute(query, enrolled_crns)
            courses = cursor.fetchall()

            schedule_str = "Your Enrolled Courses:\n"
            for course in courses:
                schedule_str += (f"CRN: {course[0]}, Title: {course[1]}, Dept: {course[2]}, Time: {course[3]}, "
                                 f"Days: {course[4]}, Semester: {course[5]}, Credits: {course[6]}\n")
            return schedule_str

        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        finally:
            cx.close()


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
        self.geometry("600x400") # Set a default size for the window
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
        btn_search_courses = tk.Button(self.main_frame, text="Search Courses", command=self.show_search_courses_menu, width=30, height=2)
        btn_search_courses.pack(pady=5)

        btn_print_schedule = tk.Button(self.main_frame, text="Print Course Schedule", command=self.display_schedule, width=30, height=2)
        btn_print_schedule.pack(pady=5)

        btn_ar_course = tk.Button(self.main_frame, text="Add/Remove Courses from Schedule", command=self.show_ar_course_menu, width=30, height=2)
        btn_ar_course.pack(pady=5)

        btn_logout = tk.Button(self.main_frame, text="Logout", command=self.logout, width=30, height=2, bg="red", fg="white")
        btn_logout.pack(pady=20)

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

    def display_schedule(self):
        """
        Displays the student's course schedule.
        """
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Your Course Schedule", font=("Arial", 14, "bold")).pack(pady=10)

        result = self.student.print_courses()
        self.result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=15, wrap=tk.WORD)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED) # Make text read-only
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
