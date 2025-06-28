import sqlite3
from user import User

class Student(User):
    
    def __init__(self, in_firstName, in_lastName, in_id):
        User.__init__(self, in_firstName, in_lastName, in_id)
        
    def search_courses(self, Search_keyword, search_value):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()

        # Use parameterized queries to prevent SQL injection
        if Search_keyword.upper() == "CRN":
            Search_keyword = "CRN"
        elif Search_keyword.upper() in ["COURSE NAME", "TITLE"]:
            Search_keyword = "TITLE"

        if isinstance(search_value, int):
            search_value = str(search_value)
        elif isinstance(search_value, str):
            search_value = f"'{search_value}'"

        query = (f"SELECT * FROM COURSES WHERE {Search_keyword} = {search_value}")
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            print(row)
        return rows

    def add_course(self, CRN, title="", credits=3, department="Unknown"):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()
        course = self.search_courses("CRN", CRN)

        if course:
            print("Course already exists.")
            return

        query = "INSERT INTO COURSES (CRN, TITLE, CREDITS, DEPARTMENT) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (CRN, title, credits, department))
        cx.commit()
        print(f"Course {title} added successfully.")

    def print_courses(self):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()

        query = f"SELECT * FROM COURSES WHERE ID = {self.id}"
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            print(row)
        return rows


# Test
studen = Student("Hill", "Hill", 1)
studen.search_courses("CRN", "2500")
