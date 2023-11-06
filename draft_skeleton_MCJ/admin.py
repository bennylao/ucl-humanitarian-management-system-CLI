import pandas as pd
import os


class Admin:

    p1 = os.path.isfile(r'C:\Users\jason\PycharmProjects\COMP0066_Humanitarian_Management_System\datauserTesting.csv')
    p2 = r'C:\Users\jason\PycharmProjects\COMP0066_Humanitarian_Management_System\data'

    def __init__(self, username, password, phone):
        self.username = username
        self.password = password
        self.phone = phone

    def default_account(self):
        # Create a default account for admin - only one admin
        Admin.user_data = [['Admin', 'None', 'None', 'None', self.username,
                            'None', self.phone, self.password]]
        admin_df = pd.DataFrame(Admin.user_data,
                                columns=['userType', 'status', 'firstName', 'lastName', 'userName',
                                         'occupation', 'phone', 'password'])
        admin_df.index.name = 'uid'
        if not Admin.p1:
            admin_df.to_csv(Admin.p2 + 'userTesting.csv')
        else:
            pass

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
        # I think the plan is supposed to end itself automatically based on the end date, similar to the auction project
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
