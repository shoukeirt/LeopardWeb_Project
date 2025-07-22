import tkinter as tk
from tkinter import *
from tkinter import messagebox
import user
import student
import instructor 
import admin
from login_menu import *
import sqlite3

cx = sqlite3.connect("assignment3.db")
cursor = cx.cursor()

# Your existing GUI setup
login_menu = tk.Tk()
login_menu.title("Login to Leopard Web")
Label(login_menu, text="Username (EXCLUDE @WIT.EDU)").grid(row=0)
Label(login_menu, text="Password (#### Format)").grid(row=1)
entry1 = Entry(login_menu)
entry2 = Entry(login_menu, show="*")  # Hide password
entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)

def login(cursor, cx):
    # Convert input() calls to .get() from entries
    email = str(entry1.get())
    password = int(entry2.get())
    
    sql_command = ("""SELECT ID FROM LOGIN WHERE EMAIL = ? AND PASSWORD = ?""")
    cursor.execute(sql_command,(email, password))
    result = cursor.fetchone()
    if result:
        id = result[0] #The ID is the first element in the LOGIN table. Use this to find the user type.
        if str(id).startswith("1"): #make ID a string to use .startswith()
            messagebox.showinfo("Success", "Student Successfully Logged In!")
            sql_command = ("SELECT NAME, SURNAME FROM STUDENT WHERE ID = ?")
            cursor.execute(sql_command,(id,))
            name = cursor.fetchone()
            if name:
                fname = name[0]
                lname = name[1]
                student_obj = student.Student(fname, lname, id)
                login_menu.destroy()  # Close login window
                student_menu(student_obj)
            else:
                messagebox.showerror("Error", "Not a valid user type. Please try again.")
        elif str(id).startswith("2"):
            messagebox.showinfo("Success", "Instructor Successfully Logged In!")
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
                login_menu.destroy()  # Close login window
                instructor_menu(instructor_obj)
            else:
                messagebox.showerror("Error", "Not a valid user type. Please try again.")
        elif str(id).startswith("3"):
            messagebox.showinfo("Success", "Admin Successfully Logged In!")
            sql_command = ("SELECT NAME, SURNAME FROM ADMIN WHERE ID = ?")
            cursor.execute(sql_command,(id,))
            name = cursor.fetchone()
            if name:
                fname = name[0]
                lname = name[1]
                admin_obj = admin.Admin(fname, lname, id, cursor, cx)
                login_menu.destroy()  # Close login window
                admin_menu(admin_obj)
        else:
            messagebox.showerror("Error", "Not a valid user type. Please try again.")
    else: 
        messagebox.showerror("Error", "Credentials Entered are Invalid. Please try again.")

# Add login button
Button(login_menu, text="Login", command=lambda: login(cursor, cx)).grid(row=2, columnspan=2)

# You'll need to pass your cursor and cx when you run this
mainloop()