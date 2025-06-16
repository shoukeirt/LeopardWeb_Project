from user import User

class Admin(User):
    def __init__(self, in_firstName, in_lastName, in_id):
        User.__init__(self, in_firstName, in_lastName, in_id)
        
    #methods    
    def add_course(self):
          return"This is the function that adds a course to the classlist"

    def remove_course(self):
         return"This it the function that removes a course from the classlist"
    
    def add_user(self):
          return"This is the function that adds a user to the system"
    
    def remove_user(self):
          return"This is the function that removes a user from the system"
    
    def add_to_course(self):
          return"This is the function that adds a student to a course"

    def remove_from_course(self):
          return"This is the function that removes a student from a course"

    def print_schedule(self):
          return "This is the print schedule function!"
    
    def print_classlist(self):
         return "This is the print classlist function!"
    
    def search_courses(self):
          return "This is the search courses for instructors/admins function!"

    def print_courses(self):
          return "This is the function to print courses"
    
    def search_roster(self):
          return "This is the function to seach the roster"

    def print_roster(self):
          return "This is the function to print a roster"
   
    
    
    
    

    
