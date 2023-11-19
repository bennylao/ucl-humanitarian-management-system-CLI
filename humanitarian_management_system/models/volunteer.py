import pandas as pd
from humanitarian_management_system.helper import extract_data


# Unsure whether to have volunteer and admin as subclasses of a "User". Do we think admin is allowed to do
# Everything that a volunteer can do? Or maybe we just have volunteer as parent class and admin as child?
class Volunteer:
    total_number = 0
    user_data = []

    def __init__(self, username, password, first_name, last_name, email, phone, occupation, active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.phone = phone
        self.email = email
        self.password = password
        self.occupation = occupation
        self.active = active

    def pass_data(self):
        # Access user enter values from helper function and assign them to Volunteer class

        # keep track of uid and increment it by 1
        id_arr = extract_data("data/user.csv","userID").tolist()

        uid = id_arr.pop()
        uid += 1

        Volunteer.user_data = [[uid, 'Volunteer', self.active, self.username, self.password, self.first_name, self.last_name,
                                self.email, self.phone, self.occupation, 'None', 'None']]
        user_df = pd.DataFrame(Volunteer.user_data,
                               columns=['userID', 'userType', 'isActive', 'username', 'password', 'firstName', 'lastName',
                                        'email', 'phone', 'occupation', 'roleID', 'campID'])
        # Pass assign values into .csv file
        with open('data/user.csv', 'a') as f:
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
