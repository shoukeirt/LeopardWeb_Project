from admin import Admin
from instructor import Instructor
from student import Student

def login(cursor, cx):
    print("========== COURSE SYSTEM ==========")
    print("1. Login")
    print("2. Exit")
    option = input("Choose an option: ").strip()

    if option == "1":
        username = input("What is your username? EXCLUDE @WIT.EDU\n").strip().lower()
        password = input("What is your password? #### Format\n").strip()

        cursor.execute("SELECT * FROM LOGIN")
        logins = cursor.fetchall()

        user_data = None
        for row in logins:
            db_id = str(row[0]).strip()
            db_email = str(row[1]).strip().lower()
            db_password = str(row[2]).strip()
            if db_email == username and db_password == password:
                user_data = (db_id, db_email)
                break

        if user_data:
            user_id = user_data[0]

            # Check Admin Table
            cursor.execute("SELECT * FROM ADMIN WHERE ID = ?", (user_id,))
            admin_data = cursor.fetchone()
            if admin_data:
                admin_obj = Admin(admin_data[1], admin_data[2], admin_data[0], cursor, cx)
                print("Admin Successfully Logged In!")
                admin_menu(admin_obj, cursor, cx)
                return

            # Check Instructor Table
            cursor.execute("SELECT * FROM INSTRUCTOR WHERE ID = ?", (user_id,))
            instructor_data = cursor.fetchone()
            if instructor_data:
                instructor_obj = Instructor(
                    instructor_data[1], instructor_data[2], instructor_data[0],
                    instructor_data[3], instructor_data[4],
                    instructor_data[5], instructor_data[6]
                )
                print("Instructor Successfully Logged In!")
                instructor_menu(instructor_obj)
                return

            # Check Student Table
            cursor.execute("SELECT * FROM STUDENT WHERE ID = ?", (user_id,))
            student_data = cursor.fetchone()
            if student_data:
                student_obj = Student(
                    student_data[1], student_data[2], student_data[0],
                    student_data[3], student_data[4], student_data[5]
                )
                print("Student Successfully Logged In!")
                student_menu(student_obj)
                return

            print("User role not found in ADMIN, INSTRUCTOR, or STUDENT tables.")
        else:
            print("Invalid login.\nLogin failed. Please try again.\n")

    elif option == "2":
        print("Exiting program.")
    else:
        print("Invalid option.")

# ----------------- ADMIN MENU ----------------- #
def admin_menu(admin, cursor, cx):
    while True:
        print("\n1.) Add Course\n2.) Add User\n3.) Print User Info\n4.) Logout")
        option = input("Choose an option: ")

        if option == "1":
            admin.add_course()
        elif option == "2":
            admin.add_user()
        elif option == "3":
            print(admin.print_all_info())
        elif option == "4":
            confirm = input("Are you sure you want to logout?\n1.) Yes\n2.) No\n")
            if confirm == "1":
                print("Logging out!")
                break
            else:
                continue
        else:
            print("Invalid option. Try again.")

# ---------------- INSTRUCTOR MENU ---------------- #
def instructor_menu(instructor):
    while True:
        print("\n1.) Search Courses\n2.) Print Course Schedule\n3.) Search Classlist\n4.) Print Classlist\n5.) Logout")
        option = input()

        if option == "1":
            crn = input("Enter CRN to search: ")
            if crn.isdigit():
                instructor.search_courses("CRN", int(crn))
            else:
                print("Invalid CRN.")
        elif option == "2":
            instructor.print_schedule()
        elif option == "3":
            crn = input("Enter CRN to search for a specific student: ")
            if crn.isdigit():
                instructor.search_roster(int(crn))
            else:
                print("Invalid CRN.")
        elif option == "4":
            crn = input("Enter CRN to print the full classlist: ")
            if crn.isdigit():
                instructor.print_roster(int(crn))
            else:
                print("Invalid CRN.")
        elif option == "5":
            confirm = input("Are you sure you want to logout?\n1.) Yes\n2.) No\n")
            if confirm == "1":
                print("Logging out!")
                break
            else:
                continue
        else:
            print("Invalid option. Try again.")

# ---------------- STUDENT MENU ---------------- #
def student_menu(student):
    while True:
        print("\n1.) Print Schedule\n2.) Print Student Info\n3.) Logout")
        option = input("Choose an option: ")

        if option == "1":
            student.print_courses()
        elif option == "2":
            print(student.print_all_info())
        elif option == "3":
            confirm = input("Are you sure you want to logout?\n1.) Yes\n2.) No\n")
            if confirm == "1":
                print("Logging out!")
                break
            else:
                continue
        else:
            print("Invalid option. Try again.")
