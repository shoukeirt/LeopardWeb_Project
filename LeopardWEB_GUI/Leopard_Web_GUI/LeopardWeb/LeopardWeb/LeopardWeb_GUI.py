import sqlite3
from user import User
import student
from student import Student
from login_menu import login
from login_gui import login_gui
import datetime
cx = sqlite3.connect("assignment3.db")
cursor = cx.cursor()

def main():
    
    login_gui(cursor,cx)
    cx.commit() 

main()
