import user
import student
import instructor 
import admin
 ##file made by Toufic Shoukeir

def login(cursor,cx):
    email = str(input("What is your username? EXCLUDE @WIT.EDU \n"))
    password = int(input("What is your password? #### Format"))
    sql_command = ("""SELECT ID FROM LOGIN WHERE EMAIL = ? AND PASSWORD = ?""")
    cursor.execute(sql_command,(email, password))
    result = cursor.fetchone()
    if result:
        id = result[0] #The ID is the first element in the LOGIN table. Use this to find the user type.
        if str(id).startswith("1"): #make ID a string to use .startswith()
            print("Student Successfully Logged In!")
            sql_command = ("SELECT NAME, SURNAME FROM STUDENT WHERE ID = ?")
            cursor.execute(sql_command,(id,))
            name = cursor.fetchone()
            if name:
                fname = name[0]
                lname = name[1]
                student_obj = student.Student(fname, lname, id)
                student_menu(student_obj)
            else:
                print("Not a valid user type. Please try again.")

        elif str(id).startswith("2"):
            print("Instructor Successfully Logged In!")
            sql_command = ("SELECT NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL FROM INSTRUCTOR WHERE ID = ?")
            cursor.execute(sql_command,(id,))
            name = cursor.fetchone()
            if name:
                fname = name[0]
                lname = name[1]
                title = name[2]
                hireyear = name[3]
                dept = name[4]
                email = name[5]
                instructor_obj = instructor.Instructor(fname, lname, id, title, hireyear, dept, email)
                instructor_menu(instructor_obj)
            else:
                print("Not a valid user type. Please try again.")

        elif str(id).startswith("3"):
            print("Admin Successfully Logged In!")
            sql_command = ("SELECT NAME, SURNAME FROM ADMIN WHERE ID = ?")
            cursor.execute(sql_command,(id,))
            name = cursor.fetchone()
            if name:
                fname = name[0]
                lname = name[1]
                admin_obj = admin.Admin(fname, lname, id, cursor, cx)
                admin_menu(admin_obj)
        else:
            print("Not a valid user type. Please try again.")
    else: 
        print("Credentials Entered are Invalid. Please try again.")
        

def admin_menu(admin):
    verify = 0
    while (verify != 1):
        choice = int(input(" 1.) Add Course to Course List \n 2.) Remove Course from Course List \n 3.) Add User \n 4.) Remove User \n 5.) Add Instructor\n 6.) Link Instructor to Course \n 7.) Unlink Instructor from Course\n 8.) Add Student to Course \n 9.) Remove Student from Course\n 10.) Logout"))
        match choice:
            case 1:
                admin.add_course()
            case 2:
                admin.remove_course()
            case 3:
                admin.add_user()
            case 4: 
                admin.remove_user()
            case 5: 
                admin.add_instructor()
            case 6:
                admin.link_prof()
            case 7:
                admin.unlink_prof()
            case 8: 
                admin.add_to_course()
            case 9:
                admin.remove_from_course()
            case 10:
                verify = int(input("Are you sure you want to logout?\n 1.) Yes \n 2.) No"))
                match verify:
                    case 1:
                        print("Logging out!\n")
                        break
                    case 2: 
                        print("Returning to menu! \n")

def instructor_menu(instructor):
    verify = 0
    while (verify != 1):
        choice = int(input(" 1.) Search Courses \n 2.) Print Course Schedule \n 3.) Search Classlist \n 4.) Print Classlist \n 5.) Logout "))
        match choice:
            case 1:
                choice1 = int(input("How would you like to search? \n 1.) TITILE \n 2.) CRN"))
                match choice1:
                    case 1:
                        title = str(input("What is the title of your course? (Spaces between words, first letter of each word capital) \n"))
                        instructor.search_courses(Search_keyword = "TITLE", search_value = title)
                    case 2:
                         crn = int(input("What is the CRN of the course you want to view? \n"))
                         instructor.search_courses(Search_keyword = "CRN", search_value = crn )
            case 2:
                instructor.print_schedule()
            case 3:
                crn = int(input("What is the CRN of the course you want to search? \n"))
                instructor.search_roster(crn)
            case 4: 
                crn = int(input("What is the CRN of the course roster you want to print? \n"))
                instructor.print_roster(crn)
            case 5:
                verify = int(input("Are you sure you want to logout? \n 1.) Yes \n 2.) No"))
                match verify:
                    case 1:
                        print("Logging out!\n")
                        break
                    case 2: 
                        print("Returning to menu! \n")

def student_menu(student):
    verify = 0
    while (verify != 1):
        choice = int(input(" 1.) Search Courses \n 2.) Add Course to Schedule \n 3.) Remove Course from Schedule\n 4.) Print Schedule \n 5.) Logout "))
        match choice:
            case 1:
                choice1 = int(input("How would you like to search? \n 1.) TITILE \n 2.) CRN"))
                match choice1:
                    case 1:
                        title = str(input("What is the title of your course? (Spaces between words, first letter of each word capital) \n"))
                        student.search_courses(Search_keyword="TITLE", search_value=title)
                    case 2:
                        crn = int(input("What is the CRN of the course you want to view? \n"))
                        student.search_courses(Search_keyword="CRN", search_value=crn)

            case 2:
                # Prompt the student to enter the CRN of the course to add
                crn = int(input("What is the CRN of the course you want to add? \n"))
                student.add_course(CRN="CRN", search_value=crn)

            case 3:
                # Prompt the student to enter the CRN of the course to remove
                crn = int(input("What is the CRN of the course you want to remove? \n"))

                # Take inputted integer CRN
                student.remove_course(crn)

            case 4:
                student.print_courses()

            case 5:
                verify = int(input("Are you sure you want to logout?\n 1.) Yes \n 2.) No"))
                match verify:
                    case 1:
                        print("Logging out!\n")
                        break
                    case 2:
                        print("Returning to menu! \n")