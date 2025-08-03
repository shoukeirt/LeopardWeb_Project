import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog 
import user
import student
import instructor 
import admin # Ensure admin module is imported
import sqlite3
import random 

# Import the InstructorMenu class from instructor.py
from instructor import InstructorMenu 
# Import the StudentMenu class from student.py
from student import StudentMenu 
# Import the AdminMenu class from admin.py
from admin import AdminMenu # ADD THIS LINE

# Connect to the database
cx = sqlite3.connect("assignment3.db")
cursor = cx.cursor()

# Your existing GUI setup
login_menu = tk.Tk()
login_menu.title("Login to Leopard Web")
Label(login_menu, text="Email").grid(row=0, column=0, padx=10, pady=5, sticky="w") 
Label(login_menu, text="Password (#### Format)").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry1 = Entry(login_menu, width=30)
entry2 = Entry(login_menu, show="*", width=30)  
entry1.grid(row=0, column=1, padx=10, pady=5)
entry2.grid(row=1, column=1, padx=10, pady=5)

def generate_unique_password():
    """Generates a unique 4-digit password."""
    while True:
        password = random.randint(1000, 9999)
        # Check if password already exists in the database
        cursor.execute("SELECT ID FROM LOGIN WHERE PASSWORD = ?", (password,))
        if not cursor.fetchone():
            return password

def login_gui_handler():
    """
    Handles the login logic for the GUI.
    Authenticates user based on email and password, then launches
    the appropriate menu (Student, Instructor, or Admin).
    """
    email_input = entry1.get().strip()
    password_input = entry2.get().strip()

    if not email_input or not password_input:
        messagebox.showwarning("Input Error", "Please enter both email and password.")
        return

    try:
        password_input = int(password_input)
    except ValueError:
        messagebox.showerror("Login Error", "Password must be a 4-digit number.")
        return

    sql_command = "SELECT ID FROM LOGIN WHERE EMAIL = ? AND PASSWORD = ?"
    cursor.execute(sql_command, (email_input, password_input))
    result = cursor.fetchone()

    if result:
        user_id = result[0]
        
        # Determine user type based on ID prefix
        if str(user_id).startswith("1"):  # Student ID starts with 1
            messagebox.showinfo("Login Success", "Student Successfully Logged In!")
            sql_command = "SELECT NAME, SURNAME, GRADYEAR, MAJOR, EMAIL FROM STUDENT WHERE ID = ?"
            cursor.execute(sql_command, (user_id,))
            student_data = cursor.fetchone()
            if student_data:
                fname, lname, grad_year, major, email = student_data
                student_obj = student.Student(fname, lname, user_id)
                
                # Hide login menu and open student menu
                login_menu.withdraw()
                StudentMenu(login_menu, student_obj)
            else:
                messagebox.showerror("Login Error", "Student data not found for this ID.")

        elif str(user_id).startswith("2"):  # Instructor ID starts with 2
            messagebox.showinfo("Login Success", "Instructor Successfully Logged In!")
            sql_command = "SELECT NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL FROM INSTRUCTOR WHERE ID = ?"
            cursor.execute(sql_command, (user_id,))
            instructor_data = cursor.fetchone()
            if instructor_data:
                fname, lname, title, hireyear, dept, email = instructor_data
                instructor_obj = instructor.Instructor(fname, lname, user_id, title, hireyear, dept, email)
                
                # Hide login menu and open instructor menu
                login_menu.withdraw()
                InstructorMenu(login_menu, instructor_obj)
            else:
                messagebox.showerror("Login Error", "Instructor data not found for this ID.")

        elif str(user_id).startswith("3"):  # Admin ID starts with 3
            messagebox.showinfo("Login Success", "Admin Successfully Logged In!")
            sql_command = "SELECT NAME, SURNAME FROM ADMIN WHERE ID = ?"
            cursor.execute(sql_command, (user_id,))
            admin_data = cursor.fetchone()
            if admin_data:
                fname, lname = admin_data
                # Create an Admin object (passing cursor and cx for database operations)
                admin_obj = admin.Admin(fname, lname, user_id, cursor, cx) # Pass cursor and cx

                # Hide login menu and open admin menu
                login_menu.withdraw()
                AdminMenu(login_menu, admin_obj) # LAUNCH THE ADMIN GUI HERE
            else:
                messagebox.showerror("Login Error", "Admin data not found for this ID.")
        else:
            messagebox.showerror("Login Error", "Invalid user ID type.")
    else:
        messagebox.showerror("Login Failed", "Invalid Email or Password.")


def forgot_password():
    """
    Handles the forgot/reset password functionality.
    Prompts for email, verifies it, generates a new password,
    updates it in the database, and displays the new password.
    """
    email_input = simpledialog.askstring("Forgot Password", "Enter your email:")
    if not email_input:
        return

    try:
        cursor.execute("SELECT ID FROM LOGIN WHERE EMAIL = ?", (email_input,))
        user_info = cursor.fetchone()

        if user_info:
            user_id = user_info[0]
            
            # Determine user type to ensure email belongs to a valid user type
            table_name = ""
            if str(user_id).startswith("1"):
                table_name = "STUDENT"
            elif str(user_id).startswith("2"):
                table_name = "INSTRUCTOR"
            elif str(user_id).startswith("3"):
                table_name = "ADMIN"
            else:
                messagebox.showerror("Error", "Invalid User ID format associated with this email.")
                return

            # Generate a new unique password
            new_password = generate_unique_password()

            # Update the password in the LOGIN table
            cursor.execute("UPDATE LOGIN SET PASSWORD = ? WHERE ID = ?", (new_password, user_id))
            cx.commit()

            messagebox.showinfo("Password Reset", f"Your password has been reset successfully!\nYour new password is: {new_password}\nPlease remember this password for future logins.")
        else:
            messagebox.showerror("User Not Found", f"No user found with email: {email_input}")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")


# Add login button
login_button = Button(login_menu, text="Login", command=login_gui_handler, width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
login_button.grid(row=2, columnspan=2, pady=15)

# Forgot Password button
forgot_password_button = Button(login_menu, text="Forgot/Reset Password", command=forgot_password, width=20, height=2, bg="#007bff", fg="white", font=("Arial", 10, "bold"))
forgot_password_button.grid(row=3, columnspan=2, pady=10)

# Start the Tkinter event loop
login_menu.mainloop()

# Close the database connection when the GUI is closed
cx.close()
