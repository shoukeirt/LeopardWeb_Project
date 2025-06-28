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
    new_admin1.add_instructor()
    cx.commit() 

# close the connection 
    cx.close() 

main()




