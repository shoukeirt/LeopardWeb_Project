from os import remove
from user import User
import sqlite3
import datetime

class Admin(User):
    def __init__(self, in_firstName, in_lastName, in_id, cursor, cx):
        User.__init__(self, in_firstName, in_lastName, in_id)
        self.cursor = cursor
        self.cx = cx
        
    #methods    
    def add_course(self):
        new_crn = int(input("What is the CRN of the new course?"))
        new_title = input("What is the title of the course?")
        new_dep = input("What department is the new course in?")
        new_start = input("Enter time in HH:MM AM/PM format: ")
        try:
            time_start = datetime.datetime.strptime(new_start, "%I:%M %p").time()
            time_start_str = time_start.strftime("%H:%M:%S")

            print(f"You entered the time: {time_start_str}")
        except ValueError:
            print("Invalid time format. Please use HH:MM AM/PM.")
        new_days = input("What days of the week? (M/T/R Format)")
        new_sem = str(input("What semester will this course be available?"))
        new_year = int(input("What year will this course be available?"))
        credits = int(input("How many credits is this course?"))
        sql_command = """INSERT INTO COURSES (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS) VALUES (?, ?, ?, ?, ?, ?, ?,?)"""
        self.cursor.execute(sql_command,(new_crn, new_title, new_dep, time_start_str, new_days, new_sem, new_year, credits))  
        self.cx.commit() 
        return "Course Successfully Added!"
   
    def remove_course(self):
        remove_crn = int(input("What is the CRN of the course you would like to remove?"))
        sql_command = """SELECT * FROM COURSES WHERE CRN = ?"""
        self.cursor.execute(sql_command,(remove_crn,))  
        rows = self.cursor.fetchall()
        if any(remove_crn == row[0] for row in rows):
            print(f"----------Are you sure you want to delete this course?----------\n")
            for row in rows:
                print(row)
            confirm = int(input(" 1.) YES \n 2.) NO"))
            match confirm:
                case 1:
                    sql_command = """DELETE FROM COURSES WHERE CRN = ?"""
                    self.cursor.execute(sql_command,(remove_crn,))
                    self.cx.commit()
                    return ("Course Removed!")
                case 2:
                    print(f"You have selected to not delete CRN {remove_crn}")
                    return
    
    def add_user(self):
        new_id = int(input("What is the ID of the new student?"))
        new_fname = str(input("What is the first name of the new student?"))
        new_lname = str(input("What is the surname of the new student?"))
        new_gradyear = int(input("What year does the new student graduate?"))
        new_major = str(input("What is the students major? (BSAS format)"))
        new_email = (new_lname + new_fname[0]).lower()
        sql_command = """INSERT INTO STUDENT (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL) VALUES (?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(sql_command, (new_id, new_fname, new_lname, new_gradyear, new_major, new_email))
        self.cx.commit()
 
    def remove_user(self):
          return"This is the function that removes a user from the system"


    def add_instructor(self):
        new_id = int(input("What is the ID of the new instructor?"))
        new_fname = str(input("What is the first name of the new instructor?"))
        new_lname = str(input("What is the surname of the new instructor?"))
        new_title = str(input("What yis the title of the new instructor?"))
        new_hireyear = int(input("What year was the new instructor hired?"))
        new_dept = str(input("What department is the new instructor in?"))
        new_email = (new_lname + new_fname[0]).lower()
        sql_command = """INSERT INTO INSTRUCTOR (ID, NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL) VALUES (?, ?, ?, ?, ?, ?,?)"""
        self.cursor.execute(sql_command, (new_id, new_fname, new_lname, new_title, new_hireyear, new_dept, new_email))
        self.cx.commit()
        return"This is the function that adds an instructor to the system"
    
    def add_to_course(self):
          return"This is the function that adds a student to a course"

    def remove_from_course(self):
          return"This is the function that removes a student from a course"

    def print_schedule(self):
          return "This is the print schedule function!"
    
    def print_classlist(self):
         return "This is the print classlist function!"
    
    def search_courses(self,search_keyword='CRN',search_value=None):
        #Connect to the SQLite database
        #Normalize the keyword input for query matching
        if search_keyword.upper() == "CRN":
            search_keyword="CRN"
        elif search_keyword.upper() in ["COURSE NAME","TITLE"]:
            search_keyword="TITLE"
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
        query=f"SELECT * FROM COURSES WHERE {search_keyword} = {search_value}"
        self.cursor.execute(query)

        #Fetch all matching rows and print them
        rows=self.cursor.fetchall()
        for row in rows:
            print(row)

    def print_courses(self):
          return "This is the function to print courses"
    
    def search_roster(self):
          return "This is the function to seach the roster"

    def print_roster(self):
          return "This is the function to print a roster"
   
    
    
    
    

    
