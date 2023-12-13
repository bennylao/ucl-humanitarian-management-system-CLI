from pathlib import Path
import pandas as pd
import passlib.hash
import logging
from .user import User
from humanitarian_management_system import helper
from ..views import ManagementView
import re


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
        try:
            vol_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/user.csv"))
            camp_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/camp.csv"))
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

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

            # update volunteer pop from the volunteer's assigned camp after this volunteer account is removed.
            user_camp = vol_df.loc[vol_df['userID'] == int(user_select)]['campID'].tolist()[0]

            if user_camp != 0:
                vol_pop = camp_df.loc[camp_df['campID'] == int(user_camp)]['volunteerPop'].tolist()[0]
                vol_pop -= 1

                helper.modify_csv_pandas("data/camp.csv", 'campID', int(user_camp),
                                         'volunteerPop', vol_pop)

            vol_df = vol_df[vol_df['userID'] != int(user_select)]
            vol_df.reset_index(drop=True, inplace=True)
            vol_df.to_csv(Path(__file__).parents[1].joinpath("data/user.csv"), index=False)
            print(f"User with ID int{user_select} has been deleted.")

            return
        return

    @staticmethod
    def verify_user():
        while True:
            user_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/user.csv"), converters={'userID': str})
            unverified_user_df = user_df.loc[user_df['isVerified'] == False]
            unverified_user_df = unverified_user_df[['userID', 'isVerified', 'isActive', 'username', 'firstName', 'lastName', 'email', 'phone', 'occupation', 'roleID']]
            unverified_user_options = unverified_user_df['userID'].tolist()
            if len(unverified_user_options) == 0:
                print("\nThere is no newly registered volunteer waiting to be verified.")
                break
            else:
                print("\nHere is the list of all newly registered volunteers waiting to be verified.")
                print(unverified_user_df.to_markdown(index=False))
                print("\nPlease select the user ID of the volunteer you would like to verify and activate.\n"
                      "or enter 'RETURN' to return to the previous menu.")
                while True:
                    user_select = input("User ID: ")
                    if user_select == 'RETURN':
                        return
                    if user_select in unverified_user_options:
                        user_df.loc[user_df['userID'] == user_select, 'isVerified'] = True
                        user_df.loc[user_df['userID'] == user_select, 'isActive'] = True
                        user_df.to_csv(Path(__file__).parents[1].joinpath("data/user.csv"), index=False)
                        print(f"User with ID {user_select} has been verified.")
                        while True:
                            to_continue = input("\nDo you want to verify another user? (y/n): ")
                            if to_continue.lower() == 'y':
                                break
                            elif to_continue.lower() == 'n':
                                return
                            else:
                                print("Invalid input!")
                                continue
                        if to_continue.lower() == 'y':
                            break
                    else:
                        print("Invalid user ID entered!")
                        continue

    def activate_user(self):
        vol_id_arr = []
        vol_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/user.csv"))

        print("A list of all volunteers and their corresponding information.")
        self.vol_table_display()

        for i in vol_df['userID'].tolist():
            vol_id_arr.append(str(i))

        while True:
            user_select = input("Please select a user ID whose active status you would like to change: ")

            if user_select == 'RETURN':
                return
            elif user_select not in vol_id_arr:
                print("Invalid user ID entered!")
                continue
            else:
                status = vol_df.loc[vol_df['userID'] == int(user_select)]['isActive'].tolist()[0]

            if status:
                while True:
                    user_input = input(f"Are you sure you want to deactivate user with ID {int(user_select)} "
                                       f"(yes or no)? ")
                    if user_input == 'RETURN':
                        return
                    elif user_input.lower() != 'yes' and user_input.lower() != 'no':
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
                if user_input == 'RETURN':
                    return
                elif user_input.lower() != 'yes' and user_input.lower() != 'no':
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
        event_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/event.csv"), converters={'ongoing': str})
        joined_camp = pd.merge(camp_df, event_df, on='eventID', how='inner')

        joined_camp.columns = ['Camp ID', 'Event ID', 'countryID', 'latitude', 'longitude', 'Refugee capacity',
                               'Health risk', 'Volunteer population',
                               'Refugee population', 'Average critical level', 'Camp status', 'ongoing', 'Event title',
                               'Location', 'Event description', 'no_camp', 'Start date', 'End date']

        joined_df_total = pd.merge(joined_df, joined_camp, on='Camp ID', how='inner')
        joined_df_total = joined_df_total.loc[:, ~joined_df_total.columns.isin(['Event ID_x', 'Event ID_y' 'countryID',
                                                                                'ongoing', 'no_camp', 'latitude',
                                                                                'Average critical level',
                                                                                 'Username', 'Password',
                                                                                'First name', 'longitude',
                                                                                'Last name', 'Email', 'Phone no.',
                                                                                'Occupation'])]

        while True:
            user_input = input("Would you like to access the camp & event profile for a particular volunteer "
                               "(yes or no)? ")

            if user_input.lower() == 'RETURN':
                return

            if user_input.lower() == 'yes':
                self.display_camp(joined_df_total)

            if user_input.lower() != 'yes' and user_input.lower() != 'no':
                print("Must enter yes or no!")
                continue
            if user_input == 'no':
                return
            break

    def display_camp(self, joined_df_total):
        df = pd.read_csv(Path(__file__).parents[1].joinpath("data/user.csv"))
        vol_id_arr = []

        for i in df.loc[df['userType'] == 'volunteer']['userID'].tolist():
            vol_id_arr.append(str(i))

        while True:
            id_input = input("Please enter the volunteer ID whose camp & event profile you would like to see: ")

            if id_input == 'RETURN':
                return
            if id_input not in vol_id_arr:
                print("Invalid volunteer ID entered!")
                continue

            joined_df_total = joined_df_total.loc[joined_df_total['User ID'] == int(id_input)]
            joined_df_total = joined_df_total.loc[:, ~joined_df_total.columns.isin(['Is verified?', 'Is active?',
                                                                                    'countryID'])]
            table_str = joined_df_total.sort_values('Camp ID').to_markdown(index=False)
            print("\n" + table_str)

            while True:
                user_input = input("Would you like to exit (yes or no)? ")
                if user_input == 'RETURN':
                    return
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
        joined_df = joined_df.loc[:, ~joined_df.columns.isin(['userType', 'roleID', 'password'])]
        joined_df.columns = ['User ID', 'Is verified?', 'Is active?', 'Username', 'First name', 'Last name',
                             'Email',
                             'Phone no.', 'Occupation', 'Camp ID', 'Camp role']

        table_str = joined_df.sort_values('User ID').to_markdown(index=False)
        print("\n" + table_str)
        return joined_df

    def edit_volunteer_profile(self, change_user):
        while True:
            ManagementView.volunteer_display_account_menu()
            user_selection = helper.validate_user_selection(ManagementView.volunteer_get_account_options())
            if user_selection == "1":
                # change username
                self.change_volunteer_username(change_user)
            if user_selection == "2":
                # change password
                self.change_volunteer_password(change_user)
            if user_selection == "3":
                # change name
                self.change_volunteer_name(change_user)
            if user_selection == "4":
                # change email
                self.change_volunteer_email(change_user)
            if user_selection == "5":
                # change phone
                self.change_volunteer_phone(change_user)
            if user_selection == "6":
                # change occupation
                self.change_volunteer_occupation(change_user)
            if user_selection == "7":
                # change occupation
                self.change_volunteer_role(change_user)
            if user_selection == "R":
                return False
            if user_selection == "L":
                return True

    @staticmethod
    def change_volunteer_username(change_user):
        existing_usernames = User.get_all_usernames()
        print(f"\nCurrent Username: '{change_user.username}'")
        while True:
            new_username = input("\nPlease enter your new username: ")
            if new_username == "RETURN":
                return
            elif new_username not in existing_usernames and new_username.isalnum():
                change_user.username = new_username
                # update csv file
                change_user.update_username()
                print("\nUsername changed successfully."
                      f"\nYour new username is '{change_user.username}'.")
                break
            elif new_username in existing_usernames:
                print("\nSorry, username already exists.")
                continue
            else:
                print("\nInvalid username entered. Only alphabet letter (Aa-Zz) and numbers (0-9) are allowed.")
                continue

    @staticmethod
    def change_volunteer_password(change_user):
        # specify allowed characters for passwords
        allowed_chars = r"[!@#$%^&*\w]"
        while True:
            new_password = input("Please enter new password: ")
            if new_password == "RETURN":
                return
            elif new_password == change_user.password:
                print("\n The new password is the same as current password!"
                      "Please enter a new one.")
                continue
            elif re.match(allowed_chars, new_password):
                confirm_password = input("Please enter the new password again: ")
                if confirm_password == "RETURN":
                    return
                elif confirm_password == new_password:
                    change_user.password = passlib.hash.sha256_crypt.hash(new_password)
                    # update csv file
                    change_user.update_password()
                    print("\nPassword changed successfully.")
                    break
                else:
                    print("The two passwords are not the same!")
            else:
                print("Invalid password entered.\n"
                      "Only alphabet, numbers and !@#$%^&* are allowed.")
                continue

    @staticmethod
    def change_volunteer_name(change_user):
        print(f"\nCurrent Name: {change_user.first_name} {change_user.last_name}")
        while True:
            while True:
                new_first_name = input("\nPlease enter your new first name: ")
                if new_first_name == "RETURN":
                    return
                elif new_first_name.replace(" ", "").isalpha():
                    break
                else:
                    print("\nInvalid first name entered. Only alphabet letter (a-z) are allowed.")
            while True:
                new_last_name = input("\nPlease enter your new last name: ")
                if new_last_name == "RETURN":
                    return
                elif new_last_name.replace(" ", "").isalpha():
                    break
                else:
                    print("\nInvalid last name entered. Only alphabet letter (a-z) are allowed.")

            if new_first_name == change_user.first_name and new_last_name == change_user.last_name:
                print("\nYour new name is the same as your current name!"
                      "Please enter a new name, or enter 'RETURN' to discard the changes and go back")
            else:
                # remove extra whitespaces between words in first name
                change_user.first_name = ' '.join(new_first_name.split())
                # remove extra whitespaces between words in last name
                change_user.last_name = ' '.join(new_last_name.split())
                # update the csv file
                change_user.update_name()
                print("\nName changed successfully."
                      f"\nYour new name is '{change_user.first_name} {change_user.last_name}'.")
                break

    @staticmethod
    def change_volunteer_email(change_user):
        # specify allowed characters for email
        email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        all_emails = User.get_all_emails()
        print(f"\nCurrent Email: {change_user.email}")

        while True:
            new_email = input("Please enter new email: ")
            if new_email == "RETURN":
                return
            elif new_email == change_user.email:
                print("\n The new email is the same as current email!"
                      "Please enter a new one.")
                continue
            elif re.fullmatch(email_format, new_email) and new_email not in all_emails:
                change_user.email = new_email
                # update csv file
                change_user.update_email()
                print("\nEmail changed successfully."
                      f"\nYour new email is '{change_user.email}'.")
                break
            elif new_email in all_emails:
                print("\nSorry, email is already linked to other account.")
            else:
                print("Invalid password entered.\n"
                      "Only alphabet, numbers and !@#$%^&* are allowed.")
                continue

    @staticmethod
    def change_volunteer_phone(change_user):
        print(f"\nCurrent Phone Number: {change_user.phone}")
        while True:
            new_phone = input("\nPlease enter new phone number: ")
            if new_phone == 'RETURN':
                return
            else:
                try:
                    new_phone = int(new_phone)
                    break
                except ValueError:
                    print("Invalid phone number entered. Only numbers are allowed.")
        change_user.phone = new_phone
        # update the csv file
        change_user.update_phone()
        print("\nPhone changed successfully."
              f"\nYour new phone is '{change_user.phone}")

    @staticmethod
    def change_volunteer_occupation(change_user):
        print(f"\nCurrent Occupation: {change_user.occupation}")
        while True:
            new_occupation = input("\nPlease enter your new occupation: ")
            if new_occupation == "RETURN":
                return
            elif new_occupation.isalpha():
                change_user.occupation = new_occupation
                # update the csv file
                change_user.update_occupation()
                print("\nName changed successfully."
                      f"\nYour new occupation is '{change_user.occupation}'.")
                break
            else:
                print("\nInvalid first name entered. Only alphabet letter (a-z) are allowed.")

    @staticmethod
    def change_volunteer_role(change_user):
        csv_path = Path(__file__).parents[1].joinpath("data/roleType.csv")
        df = pd.read_csv(csv_path)
        role_id_arr = [i for i in df['roleID'].tolist()]
        role_name = df.loc[df['roleID'] == change_user.role_id]['name'].tolist()[0]
        print(f"\n Your current camp role is: {role_name}")

        old_id = change_user.role_id

        table_str = df.to_markdown(index=False)
        print("\n" + table_str)

        while True:
            user_select = input("Please select a camp role you would like to change to by ID: ")

            if user_select == 'RETURN':
                return
            elif not user_select.isnumeric():
                print("Integer values only!")
                continue
            user_select = int(user_select)

            if user_select not in role_id_arr:
                print("Invalid role ID entered!")
                continue

            change_user.role_id = user_select
            # update the csv file
            helper.modify_csv_pandas("data/user.csv", 'roleID', old_id, 'roleID',
                                     change_user.role_id)
            role_name = df.loc[df['roleID'] == change_user.role_id]['name'].tolist()[0]
            print("\nCamp role Id changed successfully."
                  f"\nYour new camp role is '{role_name}'.")
            break







