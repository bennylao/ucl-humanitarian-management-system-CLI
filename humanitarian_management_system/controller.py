import time
from pathlib import Path
import pandas as pd
import re
import math

from humanitarian_management_system import helper
from humanitarian_management_system.models import User, Admin, Volunteer, Event, Camp, ResourceTest, Refugee, ResourceReport
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
            print(user_selection)
            print(type(user_selection))

            if user_selection == "1":
                self.admin_manage_event(username)
            if user_selection == "2":
                self.admin_manage_camp(username)
            if user_selection == "3":
                self.admin_manage_volunteer()
            if user_selection == "4":
                print("we are here at resources")
                self.admin_manage_resource()
            if user_selection == "5":
                self.admin_display_summary()
            if user_selection == "6":
                self.admin_edit_account()
            if user_selection == "L":
                self.user = None
                self.startup()
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

    def admin_manage_camp(self, username):
        ManagementView.camp_main_message()
        AdminView.display_camp_menu()
        user_selection = helper.validate_user_selection(AdminView.get_camp_options())
        if user_selection == "1":
            self.create_camp(username)
        if user_selection == "2":
            pass  # edit camp
        if user_selection == "3":
            self.delete_camp()
        if user_selection == "4":
            self.resource_alloc_menu(username)
        if user_selection == "5":
            self.add_refugee(username)
        if user_selection == "6":
            self.move_refugee()
        if user_selection == "7":
            pass  # display all camps
        if user_selection == "R":
            pass
        if user_selection == "x":
            exit()

    def admin_manage_volunteer(self):
        pass

    ####################### MAIN RESOURCE MENU ############################# 

    def admin_manage_resource(self):
        user_selection = input(AdminView.display_resource_menu())
        # user_selection = helper.validate_user_selection(AdminView.display_resource_menu())
        if user_selection == "1":
            # ("1", "Allocate resources")
            self.resource_alloc_menu()
        if user_selection == "2":
            # ("2", "View resource statistics")
            self.resource_reporting_menu()
        if user_selection == "3":
            # ("3", "Add resource / purchase from shop")
            ####################### completely undefined yet, need to make from scratch!
            ####################### might be easier to do the menu elsewhere in an isolated enviornment, before refactoring and moving over
            pass
        if user_selection == "x":
            exit()
    ####################### MAIN RESOURCE MENU ############################# 

    def admin_display_summary(self):
        pass

    def admin_edit_account(self):
        pass

    def admin_create_event(self, username):
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
                self.remove_camp()
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
        #active_event_df = Event.get_all_active_events()
        #Event.display_events(active_event_df)
        active_index = helper.extract_active_event()[0]

        # check if active event is 0
        if len(active_index) == 0:
            print("No relevant events to select from.")
            return
        else:
            # read the event csv file and extract all available events
            csv_path = Path(__file__).parents[0].joinpath("data/eventTesting.csv")
            df1 = helper.matched_rows_csv(csv_path, "ongoing", "True", "eid")
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
                        camp_info = helper.validate_camp_input()
                        c = Camp(camp_info[1], camp_info[2], camp_info[3], True)
                        c.pass_camp_info(eventID, camp_info[0])
                        print("Camp created.")
                        break
                except ValueError:
                    print(f"Invalid input! Please enter an integer from {df1[1]} for Event ID.")

    def admin_modify_camp(self):
        """This function is to modify camp info"""
        pass

    def remove_camp(self):
        """This part of the code is to delete the camp from the camp.csv"""
        ManagementView.camp_deletion_message()
        active_index = helper.extract_active_event()[0]

        csv_path0 = Path(__file__).parents[0].joinpath("data/camp.csv")
        df0 = pd.read_csv(csv_path0)

        # if there is no active events, return
        if len(active_index) == 0:
            print("No relevant events to select from")
            return
        else:
            # print the events info for users to choose
            csv_path = Path(__file__).parents[0].joinpath("data/eventTesting.csv")
            df1 = helper.matched_rows_csv(csv_path, "ongoing", "True", "eid")
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
            if df1[0].loc[eventID, "no_camp"] == 0:
                print("No relevant camps to select from")
                return
            else:
                print("\n**The following shows the info of related camps*\n")
                print(df2[0])
                while True:
                    try:
                        modify_camp_id = int(input("\nWhich camp do you want to modify? Please enter campID: "))
                        if modify_camp_id not in df2[1]:
                            print(f"Invalid input! Please enter an integer from {df2[1]} for Camp ID.")
                            continue
                        else:

                            while True:
                                print()
                                print(df2[0].loc[df2[0].index == modify_camp_id])
                                for i, column_name in enumerate(df2[0].columns[3:], start=1):
                                    print(f"[{i}] {column_name}")
                                try:
                                    target_column_index = int(input(f"Which column do you want to modify(1~5)?: "))
                                    if target_column_index not in range(1, 9):
                                        print("Please enter a valid integer from 1 to 5")
                                        continue
                                    else:
                                        target_column_name = df2[0].columns[target_column_index + 2]
                                        print(target_column_name)
                                        while True:
                                            new_value = input(f"Enter the new value for {target_column_name}: ")
                                            if target_column_index == 1:
                                                if new_value == "low" or new_value == "high":
                                                    return
                                                else:
                                                    print("Invalid input! Please enter 'low' or 'high'")
                                            elif target_column_index == 5:
                                                if new_value == "open" or new_value == "closed":
                                                    break
                                                else:
                                                    print("Invalid input! Please enter 'open' or 'closed'")
                                            else:
                                                try:
                                                    new_value = int(new_value)
                                                    if new_value >= 0:
                                                        break
                                                    else:
                                                        print("Invalid input! Please enter a non-negative integer ")
                                                except ValueError:
                                                    print("Invalid input! Please enter a non-negative integer ")

                                        index_in_csv = df0[df0["campID"] == modify_camp_id].index.tolist()[0]
                                        helper.modify_csv_value(csv_path2, index_in_csv, target_column_name, new_value)
                                        print(f"\u2714 Changes have been saved!")
                                        return
                                except ValueError:
                                    print("Invalid input! Please enter an integer between 1 to 9")

                    except ValueError:
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

###################### RESOURCE MENU LEVEL 2 ###############################################

    def resource_alloc_menu(self):
        ManagementView.resource_alloc_main_message()
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
        test_instance = ResourceTest(campID=1, pop=100, total_pop=1000)

        print(test_instance.calculate_resource_jess())

        alloc_ideal = test_instance.calculate_resource_jess()
        alloc_ideal = test_instance.determine_above_below(threshold = 0.10)
        redistribute_sum_checker = test_instance.redistribute()
        print(alloc_ideal.groupby('resourceID')['current'].sum())
        print(redistribute_sum_checker)

    def resource_reporting_menu(self):
        ManagementView.resource_report_message()
        resource_report = ResourceReport()
        while True:
            user_selection = input("--> \n: ")

            if user_selection == '1':
                print(resource_report.resource_report_total())
            elif user_selection == '2':
                print(resource_report.resource_report_camp())
            elif user_selection == '3':
                print(resource_report.determine_above_below(threshold = 0.10))
            else:
                print("Invalid resource report option entered!")
                continue

            if user_selection == 'RETURN':
                self.admin_manage_resource()
            else:
                break

        df = helper.extract_active_event()[1]
        select_pop = df.loc[df['campID'] == select_index]['refugeePop'].tolist()[0]

        r = ResourceTest(select_index, select_pop, 0)
        r.calculate_resource()
        print("Auto resource allocation completed")
        self.admin_manage_camp(username)
###################### RESOURCE MENU LEVEL 2 ###############################################
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
