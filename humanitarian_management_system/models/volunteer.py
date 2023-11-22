import pandas as pd
from humanitarian_management_system.helper import extract_data, modify_csv_pandas
from pathlib import Path
from .user import User


class Volunteer(User):

    def __init__(self, username, password, first_name, last_name, email, phone, occupation, role_id, event_id, camp_id):
        super().__init__(username, password)
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.occupation = occupation
        self.role_id = role_id
        self.event_id = event_id
        self.camp_id = camp_id

    @staticmethod
    def create_new_record(registration_info):
        user_df = pd.DataFrame(data=[registration_info],
                               columns=['userType', 'isActive', 'username', 'password', 'firstName',
                                        'lastName', 'email', 'phone', 'occupation', 'roleID', 'eventID', 'campID'])
        csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        # Pass assign values into .csv file
        user_df.to_csv(csv_path, mode='a', index=False, header=False)

    def join_camp(self, event_id, camp_id):
        csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        df = pd.read_csv(csv_path)

        modify_csv_pandas("data/user.csv", "username", self.username, "campID", camp_id)
        modify_csv_pandas("data/user.csv", "username", self.username, "eventID", event_id)
        modify_csv_pandas("data/user.csv", "username", self.username, "roleID", self.role_id)

        # update volunteer population for camp
        Volunteer.total_number = int(df.loc[df['campID'] == camp_id]['volunteerPop'].tolist()[0])
        Volunteer.total_number += 1
        modify_csv_pandas("data/camp.csv", "campID", camp_id, "volunteerPop",
                          Volunteer.total_number)
        print("Join/change camp completed.")

    def edit_personal_info(self):
        pass

    def edit_camp_info(self):
        # Should this sit in the camp class & be called by volunteer?
        pass

    def create_refugee_profile(self):
        # Should this just sit in the refugee class and be called by volunteer?
        pass
