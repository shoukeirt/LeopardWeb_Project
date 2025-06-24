from user import User
import sqlite3
import datetime

cursor = database.cursor() 

class Admin(User):
    def __init__(self, in_firstName, in_lastName, in_id):
        User.__init__(self, in_firstName, in_lastName, in_id)
        
    #methods    
    def add_course(self):
        new_crn = int(input("What is the CRN of the new course?"))
        new_title = input("What is the title of the course?")
        new_dep = input("What department is the new course in?")
        new_start = input("Enter time in HH:MM AM/PM format: ")
        try:
            time = datetime.strptime(new_start, "%I:%M %p").time()
            print(f"You entered the time: {time}")
        except ValueError:
            print("Invalid time format. Please use HH:MM AM/PM.")
        new_days = input("What days of the week? (M/T/R Format)")
        new_sem = int(input("What semester will this course be available?"))
        new_year = int(input("What year will this course be available?"))
        credits = int(input("How many credits is this course?"))
        sql_command = """("INSERT INTO COURSES (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS)) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(sql_command,(new_crn, new_title, new_dep, new_start, new_days, new_year, credits))  
        return "Course Successfully Added!"

    def remove_course(self):
         return"This it the function that removes a course from the classlist"
    
    def add_user(self):
          return"This is the function that adds a user to the system"
    
    def remove_user(self):
          return"This is the function that removes a user from the system"
    
    def add_to_course(self):
          return"This is the function that adds a student to a course"

    def remove_from_course(self):
          return"This is the function that removes a student from a course"

    def print_schedule(self):
          return "This is the print schedule function!"
    
    def print_classlist(self):
         return "This is the print classlist function!"
    
    def search_courses(self):
          return "This is the search courses for instructors/admins function!"

    def print_courses(self):
          return "This is the function to print courses"
    
    def search_roster(self):
          return "This is the function to seach the roster"

    def print_roster(self):
          return "This is the function to print a roster"
   
    
    
    
    

    
