#Import necessary modules from tkinter for GUI creation.
import tkinter as tk
from tkinter import *

#Import messagebox and simpledialog for pop-up messages and input dialogs.
from tkinter import messagebox, simpledialog

#Import  user, student, instructor, and admin functionalities.
import user
import student
import instructor
import admin 

#Import sqlite3 for database connectivity.
import sqlite3

#Import random for generating unique passwords.
import random

#Import the InstructorMenu class from instructor.py for instructor's GUI.
from instructor import InstructorMenu
#Import the StudentMenu class from student.py for student's GUI.
from student import StudentMenu
#Import the AdminMenu class from admin.py for admin's GUI.
from admin import AdminMenu 

#Connect to the SQLite database named "assignment3.db".
cx = sqlite3.connect("assignment3.db")
#Create a cursor object to execute SQL commands.
cursor = cx.cursor()

#Initialize the main Tkinter window for the login menu.
login_menu = tk.Tk()
#Set the title of the login window.
login_menu.title("Login to Leopard Web")
#Create a label for the email input field.
Label(login_menu, text="Email").grid(row=0, column=0, padx=10, pady=5, sticky="w")
#Create a label for the password input field.
Label(login_menu, text="Password (#### Format)").grid(row=1, column=0, padx=10, pady=5, sticky="w")
#Create a widget for email input.
entry1 = Entry(login_menu, width=30)
#Create a widget for password input, showing asterisks for security.
entry2 = Entry(login_menu, show="*", width=30)
#Place the email entry widget in the grid.
entry1.grid(row=0, column=1, padx=10, pady=5)
#Place the password entry widget in the grid.
entry2.grid(row=1, column=1, padx=10, pady=5)

#Define a function to generate a unique 4-digit password.
def generate_unique_password():
    """Generates a unique 4-digit password."""
    #Loop until a unique password is generated.
    while True:
        #Generate a random 4-digit integer.
        password = random.randint(1000, 9999)
        #Check if password already exists in the LOGIN table.
        cursor.execute("SELECT ID FROM LOGIN WHERE PASSWORD = ?", (password,))
        #If no matching password is found, return the generated password.
        if not cursor.fetchone():
            return password

#Define the handler function for the login button.
def login_gui_handler():
    """
    Handles the login logic for the GUI.
    Authenticates user based on email and password, then launches
    the appropriate menu (Student, Instructor, or Admin).
    """
    #Get the email input
    email_input = entry1.get().strip()
    #Get the password input from the entry field and remove leading/trailing whitespace.
    password_input = entry2.get().strip()

    #Check if either email or password fields are empty.
    if not email_input or not password_input:
        #Show a warning message if input is missing.
        messagebox.showwarning("Input Error", "Please enter both email and password.")
        return

    #Attempt to convert the password input to an integer.
    try:
        password_input = int(password_input)
    #Handle ValueError if the password is not a valid integer.
    except ValueError:
        #Show an error message for invalid password format.
        messagebox.showerror("Login Error", "Password must be a 4-digit number.")
        return

    #SQL command to select ID from LOGIN table based on email and password.
    sql_command = "SELECT ID FROM LOGIN WHERE EMAIL = ? AND PASSWORD = ?"
    #Execute the SQL command with provided email and password.
    cursor.execute(sql_command, (email_input, password_input))
    #Fetch the first matching result.
    result = cursor.fetchone()

    #Check if a user was found.
    if result:
        #Extract the user ID from the result.
        user_id = result[0]

        #Determine user type based on ID prefix.
        if str(user_id).startswith("1"):  #Student ID starts with 1
            #Show success message for student login.
            messagebox.showinfo("Login Success", "Student Successfully Logged In!")
            #SQL command to retrieve student data.
            sql_command = "SELECT NAME, SURNAME, GRADYEAR, MAJOR, EMAIL FROM STUDENT WHERE ID = ?"
           
            cursor.execute(sql_command, (user_id,))
            #Fetch student data.
            student_data = cursor.fetchone()
            #If student data is found, create a Student object and open the student menu.
            if student_data:
                fname, lname, grad_year, major, email = student_data
                student_obj = student.Student(fname, lname, user_id)

                #Hide login menu.
                login_menu.withdraw()
                #Open student menu.
                StudentMenu(login_menu, student_obj)
            #If student data not found, show an error.
            else:
                messagebox.showerror("Login Error", "Student data not found for this ID.")

        elif str(user_id).startswith("2"):  #Instructor ID starts with 2
            #Show success message for instructor login.
            messagebox.showinfo("Login Success", "Instructor Successfully Logged In!")
            #SQL command to retrieve instructor data.
            sql_command = "SELECT NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL FROM INSTRUCTOR WHERE ID = ?"
            
            cursor.execute(sql_command, (user_id,))
            #Fetch instructor data.
            instructor_data = cursor.fetchone()
            #If instructor data is found, create an Instructor object and open the instructor menu.
            if instructor_data:
                fname, lname, title, hireyear, dept, email = instructor_data
                instructor_obj = instructor.Instructor(fname, lname, user_id, title, hireyear, dept, email)

                #Hide login menu.
                login_menu.withdraw()
                #Open instructor menu.
                InstructorMenu(login_menu, instructor_obj)
            #If instructor data not found, show an error.
            else:
                messagebox.showerror("Login Error", "Instructor data not found for this ID.")

        elif str(user_id).startswith("3"):  #Admin ID starts with 3
            #Show success message for admin login.
            messagebox.showinfo("Login Success", "Admin Successfully Logged In!")
            #SQL command to retrieve admin data.
            sql_command = "SELECT NAME, SURNAME FROM ADMIN WHERE ID = ?"
         .
            cursor.execute(sql_command, (user_id,))
            #Fetch admin data.
            admin_data = cursor.fetchone()
            #If admin data is found, create an Admin object and open the admin menu.
            if admin_data:
                fname, lname = admin_data
                #Create an Admin object (passing cursor and cx for database operations).
                admin_obj = admin.Admin(fname, lname, user_id, cursor, cx) 

                #Hide login menu.
                login_menu.withdraw()
                #Launch the admin GUI.
                AdminMenu(login_menu, admin_obj) 
            #If admin data not found, show an error.
            else:
                messagebox.showerror("Login Error", "Admin data not found for this ID.")
        #Handle invalid user ID type.
        else:
            messagebox.showerror("Login Error", "Invalid user ID type.")
    #If no user found with the given email and password, show login failed message.
    else:
        messagebox.showerror("Login Failed", "Invalid Email or Password.")

#Define the function to handle forgot/reset password.
def forgot_password():
    """
    Handles the forgot/reset password functionality.
    Prompts for email, verifies it, generates a new password,
    updates it in the database, and displays the new password.
    """
    #Prompt the user to enter their email.
    email_input = simpledialog.askstring("Forgot Password", "Enter your email:")
    #If no email is entered, return.
    if not email_input:
        return

    try:
        #Check if the email exists in the LOGIN table.
        cursor.execute("SELECT ID FROM LOGIN WHERE EMAIL = ?", (email_input,))
        #Fetch the user information.
        user_info = cursor.fetchone()

        #If user information is found.
        if user_info:
            #Extract the user ID.
            user_id = user_info[0]

            #Determine user type to ensure email belongs to a valid user type (though table_name is not used later).
            table_name = ""
            if str(user_id).startswith("1"):
                table_name = "STUDENT"
            elif str(user_id).startswith("2"):
                table_name = "INSTRUCTOR"
            elif str(user_id).startswith("3"):
                table_name = "ADMIN"
            #If the user ID format is invalid, show an error.
            else:
                messagebox.showerror("Error", "Invalid User ID format associated with this email.")
                return

            #Generate a new unique password.
            new_password = generate_unique_password()

            #Update the password in the LOGIN table for the given user ID.
            cursor.execute("UPDATE LOGIN SET PASSWORD = ? WHERE ID = ?", (new_password, user_id))
            #Commit the changes to the database.
            cx.commit()

            #Show a success message with the new password.
            messagebox.showinfo("Password Reset", f"Your password has been reset successfully!\nYour new password is: {new_password}\nPlease remember this password for future logins.")
        #If no user found with the entered email.
        else:
            messagebox.showerror("User Not Found", f"No user found with email: {email_input}")
    #Handle database errors.
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

#Define a function to display "About" information.
def show_about_info():
    """
    Displays information about the group members, how to login,
    what each user type can do, and the program's purpose.
    """
    #Define the text content for the "About" message.
    about_text = (
        "Leopard Web System\n\n"
        "Developed by:\n"
        "Anthony Magliozzi\n"
        "Toufic Shoukeir\n\n"
        "How to Login:\n"
        "Enter your registered email and a 4-digit password.\n"
        "If you forget your password, use the 'Forgot/Reset Password' button.\n\n"
        "User Type Functionality:\n"
        "- Students (ID starts with '1'): Can view their registered courses, grades, and academic information.\n"
        "- Instructors (ID starts with '2'): Can manage courses they teach, update student grades, and view class rosters.\n"
        "- Administrators (ID starts with '3'): Have full system control, including adding/removing users, courses, and managing overall system data.\n\n"
        "Purpose of this Program:\n"
        "To provide a simplified course management system for students, instructors, and administrators, facilitating essential academic operations in a user-friendly graphical interface."
    )
    #Display the "About" information in a messagebox.
    messagebox.showinfo("About Leopard Web", about_text)

#Create and place the Login button.
login_button = Button(login_menu, text="Login", command=login_gui_handler, width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
login_button.grid(row=2, columnspan=2, pady=15)

#Create and place the Forgot Password button.
forgot_password_button = Button(login_menu, text="Forgot/Reset Password", command=forgot_password, width=20, height=2, bg="#007bff", fg="white", font=("Arial", 10, "bold"))
forgot_password_button.grid(row=3, columnspan=2, pady=10)

#Create and place the About button.
about_button = Button(login_menu, text="About", command=show_about_info, width=20, height=2, bg="#6c757d", fg="white", font=("Arial", 10, "bold"))
about_button.grid(row=4, columnspan=2, pady=10) #Placed below the forgot password button

#Start the Tkinter event loop, which keeps the GUI running.
login_menu.mainloop()

#Close the database connection when the GUI window is closed.
cx.close()
