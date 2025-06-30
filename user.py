import sqlite3

class User():
    def __init__(self, in_firstname, in_lastname, in_id):
        self.name = f"{in_firstname}  {in_lastname}"
        self.firstName = in_firstname
        self.lastName = in_lastname
        self.id = in_id

    def set_name(self):
        self.name = input("What would you like to set the user's name to?")

    def set_id(self):
        self.id = input("What would you like to set the user's ID to?")

    def print_name(self): 
        return "User " + self.name

    def print_id(self):
        return "USER " + str(self.id)

    def print_all_info(self):
        print("ALL INFO:")
        return "NAME: " + self.print_name() + "\n" + "ID: " + self.print_id() + "\n"
