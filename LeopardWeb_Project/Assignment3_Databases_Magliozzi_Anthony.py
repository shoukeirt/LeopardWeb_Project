import sqlite3

# database file connection 
database = sqlite3.connect("assignment3.db") 
  
# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 
  
# SQL command to create a table in the database 
sql_command = """CREATE TABLE COURSES (  
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

#Course – CRN, Title, department, time, day(s) of the week, semester, year, credits.


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


#Course – CRN, Title, department, time, day(s) of the week, semester, year, credits.
#Insert 5 Courses
# SQL command to insert the data in the table, must be done one at a time 
sql_command = """INSERT INTO Courses VALUES(2500, 'Computer Science I', 'Computer Science', '12:00pm - 1:00pm', 'M/W/F', 'Fall', 1, 3);"""
#cursor.execute(sql_command)


sql_command = """INSERT INTO Courses VALUES(2750, 'Computer Engineering II', 'Engineering', '10:30am - 11:30am', 'T/W/TR', 'Fall', 2, 4);"""
#cursor.execute(sql_command)


sql_command = """INSERT INTO Courses VALUES(3725, 'English III', 'Humanities', '2:00pm - 3:00pm', 'M/T/F', 'Spring', 3, 3);"""
#cursor.execute(sql_command)


sql_command = """INSERT INTO Courses VALUES(4670, 'Senior Design', 'Engineering', '9:30am - 11:00am', 'T/W/TR', 'Spring', 4, 4);"""
#cursor.execute(sql_command)


sql_command = """INSERT INTO Courses VALUES(4490, 'Engineering Strength of Materials', 'Engineering', '2:00pm - 4:00pm', 'M/T/TR', 'Spring', 4, 4);"""
#cursor.execute(sql_command)



'''  
# execute the statement 
cursor.execute(sql_command) 
  
# SQL command to insert the data in the table, must be done one at a time 
sql_command = """INSERT INTO PROGRAMMER VALUES(1, 'ADA', 'LOVELACE', 1815);"""
#cursor.execute(sql_command) 

sql_command = """INSERT INTO PROGRAMMER VALUES(2, 'GRACE', 'HOPPER', 1906);"""
#cursor.execute(sql_command) 

sql_command = 	"""INSERT INTO PROGRAMMER VALUES(3, 'MARY KENNETH', 'KELLER', 1913);"""
#cursor.execute(sql_command) 
               
sql_command = 	"""INSERT INTO PROGRAMMER VALUES(4, 'EVELYN', 'BOYD GRANVILLE', 1924);"""
#ursor.execute(sql_command) 

sql_command = 	"""INSERT INTO PROGRAMMER VALUES(5, 'CAROL', 'SHAW', 1955);"""
#cursor.execute(sql_command) 

# QUERY FOR ALL
print("Entire table")
cursor.execute("""SELECT * FROM PROGRAMMER""")
query_result = cursor.fetchall()
  
for i in query_result:
	print(i)


# QUERY FOR SOME
print("Only those born prior to 1950")
cursor.execute("""SELECT * FROM PROGRAMMER WHERE BIRTHYEAR < 1950""")
query_result = cursor.fetchall()

for i in query_result:
	print(i)

# ADDING FROM USER INPUT
uid = "6"
fname = raw_input("First name of a famous programmer: ")
lname = raw_input("Last name of the same programmer: ")
birthyear = raw_input("Birth year of the same programmer: ") 

cursor.execute("""INSERT INTO PROGRAMMER VALUES('%s', '%s', '%s', '%s');""" % (uid, fname, lname, birthyear))

print("Entire table")
cursor.execute("""SELECT * FROM PROGRAMMER""")
query_result = cursor.fetchall()
  
for i in query_result:
	print(i)
'''


# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 
database.commit() 
  
# close the connection 
database.close() 
