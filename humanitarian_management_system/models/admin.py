import pandas as pd
import os
from .user import User


class Admin(User):
    # Path need to be changed depend on the local path for each machine, anyone know how to define a global path that
    # works on every machines

    p = os.path.isfile(r'data\userTesting.csv')

    def __init__(self, username, password, first_name, last_name, email, phone, occupation):
        super().__init__(username, password)
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.occupation = occupation

    def edit_volunteer_account(self, volunteer_name):
        pass

    def allocate_resource(self):
        # should this just call from resources class?
        pass

    def deactivate_user(self):
        pass

    def create_humanitarian_plan(self):
        pass

    def end_event(self):
        pass

    def edit_plan(self):
        pass

    def display_humanitarian_plan(self):
        pass
