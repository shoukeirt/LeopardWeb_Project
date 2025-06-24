import sqlite3
from user import User

class Student(User):
    
    def __init__(self, in_firstName, in_lastName, in_id):
        User.__init__(self, in_firstName, in_lastName, in_id)
        
    
    #methods
    def search_courses(self,Searchh_keyword,search_value):

        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()

        # Use parameterized queries to prevent SQL injection and handle types correctly
        if Searchh_keyword.upper() == "CRN" :
            Searchh_keyword = "CRN"
        elif Searchh_keyword.upper() == "COURSE NAME" or Searchh_keyword.upper() == "TITLE":
            Searchh_keyword = "TITLE"
        

        if type(search_value) == int:
            search_value = str(search_value)
        elif type(search_value) == str:
            search_value = f"'{search_value}'"


        query = f"SELECT * FROM COURSES WHERE {Searchh_keyword} = {search_value}"
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:

            print(row)
        return rows

    def add_course(self, CRN, title=""):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()
        course = self.search_courses("CRN", CRN)

        #this need to be changed later because table name has not been mak=de yet
        query = "INSERT INTO table_name (column1, column2, column3, column4) VALUES (?, ?, ?, ?)"




        # Use parameterized queries to prevent SQL injection
        query = "INSERT INTO COURSES (CRN, TITLE, CREDITS, DEPARTMENT) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (CRN, title, credits))
        cx.commit()
        print(f"Course {title} added successfully.")


    def print_courses(self):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()

        #this need to changed based on the name of the table
        query = "SELECT * FROM COURSES WHERE ID = self.id"
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            print(row)
        return rows
    



studen = Student("Hill","Hill",1)
studen.search_courses("CRN", "2500")



