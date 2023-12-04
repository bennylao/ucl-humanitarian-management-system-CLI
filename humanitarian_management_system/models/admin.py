from pathlib import Path
import pandas as pd
from .user import User
from humanitarian_management_system import helper


class Admin(User):
    def __init__(self, user_id, username, password, first_name, last_name, email, phone, occupation):
        super().__init__(user_id, username, password, first_name, last_name, email, phone, occupation)

    def show_account_info(self):
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path)
        sub_df = df.loc[df['userID'] == int(self.user_id), ['username', 'firstName', 'lastName', 'email',
                                                            'phone', 'occupation']]
        table_str = sub_df.to_markdown(index=False)
        print("\n" + table_str)
        try:
            input("\nPress Enter to return...")
        except SyntaxError:
            pass

    def remove_user(self):
        vol_id_arr = []
        vol_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/user.csv"))

        print("A list of all volunteers and their corresponding information.")
        self.vol_table_display()

        for i in vol_df['userID'].tolist():
            vol_id_arr.append(str(i))

        while True:
            user_select = input("Please select a user ID whose account you would like to delete: ")

            if user_select not in vol_id_arr:
                print("Invalid user ID entered!")
                continue
            if user_select == 'RETURN':
                return

            vol_df = vol_df[vol_df['userID'] != int(user_select)]
            vol_df.reset_index(drop=True, inplace=True)
            vol_df.to_csv(Path(__file__).parents[1].joinpath("data/user.csv"), index=False)
            print(f"User with ID int{user_select} has been deleted.")

            return
        return

    def activate_user(self):
        vol_id_arr = []
        vol_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/user.csv"))

        print("A list of all volunteers and their corresponding information.")
        self.vol_table_display()

        for i in vol_df['userID'].tolist():
            vol_id_arr.append(str(i))

        while True:
            user_select = input("Please select a user ID whose active status you would like to change: ")

            if user_select not in vol_id_arr:
                print("Invalid user ID entered!")
                continue
            else:
                status = vol_df.loc[vol_df['userID'] == int(user_select)]['isActive'].tolist()[0]

            if user_select == 'RETURN':
                return

            if status:
                while True:
                    user_input = input(f"Are you sure you want to deactivate user with ID {int(user_select)} "
                                       f"(yes or no)? ")
                    if user_input.lower() != 'yes' and user_input.lower() != 'no':
                        print("Must enter yes or no!")
                        continue
                    if user_input == 'yes':
                        helper.modify_csv_pandas("data/user.csv", 'userID', int(user_select),
                                                 'isActive', False)
                        print(f"User ID {int(user_select)} has been deactivated.")
                    return

            else:
                user_input = input(f"Are you sure you want to re-activate user with ID {int(user_select)} "
                                   f"(yes or no)? ")

                if user_input.lower() != 'yes' and user_input.lower() != 'no':
                    print("Must enter yes or no!")
                    continue
                if user_input == 'yes':
                    helper.modify_csv_pandas("data/user.csv", 'userID', int(user_select),
                                             'isActive', True)
                    print(f"User ID {int(user_select)} has been re-activated.")
                return
            return

    def display_vol(self):

        joined_df = self.vol_table_display()

        camp_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/camp.csv"))
        event_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/eventTesting.csv"))
        joined_camp = pd.merge(camp_df, event_df, on='eventID', how='inner')

        joined_camp.columns = ['Camp ID', 'Event ID', 'countryID', 'Refugee capacity', 'Health risk',
                               'Volunteer population',
                               'Refugee population', 'Average critical level', 'Camp status', 'ongoing', 'Event title',
                               'Location', 'Event description', 'no_camp', 'Start date', 'End date']

        joined_df_total = pd.merge(joined_df, joined_camp, on='Camp ID', how='inner')
        joined_df_total = joined_df_total.loc[:, ~joined_df_total.columns.isin(['Event ID_x', 'Event ID_y' 'countryID',
                                                                                'ongoing', 'no_camp',
                                                                                'Average critical level',
                                                                                'Is active?', 'Username', 'Password',
                                                                                'First name',
                                                                                'Last name', 'Email', 'Phone no.',
                                                                                'Occupation'])]

        while True:
            user_input = input("Would you like to access the camp & event profile for a particular volunteer "
                               "(yes or no)? ")

            if user_input.lower() == 'yes':
                self.display_camp(joined_df_total)

            if user_input.lower() != 'yes' and user_input.lower() != 'no':
                print("Must enter yes or no!")
                continue
            if user_input.lower() == 'no':
                return
            break

    def display_camp(self, joined_df_total):
        df = pd.read_csv(Path(__file__).parents[1].joinpath("data/user.csv"))
        vol_id_arr = []

        for i in df.loc[df['userType'] == 'volunteer']['userID'].tolist():
            vol_id_arr.append(str(i))

        while True:
            id_input = input("Please enter the volunteer ID whose camp & event profile you would like to see: ")
            if id_input not in vol_id_arr:
                print("Invalid volunteer ID entered!")
                continue

            joined_df_total = joined_df_total.loc[joined_df_total['User ID'] == int(id_input)]
            table_str = joined_df_total.to_markdown(index=False)
            print("\n" + table_str)

            while True:
                user_input = input("Would you like to exit (yes or no)? ")
                if user_input.lower() != 'yes' and user_input.lower() != 'no':
                    print("Must enter yes or no!")
                    continue
                if user_input.lower() == 'no':
                    self.display_vol()
                return
            return
        return

    @staticmethod
    def vol_table_display():
        vol_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/user.csv"))
        vol_df = vol_df.loc[vol_df['userType'] == 'volunteer']
        role_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/roleType.csv"))

        joined_df = pd.merge(vol_df, role_df, on='roleID', how='inner')
        joined_df = joined_df.loc[:, ~joined_df.columns.isin(['userType', 'roleID'])]
        joined_df.columns = ['User ID', 'Is active?', 'Username', 'Password', 'First name', 'Last name', 'Email',
                             'Phone no.', 'Occupation', 'Event ID', 'Camp ID', 'Camp role']

        table_str = joined_df.to_markdown(index=False)
        print("\n" + table_str)
        return joined_df
