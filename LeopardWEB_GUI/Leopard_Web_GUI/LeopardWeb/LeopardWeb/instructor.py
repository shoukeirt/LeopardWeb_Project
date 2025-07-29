import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from user import User # Assuming User class is in user.py

# Database path
DB_PATH = "assignment3.db"

class Instructor(User):
    def __init__(self, in_firstName, in_lastName, in_id, in_title, in_hireyear, in_dept, in_email):
        super().__init__(in_firstName, in_lastName, in_id)
        self.title = in_title
        self.hireyear = in_hireyear
        self.dept = in_dept
        self.email = in_email

    def search_courses(self, search_keyword='CRN', search_value=None):
        """
        Searches for courses based on a keyword (CRN or TITLE) and a search value.
        Returns a list of course rows or an error message.
        """
        cx = sqlite3.connect(DB_PATH)
        cursor = cx.cursor()
        try:
            if search_keyword.upper() == "CRN":
                Search_keyword = "CRN"
            elif search_keyword.upper() in ["COURSE NAME", "TITLE"]:
                Search_keyword = "TITLE"
            else:
                return "Invalid search keyword."

            # Format the value for SQL compatibility
            if isinstance(search_value, int):
                search_value = str(search_value)
            
            # Build and execute the SQL query
            query = f"SELECT * FROM COURSES WHERE {Search_keyword} = ?"
            cursor.execute(query, (search_value,))
            rows = cursor.fetchall()
            
            if rows:
                # Prepare a formatted string of results
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

    def print_schedule(self):
        """
        Prints the instructor's teaching schedule.
        Returns a formatted string of the schedule or a message if no courses are assigned.
        """
        cx = sqlite3.connect(DB_PATH)
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
                schedule_str = "Your Teaching Schedule:\n"
                for row in rows:
                    schedule_str += (f"CRN: {row[0]}, Title: {row[1]}, Dept: {row[2]}, Time: {row[3]}, "
                                     f"Days: {row[4]}, Semester: {row[5]}, Credits: {row[6]}\n")
                return schedule_str
            else:
                return "You are not assigned to any courses."
        except sqlite3.OperationalError as e:
            return f"SQL Error: {e}"
        finally:
            cx.close()

    def search_roster(self, crn):
        """
        Searches for a specific student in the roster of a given course.
        Returns a message indicating if the student is enrolled or not.
        """
        cx = sqlite3.connect(DB_PATH)
        cursor = cx.cursor()
        try:
            # Verify instructor is assigned to teach this course
            cursor.execute("SELECT * FROM COURSE_TEACHER WHERE INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ? AND CRN = ?",
                           (self.firstName, self.lastName, crn))
            if not cursor.fetchone():
                return f"Access denied: You are not assigned to teach the course with CRN {crn}."

            # Get student full name from GUI input
            first = simpledialog.askstring("Search Student", "Enter the student's FIRST name:")
            last = simpledialog.askstring("Search Student", "Enter the student's LAST name:")
            
            if not first or not last:
                return "Student names cannot be empty."

            full_name = f"{first.strip()} {last.strip()}"

            # Check if the course exists
            cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (crn,))
            course = cursor.fetchone()
            if not course:
                return "Course not found."
            
            # Find the name column in Student_Schedule table
            cursor.execute("PRAGMA table_info(Student_Schedule)")
            col_names = [desc[1] for desc in cursor.fetchall()]
            name_column = next((col for col in col_names if col.lower() in ['studentname', 'name', 'fullname', 'student', 'student name']), None)
            
            if not name_column:
                return "Error: Could not find student name column in Student_Schedule."

            # Find CRN columns in Student_Schedule table
            crn_columns = [col for col in col_names if col.startswith('CRN')]
            
            enrolled = False
            for crn_col in crn_columns:
                cursor.execute(f'SELECT * FROM Student_Schedule WHERE "{name_column}" = ? AND "{crn_col}" = ?', (full_name, crn))
                if cursor.fetchone():
                    enrolled = True
                    break

            if enrolled:
                return f"{full_name} is enrolled in CRN {crn}."
            else:
                return f"{full_name} is NOT enrolled in CRN {crn}."
        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        finally:
            cx.close()

    def print_roster(self, crn):
        """
        Prints the full class roster for a given course.
        Returns a formatted string of the roster or a message if no students are enrolled.
        """
        cx = sqlite3.connect(DB_PATH)
        cursor = cx.cursor()
        try:
            # Verify instructor is assigned to teach this course
            cursor.execute("SELECT * FROM COURSE_TEACHER WHERE INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ? AND CRN = ?",
                           (self.firstName, self.lastName, crn))
            if not cursor.fetchone():
                return f"Access denied: You are not assigned to teach the course with CRN {crn}."

            # Find the name column in Student_Schedule table
            cursor.execute("PRAGMA table_info(Student_Schedule)")
            col_names = [desc[1] for desc in cursor.fetchall()]
            name_column = next((col for col in col_names if col.lower() in ['studentname', 'name', 'fullname', 'student', 'student name']), None)
            
            if not name_column:
                return "Error: Could not find student name column in Student_Schedule."

            # Find CRN columns in Student_Schedule table
            crn_columns = [col for col in col_names if col.startswith('CRN')]
            
            enrolled_students = set()
            for crn_col in crn_columns:
                cursor.execute(f'SELECT "{name_column}" FROM Student_Schedule WHERE "{crn_col}" = ?', (crn,))
                for result in cursor.fetchall():
                    enrolled_students.add(result[0])

            if enrolled_students:
                roster_str = f"Class Roster for CRN {crn}:\n"
                for student in sorted(enrolled_students):
                    roster_str += f"- {student}\n"
                return roster_str
            else:
                return f"No students enrolled in CRN {crn}."
        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        finally:
            cx.close()


class InstructorMenu(tk.Toplevel):
    def __init__(self, master, instructor_obj):
        """
        Initializes the InstructorMenu GUI window.
        
        Args:
            master: The parent Tkinter window (e.g., the login window).
            instructor_obj: An instance of the Instructor class.
        """
        super().__init__(master)
        self.master = master
        self.instructor = instructor_obj
        self.title(f"Instructor Menu - {self.instructor.firstName} {self.instructor.lastName}")
        self.geometry("600x400") # Set a default size for the window
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges the GUI widgets for the instructor menu.
        """
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        self.main_frame = tk.Frame(self, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill="both")

        welcome_label = tk.Label(self.main_frame, text=f"Welcome, {self.instructor.firstName} {self.instructor.lastName}!", font=("Arial", 16, "bold"))
        welcome_label.pack(pady=10)

        # Buttons for instructor actions
        btn_search_courses = tk.Button(self.main_frame, text="Search Courses", command=self.show_search_courses_menu, width=30, height=2)
        btn_search_courses.pack(pady=5)

        btn_print_schedule = tk.Button(self.main_frame, text="Print Course Schedule", command=self.display_schedule, width=30, height=2)
        btn_print_schedule.pack(pady=5)

        btn_search_classlist = tk.Button(self.main_frame, text="Search Classlist", command=self.show_search_classlist_menu, width=30, height=2)
        btn_search_classlist.pack(pady=5)

        btn_print_classlist = tk.Button(self.main_frame, text="Print Classlist", command=self.show_print_classlist_menu, width=30, height=2)
        btn_print_classlist.pack(pady=5)

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

        result = self.instructor.search_courses(search_keyword, search_value)
        self.result_text.delete(1.0, tk.END) # Clear previous results
        self.result_text.insert(tk.END, result)


    def display_schedule(self):
        """
        Displays the instructor's course schedule.
        """
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Your Course Schedule", font=("Arial", 14, "bold")).pack(pady=10)

        result = self.instructor.print_schedule()
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
        
        result = self.instructor.search_roster(crn)
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
        
        result = self.instructor.print_roster(crn)
        self.result_text_print_roster.delete(1.0, tk.END)
        self.result_text_print_roster.insert(tk.END, result)


    def logout(self):
        """
        Handles the logout process, closing the instructor menu and showing the login window.
        """
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.destroy() # Close the instructor menu window
            self.master.deiconify() # Show the login window again
            messagebox.showinfo("Logout", "Logged out successfully.")

    def clear_main_frame(self):
        """
        Clears all widgets from the main frame to switch views.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()
