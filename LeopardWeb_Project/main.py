import sqlite3



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


main()




