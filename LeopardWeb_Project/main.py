import sqlite3
from user import User
import student
from student import Student
from login_menu import login
import datetime

def main():
    cx = sqlite3.connect("assignment3.db")
    cursor = cx.cursor()
    login(cursor,cx)
    cx.commit() 


main()