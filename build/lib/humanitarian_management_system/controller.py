import time
from pathlib import Path
import pandas as pd
import re
import math
import logging
from humanitarian_management_system import helper
from humanitarian_management_system.models import (User, Admin, Volunteer, Event, Camp, Refugee,
                                                   ResourceReport, ResourceAllocator, ResourceAdder, ResourceCampCreateDelete)
from humanitarian_management_system.views import GeneralView, ManagementView, AdminView, VolunteerView


class Controller:
    def __init__(self):
        # for saving user information
        self.user = None
        self.change_user = None
        self.logout_request = False

    def initialise(self):
        # show welcome messages when the program starts
        logging.debug("Controller is initialised.")
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
        try:
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

                # user_info contains all the user information if username and password match
                # otherwise, user_info is an empty series
                user_info = User.validate_user(username, password)
                # check if account is active
                if user_info.empty:
                    print("\nUsername or password is incorrect. Please try again."
                          "\n Or Enter 'RETURN' to get back to main menu.")
                elif user_info['isVerified'] == "FALSE":
                    user_info = pd.Series()
                    print("\nSince you are newly registered. Please contact the administrator to verify your account"
                          "\n Or Enter 'RETURN' to get back to main menu.")
                elif user_info['isActive'] == "FALSE":
                    user_info = pd.Series()
                    print("\nYour account has been deactivated, contact the administrator."
                          "\n Or Enter 'RETURN' to get back to main menu.")

            # if user record is matched, print login successfully
            if not user_info.empty:
                if user_info['userType'] == "admin":
                    # self.user is now an object of admin
                    self.user = Admin(user_info['userID'], *user_info[4:11])
                    print("\n***   Login Successful!   ***")
                    print("You are now logged in as Admin.")
                    self.admin_main()
                else:
                    # self.user is not an object of volunteer
                    self.user = Volunteer(user_info['userID'], *user_info[4:])
                    print("\n***   Login Successful!   ***")
                    print("You are now logged in as Volunteer.")
                    self.volunteer_main()
        except FileNotFoundError as e:
            print(f"\nData file is not found or is damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n{e}")
            logging.critical(f"{e}")
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def admin_main(self):
        AdminView.display_login_message(self.user.username)
        while True:
            AdminView.display_menu()
            user_selection = helper.validate_user_selection(AdminView.get_main_options())

            if user_selection == "1":
                self.admin_manage_event()
            if user_selection == "2":
                self.admin_manage_camp()
            if user_selection == "3":
                self.admin_manage_volunteer()
            if user_selection == "4":
                self.admin_manage_resource()
            if user_selection == "5":
                self.admin_display_summary()
            if user_selection == "6":
                self.user_edit_account()
            if user_selection == "7":
                self.user.show_account_info()
            if user_selection == "L" or self.logout_request:
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

    def admin_manage_volunteer(self):
        while True:
            AdminView.display_volunteer_menu()
            user_selection = helper.validate_user_selection(AdminView.get_volunteer_options())
            if user_selection == "1":
                self.edit_volunteer()
            if user_selection == "2":
                self.display_volunteer()
            if user_selection == "3":
                self.verify_account()
            if user_selection == "4":
                self.activate_account()
            if user_selection == "5":
                self.remove_account()
            if user_selection == "R":
                return
            if user_selection == "L":
                self.logout_request = True
                self.user = None
                return

    def edit_volunteer(self):
        try:
            csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
            vol_id_arr = []
            df = pd.read_csv(csv_path)
            df = df.loc[df['userType'] == 'volunteer']
            df = df.loc[:, ~df.columns.isin(['userType', 'isActive', 'roleID', 'eventID', 'campID'])]
            print("Here is a list of relevant information for all existing volunteers: ")
            Event.display_events(df)

            for i in df['userID'].tolist():
                vol_id_arr.append(str(i))

            while True:
                select_id = input("Please select a volunteer ID whose information you would like to change: ")
                if select_id not in vol_id_arr:
                    print("Invalid volunteer ID entered!")
                    continue
                if select_id == 'RETURN':
                    return
                break

            csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
            df = pd.read_csv(csv_path)

            # # OOP concept - assign user info to Volunteer class attribute by user selected volunteer ID
            df_name = df.loc[df['userID'] == int(select_id)]['username'].tolist()[0]
            df_password = df.loc[df['userID'] == int(select_id)]['password'].tolist()[0]

            row = User.validate_user(df_name, str(df_password))
            self.change_user = Volunteer(row['userID'], *row[4:])
            self.user.edit_volunteer(self.change_user)
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def display_volunteer(self):
        try:
            ManagementView.display_admin_vol()
            self.user.display_vol()
            return
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def verify_account():
        Admin.verify_user()

    def activate_account(self):
        try:
            ManagementView.display_activate()
            self.user.activate_user()
            return
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def remove_account(self):
        try:
            ManagementView.display_activate()
            self.user.remove_user()
            return
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    """####################### MAIN RESOURCE MENU #############################"""

    def admin_manage_resource(self):

        while True:
            AdminView.display_resource_menu()
            user_selection = helper.validate_user_selection(AdminView.get_resource_options())
            if user_selection == "1":
                # ("1", "Allocate resources")
                self.resource_alloc_main_menu()
            if user_selection == "2":
                # ("2", "View resource statistics")
                self.resource_reporting_menu()
            if user_selection == "3":
                # ("3", "Add resource / purchase from shop"xs)
                resource_adder_instance = ResourceAdder()
                resource_adder_instance.resource_adder()
            if user_selection == "R":
                break
            if user_selection == "L":
                self.logout_request = True
                self.user = None
                break

    """ ####################### MAIN RESOURCE MENU ############################# """

    def admin_display_summary(self):
        pass

    def admin_create_event(self):
        try:
            ManagementView.event_creation_message()
            event_info = helper.validate_event_input()
            if event_info is not None:
                Event.create_new_record(event_info)
                print("Event created.")
            else:
                return
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def admin_edit_event():
        try:
            ManagementView.event_edit_message()
            Event.edit_event_info()
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def admin_delete_event():
        try:
            ManagementView.event_delete_message()
            Event.delete_event()
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def admin_close_event():
        try:
            ManagementView.event_close_message()
            Event.disable_ongoing_event()
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    """###### main camp menu #####"""

    def admin_manage_camp(self):
        while True:
            ManagementView.camp_main_message()
            AdminView.display_camp_menu()
            user_selection = helper.validate_user_selection(AdminView.get_camp_options())
            if user_selection == "1":
                self.admin_create_camp()
            if user_selection == "2":
                self.admin_modify_camp()
            if user_selection == "3":
                self.admin_remove_camp()
            if user_selection == "4":
                self.create_refugee()
            if user_selection == "5":
                self.admin_edit_refugee()
            if user_selection == "6":
                self.move_refugee_admin()
            if user_selection == "7":
                self.admin_display_refugee()
            if user_selection == "8":
                self.admin_display_camp()
                pass
            if user_selection == "9":
                self.admin_refugee_export()
            if user_selection == "R":
                break
            if user_selection == "L":
                self.user = None
                self.logout_request = True
                break

    """ ##### Edit Refugee for all camps ##### """

    @staticmethod
    def admin_edit_refugee():
        try:
            user = 'admin'
            ManagementView.refugee_edit_message()

            r = Refugee('', '', '', '', '', '', '',
                        '')
            r.edit_refugee_info(user, 0)
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    """ #################  CREATE / MODIFY / REMOVE CAMPS############### """

    def admin_create_camp(self):
        try:
            ManagementView.camp_creation_message()
            # active_event_df = Event.get_all_active_events()
            # Event.display_events(active_event_df)

            csv_path = Path(__file__).parents[0].joinpath("data/event.csv")
            df = pd.read_csv(csv_path)
            active_index = helper.extract_active_event(csv_path)[0]

            # if there is no active events, return
            filtered_df = df[(df['ongoing'] == 'True') | (df['ongoing'] == 'Yet')]

            # check if active event is 0
            # if len(active_index) == 0:
            #    print("No relevant events to select from.")
            #    return
            # else:
            if filtered_df.empty:
                print("\nAll the events are closed and there's none to choose from.")
                return
            else:
                # read the event csv file and extract all available events
                # df1 = helper.matched_rows_csv(csv_path, "ongoing", "False", "eventID")
                print("\n*The following shows the info of all available events*")
                Event.display_events(filtered_df)

                # validate input for user select index
                while True:
                    try:
                        eventID = int(input("\nEnter Event ID: "))
                        if eventID not in active_index:
                            print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")
                            continue
                        else:
                            camp_info = helper.validate_camp_input()
                            c = Camp(*camp_info[1:3])
                            c.pass_camp_info(eventID, camp_info[0])
                            print("\n\u2714 New camp created!")
                            return
                    except ValueError:
                        print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")
        except Exception as e:
            print(f"\nCamp data file may be damaged or lost."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def admin_modify_camp(self):
        try:
            """This function is for admin modify camp info"""
            ManagementView.camp_modification_message()
            csv_path = Path(__file__).parents[0].joinpath("data/event.csv")
            df = pd.read_csv(csv_path)

            csv_path0 = Path(__file__).parents[0].joinpath("data/camp.csv")
            df0 = pd.read_csv(csv_path0)

            csv_path_r = Path(__file__).parents[0].joinpath("data/refugee.csv")
            df_r = pd.read_csv(csv_path_r)
            csv_path_v = Path(__file__).parents[0].joinpath("data/user.csv")
            df_v = pd.read_csv(csv_path_v)

            active_index = helper.extract_active_event(csv_path)[0]

            # if there is no active events, return
            filtered_df = df[(df['ongoing'] == 'True') | (df['ongoing'] == 'Yet')]
            if filtered_df.empty:
                print("\nAll the events are closed and there's none to choose from.")
                return
            else:
                Event.display_events(filtered_df)

            while True:
                try:
                    eventID = int(input("\nEnter Event ID: "))
                    if eventID not in active_index:
                        print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")
                        continue
                    elif df0[df0['eventID'] == eventID].empty:
                        print("No relevant camps to select from")
                        continue
                    elif eventID == 'RETURN':
                        return
                    break
                except ValueError:
                    print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")

            # print camps info for users to choose
            # df3 = helper.matched_rows_csv(csv_path0, "eventID", eventID, "campID")
            print("\n**The following shows the info of related camps*")
            filtered_df1 = df0[df0['eventID'] == eventID]
            filtered_campID = filtered_df1['campID'].tolist()
            Event.display_events(filtered_df1)

            while True:
                try:
                    modify_camp_id = int(input("\nWhich camp do you want to modify? Please enter campID: "))
                    if modify_camp_id not in filtered_campID:
                        print(f"Invalid input! Please enter an integer from {filtered_campID} for Camp ID.")
                        continue
                    else:
                        break
                except ValueError:
                    print(f"Invalid input! Please enter an integer from {filtered_campID} for Camp ID.")

            while True:
                csv_path2 = Path(__file__).parents[0].joinpath("data/camp.csv")
                df2 = pd.read_csv(csv_path2)

                # Event.display_events(filtered_df1[filtered_df1['campID'] == modify_camp_id])
                Event.display_events(df2[(df2['campID'] == modify_camp_id) & (df2['eventID'] == eventID)])
                filtered_df1 = filtered_df1.loc[:, filtered_df1.columns != 'eventID']
                filtered_df1 = filtered_df1.loc[:, filtered_df1.columns != 'countryID']
                for i, column_name in enumerate(filtered_df1.columns[0:], start=1):
                    print(f"[{i}] {column_name}")
                try:
                    print("[8] QUIT editing")
                    target_column_index = int(input(f"Which column do you want to modify(1~7)? Or quit editing(8): "))
                    if target_column_index not in range(1, 9):
                        print("Please enter a valid integer from 1 to 8")
                        continue
                    elif target_column_index in range(1, 8):
                        target_column_name = filtered_df1.columns[target_column_index - 1]
                        while True:
                            new_value = input(f"Enter the new value for {target_column_name}: ")

                            # the ability to edit camp ID, but camp ID has to be unique
                            if target_column_index == 1:
                                camp_id_arr = []
                                camp_id_list = df0['campID'].tolist()

                                for i in camp_id_list:
                                    camp_id_arr.append(str(i))

                                if new_value in camp_id_arr:
                                    print("Camp ID already exists! Please choose a new one.")
                                    continue

                                try:
                                    # change corresponding refugee & volunteer camp ID
                                    ref_id_arr = df_r.loc[df_r['campID'] == modify_camp_id]['refugeeID'].tolist()
                                    vol_id_arr = df_v.loc[df_v['campID'] == modify_camp_id]['userID'].tolist()

                                    for j in ref_id_arr:
                                        helper.modify_csv_pandas("data/refugee.csv", 'refugeeID',
                                        int(j), 'campID', int(new_value))

                                    for k in vol_id_arr:
                                        helper.modify_csv_pandas("data/user.csv", 'userID',
                                        int(k), 'campID', int(new_value))
                                except:
                                    break
                                break

                            if target_column_index == 3:
                                if new_value == "low" or new_value == "high":
                                    break
                                else:
                                    print("Invalid input! Please enter 'low' or 'high'")
                                    continue
                            elif target_column_index == 7:
                                if new_value == "open" or new_value == "closed":
                                    break
                                else:
                                    print("Invalid input! Please enter 'open' or 'closed'")
                                    continue
                            elif target_column_index == 8:
                                return

                            else:
                                try:
                                    new_value = int(new_value)
                                    if new_value >= 0:
                                        break
                                    else:
                                        print("Invalid input! Please enter a non-negative integer ")
                                        continue
                                except ValueError:
                                    print("Invalid input! Please enter a non-negative integer ")
                                    continue

                        index_in_csv = df0[df0["campID"] == modify_camp_id].index.tolist()[0]
                        helper.modify_csv_value(csv_path0, index_in_csv, target_column_name, new_value)

                        # reorder camp ID after ID changed
                        csv_path_c = Path(__file__).parents[0].joinpath("data/camp.csv")
                        df_c = pd.read_csv(csv_path_c)

                        df_c.sort_values('campID', inplace=True)
                        df_c.to_csv(Path(__file__).parents[0].joinpath("data/camp.csv"), index=False)
                        print(f"\u2714 Changes have been saved!")
                    else:
                        return
                except ValueError:
                    print("Invalid input! Please enter an integer between 1 to 8")
                    continue
            # while True:
            #     new_value = input(f"Enter the new value for {target_column_name}: ")
            #     if target_column_index == 2:
            #         if new_value == "low" or new_value == "high":
            #             break
            #         else:
            #             print("Invalid input! Please enter 'low' or 'high'")
            #             continue
            #     elif target_column_index == 6:
            #         if new_value == "open" or new_value == "closed":
            #             break
            #         else:
            #             print("Invalid input! Please enter 'open' or 'closed'")
            #             continue
            #     else:
            #         try:
            #             new_value = int(new_value)
            #             if new_value >= 0:
            #                 break
            #             else:
            #                 print("Invalid input! Please enter a non-negative integer ")
            #                 continue
            #         except ValueError:
            #             print("Invalid input! Please enter a non-negative integer ")
            #             continue
            #
            # index_in_csv = df0[df0["campID"] == modify_camp_id].index.tolist()[0]
            # helper.modify_csv_value(csv_path0, index_in_csv, target_column_name, new_value)
            # print(f"\u2714 Changes have been saved!")
            # return
        except Exception as e:
            print(f"\nMultiple files may be damaged or lost."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def admin_remove_camp(self):
        try:
            """This part of the code is to delete the camp from the camp.csv"""
            ManagementView.camp_deletion_message()

            event_csv_path = Path(__file__).parents[0].joinpath("data/event.csv")
            camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
            active_index = helper.extract_active_event(event_csv_path)[0]

            # if there is no active events, return
            if len(active_index) == 0:
                print("No relevant events to select from")
                return
            else:
                # print the events info for users to choose
                df = pd.read_csv(event_csv_path)
                filtered_df = df[(df['ongoing'] == 'True') | (df['ongoing'] == 'Yet')]
                if filtered_df.empty:
                    print("\nAll the events are closed and there's none to choose from.")
                    return
                else:
                    print("\n*The following shows the info of all available events*")
                    Event.display_events(filtered_df)

            # read camp csv file
            df1 = pd.read_csv(camp_csv_path)
            while True:
                try:
                    eventID = int(input("\nEnter Event ID: "))
                    if eventID not in active_index:
                        print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")
                        continue
                    elif df1[df1['eventID'] == eventID].empty:
                        print("No relevant camps to select from")
                        return
                    elif eventID == 'RETURN':
                        return
                    break
                except ValueError:
                    print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")

            filtered_campID = df1[df1['eventID'] == eventID]['campID'].tolist()
            print('The following shows the info of all camps from the event')
            Event.display_events(df1[df1['eventID'] == eventID])
            while True:
                try:
                    delete_camp = int(input("\nWhich camp do you want to remove? Please enter campID: "))
                    if delete_camp not in filtered_campID:
                        print(f"Invalid input! Please enter an integer from {filtered_campID} for Camp ID.")
                        continue
                    else:
                        print("\n*The following shows the info of the camp you have chosen*")
                        Event.display_events(df1[df1['campID'] == delete_camp])
                        break
                except ValueError:
                    print(f"Invalid input! Please enter an integer from {filtered_campID} for Camp ID.")

            while True:
                aa = input(f"\nAre you sure to remove the camp {delete_camp}? (yes/no): ")
                if aa == "yes":
                    # implement the deletion in csv file
                    df2 = df1[df1["campID"] != delete_camp]
                    df2.to_csv(camp_csv_path, index=False)

                    # keep track of existing camp num of a particular event
                    no_camp = df.loc[eventID, "no_camp"]
                    no_camp -= 1
                    index = df[df["eid"] == eventID].index.tolist()
                    helper.modify_csv_value(event_csv_path, index[0], "no_camp", no_camp)
                    print("\n\u2714 You have Successfully removed the camp!")
                    return
                elif aa == "no":
                    return
                else:
                    print("Invalid input! Please enter 'yes' or 'no'")
                    continue
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def admin_display_refugee(self):
        try:
            user = 'admin'
            ManagementView.display_admin_refugee()
            r = Refugee('', '', '', '', '', '', '',
                        '')
            r.display_info(user, 0)
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def admin_display_camp(self):
        try:
            user = 'admin'
            ManagementView.display_admin_camp()
            c = Camp('', '')
            c.display_info(user, 0)
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    """" ###################### RESOURCE MENU LEVEL 2 ############################################### """

    def resource_alloc_main_menu(self):

        ### check for new camps
        resourceCamp_instance = ResourceCampCreateDelete()
        resourceCamp_instance.new_camp_resources_interface()

        ### check for closed camps
        resourceCamp_instance.closed_camp_resources_interface()

        ### check for unallocated resources
        resource_report = ResourceReport()
        unalloc_status, prompt = resource_report.unalloc_resource_checker()
        print(prompt)

        ManagementView.resource_alloc_main_message()

        while True:
            user_selection = input("\nAllocation mode: --> ")
            alloc_instance = ResourceAllocator()

            if user_selection == '1':
                alloc_instance.manual_alloc()
            elif user_selection == '2':
                alloc_instance.auto_alloc_interface()
            else:
                print("Invalid mode option entered!")
                continue

            if user_selection == 'RETURN':
                return
            else:
                break

    def man_resource(self):
        try:
            ManagementView.man_resource_message()
            index = helper.display_camp_list()
            res_man_info = helper.validate_man_resource(index)

            if res_man_info is not None:
                # r = ResourceTest(res_man_info[0], '', '')
                # r.manual_resource(res_man_info[2], res_man_info[1])
                # print("Resource allocated as request.")
                # self.admin_manage_camp()
                pass
            else:
                return
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def auto_resource():
        try:
            ManagementView.auto_resource_message()
            alloc_instance = ResourceAllocator()
            alloc_instance.auto_alloc()
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def resource_reporting_menu(self):
        try:
            ManagementView.resource_report_message()
            resource_report = ResourceReport()
            while True:
                user_selection = input("--> \n: ")

                if user_selection == '1':
                    # print(resource_report.resource_report_total())
                    pass
                elif user_selection == '2':
                    print(resource_report.resource_report_camp())
                else:
                    print("Invalid mode option entered!")
                    continue

                if user_selection == 'RETURN':
                    return
                else:
                    break
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

        # df = helper.extract_active_event()[1]
        # select_pop = df.loc[df['campID'] == select_index]['refugeePop'].tolist()[0]
        #
        # r = ResourceTest(select_index, select_pop, 0)
        # r.calculate_resource()
        # print("Auto resource allocation completed")
        # self.admin_manage_camp(username)

    """ ###################### RESOURCE MENU LEVEL 2 ############################################### """

    def volunteer_main(self):
        VolunteerView.display_login_message(self.user.username)
        while True:
            VolunteerView.display_main_menu()
            user_selection = helper.validate_user_selection(VolunteerView.get_main_options())
            if user_selection == "1":
                # join/change camp
                self.volunteer_join_camp()
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

            r = Refugee('', '', '', '', '', '',
                        '', '')
            c = Camp('', '')

            if user_selection == "1":
                # add refugee
                self.create_refugee()
            if user_selection == "2":
                self.vol_edit_refugee(r)
            if user_selection == "3":
                self.move_refugee_volunteer()
            if user_selection == "4":
                self.volunteer_edit_camp()
            if user_selection == "5":
                self.vol_display_refugee(r)
            if user_selection == "6":
                self.vol_display_camp(c)
            if user_selection == "7":
                self.display_camp_resource(c)
            if user_selection == "8":
                self.legal_advice_support()
            if user_selection == '9':
                self.refugee_training_sessions()

            if user_selection == "R":
                break
            if user_selection == "L":
                self.user = None
                self.logout_request = True
                break

    def volunteer_show_account_info(self):
        try:
            self.user.show_account_info()
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    # join camp and change camp is the same thing, basically volunteer can change to a different camp after joining a
    # camp by selecting join/change camp in the menu
    def volunteer_join_camp(self):
        try:
            csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
            df = pd.read_csv(csv_path)

            ManagementView.join_camp_message()
            index = helper.display_camp_list()

            while True:
                select_index = int(input("\nindex: "))

                if select_index not in index:
                    print("invalid index option entered!")
                    continue
                try:
                    if select_index == 'RETURN':
                        return
                except:
                    return
                break

            event_id = df.loc[df['campID'] == select_index]['eventID'].tolist()[0]
            join_info = helper.validate_join()
            if join_info is not None:
                v = Volunteer(0, self.user.username, '', '', '', '', '', '',
                              join_info, event_id, select_index)
                v.join_camp()
            return
        except Exception as e:
            print(f"\nVolunteer or camp data file may be damaged or lost."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def volunteer_edit_camp(self):
        user_id = self.user.user_id
        user_csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
        # active_index = helper.extract_active_event(camp_csv_path)[0]
        df = pd.read_csv(user_csv_path)
        dff = df[df['userID'] == int(user_id)]
        event_id = dff.at[1, 'eventID']
        camp_id = dff.at[1, 'campID']

        csv_path_r = Path(__file__).parents[0].joinpath("data/refugee.csv")
        df_r = pd.read_csv(csv_path_r)
        while True:
            csv_path2 = Path(__file__).parents[0].joinpath("data/camp.csv")
            df2 = pd.read_csv(csv_path2)

            # Event.display_events(filtered_df1[filtered_df1['campID'] == modify_camp_id])
            Event.display_events(df2[(df2['campID'] == camp_id) & (df2['eventID'] == event_id)])

            df2 = df2.loc[:, df2.columns != 'eventID']
            df2 = df2.loc[:, df2.columns != 'countryID']

            for i, column_name in enumerate(df2.columns[0:], start=1):
                print(f"[{i}] {column_name}")
            try:
                print("[8] QUIT editing")
                target_column_index = int(input(f"Which column do you want to modify(1~7)? Or quit editing(8): "))
                if target_column_index not in range(1, 9):
                    print("Please enter a valid integer from 1 to 8")
                    continue
                elif target_column_index in range(1, 8):
                    target_column_name = df2.columns[target_column_index - 1]
                    while True:
                        new_value = input(f"Enter the new value for {target_column_name}: ")

                        # the ability to edit camp ID, but camp ID has to be unique
                        if target_column_index == 1:
                            camp_id_arr = []
                            camp_id_list = df2['campID'].tolist()

                            for i in camp_id_list:
                                camp_id_arr.append(str(i))

                            if new_value in camp_id_arr:
                                print("Camp ID already exists! Please choose a new one.")
                                continue

                            try:
                                # change corresponding refugee & volunteer camp ID
                                ref_id_arr = df_r.loc[df_r['campID'] == int(camp_id)]['refugeeID'].tolist()

                                for j in ref_id_arr:
                                    helper.modify_csv_pandas("data/refugee.csv", 'refugeeID',
                                                             int(j), 'campID', int(new_value))
                                helper.modify_csv_pandas("data/user.csv", 'userID',
                                                         user_id, 'campID', int(new_value))
                            except:
                                break
                            break

                        if target_column_index == 3:
                            if new_value == "low" or new_value == "high":
                                break
                            else:
                                print("Invalid input! Please enter 'low' or 'high'")
                        elif target_column_index == 7:
                            if new_value == "open" or new_value == "closed":
                                break
                            else:
                                print("Invalid input! Please enter 'open' or 'closed'")
                        elif target_column_index == 8:
                            return

                        else:
                            try:
                                new_value = int(new_value)
                                if new_value >= 0:
                                    break
                                else:
                                    print("Invalid input! Please enter a non-negative integer ")
                            except ValueError:
                                print("Invalid input! Please enter a non-negative integer ")

                    index_in_csv = df2[df2["campID"] == int(camp_id)].index.tolist()[0]
                    helper.modify_csv_value(csv_path2, index_in_csv, target_column_name, new_value)

                    # reorder camp ID after ID changed
                    csv_path_c = Path(__file__).parents[0].joinpath("data/camp.csv")
                    df_c = pd.read_csv(csv_path_c)

                    df_c.sort_values('campID', inplace=True)
                    df_c.to_csv(Path(__file__).parents[0].joinpath("data/camp.csv"), index=False)
                    print(f"\u2714 Changes have been saved!")
                else:
                    return
            except ValueError:
                print("Invalid input! Please enter an integer between 1 to 7")

    def create_refugee(self):
        try:
            csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
            csv_path_c = Path(__file__).parents[0].joinpath("data/camp.csv")
            df = pd.read_csv(csv_path)

            user_type = df.loc[df['username'] == self.user.username]['userType'].tolist()[0]
            df_c = pd.read_csv(csv_path_c)
            active_camp = df_c.loc[df_c['status'] == 'open']['campID'].tolist()

            # check user type, for admin - can create new refugee for any camp, and for vol - camp dependent
            if user_type == 'admin':
                csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
                df1 = helper.matched_rows_csv(csv_path, "status", 'closed', "campID")
                print("\n*The following shows the info of all available events*\n")
                print(df1[0])

                while True:
                    try:
                        cid = int(input("Enter a camp ID: "))
                        row_index_new_camp = df_c[df_c['campID'] == int(cid)].index
                        new_potential_refugee_pop = (df_c.at[row_index_new_camp[0], 'refugeePop'])
                        new_camp_capacity = df_c.at[row_index_new_camp[0], 'refugeeCapacity']
                        if (new_potential_refugee_pop + 1) <= new_camp_capacity:
                            break
                        else:
                            print(
                                "\n\nOh no! The new camp you've selected doesn't have the capacity to handle another refugee. "
                                f"Camp {cid} has a current population of {new_potential_refugee_pop} and a capacity of "
                                f"{new_camp_capacity}.\nLet's go again.\n")
                        if cid not in active_camp:
                            print("Invalid camp ID entered!")
                            continue
                        if cid == 'RETURN':
                            return
                        break
                    except:
                        return
            else:
                # check if volunteer is already assigned to a camp, if no exit to menu
                cid = df.loc[df['username'] == self.user.username]['campID'].tolist()[0]
                row_index_new_camp = df_c[df_c['campID'] == int(cid)].index
                new_potential_refugee_pop = (df_c.at[row_index_new_camp[0], 'refugeePop'])
                new_camp_capacity = df_c.at[row_index_new_camp[0], 'refugeeCapacity']
                if (new_potential_refugee_pop + 1) >= new_camp_capacity:
                    print("\n\nOh no! Your camp doesn't have the capacity to handle another refugee. "
                          f"Camp {cid} has a current population of {new_potential_refugee_pop} and a capacity of "
                          f"{new_camp_capacity}.\nYou'll have to remove some refugees from your camp first.\n")
                    return
                # check if volunteer user already join a camp
                if math.isnan(cid):
                    print("You must first join a camp!")
                    return
                print(f'''\nYou're currently assigned to camp {int(cid)}.''', end='')

            ManagementView.create_refugee_message()
            # health risk level of volunteer's camp
            lvl = df_c.loc[df_c['campID'] == cid]['healthRisk'].tolist()[0]

            refugee_info = helper.validate_refugee(lvl)
            if refugee_info is not None:
                r = Refugee(refugee_info[0], refugee_info[1], refugee_info[2], refugee_info[3], refugee_info[4],
                            refugee_info[5], refugee_info[6], refugee_info[7])
                r.add_refugee_from_user_input(cid)
            else:
                return
            print("Refugee created.")
            self.admin_manage_camp()
        except Exception as e:
            print(f"\nRefugee or camp data file may be damaged or lost."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def move_refugee_volunteer(self):
        while True:
            move_or_delete = input(
                "Do you want to MOVE or DELETE a refugee from the system? M for MOVE or D for DELETE "
                "\nor RETURN to exit back: ")
            if move_or_delete.lower() == "return":
                return
            elif move_or_delete.lower() == "m":
                helper.move_refugee_helper_method()
            elif move_or_delete.lower() == "d":
                helper.delete_refugee()
            else:
                print("Sorry! Didn't catch that. Please try again or enter RETURN to exit.")

    def move_refugee_admin(self):
        while True:
            move_or_delete = input(
                "\n\nDo you want to MOVE or DELETE a refugee from the system? M for MOVE or D for DELETE "
                "\nor RETURN to exit back: ")
            if move_or_delete.lower() == "return":
                return
            elif move_or_delete.lower() == "m":
                helper.move_refugee_helper_method()
            elif move_or_delete.lower() == "d":
                helper.delete_refugee()
            else:
                print("Sorry! Didn't catch that. Please try again or enter RETURN to exit.")

    def admin_refugee_export(self):
        print(
            "----------------------------------------------------------------------------------------------------------\n"
            "Looks like you want to print out a CSV record of all the refugees we have in the system across all camps.\n"
            "---------------------------------------------------------------------------------------------------------")
        helper.admin_export_refugees_to_csv()

    def legal_advice_support(self):
        while True:
            helper.legal_advice_support()
            self.volunteer_manage_camp()

    def refugee_training_sessions(self):
        while True:
            create_add_delete = input("\nAre you looking to CREATE or DELETE a skills session, add, or \nremove "
                                      "refugees to/from a session?"
                                      "\nEnter CREATE,\nDELETE,\nADD,\nREMOVE,\nDISPLAY (to"
                                      " view all sessions in the system),\nor RETURN (to exit): ")
            if create_add_delete.lower() == 'return':
                return
            elif create_add_delete.lower() == 'create':
                helper.create_training_session()
            elif create_add_delete.lower() == 'delete':
                helper.delete_session()
            elif create_add_delete.lower() == 'add':
                helper.add_refugee_to_session()
            elif create_add_delete.lower() == 'remove':
                helper.remove_refugee_from_session()
            elif create_add_delete.lower() == 'display':
                helper.display_training_session()
            else:
                print("\nSorry! Didn't catch that. Please try again or enter RETURN to exit.")

    def user_edit_account(self):
        while True:
            ManagementView.display_account_menu()
            user_selection = helper.validate_user_selection(ManagementView.get_account_options())
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
                self.user_change_email()
            if user_selection == "5":
                # change phone
                self.user_change_phone()
            if user_selection == "6":
                # change occupation
                self.user_change_occupation()
            if user_selection == "R":
                break
            if user_selection == "L":
                self.user = None
                self.logout_request = True
                break

    def user_change_username(self):
        try:
            existing_usernames = User.get_all_usernames()
            print(f"\nCurrent Username: '{self.user.username}'")
            while True:
                new_username = input("\nPlease enter your new username: ")
                if new_username == "RETURN":
                    return
                elif new_username not in existing_usernames and new_username.isalnum():
                    self.user.username = new_username
                    # update csv file
                    self.user.update_username()
                    print("\nUsername changed successfully."
                          f"\nYour new username is '{self.user.username}'.")
                    break
                elif new_username in existing_usernames:
                    print("\nSorry, username already exists.")
                    continue
                else:
                    print("\nInvalid username entered. Only alphabet letter (Aa-Zz) and numbers (0-9) are allowed.")
                    continue
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def user_change_password(self):
        try:
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
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def user_change_name(self):
        try:
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
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def user_change_email(self):
        try:
            # specify allowed characters for email
            email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            all_emails = User.get_all_emails()
            print(f"\nCurrent Email: {self.user.email}")

            while True:
                new_email = input("Please enter new email: ")
                if new_email == "RETURN":
                    return
                elif new_email == self.user.email:
                    print("\n The new email is the same as current email!"
                          "Please enter a new one.")
                    continue
                elif re.fullmatch(email_format, new_email) and new_email not in all_emails:
                    self.user.email = new_email
                    # update csv file
                    self.user.update_email()
                    print("\nEmail changed successfully."
                          f"\nYour new username is '{self.user.email}'.")
                    break
                elif new_email in all_emails:
                    print("\nSorry, email is already linked to other account.")
                else:
                    print("Invalid password entered.\n"
                          "Only alphabet, numbers and !@#$%^&* are allowed.")
                    continue
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def user_change_phone(self):
        try:
            print(f"\nCurrent Phone Number: {self.user.phone}")
            while True:
                new_phone = input("\nPlease enter new phone number: ")
                if new_phone == 'RETURN':
                    return
                elif new_phone.isnumeric():
                    break
                else:
                    print("Invalid phone number entered. Only numbers are allowed.")
            self.user.phone = new_phone
            # update the csv file
            self.user.update_phone()
            print("\nPhone changed successfully."
                  f"\nYour new phone is '{self.user.phone}")
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def user_change_occupation(self):
        try:
            print(f"\nCurrent Occupation: {self.user.occupation}")
            while True:
                new_occupation = input("\nPlease enter your new occupation: ")
                if new_occupation == "RETURN":
                    return
                elif new_occupation.isalpha():
                    self.user.occupation = new_occupation
                    # update the csv file
                    self.user.update_occupation()
                    print("\nName changed successfully."
                          f"\nYour new occupation is '{self.user.occupation}'.")
                    break
                else:
                    print("\nInvalid first name entered. Only alphabet letter (a-z) are allowed.")
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    """ #### edit refugee for volunteer, volunteer camp dependent #### """

    def vol_edit_refugee(self, r):
        try:
            cid = helper.check_vol_assigned_camp(self.user.username)
            print(f"You're currently assigned to camp {int(cid)}.")
            user = 'volunteer'

            ManagementView.refugee_edit_message()
            r.edit_refugee_info(user, cid)
        except Exception as e:
            print(f"\nMultiple data files may to be damaged or lost."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def vol_display_refugee(self, r):
        try:
            user = 'volunteer'
            cid = helper.check_vol_assigned_camp(self.user.username)
            csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
            df = pd.read_csv(csv_path)
            if df.loc[df['campID'] == int(cid)]['refugeePop'].tolist()[0] == 0:
                print(f" No refugee(s) in camp {int(cid)}.")
                return

            ManagementView.display_vol_refugee(cid)
            r.display_info(user, cid)
        except Exception as e:
            print(f"\nRefugee or medical data file may be damaged or lost."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def vol_display_camp(self, c):
        try:
            user = 'volunteer'
            cid = helper.check_vol_assigned_camp(self.user.username)
            ManagementView.display_vol_camp(cid)
            c.display_info(user, cid)
        except Exception as e:
            print(f"\nCamp or event data file may be damaged or lost."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def display_camp_resource(self, c):
        try:
            cid = helper.check_vol_assigned_camp(self.user.username)
            ManagementView.display_camp_resource(cid)
            c.display_resinfo(cid)
        except Exception as e:
            print(f"\nCamp or resource data file may be damaged or lost."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

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
    #         self.volunteer_main()
