import pandas as pd
from humanitarian_management_system import helper


# Unsure whether to have volunteer and admin as subclasses of a "User". Do we think admin is allowed to do
# Everything that a volunteer can do? Or maybe we just have volunteer as parent class and admin as child?
class Volunteer:
    total_number = 0
    user_data = []
    id_arr = []

    def __init__(self, first_name, last_name, username, phone, password, occupation, active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.phone = phone
        self.password = password
        self.occupation = occupation
        self.active = active

    def pass_data(self):
        # Access user enter values from helper function and assign them to Volunteer class

        # keep track of uid and increment it by 1
        I = helper.extract_data('data/userTesting.csv')['uid']

        for i in I:
            Volunteer.id_arr.append(i)
        uid = Volunteer.id_arr.pop()
        uid += 1

        Volunteer.user_data = [[uid, 'Volunteer', self.active, 'None', self.first_name, self.last_name, self.username,
                                self.occupation, self.phone, self.password]]
        user_df = pd.DataFrame(Volunteer.user_data,
                               columns=['uid', 'userType', 'active', 'camp', 'firstName', 'lastName', 'userName',
                                        'occupation', 'phone', 'password'])
        # Pass assign values into .csv file
        with open('data/userTesting.csv', 'a') as f:
            user_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

        Volunteer.total_number += 1

    def edit_personal_info(self):
        pass

    def edit_camp_info(self):
        # Should this sit in the camp class & be called by volunteer?
        pass

    def create_refugee_profile(self):
        # Should this just sit in the refugee class and be called by volunteer?
        pass

    def edit_refugee_info(self):
        # Should we also give volunteer the ability to edit existing refugee profiles?
        pass
