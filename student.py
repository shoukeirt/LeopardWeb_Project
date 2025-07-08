
# WRITTER : HARLJEN HILL

import sqlite3
from user import User
import datetime

#test push to git
def slipt_time(time_str):

    start_time, end_time = time_str.split('-')
    start_time = datetime.datetime.strptime(start_time.strip(), '%I:%M%p')
    end_time = datetime.datetime.strptime(end_time.strip(), '%I:%M%p')
    return start_time, end_time


class Student(User):
    
    def __init__(self, in_firstName, in_lastName, in_id):
        User.__init__(self, in_firstName, in_lastName, in_id)


        
    def search_courses(self, Search_keyword, search_value):
        cx = sqlite3.connect("assignment3.db")
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







    def add_course(self, CRN, search_value):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()

       # CRN = int(input("Type the CRN of the course you want to add to Student Schedule "))
       
        '''
        if CRN.upper() == "CRN":
            CRN = "CRN"
            
            # query to check the course exists
            query = "SELECT * FROM COURSES WHERE CRN = ?"
            cursor.execute(query, (CRN,))
            course = cursor.fetchone()
            
            # query to check if the student is already enrolled in the course
            sql_command = "SELECT * FROM ENROLLMENT WHERE STUDENT_ID = ?"
            cursor.execute(sql_command, (self.id,))
            enrollment = cursor.fetchall()

        else:
            print("Invalid search keyword.")
            return []


       
        query = f"SELECT * FROM COURSES WHERE {CRN} = ?"
        cursor.execute(query, (search_value,))
        rows = cursor.fetchall()
        '''

        # query to check the course exists
        query = "SELECT * FROM COURSES WHERE CRN = ?"
        cursor.execute(query, (search_value,))
        course = cursor.fetchone()
            
        # query to check if the student is already enrolled in the course
        sql_command = "SELECT * FROM ENROLLMENT WHERE STUDENT_ID = ?"
        cursor.execute(sql_command, (self.id,))
        enrollment = cursor.fetchall()


       



        #if the course does not exist, print an error message
        if not course:
            print("Course not found.")
            cx.close()
            return
        # 
        else:
            enrolled_crns = [enr[1] for enr in enrollment]
           
           
            
            '''
            if enrolled_crns:
                # check for time conflicts with already enrolled courses
                query = f"SELECT * FROM COURSES WHERE CRN IN ({','.join(['?'] * len(enrolled_crns))})"
                cursor.execute(query, enrolled_crns)
                enrolled_courses = cursor.fetchall()

                #parse the course days and times
                course_days = course[4]
                course_hour_start, course_hour_end = slipt_time(course[3])

                #check for time conflicts with already enrolled courses through loops
                for enrolled_course in enrolled_courses:
                    enrolled_days = enrolled_course[4]
                    enrolled_hour_start, enrolled_hour_end = slipt_time(enrolled_course[3])
                    if any(day in enrolled_days for day in course_days) and not (course_hour_end <= enrolled_hour_start or course_hour_start >= enrolled_hour_end):
                        print(f"Time conflict with course {enrolled_course[0]}: {enrolled_course[1]}")
                        cx.close()
                        return
                    '''
            #if there is no time conflict, add the course to the enrollment table   
            query = "INSERT INTO ENROLLMENT (STUDENT_ID, CRN) VALUES (?, ?)"
            cursor.execute(query, (self.id, course[0]))
            cx.commit()
            print(f"Course {course[0]} added successfully.")
            

        cx.close()





    def remove_course(self, CRN):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()


        #querry to chek if the student is enrolled in the course
        sql_command = "SELECT * FROM ENROLLMENT WHERE STUDENT_ID = ? AND CRN = ?"
        cursor.execute(sql_command, (self.id, CRN))
        enrollment = cursor.fetchone()

        #check if the student is enrolled in the course
        if not enrollment:
            print("You are not enrolled in this course.")
            cx.close()
        else:
            query = "DELETE FROM ENROLLMENT WHERE STUDENT_ID = ? AND CRN = ?"
            cursor.execute(query, (self.id, CRN))  
            cx.commit()
            print(f"Course with CRN {CRN} removed successfully.")         
        cx.close()





    def print_courses(self):
        cx = sqlite3.connect("assignment3.db")
        cursor = cx.cursor()

        query = """
        SELECT * FROM ENROLLMENT
        WHERE ENROLLMENT.STUDENT_ID = ?
        """
        cursor.execute(query, (self.id,))
        rows = cursor.fetchall()
        course = []

        #use the enrolled courses to get the course details
        for row in rows:
            query = "SELECT * FROM COURSES WHERE CRN = ?"
            cursor.execute(query, (row[1],))
            course.append( cursor.fetchall())
        print("Courses enrolled:")
        #display the relevant course details
        for course in course:
            print("Course: ",course[0][1]," Department:", course[0][2]," Time:", course[0][3],"Days: ", course[0][4])
        cx.close()
        return rows   


