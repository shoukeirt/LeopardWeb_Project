import sqlite3

# database file connection 
database = sqlite3.connect("assignment3.db") 
  
# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 
  
#Course CRN, Title, department, time, day(s) of the week, semester, year, credits.
# SQL command to create a table in the database 
sql_command = """CREATE TABLE COURSES(  
CRN INTEGER PRIMARY KEY NOT NULL,
TITLE TEXT NOT NULL,
DEPARTMENT TEXT NOT NULL,
TIME TEXT NOT NULL,
DAYS TEXT NOT NULL,
SEMESTER TEXT NOT NULL,
YEAR INTEGER NOT NULL,
CREDITS INTEGER NOT NULL
)
;"""
#cursor.execute(sql_command)




#SQL command to insert the data in the table, must be done one at a time 
sql_command = """INSERT INTO STUDENT VALUES(5555, 'ANTHONY', 'MAGLIOZZI', 3, 'COEN', 'MA.EDU');"""
#cursor.execute(sql_command)


sql_command = """INSERT INTO STUDENT VALUES(8888, 'TO', 'JO', 4, 'MECH', 'TJ.EDU');"""
#cursor.execute(sql_command)


#Execute the SQL delete command
sql_command = """DELETE FROM INSTRUCTOR WHERE ID = 20001;"""
#cursor.execute(sql_command)


#Execute the SQL update command
sql_command = """UPDATE admin SET TITLE = 'Vice-President' WHERE NAME = 'Vera';"""
#cursor.execute(sql_command)


#Course CRN, Title, department, time, day(s) of the week, semester, year, credits.
#Insert 5 Courses
# SQL command to insert the data in the table, must be done one at a time 
sql_command = """INSERT INTO COURSES VALUES(2500, 'Computer Science I', 'BSAS', '12:00pm - 1:00pm', 'M/W/F', 'Fall',2022, 3)"""
#cursor.execute(sql_command)


sql_command = """INSERT INTO COURSES VALUES(2750, 'Computer Engineering II', 'BSCO', '10:30am - 11:30am', 'T/W/TR', 'Fall', 2222,4)"""
#cursor.execute(sql_command)


sql_command = """INSERT INTO COURSES VALUES(3725, 'English III', 'HUSS', '2:00pm - 3:00pm', 'M/T/F', 'Spring',2222, 3)"""
#cursor.execute(sql_command)


sql_command = """INSERT INTO COURSES VALUES(4670, 'Senior Design', 'BSCO', '9:30am - 11:00am', 'T/W/TR', 'Spring',2222, 4)"""
#cursor.execute(sql_command)


sql_command = """INSERT INTO COURSES VALUES(4490, 'Engineering Strength of Materials', 'BSME', '2:00pm - 4:00pm', 'M/T/TR', 'Spring',2021, 4)"""
#cursor.execute(sql_command)


#print the courses to the console
print("Entire table")
cursor.execute("""SELECT * FROM Courses""")
query_result = cursor.fetchall()
  
for i in query_result:
	print(i)



# create a table that cointains who is teaching which course

sql_command = """
CREATE TABLE IF NOT EXISTS COURSE_TEACHER AS  
SELECT 
    C.CRN, 
    C.TITLE, 
    C.DEPARTMENT, 
    C.TIME, 
    C.DAYS, 
    C.SEMESTER, 
    C.CREDITS,
    I.ID AS INSTRUCTOR_ID,
    I.NAME AS INSTRUCTOR_NAME,
    I.SURNAME AS INSTRUCTOR_SURNAME,
    I.TITLE AS INSTRUCTOR_TITLE
FROM COURSES C
JOIN INSTRUCTOR I ON C.DEPARTMENT = I.DEPT;
"""
#cursor.execute(sql_command)

# print the courses and what professor is teaching them
print("Entire table")
cursor.execute("""SELECT * FROM COURSE_TEACHER""")
query_result = cursor.fetchall()
for i in query_result:
	print(i)



# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 
database.commit() 
  
# close the connection 
database.close() 
