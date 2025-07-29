import tkinter as tk
from tkinter import *
from tkinter import messagebox
import user
import student
import instructor 
import admin
# from login_menu import * # This import is no longer needed as login_menu is handled by login_gui directly
import sqlite3
# Import the InstructorMenu class from instructor.py
from instructor import InstructorMenu 
# Import the StudentMenu class from student.py
from student import StudentMenu 
# Connect to the database
cx = sqlite3.connect("assignment3.db")
cursor = cx.cursor()

# Your existing GUI setup
login_menu = tk.Tk()
login_menu.title("Login to Leopard Web")
Label(login_menu, text="Username (EXCLUDE @WIT.EDU)").grid(row=0, column=0, padx=10, pady=5, sticky="w")
Label(login_menu, text="Password (#### Format)").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry1 = Entry(login_menu, width=30)
entry2 = Entry(login_menu, show="*", width=30)  # Hide password
entry1.grid(row=0, column=1, padx=10, pady=5)
entry2.grid(row=1, column=1, padx=10, pady=5)

def login_gui_handler():
    """
    Handles the login logic for the GUI.
    """
    email = str(entry1.get()).strip()
    password_str = entry2.get().strip()

    if not email or not password_str:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return

    try:
        password = int(password_str)
    except ValueError:
        messagebox.showerror("Input Error", "Password must be a number (#### Format).")
        return
    
    sql_command = ("""SELECT ID FROM LOGIN WHERE EMAIL = ? AND PASSWORD = ?""")
    cursor.execute(sql_command,(email, password))
    result = cursor.fetchone()

    if result:
        user_id = result[0] # The ID is the first element in the LOGIN table.
        
        if str(user_id).startswith("1"): # Student
            messagebox.showinfo("Success", "Student Successfully Logged In!")
            sql_command = ("SELECT NAME, SURNAME FROM STUDENT WHERE ID = ?")
            cursor.execute(sql_command,(user_id,))
            name = cursor.fetchone()
            if name:
                fname = name[0]
                lname = name[1]
                student_obj = student.Student(fname, lname, user_id)
                login_menu.withdraw() # Hide login window

                # Open the Student GUI menu
                student_gui_window = StudentMenu(login_menu, student_obj)
                student_gui_window.protocol("WM_DELETE_WINDOW", lambda: on_student_menu_close(student_gui_window)) # Handle window close


            else:
                messagebox.showerror("Error", "Not a valid student user. Please try again.")
       
        elif str(user_id).startswith("2"): # Instructor
            messagebox.showinfo("Success", "Instructor Successfully Logged In!")
            sql_command = ("SELECT NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL FROM INSTRUCTOR WHERE ID = ?")
            cursor.execute(sql_command,(user_id,))
            name = cursor.fetchone()
            if name:
                fname = name[0]
                lname = name[1]
                title = name[2]
                hireyear = name[3]
                dept = name[4]
                email = name[5]
                instructor_obj = instructor.Instructor(fname, lname, user_id, title, hireyear, dept, email)
                login_menu.withdraw() # Hide login window
                # Open the instructor GUI menu
                instructor_gui_window = InstructorMenu(login_menu, instructor_obj)
                instructor_gui_window.protocol("WM_DELETE_WINDOW", lambda: on_instructor_menu_close(instructor_gui_window)) # Handle window close
            else:
                messagebox.showerror("Error", "Not a valid instructor user. Please try again.")
        
        elif str(user_id).startswith("3"): # Admin
            messagebox.showinfo("Success", "Admin Successfully Logged In!")
            sql_command = ("SELECT NAME, SURNAME FROM ADMIN WHERE ID = ?")
            cursor.execute(sql_command,(user_id,))
            name = cursor.fetchone()
            if name:
                fname = name[0]
                lname = name[1]
                admin_obj = admin.Admin(fname, lname, user_id, cursor, cx)
                login_menu.withdraw() # Hide login window
                # Assuming admin_menu is defined elsewhere or will be implemented
                # admin_menu(admin_obj)
                messagebox.showinfo("Feature Coming Soon", "Admin menu is not yet implemented with GUI.")
                login_menu.deiconify() # Show login window again for now
            else:
                messagebox.showerror("Error", "Not a valid admin user. Please try again.")
        else:
            messagebox.showerror("Error", "Not a valid user type. Please try again.")
    else: 
        messagebox.showerror("Error", "Credentials Entered are Invalid. Please try again.")

def on_instructor_menu_close(instructor_gui_window):
    """
    Handles the closing of the instructor menu window.
    """
    instructor_gui_window.destroy()
    login_menu.deiconify() # Show the login window again


def on_student_menu_close(student_gui_window):
    """
    Handles the closing of the student menu window.
    """
    student_gui_window.destroy()
    login_menu.deiconify() # Show the login window again

# Add login button
login_button = Button(login_menu, text="Login", command=login_gui_handler, width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
login_button.grid(row=2, columnspan=2, pady=15)

# Start the Tkinter event loop
login_menu.mainloop()
