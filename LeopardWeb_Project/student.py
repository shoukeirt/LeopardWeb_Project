import sqlite3
from user import User

class Student(User):
    
    def __init__(self, in_firstName, in_lastName, in_id):
        User.__init__(self, in_firstName, in_lastName, in_id)
        
    #methods
    def search_courses(self):
          return "This it the function for students to search courses"
    
        

    
