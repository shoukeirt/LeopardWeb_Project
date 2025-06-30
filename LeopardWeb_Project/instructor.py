#import User class
from user import User
import sqlite3

#Instructor subclass inheriting from User
class Instructor(User):
    def __init__(self, in_id, in_firstName,in_lastName, in_title, in_hireyear, in_dept, in_email):
        #Call the superclass (User) constructor
        super().__init__(in_firstName,in_lastName,in_id)
        self.title = in_title
        self.hireyear = in_hireyear
        self.dept = in_dept
        self.email = in_email;

    #Search for courses based on CRN (default) or Course Name (user-specified)
    def search_courses(self,Search_keyword='CRN',search_value=None):
        #Connect to the SQLite database
        cx=sqlite3.connect("assignment3.db")
        cursor=cx.cursor()

        #Normalize the keyword input for query matching
        if Search_keyword.upper() == "CRN":
            Search_keyword="CRN"
        elif Search_keyword.upper() in ["COURSE NAME","TITLE"]:
            Search_keyword="TITLE"
        else:
            #Exit if the keyword is not valid
            print("Invalid search keyword.")
            return

        #Format the value for SQL compatibility
        if isinstance(search_value,int):
            search_value=str(search_value)
        else:
            search_value=f"'{search_value}'"

        #Build and execute the SQL query
        query=f"SELECT * FROM COURSES WHERE {Search_keyword} = {search_value}"
        cursor.execute(query)

        #Fetch all matching rows and print them
        rows=cursor.fetchall()
        for row in rows:
            print(row)

    #Print the instructor's teaching schedule by matching instructor ID
    def print_schedule(self):
        #Connect to the SQLite database
        cx=sqlite3.connect("assignment3.db")
        cursor=cx.cursor()

        #Convert instructor ID to string
        instructor_id=str(self.id)

        #Query the COURSES table for any course taught by this instructor
        query=f"SELECT * FROM COURSES WHERE INSTRUCTOR_ID = {instructor_id}"
        cursor.execute(query)
        rows=cursor.fetchall()

        #Print all courses returned from the query
        print("Teaching Schedule:")
        for row in rows:
            print(row)

    #Search a specific CRN course and check if a given student is enrolled
    def search_roster(self,crn,student_name):
        #Connect to the SQLite database
        cx=sqlite3.connect("assignment3.db")
        cursor=cx.cursor()

        #Query the COURSES table to confirm the course exists
        query_course=f"SELECT * FROM COURSES WHERE CRN = {crn}"
        cursor.execute(query_course)
        course=cursor.fetchone()

        #If the course exists, continue to search for the student
        if course:
            print(f"Course found: {course[1]}")

            #Query the Student_Schedule table to check student enrollment
            query_student=f"SELECT * FROM Student_Schedule WHERE StudentName = '{student_name}' AND CRN = {crn}"
            cursor.execute(query_student)
            student=cursor.fetchone()

            #Print result based on presence of the student in the course
            if student:
                print(f"{student_name} is enrolled in CRN {crn}")
            else:
                print(f"{student_name} is NOT enrolled in CRN {crn}")
        else:
            #If course not found, inform the user
            print("Course not found.")

    #Print the full class roster for a specific course by CRN
    def print_roster(self,crn):
        #Connect to the SQLite database
        cx=sqlite3.connect("assignment3.db")
        cursor=cx.cursor()

        #Query for student names enrolled in the specified course
        query=f"SELECT StudentName FROM Student_Schedule WHERE CRN = {crn}"
        cursor.execute(query)
        rows=cursor.fetchall()

        #Display the roster
        print(f"Class Roster for CRN {crn}:")
        for row in rows:
            print(row[0])

    #Print all instructor information using existing print_name and print_id methods
    def print_all_info(self):
        print("ALL INSTRUCTOR INFO:")
        return"NAME: "+self.print_name()+"\\nID: "+self.print_id()+"\\n"
