import sys
import time
from pathlib import Path
import pandas as pd
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
                # if registration is successful, direct user to login page
                # otherwise, return to startup menu
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
                self.user = Admin(*user_info[3:10])
                print("You are now logged in as Admin.")
                self.admin_main()
            else:
                # self.user is not an object of volunteer
                self.user = Volunteer(*user_info[3:])
                print("You are now logged in as Volunteer.")
                self.volunteer_main()

    def admin_main(self):
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
                self.admin_edit_account()
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
                # remove event
                pass
            if user_selection == "4":
                # display all events
                pass
            if user_selection == "R":
                break
            if user_selection == "L":
                self.user = None
                self.logout_request = True
                break

    def admin_create_event(self):
        ManagementView.event_creation_message()
        event_info = helper.validate_event_input()
        if event_info is not None:
            Event.create_new_record(event_info)
            print("Event created.")
            self.admin_manage_event()
        else:
            return

    @staticmethod
    def admin_edit_event():
        ManagementView.event_edit_message()
        Event.edit_event_info()

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
                self.resource_main()
            if user_selection == "5":
                self.add_refugee()
            if user_selection == "6":
                self.move_refugee()
            if user_selection == "7":
                pass  # display all camps
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
        allowed_event_id = active_event_df['eid'].tolist()
        while True:
            selected_event_id = input("\nPlease Enter the Event ID of which you want to create new camp in: ")
            if selected_event_id == "RETURN":
                break
            elif selected_event_id in allowed_event_id:
                break
            else:
                print(f"Invalid input! Please enter an integer from {allowed_event_id} for Event ID.")
        while True:
            refugee_capacity = input("\nPlease Enter the camp capacity: ")
            if refugee_capacity == "RETURN":
                break
            elif int(refugee_capacity) > 0:
                break
            else:
                print("Please enter a positive integer")

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

    def modify_camp(self):
        """This function is to modify camp info"""

    def admin_manage_volunteer(self):
        pass

    def admin_manage_resource(self):
        pass

    def admin_display_summary(self):
        pass

    def admin_edit_account(self):
        pass

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

    def volunteer_main(self):
        while True:
            VolunteerView.login_message()
            VolunteerView.display_main_menu()
            user_selection = helper.validate_user_selection(VolunteerView.get_main_options())
            if user_selection == "1":
                self.volunteer_join_change_camp()
            if user_selection == "2":
                self.volunteer_manage_camp()
            if user_selection == "3":
                pass
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

    def volunteer_edit_account(self):
        while True:
            VolunteerView.display_account_menu()
            user_selection = helper.validate_user_selection(VolunteerView.get_account_options())
            if user_selection == "1":
                # change username
                pass
            if user_selection == "2":
                # change password
                pass
            if user_selection == "3":
                # change name
                pass
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
