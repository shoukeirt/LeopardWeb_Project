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





class StudentMenu(tk.Toplevel):
    def __init__(self, master, student_obj):
        """
        Initializes the StudentMenu GUI window.
        
        Args:
            master: The parent Tkinter window (e.g., the login window).
            student_obj: An instance of the Instructor class.
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

        #add/remove course   #Time conflict is inside this funciton since adding a course involves checking for time conflicts
        btn_ar_course = tk.Button(self.main_frame, text="Add/Remove Courses from Schedule", command=self.show_ar_course_menu, width=30, height=2)
        btn_ar_course.pack(pady=5)


        btn_logout = tk.Button(self.main_frame, text="Logout", command=self.logout, width=30, height=2, bg="red", fg="white")
        btn_logout.pack(pady=20)

    def show_search_courses_menu(self):
        """
        Displays the menu for searching courses.
        """
        self.clear_main_frame()
        
        # Labels and entry for search keyword and value
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

        # Attempt to convert CRN to int if selected
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

        result = self.student.print_schedule()
        self.result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=15, wrap=tk.WORD)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED) # Make text read-only
        self.result_text.pack(pady=10)

        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def show_search_classlist_menu(self):
        """
        Displays the menu for searching a student in a classlist.
        """
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Search Student in Classlist", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Enter Course CRN:").pack()
        self.crn_entry_search_roster = tk.Entry(self.main_frame, width=20)
        self.crn_entry_search_roster.pack(pady=5)

        btn_search = tk.Button(self.main_frame, text="Search Student", command=self.perform_search_classlist, width=20)
        btn_search.pack(pady=10)

        self.result_label_search_roster = tk.Label(self.main_frame, text="", wraplength=400)
        self.result_label_search_roster.pack(pady=10)

        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def perform_search_classlist(self):
        """
        Performs the search for a student in a classlist and displays the result.
        """
        crn_str = self.crn_entry_search_roster.get().strip()
        if not crn_str:
            messagebox.showwarning("Input Error", "Please enter a CRN.")
            return
        try:
            crn = int(crn_str)
        except ValueError:
            messagebox.showerror("Input Error", "CRN must be a number.")
            return
        
        result = self.student.search_roster(crn)
        self.result_label_search_roster.config(text=result)


    def show_print_classlist_menu(self):
        """
        Displays the menu for printing a classlist.
        """
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Print Classlist", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Enter Course CRN:").pack()
        self.crn_entry_print_roster = tk.Entry(self.main_frame, width=20)
        self.crn_entry_print_roster.pack(pady=5)

        btn_print = tk.Button(self.main_frame, text="Print Roster", command=self.perform_print_classlist, width=20)
        btn_print.pack(pady=10)

        self.result_text_print_roster = scrolledtext.ScrolledText(self.main_frame, width=70, height=15, wrap=tk.WORD)
        self.result_text_print_roster.pack(pady=10)

        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def perform_print_classlist(self):
        """
        Performs the printing of a classlist and displays the result.
        """
        crn_str = self.crn_entry_print_roster.get().strip()
        if not crn_str:
            messagebox.showwarning("Input Error", "Please enter a CRN.")
            return
        try:
            crn = int(crn_str)
        except ValueError:
            messagebox.showerror("Input Error", "CRN must be a number.")
            return
        
        result = self.student.print_roster(crn)
        self.result_text_print_roster.delete(1.0, tk.END)
        self.result_text_print_roster.insert(tk.END, result)


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
