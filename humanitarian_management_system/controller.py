import time
from pathlib import Path
import pandas as pd
import re
import math

from humanitarian_management_system import helper
from humanitarian_management_system.models import User, Admin, Volunteer, Event, Camp, ResourceTest, Refugee
from humanitarian_management_system.views import GeneralView, ManagementView, AdminView, VolunteerView


class Controller:
    def __init__(self):
        # for saving user information
        self.user = None
        self.logout_request = False

    def initialise(self):
        # show welcome messages when the program starts
        GeneralView.display_startup_logo()
        GeneralView.display_welcome_message()
        self.startup()

    def startup(self):
        while True:
            self.logout_request = False
            # display startup menu
            GeneralView.display_startup_menu()
            # validate user selection based on startup menu
            user_selection = helper.validate_user_selection(GeneralView.get_startup_options())
            # direct user to different page based on user selection
            if user_selection == "1":
                # login
                self.login()
            if user_selection == "2":
                # register
                is_register_successful = self.register()
                # if registration is successful, direct user to login page. Otherwise, return to startup menu
                if is_register_successful:
                    self.login()
            if user_selection == "x":
                # exit the program
                break

    @staticmethod
    def register():
        GeneralView.display_registration_message()
        usernames = User.get_all_usernames()
        # registration_info will contain all the required info for creating new volunteer
        # if registration_info is none, the registration is fail and user will be redirected back to startup page
        registration_info = helper.validate_registration(usernames)
        if registration_info is not None:
            # write new volunteer record into csv
            Volunteer.create_new_record(registration_info)
            print("\n***   Your volunteer account is created successfully!   ***"
                  "\n\nYou will be redirected to Login Page shortly.")
            time.sleep(3)
            return True
        else:
            return False

    def login(self):
        user_info = pd.Series()
        # get all existing usernames in a list
        all_usernames = User.get_all_usernames()
        GeneralView.display_login_message()

        while user_info.empty:
            username = input("\nUsername: ")
            if username == 'RETURN':
                break
            if username not in all_usernames:
                print("Account doesn't exist!")
                continue
            password = input("\nPassword: ")
            if username == 'RETURN':
                break
            # user_info contains all the user information if username and password match
            # otherwise, user_info is an empty series
            user_info = User.validate_user(username, password)
            # check if account is active
            if user_info.empty:
                print("\nUsername or password is incorrect. Please try again.")
            elif user_info['isActive'] == "FALSE":
                user_info = pd.Series()
                print("\nYour account has been deactivated, contact the administrator.")

        # if user record is matched, print login successfully
        if not user_info.empty:
            print("\n***   Login Successful!   ***")
            if user_info['userType'] == "admin":
                # self.user is now an object of admin
                self.user = Admin(user_info['userID'], *user_info[3:10])
                print("You are now logged in as Admin.")
                self.admin_main()
            else:
                # self.user is not an object of volunteer
                self.user = Volunteer(user_info['userID'], *user_info[3:])
                print("You are now logged in as Volunteer.")
                self.volunteer_main()

    def admin_main(self):
        AdminView.display_login_message(self.user.username)
        while True:
            AdminView.display_menu()
            user_selection = helper.validate_user_selection(AdminView.get_main_options())

            if user_selection == "1":
                self.admin_manage_event()
            elif user_selection == "2":
                self.admin_manage_camp()
            elif user_selection == "3":
                self.admin_manage_volunteer()
            elif user_selection == "4":
                self.admin_manage_resource()
            elif user_selection == "5":
                self.admin_display_summary()
            elif user_selection == "6":
                self.user_edit_account()
            elif user_selection == "7":
                self.user.show_account_info()
            # log out if user has selected "L" or self.logout_request is True
            if user_selection == "L" or self.logout_request is True:
                self.user = None
                break

    def admin_manage_event(self):
        while True:
            AdminView.display_event_menu()
            user_selection = helper.validate_user_selection(AdminView.get_event_options())
            if user_selection == "1":
                self.admin_create_event()
            if user_selection == "2":
                self.admin_edit_event()
            if user_selection == "3":
                self.admin_close_event()
            if user_selection == "4":
                self.admin_delete_event()
            if user_selection == "5":
                # display all events
                pass
            if user_selection == "R":
                break
            if user_selection == "L":
                self.user = None
                self.logout_request = True
                break

    @staticmethod
    def admin_create_event():
        ManagementView.event_creation_message()
        event_info = helper.validate_event_input()
        if event_info is not None:
            Event.create_new_record(event_info)
            print("Event created.")
        else:
            return

    @staticmethod
    def admin_edit_event():
        ManagementView.event_edit_message()
        Event.edit_event_info()

    @staticmethod
    def admin_delete_event():
        ManagementView.event_delete_message()
        Event.delete_event()

    @staticmethod
    def admin_close_event():
        ManagementView.event_close_message()
        Event.disable_ongoing_event()

    def admin_manage_camp(self):
        while True:
            ManagementView.camp_main_message()
            AdminView.display_camp_menu()
            user_selection = helper.validate_user_selection(AdminView.get_camp_options())
            if user_selection == "1":
                self.create_camp()
            if user_selection == "2":
                pass  # edit camp
            if user_selection == "3":
                self.delete_camp()
            if user_selection == "4":
                self.add_refugee()
            if user_selection == "5":
                self.move_refugee()
            if user_selection == "6":
                # display all camps
                pass
            if user_selection == "R":
                break
            if user_selection == "L":
                self.user = None
                self.logout_request = True
                break

    def create_camp(self):
        ManagementView.camp_creation_message()
        active_event_df = Event.get_all_active_events()
        Event.display_events(active_event_df)
        active_index = helper.extract_active_event()[0]

        # check if active event is 0
        if len(active_index) == 0:
            print("No relevant events to select from.")
            return
        else:
            # read the event csv file and extract all available events
            csv_path = Path(__file__).parents[0].joinpath("data/eventTesting.csv")
            df1 = helper.matched_rows_csv(csv_path, "ongoing", True, "eid")
            print("\n*The following shows the info of all available events*\n")
            print(df1[0])

            # validate input for user select index
            while True:
                try:
                    eventID = int(input("\nEnter Event ID: "))
                    if eventID not in df1[1]:
                        print(f"Invalid input! Please enter an integer from {df1[1]} for Event ID.")
                        continue
                    else:
                        break
                except ValueError:
                    print(f"Invalid input! Please enter an integer from {df1[1]} for Event ID.")

    def admin_modify_camp(self):
        """This function is to modify camp info"""
        pass

    def delete_camp(self):
        """This part of the code is to delete the camp from the camp.csv"""
        ManagementView.camp_deletion_message()
        active_index = helper.extract_active_event()[0]

        # if there is no active events, return
        if len(active_index) == 0:
            print("No relevant events to select from")
            return
        else:
            # print the events info for users to choose
            csv_path = Path(__file__).parents[0].joinpath("data/eventTesting.csv")
            df1 = helper.matched_rows_csv(csv_path, "ongoing", True, "eid")
            print("\n*The following shows the info of all available events*\n")
            print(df1[0])
            while True:
                try:
                    eventID = int(input("\nEnter Event ID: "))
                    if eventID not in df1[1]:
                        print(f"Invalid input! Please enter an integer from {df1[1]} for Event ID.")
                        continue
                    else:
                        break
                except ValueError:
                    print(f"Invalid input! Please enter an integer from {df1[1]} for Event ID.")

            # print camps info for users to choose
            csv_path2 = Path(__file__).parents[0].joinpath("data/camp.csv")
            df2 = helper.matched_rows_csv(csv_path2, "eventID", eventID, "campID")
            print("\n**The following shows the info of related camps*\n")
            print(df2[0])
            while True:
                try:
                    delete_camp = int(input("\nWhich camp do you want to delete? Please enter campID: "))
                    if delete_camp not in df2[1]:
                        print(f"Invalid input! Please enter an integer from {df2[1]} for Camp ID.")
                        continue
                    else:
                        while True:
                            aa = input(f"\nAre you sure to delete camp {delete_camp}? (yes/no): ")
                            if aa == "yes":
                                # implement the deletion in csv file
                                df3 = pd.read_csv(csv_path2)
                                df3 = df3[df3["campID"] != delete_camp]
                                df3.to_csv(csv_path2, index=False)

                                # keep track of existing camp num of a particular event
                                no_camp = df1[0].loc[eventID, "no_camp"]
                                no_camp -= 1
                                df4 = pd.read_csv(csv_path)
                                index = df4[df4["eid"] == eventID].index.tolist()
                                helper.modify_csv_value(csv_path, index[0], "no_camp", no_camp)
                                print("Deletion Successful")
                                break
                            elif aa == "no":
                                break
                            else:
                                print("Invalid input! Please enter 'yes' or 'no'")
                                continue
                        break
                except ValueError:
                    print(f"Invalid input! Please enter an integer from {df2[1]} for Camp ID.")

    def resource_main(self):
        ManagementView.resource_main_message()
        while True:
            user_selection = input("\nAllocation mode: ")

            if user_selection == '1':
                self.man_resource()
            elif user_selection == '2':
                self.auto_resource()
            else:
                print("Invalid mode option entered!")
                continue

            if user_selection == 'RETURN':
                return
            else:
                break

    def man_resource(self):
        ManagementView.man_resource_message()
        index = helper.display_camp_list()
        res_man_info = helper.validate_man_resource(index)

        if res_man_info is not None:
            r = ResourceTest(res_man_info[0], '', '')
            r.manual_resource(res_man_info[2], res_man_info[1])
            print("Resource allocated as request.")
            self.admin_manage_camp()
        else:
            return

    def auto_resource(self):
        ManagementView.auto_resource_message()
        index = helper.display_camp_list()

        while True:
            select_index = int(input("\nEnter index: "))

            if select_index not in index:
                print("invalid index option entered!")
                continue
            try:
                if select_index == 'RETURN':
                    return
            except:
                return
            break

        df = helper.extract_active_event()[1]
        select_pop = df.loc[df['campID'] == select_index]['refugeePop'].tolist()[0]

        r = ResourceTest(select_index, select_pop, 0)
        r.calculate_resource()
        print("Auto resource allocation completed")
        self.admin_manage_camp()

    def admin_manage_volunteer(self):
        pass

    def admin_manage_resource(self):
        pass

    def user_edit_account(self):
        while True:
            VolunteerView.display_account_menu()
            user_selection = helper.validate_user_selection(VolunteerView.get_account_options())
            if user_selection == "1":
                # change username
                self.user_change_username()
            if user_selection == "2":
                # change password
                self.user_change_password()
            if user_selection == "3":
                # change name
                self.user_change_name()
            if user_selection == "4":
                # change email
                pass
            if user_selection == "5":
                # change phone
                pass
            if user_selection == "6":
                # change occupation
                pass
            if user_selection == "R":
                break
            if user_selection == "L":
                self.user = None
                self.logout_request = True
                break

    def user_change_username(self):
        existing_usernames = User.get_all_usernames()
        print(f"\nCurrent Username: {self.user.username}")
        while True:
            new_username = input("\nPlease enter your new username: ")
            if new_username == "RETURN":
                return
            elif new_username not in existing_usernames and new_username.isalnum():
                self.user.username = new_username
                # update csv file
                self.user.update_username()
                print("\nUsername changed successfully.")
                break
            elif new_username in existing_usernames:
                print("\nSorry, username already exists.")
                continue
            else:
                print("\nInvalid username entered. Only alphabet letter (Aa-Zz) and numbers (0-9) are allowed.")
                continue

    def user_change_password(self):
        # specify allowed characters for passwords
        allowed_chars = r"[!@#$%^&*\w]"
        while True:
            new_password = input("Please enter new password: ")
            if new_password == "RETURN":
                return
            elif new_password == self.user.password:
                print("\n The new password is the same as current password!"
                      "Please enter a new one.")
                continue
            elif re.match(allowed_chars, new_password):
                confirm_password = input("Please enter the new password again: ")
                if confirm_password == "RETURN":
                    return
                elif confirm_password == new_password:
                    self.user.password = new_password
                    # update csv file
                    self.user.update_password()
                    print("\nPassword changed successfully.")
                    break
                else:
                    print("The two passwords are not the same!")
            else:
                print("Invalid password entered.\n"
                      "Only alphabet, numbers and !@#$%^&* are allowed.")
                continue

    def user_change_name(self):
        print(f"\nCurrent Name: {self.user.first_name} {self.user.last_name}")
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

            if new_first_name == self.user.first_name and new_last_name == self.user.last_name:
                print("\nYour new name is the same as your current name!"
                      "Please enter a new name, or enter 'RETURN' to discard the changes and go back")
            else:
                # remove extra whitespaces between words in first name
                self.user.first_name = ' '.join(new_first_name.split())
                # remove extra whitespaces between words in last name
                self.user.last_name = ' '.join(new_last_name.split())
                # update the csv file
                self.user.update_name()
                print("\nName changed successfully."
                      f"\nYour new name is '{self.user.first_name} {self.user.last_name}'.")
                break

    def admin_display_summary(self):
        pass

    def volunteer_main(self):
        VolunteerView.display_login_message(self.user.username)
        while True:
            VolunteerView.display_main_menu()
            user_selection = helper.validate_user_selection(VolunteerView.get_main_options())
            if user_selection == "1":
                # join/change camp
                self.volunteer_join_change_camp()
            if user_selection == "2":
                # manage camp
                self.volunteer_manage_camp()
            if user_selection == "3":
                # edit personal account
                self.user_edit_account()
            if user_selection == "4":
                # show personal information
                self.volunteer_show_account_info()
            # log out if user has selected "L" or self.logout_request is True
            if user_selection == "L" or self.logout_request is True:
                self.user = None
                break

    def volunteer_manage_camp(self):
        while True:
            VolunteerView.display_camp_menu()
            user_selection = helper.validate_user_selection(VolunteerView.get_camp_options())
            if user_selection == "1":
                # add refugee
                self.add_refugee()
            if user_selection == "2":
                # edit refugee
                pass
            if user_selection == "3":
                self.move_refugee()

            if user_selection == "4":
                # edit camp info
                pass
            if user_selection == "5":
                # display all refugees
                pass
            if user_selection == "6":
                # display camp info
                pass
            if user_selection == "7":
                # display all resource
                pass
            if user_selection == "R":
                break
            if user_selection == "L":
                self.user = None
                self.logout_request = True
                break

    def volunteer_show_account_info(self):
        self.user.show_account_info()

    # def join_camp(self):
    #     csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
    #     df = pd.read_csv(csv_path)
    #
    #     ManagementView.join_camp_message()
    #     index = helper.display_camp_list()
    #
    #     while True:
    #         select_index = int(input("\nindex: "))
    #
    #         if select_index not in index:
    #             print("invalid index option entered!")
    #             continue
    #         try:
    #             if select_index == 'RETURN':
    #                 return
    #         except:
    #             return
    #         break
    #
    #     event_id = df.loc[df['campID'] == select_index]['eventID'].tolist()[0]
    #     join_info = helper.validate_join()
    #     if join_info is not None:
    #         v = Volunteer(username, '', '', '', '', '', '', join_info)
    #         v.join_camp(event_id, select_index)
    #     return
    #
    # def add_refugee(self):
    #     df = helper.extract_data_df("data/user.csv")
    #     user_type = df.loc[df['username'] == username]['userType'].tolist()[0]
    #     df_c = helper.extract_data_df("data/camp.csv")
    #     active_camp = df_c.loc[df_c['status'] == 'open']['campID'].tolist()
    #     if user_type == 'admin':
    #         csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
    #         df1 = helper.matched_rows_csv(csv_path, "status", 'open', "campID")
    #         print("\n*The following shows the info of all available events*\n")
    #         print(df1[0])
    #
    #         cid = int(input("Enter a camp ID: "))
    #         while True:
    #             if cid not in active_camp:
    #                 print("Invalid camp ID entered!")
    #                 continue
    #             break
    #     else:
    #         cid = df.loc[df['username'] == username]['campID'].tolist()[0]
    #         # check if volunteer user already join a camp
    #         if math.isnan(cid):
    #             print("You must first join a camp!")
    #             return
    #         print(f'''\nYou're currently assigned to camp {int(cid)}.''', end='')
    #
    #     ManagementView.create_refugee_message()
    #     df_c = helper.extract_data_df("data/camp.csv")
    #     # health risk level of volunteer's camp
    #     lvl = df_c.loc[df_c['campID'] == cid]['healthRisk'].tolist()[0]
    #
    #     refugee_info = helper.validate_refugee(lvl)
    #     if refugee_info is not None:
    #         r = Refugee(refugee_info[0], refugee_info[1], refugee_info[2], refugee_info[3], refugee_info[4],
    #                     refugee_info[5], refugee_info[6], refugee_info[7])
    #         r.add_refugee_from_user_input(cid)
    #     else:
    #         return
    #     print("Refugee created.")
    #     self.admin_manage_camp()
    #
    # def move_refugee(self):
    #     rid = 0
    #     helper.move_refugee_helper_method(rid)
    #
    #
    #
    # def volunteer_join_change_camp(self):
    #     csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
    #     df = pd.read_csv(csv_path)
    #
    #     ManagementView.join_camp_message()
    #     index = helper.display_camp_list()
    #
    #     while True:
    #         select_index = int(input("\nindex: "))
    #
    #         if select_index not in index:
    #             print("invalid index option entered!")
    #             continue
    #         try:
    #             if select_index == 'RETURN':
    #                 return
    #         except:
    #             return
    #         break
    #
    #     event_id = df.loc[df['campID'] == select_index]['eventID'].tolist()[0]
    #     join_info = helper.validate_join()
    #     if join_info is not None:
    #         v = Volunteer(username, '', '', '', '', '', '', join_info,
    #                       event_id, select_index)
    #         v.join_camp(event_id, select_index)
    #     self.volunteer_main()
