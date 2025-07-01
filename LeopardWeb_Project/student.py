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
        cx = sqlite3.connect("../LeopardWeb_Project/LeopardWeb_Project/test.db")  # This has to be changed to the correct DB File 
        cursor = cx.cursor()

        # Check if the student exists in the database
        sql_command = "SELECT * FROM STUDENT WHERE ID = ? and NAME = ? and SURNAME = ?"
        cursor.execute(sql_command, (self.id,self.firstName, self.lastName))
        student = cursor.fetchone()
        if not student:
            print("Student not found.")
            cx.close()
            return []
        


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

        
        # Check if the student exists in the database
        sql_command = "SELECT * FROM STUDENT WHERE ID = ? and NAME = ? and SURNAME = ?"
        cursor.execute(sql_command, (self.id,self.firstName, self.lastName))
        student = cursor.fetchone()
        if not student:
            print("Student not found.")
            cx.close()
            return []
        


        # query to check the course exists
        query = "SELECT * FROM COURSES WHERE CRN = ?"
        cursor.execute(query, (CRN,))
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
            #if there is no time conflict, add the course to the enrollment table   
            query = "INSERT INTO ENROLLMENT (STUDENT_ID, CRN) VALUES (?, ?)"
            cursor.execute(query, (self.id, course[0]))
            cx.commit()
            print(f"Course {course[0]} added successfully.")
        cx.close()



    def remove_course(self, CRN):
        cx = sqlite3.connect("../LeopardWeb_Project/LeopardWeb_Project/test.db")  # REMEMBER TO FIX THIS LATER
        cursor = cx.cursor()

        # Check if the student exists in the database
        sql_command = "SELECT * FROM STUDENT WHERE ID = ? and NAME = ? and SURNAME = ?"
        cursor.execute(sql_command, (self.id,self.firstName, self.lastName))
        student = cursor.fetchone()
        if not student:
            print("Student not found.")
            cx.close()
            return []
        





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
        cx = sqlite3.connect("../LeopardWeb_Project/LeopardWeb_Project/test.db")  # FIX LATTER
        cursor = cx.cursor()

        # Check if the student exists in the database
        sql_command = "SELECT * FROM STUDENT WHERE ID = ? and NAME = ? and SURNAME = ?"
        cursor.execute(sql_command, (self.id,self.firstName, self.lastName))
        student = cursor.fetchone()
        if not student:
            print("Student not found.")
            cx.close()
            return []
        



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
            print("Name: ",course[0][1]," Department:", course[0][2]," Time:", course[0][3],"Days: ", course[0][4])
        cx.close()
        return rows   



if __name__ == "__main__":




    student2 = Student("John", "Doe", 9999999999999)
    student= Student("Toufic", "Shoukeir", 10015)
    student.remove_course(2500)
    student.remove_course(2750)
    student.remove_course(4670)
    student.add_course(2500)
    student.add_course(2750)
    student.add_course(4670)
    student2.add_course(2500)
    student2.remove_course(2750)
    student2.print_courses()
    student.print_courses()

    #test testing funtionaliity of program
    first_name =input("What is your first name: ")  
    last_name = input("what is your last name: ")
    student_id = int(input("What is your student id: "))
    choose = input("Choose what you want to do 0 for search, \n1 for add, \n2 for remove, \n3 for print courses, \n4 for exit ")
    
    # Create a Student object with the provided information
    student_test = Student(first_name, last_name, student_id)

    # Loop until the user chooses to exit with 4
    while choose != "4":
        #if the user chooses to search for courses, call the search_courses method
        if choose == "0":
            search_keyword = input("What do you want to search for? (CRN, COURSE NAME, TITLE) ")
            if search_keyword == "":
                print("seach will be CRN ")
            search_value = input("What is the value you want to search for? ")
            while search_value == "":
                print("search value cannot be empty ")
                search_value = input("What is the value you want to search for? ")
            student_test.search_courses(search_keyword, search_value.upper())
        #if the user chooses to add a course, call the add_course method
        elif choose == "1":
            crn = int(input("Enter the CRN to add: "))
            student_test.add_course(crn)
        #if the user chooses to remove a course, call the remove_course method
        elif choose == "2":
            crn = int(input("Enter the CRN to remove: "))
            student_test.remove_course(crn)
        #if the user chooses to print courses, call the print_courses method
        elif choose == "3":
            student_test.print_courses()
        else:
            print("Invalid choice. Please try again.")
        # Ask the user for their next action
        choose = input("Choose what you want to do 0 for search, \n1 for add, \n2 for remove, \n3 for print courses, \n4 for exit ")
    
