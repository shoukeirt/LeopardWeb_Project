import sqlite3
from user import User
import datetime

def slipt_time(time_str):

    start_time, end_time = time_str.split('-')
    start_time = datetime.datetime.strptime(start_time.strip(), '%I:%M%p')
    end_time = datetime.datetime.strptime(end_time.strip(), '%I:%M%p')
    return start_time, end_time



class Student(User):
    
    def __init__(self, in_firstName, in_lastName, in_id):
        User.__init__(self, in_firstName, in_lastName, in_id)
        
    def search_courses(self, Search_keyword, search_value):
        cx = sqlite3.connect("../LeopardWeb_Project/LeopardWeb_Project/test.db")  # This has to be changed to the correct DB File 
        cursor = cx.cursor()

        if Search_keyword.upper() == "CRN":
            Search_keyword = "CRN"
        elif Search_keyword.upper() in ["COURSE NAME", "TITLE"]:
            Search_keyword = "TITLE"
        else:
            print("Invalid search keyword.")
            return []

        query = f"SELECT * FROM COURSES WHERE {Search_keyword} = ?"
        cursor.execute(query, (search_value,))
        rows = cursor.fetchall()

        for row in rows:
            print(row)
        return rows







    def add_course(self, CRN):
        cx = sqlite3.connect("../LeopardWeb_Project/LeopardWeb_Project/test.db")  # Adjust the path to your database file
        cursor = cx.cursor()


        query = "SELECT * FROM COURSES WHERE CRN = ?"
        cursor.execute(query, (CRN,))
        course = cursor.fetchone()

        sql_command = "SELECT * FROM ENROLLMENT WHERE STUDENT_ID = ?"
        cursor.execute(sql_command, (self.id,))
        enrollment = cursor.fetchall()

        if not course:
            print("Course not found.")

        else:
            enrolled_crns = [enr[1] for enr in enrollment]
            if enrolled_crns:
                
                query = f"SELECT * FROM COURSES WHERE CRN IN ({','.join(['?'] * len(enrolled_crns))})"
                cursor.execute(query, enrolled_crns)
                enrolled_courses = cursor.fetchall()

                course_days = course[4]
                course_hour_start, course_hour_end = slipt_time(course[3])
                for enrolled_course in enrolled_courses:
                    enrolled_days = enrolled_course[4]
                    enrolled_hour_start, enrolled_hour_end = slipt_time(enrolled_course[3])
                    if any(day in enrolled_days for day in course_days) and not (course_hour_end <= enrolled_hour_start or course_hour_start >= enrolled_hour_end):
                        print(f"Time conflict with course {enrolled_course[0]}: {enrolled_course[1]}")
                        cx.close()
                        return
            query = "INSERT INTO ENROLLMENT (STUDENT_ID, CRN) VALUES (?, ?)"
            cursor.execute(query, (self.id, course[0]))
            cx.commit()
            print(f"Course {course[0]} added successfully.")
        cx.close()



    def remove_course(self, CRN):
        cx = sqlite3.connect("../LeopardWeb_Project/LeopardWeb_Project/test.db")  # REMEMBER TO FIX THIS LATER
        cursor = cx.cursor()
        query = "DELETE FROM ENROLLMENT WHERE STUDENT_ID = ? AND CRN = ?"
        cursor.execute(query, (self.id, CRN))  
        cx.commit()
        print(f"Course with CRN {CRN} removed successfully.")         
        cx.close()


    def print_courses(self):
        cx = sqlite3.connect("../LeopardWeb_Project/LeopardWeb_Project/test.db")  # FIX LATTER
        cursor = cx.cursor()

        query = """
        SELECT * FROM ENROLLMENT
        WHERE ENROLLMENT.STUDENT_ID = ?
        """
        cursor.execute(query, (self.id,))

        rows = cursor.fetchall()
        for row in rows:
            print(row)  
        return rows   

if __name__ == "__main__":
    student= Student("John", "Doe", 12345)
    student.remove_course(2500)
    student.add_course(2500)

    student.print_courses()

    for i in range(0, 5):
            print('Test')
