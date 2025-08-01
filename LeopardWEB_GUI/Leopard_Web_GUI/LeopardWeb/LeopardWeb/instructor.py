import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from user import User # Assuming User class is in user.py

# Database path for the SQLite database connection
DB_PATH = "assignment3.db"

# --- Classes for Database Interaction (Instructor's perspective) ---
# These classes encapsulate data when interacting with the database,
# ensuring that data is handled as objects rather than raw tuples/lists.

class Course:
    """
    Represents a course with its various attributes such as CRN, title, department,
    time, days, semester, year, and credits. This class is used to create
    course objects from database queries, facilitating object-oriented interaction
    with course information. It's a general representation of a course.
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
        Returns a string representation of the Course object, suitable for printing
        and displaying course details in a readable format.
        """
        return (f"CRN: {self.crn}, Title: {self.title}, Dept: {self.dept}, "
                f"Time: {self.time}, Days: {self.days}, Semester: {self.semester}, "
                f"Year: {self.year}, Credits: {self.credits}")

class EnrolledStudent:
    """
    Represents a student enrolled in a course. This class is specifically used
    when retrieving and displaying student names from class rosters, providing
    a simple object to hold the student's full name.
    """
    def __init__(self, student_name):
        """
        Initializes an EnrolledStudent object with the student's full name.

        Args:
            student_name (str): The full name of the enrolled student.
        """
        self.student_name = student_name

    def __str__(self):
        """
        Returns the student's full name as a string.
        """
        return self.student_name

# --- End New Classes ---

class Instructor(User):
    """
    The Instructor class inherits from the User class and provides comprehensive
    functionalities specific to an instructor within the university system.
    This includes searching for courses, viewing their teaching schedule,
    and managing (searching/printing) class rosters.
    It interacts directly with the SQLite database using provided connection and cursor.
    """
    def __init__(self, in_firstName, in_lastName, in_id, in_title, in_hireyear, in_dept, in_email):
        """
        Initializes an Instructor object.

        Args:
            in_firstName (str): The first name of the instructor.
            in_lastName (str): The last name of the instructor.
            in_id (int): The unique ID of the instructor.
            in_title (str): The academic title of the instructor (e.g., "Professor", "Lecturer").
            in_hireyear (int): The year the instructor was hired.
            in_dept (str): The department the instructor belongs to.
            in_email (str): The email address of the instructor.
        """
        super().__init__(in_firstName, in_lastName, in_id)
        self.title = in_title
        self.hireyear = in_hireyear
        self.dept = in_dept
        self.email = in_email

    def print_all_courses(self):
        """
        Retrieves all available courses from the COURSES table in the database
        and formats them into a readable string with an empty line between courses.

        Returns:
            str: A formatted string listing all courses, or a message if no courses are found.
        """
        cx = sqlite3.connect(DB_PATH)
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
                    result_str += str(course_obj) + "\n\n" # Add an extra newline here
                return result_str
            else:
                return "No courses found in the system."
        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        finally:
            cx.close()

    def search_courses(self, search_keyword='CRN', search_value=None):
        """
        Searches for courses based on a keyword (CRN or TITLE) and a search value.
        Retrieves course data from the database and converts each row into a `Course` object.
        Returns a formatted string of `Course` objects found or an error message if none are found
        or an invalid search keyword is provided.

        Args:
            search_keyword (str): The criterion to search by, either "CRN" or "TITLE".
            search_value (str or int): The value to search for (e.g., a CRN number or a course title).

        Returns:
            str: A string containing the search results (formatted `Course` objects) or an error/info message.
        """
        cx = sqlite3.connect(DB_PATH)
        cursor = cx.cursor()
        try:
            # Determine the correct database column to search based on the keyword
            if search_keyword.upper() == "CRN":
                Search_keyword = "CRN"
            elif search_keyword.upper() in ["COURSE NAME", "TITLE"]:
                Search_keyword = "TITLE"
            else:
                return "Invalid search keyword. Please use 'CRN' or 'TITLE'."

            # Ensure search_value is a string for SQL query compatibility, especially for CRN
            if isinstance(search_value, int):
                search_value = str(search_value)
            
            # Construct and execute the SQL query to fetch course details
            # All columns necessary to instantiate a Course object are selected
            query = f"SELECT CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS FROM COURSES WHERE {Search_keyword} = ?"
            cursor.execute(query, (search_value,))
            rows = cursor.fetchall()
            
            if rows:
                # Iterate through the fetched rows and convert each into a Course object
                courses = [Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in rows]
                
                # Build a formatted string of results by calling the __str__ method of each Course object
                result_str = "Search Results:\n"
                for course in courses:
                    result_str += str(course) + "\n\n" # Added extra newline here
                return result_str
            else:
                return "No courses found matching your criteria."
        except sqlite3.Error as e:
            # Catch any SQLite database errors and return an informative message
            return f"SQL Error: {e}"
        finally:
            # Ensure the database connection is closed
            cx.close()

    def print_schedule(self):
        """
        Prints the instructor's teaching schedule.
        Retrieves course data for the instructor from the `COURSE_TEACHER` table and
        converts each row into a `Course` object.
        Returns a formatted string of the schedule using `Course` objects or a message
        if the instructor is not assigned to any courses.

        Returns:
            str: A string containing the instructor's schedule (formatted `Course` objects) or an info message.
        """
        cx = sqlite3.connect(DB_PATH)
        cursor = cx.cursor()
        try:
            # Query to select courses assigned to the current instructor based on their first and last name
            query = """
            SELECT COURSE_TEACHER.CRN, COURSE_TEACHER.TITLE, COURSE_TEACHER.DEPARTMENT,
                   COURSE_TEACHER.TIME, COURSE_TEACHER.DAYS, COURSE_TEACHER.SEMESTER, COURSE_TEACHER.CREDITS
            FROM COURSE_TEACHER
            WHERE INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ?
            """
            cursor.execute(query, (self.firstName, self.lastName))
            rows = cursor.fetchall()
            if rows:
                # Create `Course` objects from the fetched schedule data.
                # Note: The 'YEAR' column might not be present in `COURSE_TEACHER`,
                # so 'None' is used as a placeholder if not available to match Course object's constructor.
                schedule_courses = [Course(row[0], row[1], row[2], row[3], row[4], row[5], None, row[6]) for row in rows]
                
                schedule_str = "Your Teaching Schedule:\n"
                # Iterate through the `Course` objects and build the schedule string
                for course in schedule_courses:
                    # Access attributes directly from the `Course` object for display
                    schedule_str += (f"CRN: {course.crn}, Title: {course.title}, Dept: {course.dept}, Time: {course.time}, "
                                     f"Days: {course.days}, Semester: {course.semester}, Credits: {course.credits}\n\n") # Added extra newline
                return schedule_str
            else:
                return "You are not assigned to any courses."
        except sqlite3.OperationalError as e:
            # Catch database operation errors (e.g., table not found)
            return f"SQL Error: {e}"
        finally:
            cx.close()

    def search_roster(self, crn):
        """
        Searches for a specific student in the roster of a given course.
        It first verifies if the instructor is assigned to teach the course to ensure authorization.
        When checking for course existence, a temporary `Course` object is created to
        demonstrate object interaction. When a student is found, an `EnrolledStudent`
        object is created to encapsulate their name.
        Prompts the user for student's first and last name via a simple dialog.

        Args:
            crn (int): The CRN of the course whose roster is to be searched.

        Returns:
            str: A message indicating if the student is enrolled or not, or an access denied/error message.
        """
        cx = sqlite3.connect(DB_PATH)
        cursor = cx.cursor()
        try:
            # First, verify if the instructor is authorized to view this course's roster
            cursor.execute("SELECT * FROM COURSE_TEACHER WHERE INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ? AND CRN = ?",
                           (self.firstName, self.lastName, crn))
            if not cursor.fetchone():
                return f"Access denied: You are not assigned to teach the course with CRN {crn}."

            # Use Tkinter's simpledialog to get student's first and last name from the user
            first = simpledialog.askstring("Search Student", "Enter the student's FIRST name:")
            last = simpledialog.askstring("Search Student", "Enter the student's LAST name:")
            
            if not first or not last:
                return "Student names cannot be empty."

            full_name_input = f"{first.strip()} {last.strip()}"

            # Check if the course exists by fetching its details and creating a temporary `Course` object
            cursor.execute("SELECT CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS FROM COURSES WHERE CRN = ?", (crn,))
            course_data = cursor.fetchone()
            if not course_data:
                return "Course not found."
            # A temporary `Course` object is created here to show that even for checks,
            # data can be brought into an object (though not strictly necessary for this specific check).
            temp_course = Course(course_data[0], course_data[1], course_data[2], course_data[3], course_data[4], course_data[5], course_data[6], course_data[7])
            
            # Dynamically find the column that stores student names in the `Student_Schedule` table
            # This makes the code more robust to variations in column naming (e.g., 'StudentName', 'name').
            cursor.execute("PRAGMA table_info(Student_Schedule)")
            col_names = [desc[1] for desc in cursor.fetchall()]
            name_column = next((col for col in col_names if col.lower() in ['studentname', 'name', 'fullname', 'student', 'student name']), None)
            
            if not name_column:
                return "Error: Could not find student name column in Student_Schedule."

            # Dynamically find columns that store CRNs in `Student_Schedule` (e.g., CRN1, CRN2, etc.)
            crn_columns = [col for col in col_names if col.startswith('CRN')]
            
            enrolled = False
            found_student_obj = None # Will store the `EnrolledStudent` object if found
            # Iterate through potential CRN columns in the `Student_Schedule` table to find the student's enrollment
            for crn_col in crn_columns:
                cursor.execute(f'SELECT "{name_column}" FROM Student_Schedule WHERE "{name_column}" = ? AND "{crn_col}" = ?', (full_name_input, crn))
                student_row = cursor.fetchone()
                if student_row:
                    # Create an `EnrolledStudent` object for the found student
                    found_student_obj = EnrolledStudent(student_row[0]) 
                    enrolled = True
                    break

            if enrolled:
                # Use the student object's attribute (`student_name`) for the output message
                return f"{found_student_obj.student_name} is enrolled in CRN {temp_course.crn}."
            else:
                return f"{full_name_input} is NOT enrolled in CRN {temp_course.crn}."
        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        finally:
            cx.close()

    def print_roster(self, crn):
        """
        Prints the full class roster for a given course.
        It first verifies if the instructor is assigned to teach the course to ensure authorization.
        Retrieves student names for the specified CRN from the database and
        converts each into an `EnrolledStudent` object.
        Returns a formatted string of the roster using `EnrolledStudent` objects or a message
        if no students are enrolled or access is denied.

        Args:
            crn (int): The CRN of the course whose roster is to be printed.

        Returns:
            str: A string containing the class roster (formatted `EnrolledStudent` objects) or an info/error message.
        """
        cx = sqlite3.connect(DB_PATH)
        cursor = cx.cursor()
        try:
            # Verify instructor authorization to view this course's roster
            cursor.execute("SELECT * FROM COURSE_TEACHER WHERE INSTRUCTOR_NAME = ? AND INSTRUCTOR_SURNAME = ? AND CRN = ?",
                           (self.firstName, self.lastName, crn))
            if not cursor.fetchone():
                return f"Access denied: You are not assigned to teach the course with CRN {crn}."

            # Dynamically find the student name column in `Student_Schedule` table
            cursor.execute("PRAGMA table_info(Student_Schedule)")
            col_names = [desc[1] for desc in cursor.fetchall()]
            name_column = next((col for col in col_names if col.lower() in ['studentname', 'name', 'fullname', 'student', 'student name']), None)
            
            if not name_column:
                return "Error: Could not find student name column in Student_Schedule."

            # Dynamically find all CRN columns in `Student_Schedule` (e.g., CRN1, CRN2, CRN3, CRN4)
            crn_columns = [col for col in col_names if col.startswith('CRN')]
            
            enrolled_students = set() # Use a set to automatically handle duplicate student entries
            # Iterate through all CRN columns to collect all students enrolled in the specified CRN
            for crn_col in crn_columns:
                cursor.execute(f'SELECT "{name_column}" FROM Student_Schedule WHERE "{crn_col}" = ?', (crn,))
                for result in cursor.fetchall():
                    # Create an `EnrolledStudent` object for each student found and add to the set
                    enrolled_students.add(EnrolledStudent(result[0])) 

            if enrolled_students:
                roster_str = f"Class Roster for CRN {crn}:\n"
                # Convert the set to a list and sort students by name for consistent output
                sorted_students = sorted(list(enrolled_students), key=lambda s: s.student_name)
                for student_obj in sorted_students:
                    # Access the student name attribute directly from the `EnrolledStudent` object
                    roster_str += f"- {student_obj.student_name}\n\n" # Added extra newline here
                return roster_str
            else:
                return f"No students enrolled in CRN {crn}."
        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        finally:
            cx.close()


class InstructorMenu(tk.Toplevel):
    """
    Implements the graphical user interface (GUI) for the instructor menu.
    This class handles the display of instructor options and triggers the corresponding
    methods in the `Instructor` object based on user interactions. It provides forms
    and displays results for various instructor tasks.
    """
    def __init__(self, master, instructor_obj):
        """
        Initializes the InstructorMenu GUI window.
        
        Args:
            master: The parent Tkinter window (e.g., the login window).
            instructor_obj: An instance of the Instructor class, representing the logged-in instructor.
        """
        super().__init__(master)
        self.master = master
        self.instructor = instructor_obj
        self.title(f"Instructor Menu - {self.instructor.firstName} {self.instructor.lastName}")
        self.geometry("600x450") # Set a default size for the window
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges the primary GUI widgets for the instructor main menu.
        This includes a welcome message and buttons for various instructor actions.
        """
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        self.main_frame = tk.Frame(self, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill="both")

        welcome_label = tk.Label(self.main_frame, text=f"Welcome, {self.instructor.firstName} {self.instructor.lastName}!", font=("Arial", 16, "bold"))
        welcome_label.pack(pady=10)

        # Buttons for instructor actions, each linked to a specific method
        btn_print_all_courses = tk.Button(self.main_frame, text="Print All Courses", command=self.display_all_courses, width=30, height=2)
        btn_print_all_courses.pack(pady=5)

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

    def display_all_courses(self):
        """
        Calls `instructor.print_all_courses` to retrieve all course information
        and displays it in a scrollable text area.
        """
        self.clear_main_frame()

        tk.Label(self.main_frame, text="All Available Courses", font=("Arial", 14, "bold")).pack(pady=10)

        result = self.instructor.print_all_courses() # This will now call the method in Instructor class
        self.result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=15, wrap=tk.WORD)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED) # Make the text area read-only
        self.result_text.pack(pady=10)

        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def show_search_courses_menu(self):
        """
        Displays the specific GUI elements for searching courses.
        This includes input fields for search keyword (CRN/TITLE) and search value,
        and a scrolled text area to display results.
        """
        self.clear_main_frame()
        
        # Labels and entry for search keyword and value
        tk.Label(self.main_frame, text="Search Courses", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Search by:").pack()
        self.search_by_var = tk.StringVar(self.main_frame)
        self.search_by_var.set("CRN") # Set default search option
        search_by_option = tk.OptionMenu(self.main_frame, self.search_by_var, "CRN", "TITLE")
        search_by_option.pack(pady=5)

        tk.Label(self.main_frame, text="Search Value:").pack()
        self.search_value_entry = tk.Entry(self.main_frame, width=40)
        self.search_value_entry.pack(pady=5)

        btn_search = tk.Button(self.main_frame, text="Search", command=self.perform_search_courses, width=20)
        btn_search.pack(pady=10)

        # ScrolledText widget to display potentially long search results
        self.result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=10, wrap=tk.WORD)
        self.result_text.pack(pady=10)

        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def perform_search_courses(self):
        """
        Performs the course search operation based on user input from the GUI.
        It retrieves the search keyword and value, validates them, and then calls
        the `instructor.search_courses` method. The result is displayed in the GUI.
        """
        search_keyword = self.search_by_var.get()
        search_value = self.search_value_entry.get().strip()

        if not search_value:
            messagebox.showwarning("Input Error", "Please enter a search value.")
            return

        # Validate CRN input to ensure it's a number if searching by CRN
        if search_keyword == "CRN":
            try:
                search_value = int(search_value)
            except ValueError:
                messagebox.showerror("Input Error", "CRN must be a number.")
                return

        # Call the instructor object's method which now returns formatted string of Course objects
        result = self.instructor.search_courses(search_keyword, search_value)
        self.result_text.delete(1.0, tk.END) # Clear previous results from the text area
        self.result_text.insert(tk.END, result) # Insert new results


    def display_schedule(self):
        """
        Displays the instructor's course schedule in a scrolled text area.
        It calls the `instructor.print_schedule` method and shows the returned formatted string.
        """
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Your Course Schedule", font=("Arial", 14, "bold")).pack(pady=10)

        # Call the instructor object's method which returns formatted string of Course objects
        result = self.instructor.print_schedule()
        self.result_text = scrolledtext.ScrolledText(self.main_frame, width=70, height=15, wrap=tk.WORD)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED) # Make the text area read-only
        self.result_text.pack(pady=10)

        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def show_search_classlist_menu(self):
        """
        Displays the GUI elements for searching a student within a classlist (roster).
        This includes an input field for the course CRN and a label to display the search result.
        It also includes a note about case sensitivity for student names.
        """
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Search Student in Classlist", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Enter Course CRN:").pack()
        self.crn_entry_search_roster = tk.Entry(self.main_frame, width=20)
        self.crn_entry_search_roster.pack(pady=5)

        # Add the note about case sensitivity for student names
        tk.Label(self.main_frame, text="Note: Student name is case sensitive.", fg="blue", font=("Arial", 10, "italic")).pack(pady=5)

        btn_search = tk.Button(self.main_frame, text="Search Student", command=self.perform_search_classlist, width=20)
        btn_search.pack(pady=10)

        # Label to display the outcome of the student search
        self.result_label_search_roster = tk.Label(self.main_frame, text="", wraplength=400)
        self.result_label_search_roster.pack(pady=10)

        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def perform_search_classlist(self):
        """
        Performs the search for a student in a classlist based on the entered CRN.
        It validates the CRN and then calls the `instructor.search_roster` method.
        The result message returned from the `Instructor` object is then displayed in the GUI.
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
        
        # Call the instructor object's method; it handles internal object creation and returns a string message
        result = self.instructor.search_roster(crn)
        self.result_label_search_roster.config(text=result) # Update the label with the result


    def show_print_classlist_menu(self):
        """
        Displays the GUI elements for printing the full classlist (roster) of a course.
        This includes an input field for the course CRN and a scrolled text area
        to display the full roster.
        """
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Print Classlist", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Enter Course CRN:").pack()
        self.crn_entry_print_roster = tk.Entry(self.main_frame, width=20)
        self.crn_entry_print_roster.pack(pady=5)

        btn_print = tk.Button(self.main_frame, text="Print Roster", command=self.perform_print_classlist, width=20)
        btn_print.pack(pady=10)

        # ScrolledText widget to display the class roster
        self.result_text_print_roster = scrolledtext.ScrolledText(self.main_frame, width=70, height=15, wrap=tk.WORD)
        self.result_text_print_roster.pack(pady=10)

        btn_back = tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_widgets, width=20)
        btn_back.pack(pady=10)

    def perform_print_classlist(self):
        """
        Performs the operation to print the full classlist for a given CRN.
        It validates the CRN and then calls the `instructor.print_roster` method.
        The returned formatted roster string is displayed in the GUI.
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
        
        # Call the instructor object's method; it handles internal object creation and returns a string
        result = self.instructor.print_roster(crn)
        self.result_text_print_roster.delete(1.0, tk.END) # Clear previous roster
        self.result_text_print_roster.insert(tk.END, result) # Display new roster


    def logout(self):
        """
        Handles the logout process for the instructor.
        Asks for user confirmation, closes the instructor menu window,
        and re-displays (deiconifies) the parent login window.
        """
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.destroy() # Close the instructor menu window
            self.master.deiconify() # Show the login window again
            messagebox.showinfo("Logout", "Logged out successfully.")

    def clear_main_frame(self):
        """
        Utility method to clear all widgets from the `main_frame`.
        This is typically called before redrawing the GUI for a new menu or operation,
        preventing widgets from overlapping.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()
