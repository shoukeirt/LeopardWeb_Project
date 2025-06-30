import sqlite3
import os
import user
import student
import instructor 
import admin
import login_menu
cx = sqlite3.connect("assignment3.db")
cursor = cx.cursor()

# def login(cursor,cx):
#     email = str(input("What is your username? EXCLUDE @WIT.EDU \n"))
#     password = int(input("What is your password? #### Format"))
#     sql_command = ("""SELECT ID FROM LOGIN WHERE EMAIL = ? AND PASSWORD = ?""")
#     cursor.execute(sql_command,(email, password))
#     result = cursor.fetchone()
#     if result:
#         id = result[0] #The ID is the first element in the LOGIN table. Use this to find the user type.
#         if str(id).startswith("1"): #make ID a string to use .startswith()
#             print("Student Successfully Logged In!")
#             sql_command = ("SELECT NAME, SURNAME FROM STUDENT WHERE ID = ?")
#             cursor.execute(sql_command,(id,))
#             name = cursor.fetchone()
#             if name:
#                 fname = name[0]
#                 lname = name[1]
#                 student_obj = student.Student(fname, lname, id)
#                 student_menu(student_obj)
#             else:
#                 print("Not a valid user type. Please try again.")

#         elif str(id).startswith("2"):
#             print("Instructor Successfully Logged In!")
#             sql_command = ("SELECT NAME, SURNAME FROM INSTRUCTOR WHERE ID = ?")
#             cursor.execute(sql_command,(id,))
#             name = cursor.fetchone()
#             if name:
#                 fname = name[0]
#                 lname = name[1]
#                 instructor_obj = instructor.Instructor(fname, lname, id)
#                 instructor_menu(instructor_obj)
#             else:
#                 print("Not a valid user type. Please try again.")

#         elif str(id).startswith("3"):
#             print("Admin Successfully Logged In!")
#             sql_command = ("SELECT NAME, SURNAME FROM ADMIN WHERE ID = ?")
#             cursor.execute(sql_command,(id,))
#             name = cursor.fetchone()
#             if name:
#                 fname = name[0]
#                 lname = name[1]
#                 admin_obj = admin.Admin(fname, lname, id, cursor, cx)
#                 admin_menu(admin_obj)
#         else:
#             print("Not a valid user type. Please try again.")
#     else: 
#         print("Credentials Entered are Invalid. Please try again.")
        

# def admin_menu(admin):
#     verify = 0
#     while (verify != 1):
#         choice = int(input(" 1.) Add Course to Course List \n 2.) Remove Course from Course List \n 3.) Add User \n 4.) Remove User \n 5.) Add Instructor\n 6.) Link Instructor to Course \n 7.) Logout\n"))
#         match choice:
#             case 1:
#                 admin.add_course()
#             case 2:
#                 admin.remove_course()
#             case 3:
#                 admin.add_user()
#             case 4: 
#                 admin.remove_user()
#             case 5: 
#                 admin.add_instructor()
#             case 6:
#                 admin.link_prof()
#             case 7:
#                 verify = int(input("Are you sure you want to logout?\n 1.) Yes \n 2.) No \n"))
#                 match verify:
#                     case 1:
#                         print("Logging out!\n")
#                         break
#                     case 2: 
#                         print("Returning to menu! \n")

# def instructor_menu(instructor):
#     verify = 0
#     while (verify != 1):
#         choice = int(input(" 1.) Search Courses \n 2.) Print Course Schedule \n 3.) Search Classlist \n 4.) Print Classlist \n 5.) Logout \n"))
#         match choice:
#             case 1:
#                 instructor.search_courses()
#             case 2:
#                 instructor.print_schedule()
#             case 3:
#                 instructor.search_roster()
#             case 4: 
#                 instructor.print_roster()
#             case 5:
#                 verify = int(input("Are you sure you want to logout? \n 1.) Yes \n 2.) No \n"))
#                 match verify:
#                     case 1:
#                         print("Logging out!\n")
#                         break
#                     case 2: 
#                         print("Returning to menu! \n")

# def student_menu(student):
#     verify = 0
#     while (verify != 1):
#         choice = int(input(" 1.) Search Courses \n 2.) Add Course to Schedule \n 3.) Remove Course from Schedule\n 4.) Print Schedule \n 5.) Logout \n"))
#         match choice:
#             case 1:
#                 student.search_courses()
#             case 2:
#                 student.add_course()
#             case 3:
#                 student.remove_course()
#             case 4: 
#                 student.print_schedule()
#             case 5:
#                 verify = int(input("Are you sure you want to logout?\n 1.) Yes \n 2.) No \n"))
#                 match verify:
#                     case 1:
#                         print("Logging out!\n")
#                         break
#                     case 2: 
#                         print("Returning to menu! \n")

                 

def main():
    cursor.execute("SELECT * FROM STUDENT")
    rows = cursor.fetchall();

    for row in rows:
        print(row)
    
    cursor.execute("SELECT * FROM INSTRUCTOR")
    rows = cursor.fetchall()

    for row in rows:
        print(row)
        
    sql_command = """INSERT INTO student VALUES(10011, 'ANTHONY', 'MAGLIOZZI', 2026, "BSCE",'Magliozzia');"""
    #cursor.execute(sql_command)
    cursor.execute("SELECT * FROM STUDENT")
    # rows = cursor.fetchall();
    sql_command = """DELETE FROM COURSES WHERE CRN = 4"""

    # cursor.execute(sql_command)
    for row in rows:
        print(row)
        
    # cursor.execute("PRAGMA table_info(STUDENT);")
    # for col in cursor.fetchall():
    #     print(col)
    
    # print("USING:", os.path.abspath("assignment3.db"))
  
    student1 = student.Student("Hill","Hill",1)
    student1.search_courses("CRN", "2500")
    new_admin1 = admin.Admin("First","Admin", 30003, cursor, cx)

    # new_admin1.add_course()
    # new_admin1.remove_course()
    # new_admin1.search_courses("TITLE", "Advanced Digital Circuit Design")
    # new_admin1.add_user()
    # new_admin1.add_instructor()
    # new_admin1.add_to_course()
    # new_admin1.remove_from_course()
    # new_admin1.link_prof()
    # new_admin1.unlink_prof()

    login_menu.login(cursor,cx)



    cx.commit() 

# close the connection 
    cx.close() 

main()




