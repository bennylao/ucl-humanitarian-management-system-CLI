import pandas as pd
import os


class Admin:
    # Path need to be changed depend on the local path for each machine, anyone know how to define a global path that
    # works on every machines

    p = os.path.isfile(r'data\userTesting.csv')

    def __init__(self, username, password, phone):
        self.username = username
        self.password = password
        self.phone = phone


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
        # where should this sit? In event class or here?
        # ben: think we can hv a func to end in event class,
        # and we call the func here
        pass

    # should we've an edit method here? i.e: say admin want to change some details on an already created plan
    def edit_plan(self):
        pass

    def display_humanitarian_plan(self):
        # again, should this probably just be called from the event file?
        # ben: is it the func listing all the plan?
        # if so, in the event class, we can have func __str__ format the description for one plan
        # and use a for loop here to print info of all plans
        # alternatively, we can create a static method in the event class,
        # by calling that method, we read the csv file and print out the info (maybe

        # martha: Yeah, i think that would work, from what i can understand anyway! It's the func
        # that is the requirement where admin can display summary of all related details; including,
        # number of refugees, their campidentification, and number of humanitarian volunteers working
        # at each camp
        pass
