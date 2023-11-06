import pandas as pd


# Unsure whether to have volunteer and admin as subclasses of a "User". Do we think admin is allowed to do
# Everything that a volunteer can do? Or maybe we just have volunteer as parent class and admin as child?
class Volunteer:
    total_number = 0
    user_data = []
    path = r'C:\Users\jason\PycharmProjects\COMP0066_Humanitarian_Management_System\data'

    def __init__(self, first_name, last_name, username, phone, password, occupation):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.phone = phone
        self.password = password
        self.occupation = occupation

    def pass_data(self):
        # Access user enter values from helper function and assign them to Volunteer class
        Volunteer.user_data = [['Volunteer', 'Active', self.first_name, self.last_name, self.username,
                                self.occupation, self.phone, self.password]]
        user_df = pd.DataFrame(Volunteer.user_data,
                               columns=['userType', 'status', 'firstName', 'lastName', 'userName',
                                        'occupation', 'phone', 'password'])
        user_df.index.name = 'uid'
        # Pass assign values into .csv file
        with open(Volunteer.path + 'userTesting.csv', 'a') as f:
            user_df.to_csv(f, mode='a', header=f.tell() == 0, index=True)

        Volunteer.total_number += 1


    @staticmethod
    def read_data(self):
        # Extract data info from .csv file, ie. extract all usernames from the data and return them to helper
        # function for validation
        try:
            result_df = pd.read_csv(Volunteer.path + 'userTesting.csv')
            data_username = result_df['userName']
            data_password = result_df['password']
            data_status = result_df['status']
            return data_username, data_password, data_status
        except:
            data_username = ''
            data_password = ''
            return data_username, data_password

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
