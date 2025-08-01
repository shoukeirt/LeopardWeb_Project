import sqlite3


class User():
    def __init__(self, in_firstname, in_lastname, in_id):

        #attributes 
        self.firstName = in_firstname
        self.lastName = in_lastname
        self.name = in_firstname + " " +  in_lastname
        self.id = in_id

    #Methods
    def set_name(self):
        first_name = input("What is your first name?")
        last_name = input("What is your last name?")
        self.name = first_name + "  " + last_name

    def print_name(self): 
        return "User " + " " + self.name;

    def print_id(self):
        return "USER" + " " + self.id
    
    def set_name(self):
        self.name =  input("What would you like to set the user's name to?") 
    
    def set_id(self):
        self.id =  input("What would you like to set the user's ID to?") 
    
    def print_all_info(self):
        print(f"ALL INFO: \n")
        return "NAME: " + " " + self.print_name() + "\n" + "ID: " + self.print_id() +"\n"