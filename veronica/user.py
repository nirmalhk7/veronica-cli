from getpass import getuser

class User():
    firstname       = None
    middlename      = None
    lastname        = None
    phone_numbers   = None
    birthdate       = None
    address         = None
    system_username = getuser()

    def get_name(self):
        return self.firstname or self.system_username.capitalize()
    
    def sanitise(self,statement):
        return statement