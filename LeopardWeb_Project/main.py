import sqlite3
import os
import user
import student
import instructor 
import admin

def main():
    cx = sqlite3.connect("assignment3.db")
    cursor = cx.cursor()

    cursor.execute("SELECT * FROM STUDENT")
    rows = cursor.fetchall();

    for row in rows:
        print(row)

    cx = sqlite3.connect("assignment3.db")
    cursor = cx.cursor()
    
    cursor.execute("SELECT * FROM INSTRUCTOR")
    rows = cursor.fetchall();

    for row in rows:
        print(row)
        
    sql_command = """INSERT INTO student VALUES(10011, 'ANTHONY', 'MAGLIOZZI', 2026, "BSCE",'Magliozzia');"""
    cursor.execute(sql_command)
    
    cursor.execute("SELECT * FROM STUDENT")
    rows = cursor.fetchall();

    for row in rows:
        print(row)
        
    cursor.execute("PRAGMA table_info(STUDENT);")
    for col in cursor.fetchall():
        print(col)
    
    print("USING:", os.path.abspath("assignment3.db"))
    
    student = student.Student("Hill","Hill",1)
    student.search_courses("CRN", "2500")
    
    new_admin1 = admin.Admin("Boss","Man", 30003)
    new_admin1.add_course()


main()




