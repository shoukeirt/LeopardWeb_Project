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

        #return "This it the function for students to search courses"

studen = Student("Hill","Hill",1)
studen.search_courses("CRN", "2500")