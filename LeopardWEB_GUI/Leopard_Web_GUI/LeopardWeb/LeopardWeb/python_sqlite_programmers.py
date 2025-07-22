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


sql_command = """CREATE TABLE IF NOT EXISTS LOGIN(  
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

#Create Student_Schedule table on startup if not already in the database


    #SQL table definition
# create_schedule_table = """
#     CREATE TABLE IF NOT EXISTS Student_Schedule (
#     StudentName TEXT PRIMARY KEY NOT NULL,
#     CRN1 INTEGER NOT NULL,
#     Course1 TEXT NOT NULL,
#     DOW1 TEXT NOT NULL,
#     Time1 TEXT NOT NULL,
#     CRN2 INTEGER NOT NULL,
#     Course2 TEXT,
#     DOW2 TEXT,
#     Time2 TEXT,
#     CRN3 INTEGER NOT NULL,
#     Course3 TEXT,
#     DOW3 TEXT,
#     Time3 TEXT,
#     CRN4 INTEGER NOT NULL,
#     Course4 TEXT,
#     DOW4 TEXT,
#     Time4 TEXT,
#     CRN5 INTEGER NOT NULL,
#     Course5 TEXT,
#     DOW5 TEXT,
#     Time5 TEXT
# );
# """

update_course_prof = """
INSERT INTO COURSE_TEACHER (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, CREDITS, INSTRUCTOR_ID, INSTRUCTOR_NAME, INSTRUCTOR_SURNAME, INSTRUCTOR_TITLE) VALUES
(2850, 'Microcontrollers Using C', 'BSCOE', '08:00 AM - 9:15 AM', 'T/R/F', 'Fall, Spring', 4, 20010, 'Lena', 'Irons', 'Assistant Prof.'),
(2025, 'Multivariable Calculus', 'MATH', '11:00 AM - 12:00 PM', 'M/T/R', 'Fall, Spring', 4, 20015, 'Randy', 'Moss', 'Associate Prof.'),
(2000, 'Statics and Mechanics I', 'BSCE', '1:00 PM - 2:15 PM', 'T/R', 'Fall, Spring', 3, 20007, 'Brad', 'Stevens', 'Full Prof.'),
(3150, 'Object Oriented Programming', 'BSCO', '2:30 PM - 3:45 PM', 'M/W/F', 'Fall', 4, 20008, 'Edward', 'Duncan', 'Full Prof.'),
(3250, 'Analog Circuit Design', 'BSEE', '3:30 PM - 4:45 PM', 'T/W/R', 'Spring', 4, 20009, 'Helen', 'Griffin', 'Associate Prof.'),
(3225, 'Applied Programming Concepts', 'BSCO', '10:00 AM - 11:45 AM', 'M/W/R', 'Fall, Spring', 3, 20011, 'Morgan', 'Chambers', 'Associate Prof.'),
(3200, 'Engineering Economy', 'MGMT', '09:30 AM - 10:45 AM', 'T/R', 'Spring', 3, 20014, 'Larry', 'Bird', 'Assistant Prof.'),
(4075, 'Engineering Operating Systems', 'BSCO', '3:00 PM - 4:45 PM', 'M/W', 'Fall', 4, 20013, 'Marcus', 'Smith', 'Full Prof.'),
(3999, 'Engineering Electromagnetics', 'BSEE', '11:00 AM - 12:15 PM', 'M/W/F', 'Spring', 4, 20009, 'Helen', 'Griffin', 'Associate Prof.'),
(4050, 'Motors and Controls', 'BSEE', '09:00 AM - 10:15 AM', 'T/R/F', 'Fall', 4, 20012, 'Carl', 'Weathers', 'Assistant Prof.'),
(5800, 'Mathematical Methods', 'MATH', '1:00 PM - 2:15 PM', 'T/R', 'Fall, Spring', 3, 20015, 'Randy', 'Moss', 'Associate Prof.'),
(7100, 'Project Management Applications', 'MGMT', '12:30 PM - 1:45 PM', 'W/F', 'Spring', 3, 20014, 'Larry', 'Bird', 'Assistant Prof.'),
(7101, 'Professional Perspectives', 'BSEE', '10:00 AM - 11:45 AM', 'M/F', 'Fall', 3, 20012, 'Carl', 'Weathers', 'Assistant Prof.'),
(4025, 'Hardware Security', 'BSCOE', '2:00 PM - 3:30 PM', 'T/F', 'Fall', 3, 20005, 'Katie', 'Bouman', 'Assistant Prof.');"""
# cursor.execute(update_course_prof)

# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 
update_enrollment = """-- Clear existing enrollment data and insert new data
DELETE FROM ENROLLMENT;

INSERT INTO ENROLLMENT (STUDENT_ID, CRN) VALUES
(10001, 7100),
(10001, 4670),
(10001, 2025),
(10001, 4025),
(10001, 3250),
(10002, 2850),
(10002, 3999),
(10002, 4670),
(10002, 2000),
(10002, 4075),
(10003, 4025),
(10003, 4670),
(10003, 7100),
(10003, 2025),
(10003, 3250),
(10004, 2000),
(10004, 3200),
(10004, 7100),
(10004, 2850),
(10004, 4075),
(10005, 2000),
(10005, 3200),
(10005, 2025),
(10005, 7100),
(10005, 2850),
(10006, 2000),
(10006, 2025),
(10006, 2850),
(10006, 3200),
(10006, 7100),
(10007, 2750),
(10007, 4075),
(10007, 5800),
(10007, 7101),
(10007, 2850),
(10009, 2850),
(10009, 3999),
(10009, 3250),
(10009, 7100),
(10009, 4670),
(10010, 2000),
(10010, 2850),
(10010, 2750),
(10010, 7101),
(10010, 4075),
(10011, 2850),
(10011, 3250),
(10011, 3200),
(10011, 3999),
(10011, 2000),
(10012, 2025),
(10012, 7100),
(10012, 3250),
(10012, 3725),
(10012, 3200),
(10013, 3150),
(10013, 2000),
(10013, 7100),
(10013, 3999),
(10013, 3200),
(10014, 4025),
(10014, 3200),
(10014, 7101),
(10014, 4075),
(10014, 2850),
(10017, 3200),
(10017, 3250),
(10017, 4025),
(10017, 7100),
(10017, 2850),
(10019, 7100),
(10019, 3250),
(10019, 2850),
(10019, 4670),
(10019, 3725),
(10020, 4025),
(10020, 4075),
(10020, 3200),
(10020, 7101),
(10020, 7100);"""

# cursor.executescript(update_enrollment)

update_student_schedule = """-- Clear existing student schedule data and insert new data
DELETE FROM student_schedule;

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Isaac Newton', 7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM',
    4670, 'Senior Design', 'T/W/TR', '09:30 AM - 11:00 AM',
    2025, 'Multivariable Calculus', 'M/T/R', '11:00 AM - 12:00 PM',
    4025, 'Hardware Security', 'T/F', '02:00 PM - 03:30 PM',
    3250, 'Analog Circuit Design', 'T/W/R', '03:30 PM - 04:45 PM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Marie Curie', 2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM',
    3999, 'Engineering Electromagnetics', 'M/W/F', '11:00 AM - 12:15 PM',
    4670, 'Senior Design', 'T/W/TR', '09:30 AM - 11:00 AM',
    2000, 'Statics and Mechanics I', 'T/R', '01:00 PM - 02:15 PM',
    4075, 'Engineering Operating Systems', 'M/W', '03:00 PM - 04:45 PM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Nikola Tesla', 4025, 'Hardware Security', 'T/F', '02:00 PM - 03:30 PM',
    4670, 'Senior Design', 'T/W/TR', '09:30 AM - 11:00 AM',
    7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM',
    2025, 'Multivariable Calculus', 'M/T/R', '11:00 AM - 12:00 PM',
    3250, 'Analog Circuit Design', 'T/W/R', '03:30 PM - 04:45 PM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Thomas Edison', 2000, 'Statics and Mechanics I', 'T/R', '01:00 PM - 02:15 PM',
    3200, 'Engineering Economy', 'T/R', '09:30 AM - 10:45 AM',
    7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM',
    2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM',
    4075, 'Engineering Operating Systems', 'M/W', '03:00 PM - 04:45 PM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'John von Neumann', 2000, 'Statics and Mechanics I', 'T/R', '01:00 PM - 02:15 PM',
    3200, 'Engineering Economy', 'T/R', '09:30 AM - 10:45 AM',
    2025, 'Multivariable Calculus', 'M/T/R', '11:00 AM - 12:00 PM',
    7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM',
    2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Grace Hopper', 2000, 'Statics and Mechanics I', 'T/R', '01:00 PM - 02:15 PM',
    2025, 'Multivariable Calculus', 'M/T/R', '11:00 AM - 12:00 PM',
    2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM',
    3200, 'Engineering Economy', 'T/R', '09:30 AM - 10:45 AM',
    7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Mae Jemison', 2750, 'Computer Engineering II', 'T/W/TR', '10:30 AM - 11:30 AM',
    4075, 'Engineering Operating Systems', 'M/W', '03:00 PM - 04:45 PM',
    5800, 'Mathematical Methods', 'T/R', '01:00 PM - 02:15 PM',
    7101, 'Professional Perspectives', 'M/F', '10:00 AM - 11:45 AM',
    2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Michael Faraday', 2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM',
    3999, 'Engineering Electromagnetics', 'M/W/F', '11:00 AM - 12:15 PM',
    3250, 'Analog Circuit Design', 'T/W/R', '03:30 PM - 04:45 PM',
    7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM',
    4670, 'Senior Design', 'T/W/TR', '09:30 AM - 11:00 AM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Ada Lovelace', 2000, 'Statics and Mechanics I', 'T/R', '01:00 PM - 02:15 PM',
    2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM',
    2750, 'Computer Engineering II', 'T/W/TR', '10:30 AM - 11:30 AM',
    7101, 'Professional Perspectives', 'M/F', '10:00 AM - 11:45 AM',
    4075, 'Engineering Operating Systems', 'M/W', '03:00 PM - 04:45 PM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Anthony Magliozzi', 2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM',
    3250, 'Analog Circuit Design', 'T/W/R', '03:30 PM - 04:45 PM',
    3200, 'Engineering Economy', 'T/R', '09:30 AM - 10:45 AM',
    3999, 'Engineering Electromagnetics', 'M/W/F', '11:00 AM - 12:15 PM',
    2000, 'Statics and Mechanics I', 'T/R', '01:00 PM - 02:15 PM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'To Jo', 2025, 'Multivariable Calculus', 'M/T/R', '11:00 AM - 12:00 PM',
    7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM',
    3250, 'Analog Circuit Design', 'T/W/R', '03:30 PM - 04:45 PM',
    3725, 'English III', 'M/T/F', '02:00 PM - 03:00 PM',
    3200, 'Engineering Economy', 'T/R', '09:30 AM - 10:45 AM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Jalen Brown', 3150, 'Object Oriented Programming', 'M/W/F', '02:30 PM - 03:45 PM',
    2000, 'Statics and Mechanics I', 'T/R', '01:00 PM - 02:15 PM',
    7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM',
    3999, 'Engineering Electromagnetics', 'M/W/F', '11:00 AM - 12:15 PM',
    3200, 'Engineering Economy', 'T/R', '09:30 AM - 10:45 AM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Marcus Smart', 4025, 'Hardware Security', 'T/F', '02:00 PM - 03:30 PM',
    3200, 'Engineering Economy', 'T/R', '09:30 AM - 10:45 AM',
    7101, 'Professional Perspectives', 'M/F', '10:00 AM - 11:45 AM',
    4075, 'Engineering Operating Systems', 'M/W', '03:00 PM - 04:45 PM',
    2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Mason Moore', 2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM',
    3725, 'English III', 'M/T/F', '02:00 PM - 03:00 PM',
    3999, 'Engineering Electromagnetics', 'M/W/F', '11:00 AM - 12:15 PM',
    3250, 'Analog Circuit Design', 'T/W/R', '03:30 PM - 04:45 PM',
    7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Ryan Irwin', 3150, 'Object Oriented Programming', 'M/W/F', '02:30 PM - 03:45 PM',
    4670, 'Senior Design', 'T/W/TR', '09:30 AM - 11:00 AM',
    2000, 'Statics and Mechanics I', 'T/R', '01:00 PM - 02:15 PM',
    7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM',
    2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Taylor Lawrence', 3200, 'Engineering Economy', 'T/R', '09:30 AM - 10:45 AM',
    3250, 'Analog Circuit Design', 'T/W/R', '03:30 PM - 04:45 PM',
    4025, 'Hardware Security', 'T/F', '02:00 PM - 03:30 PM',
    7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM',
    2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Owen Wilson', 7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM',
    2000, 'Statics and Mechanics I', 'T/R', '01:00 PM - 02:15 PM',
    3200, 'Engineering Economy', 'T/R', '09:30 AM - 10:45 AM',
    7101, 'Professional Perspectives', 'M/F', '10:00 AM - 11:45 AM',
    3150, 'Object Oriented Programming', 'M/W/F', '02:30 PM - 03:45 PM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Peter Parker', 7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM',
    3250, 'Analog Circuit Design', 'T/W/R', '03:30 PM - 04:45 PM',
    2850, 'Microcontrollers Using C', 'T/R/F', '08:00 AM - 09:15 AM',
    4670, 'Senior Design', 'T/W/TR', '09:30 AM - 11:00 AM',
    3725, 'English III', 'M/T/F', '02:00 PM - 03:00 PM'
);

INSERT INTO student_schedule (
    StudentName, CRN1, Course1, DOW1, Time1,
    CRN2, Course2, DOW2, Time2,
    CRN3, Course3, DOW3, Time3,
    CRN4, Course4, DOW4, Time4,
    CRN5, Course5, DOW5, Time5
) VALUES (
    'Tom Brady', 4025, 'Hardware Security', 'T/F', '02:00 PM - 03:30 PM',
    4075, 'Engineering Operating Systems', 'M/W', '03:00 PM - 04:45 PM',
    3200, 'Engineering Economy', 'T/R', '09:30 AM - 10:45 AM',
    7101, 'Professional Perspectives', 'M/F', '10:00 AM - 11:45 AM',
    7100, 'Project Management Applications', 'W/F', '12:30 PM - 01:45 PM'
);"""


import sqlite3

# Database connection
update_instructor = """-- Clear existing instructor data and insert new data
DELETE FROM INSTRUCTOR;

INSERT INTO INSTRUCTOR (ID, NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL) VALUES
(20002, 'Nelson', 'Patrick', 'Full Prof.', 1994, 'HUS', 'spatrickn@college.edu'),
(20003, 'Galileo', 'Galilei', 'Full Prof.', 1600, 'BSAS', 'ggalileig@college.edu'),
(20004, 'Alan', 'Turing', 'Associate Prof.', 1940, 'BSCO', 'aturinga@college.edu'),
(20005, 'Katie', 'Bouman', 'Assistant Prof.', 2019, 'BSCOE', 'kboumank@college.edu'),
(20006, 'Daniel', 'Bernoulli', 'Associate Prof.', 1760, 'BSME', 'dbernoullid@college.edu'),
(20007, 'Brad', 'Stevens', 'Full Prof.', 2020, 'BSCE', 'bstevensb@college.edu'),
(20008, 'Edward', 'Duncan', 'Full Prof.', 2011, 'BSCO', 'eduncane@college.edu'),
(20009, 'Helen', 'Griffin', 'Associate Prof.', 2023, 'BSEE', 'hgriffinh@college.edu'),
(20010, 'Lena', 'Irons', 'Assistant Prof.', 2024, 'BSCO', 'lironsl@college.edu'),
(20011, 'Morgan', 'Chambers', 'Associate Prof.', 2021, 'BSCO', 'mchambersm@college.edu'),
(20012, 'Carl', 'Weathers', 'Assistant Prof.', 2022, 'BSEE', 'cweathersc@college.edu'),
(20013, 'Marcus', 'Smith', 'Full Prof.', 2013, 'BSCOE', 'msmithm@college.edu'),
(20014, 'Larry', 'Bird', 'Assistant Prof.', 2020, 'MGMT', 'lbirdl@college.edu'),
(20015, 'Randy', 'Moss', 'Associate Prof.', 2021, 'MATH', 'rmossr@college.edu'),
(20016, 'Chet', 'Holmgren', 'Full Prof.', 2022, 'BSCO', 'cholmgren@college.edu');"""


cursor.executescript(update_instructor)
print("Success!")
database.commit() 
  
# close the connection 
database.close() 