from user import User

class Instructor(User):
    def __init__(self, in_firstName, in_lastName, in_id):
        User.__init__(self, in_firstName, in_lastName, in_id)
        
    def print_schedule(self):
          return "This is the print schedule function!"
    
    def print_classlist(self):
          return "This is the print classlist function!"
    
    def search_courses(self):
          return "This is the search courses for instructors function!"

    def print_all_info(self):
        print(f"ALL INSTRUCTOR INFO: \n")
        return "NAME: " + " " + self.print_name() + "\n" + "ID: " + self.print_id() +"\n"
