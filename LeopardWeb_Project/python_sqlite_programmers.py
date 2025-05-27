import sqlite3

# database file connection 
database = sqlite3.connect("pythonProgrammers.db") 
  
# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 
  
# SQL command to create a table in the database 
sql_command = """CREATE TABLE PROGRAMMER (  
ID INTEGER PRIMARY KEY NOT NULL,
NAME TEXT NOT NULL,
SURNAME TEXT NOT NULL,
BIRTHYEAR INTEGER NOT NULL)
;"""
  
# execute the statement 
cursor.execute(sql_command) 
  
# SQL command to insert the data in the table, must be done one at a time 
sql_command = """INSERT INTO PROGRAMMER VALUES(1, 'ADA', 'LOVELACE', 1815);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO PROGRAMMER VALUES(2, 'GRACE', 'HOPPER', 1906);"""
cursor.execute(sql_command) 

sql_command = 	"""INSERT INTO PROGRAMMER VALUES(3, 'MARY KENNETH', 'KELLER', 1913);"""
cursor.execute(sql_command) 
               
sql_command = 	"""INSERT INTO PROGRAMMER VALUES(4, 'EVELYN', 'BOYD GRANVILLE', 1924);"""
cursor.execute(sql_command) 

sql_command = 	"""INSERT INTO PROGRAMMER VALUES(5, 'CAROL', 'SHAW', 1955);"""
cursor.execute(sql_command) 

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

# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 
database.commit() 
  
# close the connection 
database.close() 
