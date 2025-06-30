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
# cursor.execute(sql_command)


#SQL command to insert the data in the table, must be done one at a time 
sql_command = """INSERT INTO STUDENT VALUES(8765, 'ANTHONY', 'MAGLIOZZI', 2026, "BSCE",'Magliozzia');"""
# cursor.execute(sql_command)


sql_command = """INSERT INTO STUDENT VALUES(8888, 'TO', 'JO', 4, 'MECH', 'TJ.EDU');"""
# cursor.execute(sql_command)

#Execute the SQL delete command
sql_command = """DELETE FROM INSTRUCTOR WHERE ID = 20001;"""
# cursor.execute(sql_command)


#Execute the SQL update command
sql_command = """UPDATE admin SET TITLE = 'Vice-President' WHERE NAME = 'Vera';"""
# cursor.execute(sql_command)


#Course CRN, Title, department, time, day(s) of the week, semester, year, credits.
#Insert 5 Courses
# SQL command to insert the data in the table, must be done one at a time 
sql_command = """INSERT INTO COURSES VALUES(2500, 'Computer Science I', 'BSAS', '12:00pm - 1:00pm', 'M/W/F', 'Fall',2022, 3)"""
# cursor.execute(sql_command)


sql_command = """INSERT INTO COURSES VALUES(2750, 'Computer Engineering II', 'BSCO', '10:30am - 11:30am', 'T/W/TR', 'Fall', 2222,4)"""
# cursor.execute(sql_command)


sql_command = """INSERT INTO COURSES VALUES(3725, 'English III', 'HUSS', '2:00pm - 3:00pm', 'M/T/F', 'Spring',2222, 3)"""
# cursor.execute(sql_command)


sql_command = """INSERT INTO COURSES VALUES(4670, 'Senior Design', 'BSCO', '9:30am - 11:00am', 'T/W/TR', 'Spring',2222, 4)"""
# cursor.execute(sql_command)


sql_command = """INSERT INTO COURSES VALUES(4490, 'Engineering Strength of Materials', 'BSME', '2:00pm - 4:00pm', 'M/T/TR', 'Spring',2021, 4)"""
# cursor.execute(sql_command)


#print the courses to the console
# print("Entire table")
# cursor.execute("""SELECT * FROM Courses""")
# query_result = cursor.fetchall()
  
# for i in query_result:
# 	print(i)


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
# cursor.execute(sql_command)

sql_command = """
CREATE TABLE IF NOT EXISTS ENROLLMENT (
    STUDENT_ID INTEGER,
    CRN INTEGER,
    FOREIGN KEY(STUDENT_ID) REFERENCES STUDENT(ID), 
    FOREIGN KEY(CRN) REFERENCES COURSES(CRN)
)
""" #student has to exist in STUDENTS to be added to a course. 
    #If not, we will display a message saying the user doesn't exist.
# cursor.execute(sql_command)

# print the courses and what professor is teaching them
# print("Entire table")
# cursor.execute("""SELECT * FROM COURSE_TEACHER""")
# query_result = cursor.fetchall()
# for i in query_result:
# 	print(i)


sql_command = """CREATE TABLE LOGIN(  
ID INTEGER PRIMARY KEY NOT NULL,
EMAIL TEXT NOT NULL,
PASSWORD INTEGER NOT NULL
)
;"""
# cursor.execute(sql_command)

#STUDENT TABLE INFO
# sql_command = """INSERT INTO LOGIN VALUES(10001, "newtoni", 1144)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10002, "curiem", 6760)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10003, "telsan", 1691)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10004, "notcool", 9391)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10005, "vonneumannj", 6407)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10006, "hopperg", 6595)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10007, "jemisonm", 9304)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10008, "deanm", 9469)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10009, "faradaym", 7886)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10010, "lovelacea", 5598)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10011, "magliozzia", 7761)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10012, "jot", 1598)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10013, "brownj", 2382)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10014, "smartm", 1121)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10015, "moorem", 3313)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10016, "irwinr", 5749)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10017, "lawrencet", 1981)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10018, "wilsono", 8727)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10019, "parkerp", 7665)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(10020, "bradyt", 2957)"""
# cursor.execute(sql_command)
# #INSTRUCTOR LOGIN TABLE INFO
# sql_command = """INSERT INTO LOGIN VALUES(20002, "patrickn", 6034)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20003, "galileig", 3074)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20004, "turinga", 5396)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20005, "boumank", 5896)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20006, "bernoullid", 9916)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20007, "stevensb", 4140)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20008, "duncane", 5235)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20009, "griffinh", 9618)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20010, "ironsl", 4100)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20011, "chambersm", 3451)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20012, "weathersc", 4385)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20013, "smithm", 8321)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20014, "birdl", 4016)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(20015, "mossr", 5166)"""
# cursor.execute(sql_command)
# #ADMIN LOGIN TABLE INFO
# sql_command = """INSERT INTO LOGIN VALUES(30001, "hamiltonm", 8212)"""
# cursor.execute(sql_command)
# sql_command = """INSERT INTO LOGIN VALUES(30002, "rubinv", 3325)"""
# cursor.execute(sql_command)



# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 

print("Success!")
database.commit() 
  
# close the connection 
database.close() 