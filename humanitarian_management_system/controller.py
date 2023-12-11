import time
from pathlib import Path
import pandas as pd
import re
import math
import logging

from passlib.handlers.sha2_crypt import sha256_crypt

from humanitarian_management_system import helper
from humanitarian_management_system.data_analysis import (visualization_v, resources_distribution, medical_info,
                                                          gender_distribution, age_distribution, num_camp)
from humanitarian_management_system.models import (User, Admin, Volunteer, Event, Camp, Refugee,
                                                   ResourceReport, ResourceAllocator, ResourceAdder,
                                                   ResourceCampCreateDelete)
from humanitarian_management_system.views import GeneralView, ManagementView, AdminView, VolunteerView


class Controller:
    def __init__(self):
        # for saving user information
        self.user = None
        self.logout_request = False

    def initialise(self):
        # show welcome messages when the program starts
        logging.info("Controller is initialised")
        GeneralView.display_startup_logo()
        GeneralView.display_welcome_message()
        logging.info("welcome message is displayed")
        self.startup()

    def startup(self):
        while True:
            self.logout_request = False
            # display startup menu
            GeneralView.display_startup_menu()
            logging.info("Startup page is shown")
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
            if user_selection == 'H':
                self.help_center()
            if user_selection == "x":
                # exit the program
                break

    @staticmethod
    def register():
        GeneralView.display_registration_message()
        logging.info("Register page is shown")
        usernames = User.get_all_usernames()
        # registration_info will contain all the required info for creating new volunteer
        # if registration_info is none, the registration is fail and user will be redirected back to startup page
        registration_info = helper.validate_registration(usernames)
        if registration_info is not None:
            # write new volunteer record into csv
            Volunteer.create_new_record(registration_info)
            print("\n***   Your volunteer account is created successfully!   ***"
                  "\n\nYou will be redirected to Login Page shortly.")
            logging.info("New volunteer account is created")
            time.sleep(3)
            return True
        else:
            logging.info("Registration is cancelled")
            return False

    def login(self):
        user_info = pd.Series()
        # get all existing usernames in a list
        try:
            all_usernames = User.get_all_usernames()
            GeneralView.display_login_message()
            logging.info("login page is shown")

            while user_info.empty:
                username = input("\nUsername: ")
                if username == 'RETURN':
                    break
                if username not in all_usernames:
                    logging.info("login failed due to non-existent username")
                    print("Account doesn't exist!")
                    continue
                password = input("\nPassword: ")

                # user_info contains all the user information if username and password match
                # otherwise, user_info is an empty series
                user_info = User.validate_user(username, password)
                # check if account is active
                if user_info.empty:
                    logging.info("login failed due to invalid password")
                    print("\nUsername or password is incorrect. Please try again."
                          "\n Or Enter 'RETURN' to get back to main menu.")
                elif not user_info['isVerified']:
                    user_info = pd.Series()
                    logging.info("login failed as account has not been verified yet")
                    print("\nSince you are newly registered. Please contact the administrator to verify your account"
                          "\n Or Enter 'RETURN' to get back to main menu.")
                elif not user_info['isActive']:
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

    def admin_main(self):
        logging.info("login successfully as admin")
        AdminView.display_login_message(self.user.username)
        while True:
            AdminView.display_menu()
            logging.info("admin main menu is shown")
            user_selection = helper.validate_user_selection(AdminView.get_main_options())

            if user_selection == "1":
                self.admin_manage_event()
            elif user_selection == "2":
                self.admin_manage_camp()
            elif user_selection == "3":
                self.admin_manage_refugee()
            elif user_selection == "4":
                self.admin_manage_resource()
            elif user_selection == "5":
                self.admin_manage_volunteer()
            elif user_selection == "6":
                self.admin_display_summary()
            elif user_selection == "7":
                self.user_edit_account()
            elif user_selection == "8":
                self.user.show_account_info()
            if user_selection == "L" or self.logout_request:
                logging.info("logging out from admin main menu")
                self.user = None
                break

    def admin_manage_event(self):
        while True:
            AdminView.display_event_menu()
            logging.info("admin event management is shown")
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
                self.admin_display_event()
            if user_selection == "R":
                break
            if user_selection == "L":
                logging.info("logging out from admin event management menu")
                self.user = None
                self.logout_request = True
                break

    def admin_manage_volunteer(self):
        while True:
            AdminView.display_volunteer_menu()
            logging.info("admin volunteer management menu is shown")
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
                logging.info("logging out from admin volunteer management menu")
                self.logout_request = True
                self.user = None
                return

    def edit_volunteer(self):
        logging.info("admin edit volunteer")
        try:
            csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
            vol_id_arr = []
            df = pd.read_csv(csv_path)
            df = df.loc[df['userType'] == 'volunteer']
            df = df.loc[:, ~df.columns.isin(['userType', 'password'])]
            print("Here is a list of relevant information for all existing volunteers: ")
            Event.display_events(df)

            for i in df['userID'].tolist():
                vol_id_arr.append(str(i))

            while True:
                select_id = input("Please select a volunteer ID whose information you would like to change: ")
                if select_id in vol_id_arr:
                    break
                elif select_id == 'RETURN':
                    return
                else:
                    print("Invalid volunteer ID entered!")
                    continue

            select_id = int(select_id)
            df = pd.read_csv(csv_path)
            row = df.loc[df['userID'] == select_id].squeeze()
            target_user = Volunteer(row['userID'], *row[4:])
            self.user.edit_volunteer_profile(target_user)
            logging.info("admin edit volunteer successfully")
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")
        except ValueError as e:
            print(f"\nInvalid ID input."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def display_volunteer(self):
        ManagementView.display_admin_vol()
        self.user.display_vol()
        logging.info("all volunteer is displayed")
        return

    @staticmethod
    def verify_account():
        logging.info("Start Verifying volunteer account")
        Admin.verify_user()
        logging.info("Finish verifying volunteer account")

    def activate_account(self):
        try:
            logging.info("Start activating account")
            ManagementView.display_activate()
            self.user.activate_user()
            logging.info("Finish activating account")
            return
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")
        except ValueError as e:
            print(f"\nInvalid ID input."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def remove_account(self):
        try:
            logging.info("Start removing account")
            ManagementView.display_activate()
            self.user.remove_user()
            logging.info("Finish removing account")
            return
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")
        except ValueError as e:
            print(f"\nInvalid ID input."
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
            if user_selection == "3":
                # ("2", "View resource statistics")
                self.resource_reporting_menu()
            if user_selection == "2":
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

    @staticmethod
    def admin_display_summary():
        try:
            ManagementView.display_summary_message()
            event_csv_path = Path(__file__).parents[0].joinpath("data/event.csv")
            df_event = pd.read_csv(event_csv_path)
            camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
            df_camp = pd.read_csv(camp_csv_path)
            resource_csv_path = Path(__file__).parents[0].joinpath("data/resourceAllocation.csv")
            df_resource = pd.read_csv(resource_csv_path)
            filtered_df_event = df_event[(df_event['ongoing'] == 'True') | (df_event['ongoing'] == 'Yet')]

            if filtered_df_event.empty:
                print('There is no ongoing event.\n')
            else:
                filtered_df_camp = df_camp.loc[
                    df_camp['status'] == 'open', ['eventID', 'campID', 'volunteerPop', 'refugeePop']]
                qty_sum_by_camp = df_resource.groupby('campID')['qty'].sum().reset_index()
                qty_sum_by_camp.rename(columns={'qty': '# resource'}, inplace=True)
                merge_resource = pd.merge(filtered_df_camp, qty_sum_by_camp, how='left', on='campID')
                result_df = pd.merge(filtered_df_event, merge_resource, how='left', on='eventID')
                result_df.rename(columns={'volunteerPop': '# volunteer'}, inplace=True)
                result_df.rename(columns={'refugeePop': '# refugee'}, inplace=True)
                result_df = result_df.drop(['ongoing', 'description', 'no_camp'], axis=1)
                Event.display_events(result_df)
        except FileNotFoundError as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def admin_create_event():
        ManagementView.event_creation_message()
        event_info = helper.validate_event_input()
        if event_info is not None:
            Event.create_new_record(event_info)
            print("\n\u2714 New event created.")
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

    @staticmethod
    def admin_display_event():
        print("This page shows all the events.")
        try:
            csv_event_path = Path(__file__).parents[0].joinpath("data/event.csv")
            df_e = pd.read_csv(csv_event_path)
            Event.display_events(df_e)

            user_input = input("Enter any to exit...")
            if not user_input:
                return
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")
        except ValueError as e:
            print(f"\nInvalid ID input."
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
            elif user_selection == "2":
                self.admin_modify_camp()
            elif user_selection == "3":
                self.admin_delete_camp()
            elif user_selection == "4":
                self.admin_close_camp()
            elif user_selection == "5":
                self.admin_display_camp()
            elif user_selection == "6":
                self.admin_data_visualization()
            elif user_selection == "R":
                break
            elif user_selection == "L":
                self.user = None
                self.logout_request = True
                break

    def admin_manage_refugee(self):
        while True:
            AdminView.display_refugee_welcome_message()
            AdminView.display_refugee_menu()
            user_selection = helper.validate_user_selection(AdminView.get_refugee_options())
            if user_selection == "1":
                self.create_refugee()
            elif user_selection == "2":
                self.admin_edit_refugee()
            elif user_selection == "3":
                self.move_refugee_admin()
            elif user_selection == "4":
                self.admin_display_refugee()
            elif user_selection == "5":
                self.admin_refugee_export()
            elif user_selection == "R":
                break
            elif user_selection == "L":
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
        except FileNotFoundError as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    """ #################  CREATE / MODIFY / REMOVE CAMPS############### """
    @staticmethod
    def admin_data_visualization():
        ManagementView.data_visual_message()
        # AdminView.display_data_visual_menu()
        csv_path0 = Path(__file__).parents[0].joinpath("data/camp.csv")
        df0 = pd.read_csv(csv_path0)
        campList = df0['campID'].tolist()

        while True:
            AdminView.display_data_visual_menu()
            try:
                userInput = int(input("Please choose one option: "))
                if userInput not in range(1, 8):
                    print('Invalid Input, please try again')
                    continue
                else:
                    if userInput == 1:
                        camp_map = visualization_v.DataVisual()
                        camp_map.map()

                    elif userInput == 2:
                        c = num_camp
                        c.num_camp()

                    elif userInput == 3:
                        while True:
                            campId = int(input('Please enter a camp ID: '))
                            if campId not in campList:
                                print("Camp id doesn't exist")
                                continue
                            else:
                                gender = gender_distribution
                                gender.gender_pie_chart(campId)
                                break

                    elif userInput == 4:
                        while True:
                            campId = int(input('Please enter a camp ID: '))
                            if campId not in campList:
                                print("Camp id doesn't exist")
                                continue
                            else:
                                age1 = age_distribution
                                age1.age_bar_chart(campId)
                                print(3)
                                break

                    elif userInput == 5:
                        while True:
                            campId = int(input('Please enter a camp ID: '))
                            if campId not in campList:
                                print("Camp id doesn't exist")
                                continue
                            else:
                                r = resources_distribution
                                r.resources(campId)
                                break
                    elif userInput == 6:
                        while True:
                            campId = int(input('Please enter a camp ID: '))
                            if campId not in campList:
                                print("Camp id doesn't exist")
                                continue
                            else:
                                medical_info.medical_info(campId)
                                break
                    else:
                        return

            except ValueError as e:
                print("Invalid Input, please try again")
                logging.critical(f"{e}")


    @staticmethod
    def admin_create_camp():
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
                        eventID = input("\nEnter Event ID: ")

                        if eventID == 'RETURN':
                            return

                        if int(eventID) not in active_index:
                            print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")
                            continue
                        else:
                            camp_info = helper.validate_camp_input()
                            c = Camp(*camp_info[1:3])
                            c.pass_camp_info(int(eventID), camp_info[0])
                            print("\n\u2714 New camp created!")
                            return
                    except ValueError:
                        print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")
        except FileNotFoundError as e:
            print(f"\n File not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")
        except ValueError as e:
            print(f"\nInvalid user input.."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def admin_modify_camp():
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
            csv_path_a = Path(__file__).parents[0].joinpath("data/resourceAllocation.csv")
            df_a = pd.read_csv(csv_path_a)

            # if there is no active events, return
            # print the events info for users to choose
            filtered_df = df[(df['ongoing'] == 'True') | (df['ongoing'] == 'Yet')]
            campID_df = df0[['campID', 'eventID']].copy()
            campID_df['campID'] = campID_df['campID'].astype(str)
            campID_df = campID_df.groupby('eventID')['campID'].apply(lambda x: ', '.join(x.dropna())).reset_index()
            merged_df = pd.merge(filtered_df, campID_df, on='eventID', how='left')
            merged_df = merged_df.dropna(subset=['campID'])
            if filtered_df.empty:
                print("\nAll the events are closed and there's none to choose from.")
                return
            else:
                print("\n*The following shows the info of all available events*")
                Event.display_events(merged_df)

            while True:
                try:
                    eventID = input("\nEnter Event ID: ")

                    if eventID == 'RETURN':
                        return
                    eventID = int(eventID)

                    if eventID not in merged_df['eventID'].values:
                        print(f"Invalid input! Please enter an integer from {merged_df['eventID'].values} for Event ID.")
                        continue
                    break
                except ValueError as e:
                    print(f"Invalid input! Please enter an integer from {merged_df['eventID'].values} for Event ID.")
                    logging.critical(f"{e}")

            # print camps info for users to choose
            # df3 = helper.matched_rows_csv(csv_path0, "eventID", eventID, "campID")
            print("\n**The following shows the info of related camps*")
            filtered_df1 = df0[df0['eventID'] == eventID]
            filtered_campID = filtered_df1['campID'].tolist()
            Event.display_events(filtered_df1)

            while True:
                try:
                    modify_camp_id = input("\nWhich camp do you want to modify? Please enter campID: ")
                    if modify_camp_id == 'RETURN':
                        return
                    elif int(modify_camp_id) not in filtered_campID:
                        print(f"\nInvalid input! Please enter an integer from {filtered_campID} for Camp ID.")
                        continue
                    else:
                        break
                except ValueError as e:
                    print(f"\nInvalid input! Please enter an integer from {filtered_campID} for Camp ID.")
                    logging.critical(f"{e}")
                    continue

            while True:
                csv_path2 = Path(__file__).parents[0].joinpath("data/camp.csv")
                df2 = pd.read_csv(csv_path2)

                # Event.display_events(filtered_df1[filtered_df1['campID'] == modify_camp_id])
                Event.display_events(df2[(df2['campID'] == int(modify_camp_id)) & (df2['eventID'] == eventID)])
                selected_columns = ['campID', 'refugeeCapacity', 'healthRisk', 'status']
                filtered_df1 = filtered_df1[selected_columns]
                for i, column_name in enumerate(filtered_df1.columns[0:], start=1):
                    print(f"[{i}] {column_name}")
                try:
                    print("[R] QUIT editing")
                    target_column_index = input(f"Which column do you want to modify(1~4)? Or quit editing(R): ")

                    if target_column_index == 'RETURN' or target_column_index.lower() == 'r':
                        return
                    if int(target_column_index) not in range(1, 5) and str(target_column_index).lower() != 'r':
                        print("Please enter a valid integer from 1 to 4")
                        continue
                    elif int(target_column_index) in range(1, 5):

                        temp_id = int(modify_camp_id)

                        target_column_name = filtered_df1.columns[int(target_column_index) - 1]
                        while True:
                            new_value = input(f"Enter the new value for {target_column_name}: ")

                            if str(new_value) == 'RETURN':
                                return
                            # the ability to edit camp ID, but camp ID has to be unique

                            if target_column_index == '1':

                                camp_id_arr = [int(i) for i in df0['campID'].tolist()]

                                if int(new_value) in camp_id_arr:
                                    print("Camp ID already exists! Please choose a new one.")
                                    continue

                                # change corresponding refugee & volunteer & resource allocation camp ID
                                ref_id_arr = df_r.loc[df_r['campID'] == int(modify_camp_id)]['refugeeID'].tolist()
                                vol_id_arr = df_v.loc[df_v['campID'] == int(modify_camp_id)]['userID'].tolist()
                                res_id_arr = df_a.loc[df_a['campID'] == int(modify_camp_id)]['campID'].tolist()

                                for j in ref_id_arr:
                                    helper.modify_csv_pandas("data/refugee.csv", 'refugeeID',
                                                             int(j), 'campID', int(new_value))

                                for k in vol_id_arr:
                                    helper.modify_csv_pandas("data/user.csv", 'userID',
                                                             int(k), 'campID', int(new_value))

                                for m in res_id_arr:
                                    helper.modify_csv_pandas("data/resourceAllocation.csv", 'campID',
                                                             int(m), 'campID', int(new_value))

                                modify_camp_id = int(new_value)
                                break

                            if target_column_index == '3':

                                if new_value == "low" or new_value == "high":
                                    break
                                else:
                                    print("Invalid input! Please enter 'low' or 'high'")
                                    continue
                            elif target_column_index == '5':

                                if new_value == "open" or new_value == "closed":
                                    break
                                else:
                                    print("Invalid input! Please enter 'open' or 'closed'")
                                    continue
                            else:
                                try:

                                    new_value = int(new_value)
                                    if new_value >= 0:
                                        break
                                    else:
                                        print("Invalid input! Please enter a non-negative integer ")
                                        continue
                                except ValueError as e:
                                    print("Invalid input! Please enter a non-negative integer ")
                                    logging.critical(f"{e}")
                                    continue

                        helper.modify_csv_pandas(csv_path0, 'campID', temp_id, target_column_name,
                                                 new_value)
                        temp_id = modify_camp_id
                        csv_path_c = Path(__file__).parents[0].joinpath("data/camp.csv")
                        df_c = pd.read_csv(csv_path_c)

                        df_c.sort_values('campID', inplace=True)
                        df_c.to_csv(Path(__file__).parents[0].joinpath("data/camp.csv"), index=False)
                        print(f"\u2714 Changes have been saved!")
                    else:
                        return
                except ValueError as e:
                    print("Invalid input! Please enter an integer between 1 to 9")
                    logging.critical(f"{e}")
        except FileNotFoundError as e:
            print(f"\nMultiple files may be damaged or lost."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def admin_delete_camp():
        try:
            """This part of the code is to delete the camp from the camp.csv"""
            ManagementView.camp_deletion_message()

            event_csv_path = Path(__file__).parents[0].joinpath("data/event.csv")
            camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
            resource_allocation_csv_path = Path(__file__).parents[0].joinpath("data/resourceAllocation.csv")
            active_index = helper.extract_active_event(event_csv_path)[0]

            # if there is no active events, return
            if len(active_index) == 0:
                print("No relevant events to select from")
                return
            else:
                # print the events info for users to choose
                df = pd.read_csv(event_csv_path)
                df1 = pd.read_csv(camp_csv_path)
                filtered_df = df[(df['ongoing'] == 'True') | (df['ongoing'] == 'Yet')]
                campID_df = df1[['campID', 'eventID']].copy()
                campID_df['campID'] = campID_df['campID'].astype(str)
                campID_df = campID_df.groupby('eventID')['campID'].apply(lambda x: ', '.join(x.dropna())).reset_index()
                merged_df = pd.merge(filtered_df, campID_df, on='eventID', how='left')
                if filtered_df.empty:
                    print("\nAll the events are closed and there's none to choose from.")
                    return
                else:
                    print("\n*The following shows the info of all available events*")
                    Event.display_events(merged_df)

            # read camp csv file
            df1 = pd.read_csv(camp_csv_path)
            while True:
                try:
                    event_id = input("\nEnter Event ID: ")
                    if event_id == "RETURN":
                        return
                    event_id = int(event_id)
                    if event_id not in active_index:
                        print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")
                        continue
                    elif df1[df1['eventID'] == event_id].empty:
                        print("No relevant camps to select from")
                        return
                    elif event_id == 'RETURN':
                        return
                    break
                except ValueError as e:
                    print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")
                    logging.critical(f"{e}")

            filtered_camp_id = df1[df1['eventID'] == event_id]['campID'].tolist()
            df_resource = pd.read_csv(resource_allocation_csv_path)
            resource_camp_id_list = df_resource['campID'].tolist()
            print('The following shows the info of all camps from the event')
            Event.display_events(df1[df1['eventID'] == event_id])
            while True:
                try:
                    delete_camp_id = input("\nWhich camp do you want to delete? Please enter campID: ")
                    if delete_camp_id.upper() == "RETURN":
                        return
                    delete_camp_id = int(delete_camp_id)
                    if delete_camp_id not in filtered_camp_id:
                        print(f"Invalid input! Please enter an integer from {filtered_camp_id} for Camp ID. "
                              f"Or enter RETURN")
                        continue
                    elif delete_camp_id in resource_camp_id_list:
                        print(f"\nThere is allocated resource in camp {delete_camp_id}."
                              f"\nPlease transfer them before deleting the camp.")
                        continue
                    else:
                        print("\n*The following shows the info of the camp you have chosen*")
                        Event.display_events(df1[df1['campID'] == delete_camp_id])
                        break
                except ValueError as e:
                    print(f"Invalid input! Please enter an integer from {filtered_camp_id} for Camp ID.")
                    logging.critical(f"{e}")

            while True:
                aa = input(f"\nAre you sure to delete the camp {delete_camp_id}? (yes/no)\n"
                            f"Note: you'll also be deleting all associated refugees from the system and unassigning"
                           f" all volunteers from camp {delete_camp_id}: ")
                if aa == "yes":
                    # implement the deletion in csv file
                    df2 = df1[df1["campID"] != delete_camp_id]
                    df2.to_csv(camp_csv_path, index=False)
                    # --------- added logic to delete refugees in this camp -----------------
                    try:
                        refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
                        ref_df = pd.read_csv(refugee_csv_path)
                        logging.info("Refugee file successfully opened.")
                    except FileNotFoundError as e:
                        print("Oh no, the file didn't open. The camp has been deleted but you'll have to manually"
                              f" delete associated refugees from camp {delete_camp_id}. Let's take you back.\n\n")
                        logging.critical(f"File not found {e} when opening refugee file for deleting camp.")
                        return
                    refugees_in_camp = ref_df[ref_df['campID'] == delete_camp_id]
                    ref_df.drop(refugees_in_camp.index, inplace=True)
                    ref_df.reset_index(drop=True, inplace=True)
                    ref_df.to_csv(refugee_csv_path, index=False)
                    # keep track of existing camp num of a particular event
                    no_camp = df.loc[df['eventID'] == event_id][ "no_camp"].tolist()[0]
                    no_camp -= 1
                    index = df[df["eventID"] == event_id].index.tolist()
                    helper.modify_csv_value(event_csv_path, index[0], "no_camp", no_camp)
                    # ---------- added logic to unassign volunteers from this camp -------------
                    try:
                        user_csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
                        user_df = pd.read_csv(user_csv_path)
                        logging.info("User file loaded successfully for admin closing a camp.")
                    except FileNotFoundError as e:
                        print("Oh no, the file didn't open. The camp has been deleted but you'll have to manually"
                              f" unassign associated volunteers from camp {delete_camp_id}. Let's take you back.")
                        logging.critical(f"File not found {e} when opening user file for deleting camp.\n\n")
                        return
                    volunteers_in_camp = user_df[
                        (user_df['campID'] == delete_camp_id) & (user_df['userType'] == 'volunteer')]
                    volunteers_df_filtered = volunteers_in_camp.drop(columns=['password'])
                    print("\nBelow are the volunteers you are going to be unassigning from any camp in the system: ")
                    print(volunteers_df_filtered.to_markup)
                    for index, row in volunteers_in_camp.iterrows():
                        old_camp_id = row['campID']
                        row_index_old_camp = user_df[user_df['campID'] == old_camp_id].index
                        user_df.at[row_index_old_camp[0], 'campID'] = 0

                    user_df.to_csv(user_csv_path, index=False)
                    print("\n\u2714 You have Successfully deleted the camp, deleted its associated refugees "
                          f"and unassigned all volunteers from camp {delete_camp_id}!\n\n")
                    print("\n\u2714 You have Successfully deleted the camp!")
                    return
                elif aa == "no":
                    return
                elif aa == "RETURN":
                    return
                else:
                    print("Invalid input! Please enter 'yes' or 'no'")
                    continue
        except Exception as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def admin_close_camp():
        try:
            """This part of the code is to close the camp from the camp.csv"""
            ManagementView.camp_close_message()

            event_csv_path = Path(__file__).parents[0].joinpath("data/event.csv")
            camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
            resource_allocation_csv_path = Path(__file__).parents[0].joinpath("data/resourceAllocation.csv")
            active_index = helper.extract_active_event(event_csv_path)[0]

            # if there is no active events, return
            if len(active_index) == 0:
                print("\nNo relevant events to select from")
                return
            else:
                # print the events info for users to choose
                df = pd.read_csv(event_csv_path)
                df1 = pd.read_csv(camp_csv_path)
                filtered_df = df[(df['ongoing'] == 'True') | (df['ongoing'] == 'Yet')]
                campID_df = df1[['campID', 'eventID']].copy()
                campID_df['campID'] = campID_df['campID'].astype(str)
                campID_df = campID_df.groupby('eventID')['campID'].apply(lambda x: ', '.join(x.dropna())).reset_index()
                merged_df = pd.merge(filtered_df, campID_df, on='eventID', how='left')
                if filtered_df.empty:
                    print("\nAll the events are closed and there's none to choose from.")
                    return
                else:
                    print("\n*The following shows the info of all available events*")
                    Event.display_events(merged_df)

            # read camp csv file
            df1 = pd.read_csv(camp_csv_path)
            while True:
                try:
                    event_id = input("\nEnter Event ID: ")
                    if event_id == "RETURN":
                        return
                    event_id = int(event_id)
                    if event_id in active_index:
                        break
                    elif df1[df1['eventID'] == event_id].empty:
                        print("No relevant camps to select from")
                        return
                    else:
                        print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")
                        continue
                except ValueError as e:
                    print(f"Invalid input! Please enter an integer from {active_index} for Event ID.")
                    logging.critical(f"{e}")

            filtered_camp_id = df1[df1['eventID'] == event_id]['campID'].tolist()
            filtered_camp_id_int = [int(i) for i in filtered_camp_id]
            print('The following shows the info of all camps from the event')
            Event.display_events(df1[df1['eventID'] == event_id])
            while True:
                try:
                    close_camp_id = input("\nWhich camp do you want to close? Please enter campID: ")
                    if close_camp_id.upper() == "RETURN":
                        return
                    close_camp_id = int(close_camp_id)
                    if (df1.loc[df1['campID'] == close_camp_id, 'status'] == "closed").any():
                        print("\nThat camp is already closed! Don't worry. Let's go back.")
                        return
                    elif close_camp_id not in filtered_camp_id:
                        print(f"Invalid input! Please enter an integer from {filtered_camp_id} for Camp ID.")
                        continue
                    else:
                        print("\n*The following shows the info of the camp you have chosen*")
                        Event.display_events(df1[df1['campID'] == close_camp_id])
                        break
                except ValueError as e:
                    print(f"Invalid input! Please enter an integer from {filtered_camp_id} for Camp ID.")
                    logging.critical(f"{e}")

            while True:
                aa = input(f"\nAre you sure to close the camp {close_camp_id}? (yes/no)\n")
                if aa == "yes":
                    # close the camp
                    df1.loc[df1['campID'] == int(close_camp_id), 'status'] = "closed"
                    df1.to_csv(camp_csv_path, index=False)
                    print("\n\u2714 You have Successfully closed the camp!")
                    try:
                        user_csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
                        user_df = pd.read_csv(user_csv_path)
                        logging.info("User file loaded successfully for admin closing a camp.")
                        camps_in_event = df1.loc[df1['eventID'] == event_id, 'campID'].tolist()
                        volunteers_in_camp = user_df[(user_df['campID'] == close_camp_id) & (user_df['userType'] == 'volunteer')]
                        volunteers_df_filtered = volunteers_in_camp.drop(columns=['password'])
                        # volunteers_in_camp = user_df.loc[user_df['campID'] == close_camp_id, 'campID'].tolist()
                        print(
                            f"\nYou've closed camp {close_camp_id}. But now you might want to allocate the current volunteers "
                            f"to another camp in the same event. Or just leave them if preferred.")
                        move_volunteers = input("\n\nDo you want to move volunteers to another camp?"
                                                "\nEnter 'y' or 'n': ")
                        if move_volunteers.lower() == 'n':
                            break
                        elif move_volunteers.lower() == 'y':
                            if len(volunteers_in_camp) == 0:
                                print("Just checked - looks like there are no volunteers left in that camp, anyway. "
                                      "Redirecting you back now.")
                                return
                            print("Below are the volunteers in the camp: ")
                            print('\n\n', volunteers_df_filtered.to_markdown(index=False))

                            new_camp = input("\nFrom the list below, which are the camps in the same event as the one"
                                             "you have just closed, please enter which camp you want to move volunteers to: ")
                            print(filtered_camp_id)
                            if new_camp.lower() == 'return':
                                return
                            else:
                                try:
                                    new_camp = int(new_camp)
                                    break
                                except ValueError as e:
                                    logging.info(f"Error when user is selecting new camp to move volunteers to.")
                                    print("Oh no! R")
                    except Exception as e:
                        logging.critical(f"Error {e} when trying to display volunteers in camp when closing a camp.")
                        print(f"\nOh no. Error {e} has occurred. We'll take you back. The camp has still been closed "
                              f"but you'll have to manually remove volunteers.")
                    return
                elif aa == "no":
                    return
                elif aa == "RETURN":
                    return
                else:
                    print("Invalid input! Please enter 'yes' or 'no'")
                    continue
            while True:
                if new_camp in filtered_camp_id:
                    for index, row in volunteers_in_camp.iterrows():
                        old_camp_id = row['campID']
                        row_index_old_camp = user_df[user_df['campID'] == old_camp_id].index
                        user_df.at[row_index_old_camp[0], 'campID'] = new_camp
                        df1.loc[df1['campID'] == int(old_camp_id), 'volunteerPop'] -= 1
                        df1.loc[df1['campID'] == int(new_camp), 'volunteerPop'] += 1
                    df1.to_csv(camp_csv_path, index=False)
                    user_df.to_csv(user_csv_path, index=False)
                    print(f"Successfully assigned these volunteers to the new camp {new_camp}! See below: ")
                    print(df1[df1['campId'] == close_camp_id].to_markdown)
                    print(df1[df1['campID'] == new_camp].to_markdown)
                    break
                else:
                    print("Not a valid camp to choose from. Try again: ")
        except FileNotFoundError as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def admin_display_refugee():
        try:
            user = 'admin'
            ManagementView.display_admin_refugee()
            r = Refugee('', '', '', '', '', '', '',
                        '')
            r.display_info(user, 0)
        except FileNotFoundError as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def admin_display_camp():
        try:
            user = 'admin'
            ManagementView.display_admin_camp()
            c = Camp('', '')
            c.display_info(user, 0)
        except FileNotFoundError as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    """" ###################### RESOURCE MENU LEVEL 2 ############################################### """

    @staticmethod
    def resource_alloc_main_menu():

        # check for new camps
        resource_camp_instance = ResourceCampCreateDelete()
        resource_camp_instance.new_camp_resources_interface()

        # check for closed camps
        resource_camp_instance.closed_camp_resources_interface()

        # check for unallocated resources
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
            elif user_selection == 'RETURN':
                print("\nReturning you to main resource mgmt menu...")
                return
            else:
                print("Invalid mode option entered!")
                continue

            if user_selection == 'RETURN':
                return
            else:
                break

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

    @staticmethod
    def resource_reporting_menu():
        try:
            ManagementView.resource_report_message()
            resource_report = ResourceReport()
            while True:
                user_selection = input("--> \n: ")

                if user_selection == '1':
                    print("\nHere is the current snapshot of: \n> how resources are distributed across each camp; and"
                          "\n> the status and refugee population of each camp.\n")
                    table = resource_report.master_resource_stats()
                    table_pretty = resource_report.PRETTY_PIVOT_CAMP(table)
                    print(table_pretty.to_string(index=False).replace('.0', '  '))
                elif user_selection == '2':
                    unbalanced = resource_report.ALLOC_IDEAL_OUTPUT()  # if empty then other message
                    if unbalanced.empty:
                        print(
                            "\n＼(^o^)／ GOOD NEWS ＼(^o^)／ There are currently no unbalanced resources across any camps (that "
                            "deviate +/-10% of the ideal amounts).")
                    else:
                        print("Below are all the resource x camp pairs where the resource is unbalanced.\n")
                        print("A resource is considered unbalanced if: \n"
                              "...the current level falls outwith a +/-10% threshold of the ideal amount.\n")
                        print("The ideal amount is proportional to the refugee population\n(camp refugees /  "
                              "total refugees in open camps X total across all camps per resource)\n")
                        print(unbalanced.to_markdown(index=False))
                else:
                    print("Invalid mode option entered!")
                    continue

                if user_selection == 'RETURN':
                    return
                else:
                    break
        except FileNotFoundError as e:
            print(f"\nData file seems to be damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    """ ###################### RESOURCE MENU LEVEL 2 ############################################### """

    def volunteer_main(self):
        logging.info("login successfully as volunteer")
        # if volunteer is not assigned to a camp
        if self.user.camp_id == 0:
            while True:
                print("\n================================="
                      f"\n       Welcome Back {self.user.username}       "
                      "\n=================================")
                print("\nYou has not been assigned to any camp yet"
                      "\nPlease select a cmap below to join")
                input("\nPlease press Enter to see the camp list...")
                try:
                    camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
                    df_camp = pd.read_csv(camp_csv_path)
                    logging.info("successfully got info for camp csv file for volunteer joining a camp")
                    available_camp_index = helper.display_open_camp_list()
                except FileNotFoundError as e:
                    logging.critical(e)
                    print("Data file seems to be damaged"
                          "\nPlease contact admin for help"
                          "\n[Error]: {e}")
                    return
                # Force volunteer to join a camp
                try:
                    select_index = input("\nSelect a camp ID you would like to join: ")
                    if int(select_index) in available_camp_index:
                        user_csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
                        df_user = pd.read_csv(user_csv_path)
                        select_index = int(select_index)
                        self.user.camp_id = select_index
                        df_camp.loc[df_camp['campID'] == select_index, 'volunteerPop'] += 1
                        df_camp.to_csv(camp_csv_path, index=False)
                        df_user.loc[df_user['userID'] == self.user.user_id, 'campID'] = select_index
                        df_user.to_csv(user_csv_path, index=False)
                        logging.info(f"successfully add user into camp {select_index}")
                        print(f"You are successfully getting into camp {select_index}")
                        input("Please press Enter to continue...")
                        break
                    else:
                        print("invalid camp ID entered!")
                        continue
                except ValueError as e:
                    print("Camp ID must be an integer")
                    logging.warning("user input an invalid camp id"
                                    f"\n{e}")
        VolunteerView.display_login_message(self.user.username)
        while True:
            logging.info("volunteer main menu is displayed")
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
                self.user.show_account_info()
            # log out if user has selected "L" or self.logout_request is True
            if user_selection == "L" or self.logout_request is True:
                logging.info("logging out from volunteer main menu")
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
        return

    # join camp and change camp is the same thing, basically volunteer can change to a different camp after joining a
    # camp by selecting join/change camp in the menu
    def volunteer_join_camp(self):
        try:
            camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
            df_camp = pd.read_csv(camp_csv_path)
            logging.info("successfully got info for camp csv file for volunteer joining a camp")
            ManagementView.join_camp_message()
            available_camp_index = helper.display_open_camp_list()
        except FileNotFoundError as e:
            logging.critical(e)
            print("Data file seems to be damaged"
                  "\nPlease contact admin for help"
                  "\n[Error]: {e}")
            return
        old_camp_id = self.user.camp_id
        print(f"You're currently assigned to camp {int(old_camp_id)}.")

        while True:
            try:
                select_index = input("\nSelect a camp ID you would like to join: ")
                if select_index.upper() == 'RETURN':
                    return
                elif int(select_index) in available_camp_index:
                    user_csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
                    df_user = pd.read_csv(user_csv_path)
                    select_index = int(select_index)
                    self.user.camp_id = select_index
                    # camp volunteer population minus 1
                    df_camp.loc[df_camp['campID'] == old_camp_id, 'volunteerPop'] -= 1
                    df_camp.loc[df_camp['campID'] == select_index, 'volunteerPop'] += 1
                    df_camp.to_csv(camp_csv_path, index=False)
                    df_user.loc[df_user['userID'] == self.user.user_id, 'campID'] = select_index
                    df_user.to_csv(user_csv_path, index=False)
                    logging.info(f"successfully changed user input into {select_index} index")
                    print(f"You are successfully changed from camp {old_camp_id} to camp {select_index}")
                    return
                else:
                    print("invalid camp ID entered!")
                    continue
            except ValueError as e:
                print("Camp ID must be an integer")
                logging.warning("user input an invalid camp id"
                                f"\n{e}")

    def volunteer_edit_camp(self):
        try:
            user_id = self.user.user_id
            user_csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
            camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
            # active_index = helper.extract_active_event(camp_csv_path)[0]
            df = pd.read_csv(user_csv_path)
            dff = df[df['userID'] == int(user_id)]
            dfc = pd.read_csv(camp_csv_path)

            csv_path_a = Path(__file__).parents[0].joinpath("data/resourceAllocation.csv")
            df_a = pd.read_csv(csv_path_a)

            camp_id = dff.at[1, 'campID']
            event_id = dfc.loc[dfc['campID'] == int(camp_id)]['eventID'].tolist()[0]

            csv_path_r = Path(__file__).parents[0].joinpath("data/refugee.csv")
            df_r = pd.read_csv(csv_path_r)
        except FileNotFoundError as e:
            logging.critical("Not able to open camp file.")
            print(f"Oh no. We haven't been able to locate the file for this. \nError: {e}")
            return

        while True:
            try:
                csv_path2 = Path(__file__).parents[0].joinpath("data/camp.csv")
                df2 = pd.read_csv(csv_path2)
                logging.info("Camp file opened successfully.")
            except FileNotFoundError as e:
                logging.critical("Not able to open camp file.")
                print(f"Oh no. We haven't been able to locate the file for this. \nError: {e}")
                return
            # Event.display_events(filtered_df1[filtered_df1['campID'] == modify_camp_id])
            Event.display_events(df2[(df2['campID'] == camp_id) & (df2['eventID'] == event_id)])

            cid = helper.check_vol_assigned_camp(self.user.username)
            print(f"You're currently assigned to camp {int(cid)}.")

            df2 = df2.loc[:, df2.columns != 'eventID']
            df2 = df2.loc[:, df2.columns != 'countryID']

            camp_id_arr = [int(i) for i in df2['campID'].tolist()]

            for i, column_name in enumerate(df2.columns[0:], start=1):
                print(f"[{i}] {column_name}")
                logging.info("Successfully printed iteration in camp dataframe.")
            try:
                print("[R] QUIT editing")
                target_column_index = input(f"Which column do you want to modify(1~9)? Or quit editing(R): ")

                if target_column_index == 'RETURN' or target_column_index.lower() == 'r':
                    return
                if int(target_column_index) not in range(1, 10) and str(target_column_index).lower() != 'r':
                    print("Please enter a valid integer from 1 to 9")
                    continue
                elif int(target_column_index) in range(1, 10):
                    target_column_name = df2.columns[int(target_column_index) - 1]
                    while True:
                        new_value = input(f"Enter the new value for {target_column_name}: ")

                        if new_value == "RETURN":
                            return
                        # the ability to edit camp ID, but camp ID has to be unique
                        if target_column_index == '1':

                            if int(new_value) in camp_id_arr:
                                print("Camp ID already exists! Please choose a new one.")
                                continue

                            # change corresponding refugee & volunteer camp ID
                            ref_id_arr = df_r.loc[df_r['campID'] == int(camp_id)]['refugeeID'].tolist()
                            res_id_arr = df_a.loc[df_a['campID'] == int(camp_id)]['campID'].tolist()

                            for j in ref_id_arr:
                                helper.modify_csv_pandas("data/refugee.csv", 'refugeeID',
                                                         int(j), 'campID', int(new_value))
                            helper.modify_csv_pandas("data/user.csv", 'userID',
                                                     user_id, 'campID', int(new_value))
                            for k in res_id_arr:
                                helper.modify_csv_pandas("data/resourceAllocation.csv", 'campID',
                                                         int(k), 'campID', int(new_value))
                            new_value = int(new_value)

                        if target_column_index == '5':
                            if new_value == "low" or new_value == "high":
                                break
                            else:
                                print("Invalid input! Please enter 'low' or 'high'")
                        elif target_column_index == '9':
                            if new_value == "open" or new_value == "closed":
                                break
                            else:
                                print("Invalid input! Please enter 'open' or 'closed'")
                        elif target_column_index.lower() == 'r':
                            exit()
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
            except ValueError as e:
                print("Invalid input! Please enter an integer between 1 to 9")
                logging.critical(f"{e}")

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
                print("\n*The following shows the info of all available events*\n")
                t = df_c.to_markdown(index=False)
                print("\n" + t)

                while True:
                    try:
                        cid = int(input("Enter a camp ID: "))
                        if cid not in active_camp:
                            print("Invalid camp ID entered!")
                            continue
                        if cid == 'RETURN':
                            return

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
                    except ValueError as e:
                        print("Invalid camp ID entered!")
                        logging.critical(f"{e}")
                        continue
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
            self.volunteer_manage_camp()
        except FileNotFoundError as e:
            print(f"\nRefugee or camp data file may be damaged or lost."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def help_center():
        helper.help_center_page()

    def delete_refugee(self):
        print(
            "\nYOU ARE REQUESTING TO DELETE A REFUGEE. Enter RETURN if you didn't mean to select this. "
            "Otherwise, proceed as instructed.")
        try:
            refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
            ref_df = pd.read_csv(refugee_csv_path)
            logging.info("Refugee data file to delete a refugee from system loaded successfully.")
            user_csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
            user_df = pd.read_csv(user_csv_path)
            user_type = user_df.loc[user_df['username'] == self.user.username]['userType'].tolist()[0]
            logging.info("Users data file successfully loaded when needing to delete refugee. ")
            if user_type == 'volunteer':
                cid = helper.check_vol_assigned_camp(self.user.username)
                print(f"You're currently assigned to camp {int(cid)}.")

                cid = user_df.loc[user_df['username'] == self.user.username]['campID'].tolist()[0]
                print(f"\nREMEMBER: As a volunteer, you can only delete refugees from your own camp, "
                      f"which is {cid}...\n")
                refugees_in_camp = ref_df[ref_df['campID'] == int(cid)]
                if len(refugees_in_camp) == 0:
                    print("Looks like you aren't assigned to a camp yet. Contact admin!")
                    return
                while True:
                    Event.display_events(refugees_in_camp)
                    # print(refugees_in_camp.to_string(index=False))
                    rid = input(
                        "\nFrom the list above enter the refugee ID for the refugee you wish to remove from "
                        "the system: ")
                    if rid.lower() == "return":
                        return
                    try:
                        rid = int(rid)
                        if refugees_in_camp['refugeeID'].eq(rid).any():
                            break
                        else:
                            print("\nSorry - that refugee ID doesn't exist in your camp. Pick again.\n")
                    except Exception as e:
                        logging.info(f"Error {e} with volunteer user input when selecting refugee to delete.")
                        print(f"Oh no! Error {e}from invalid input! Please try again, with an integer.\n")

                print("\nBelow is the information about this refugee.")
                specific_refugee_row = ref_df[ref_df['refugeeID'] == int(rid)]
                # print("\n", specific_refugee_row.to_string(index=False))
                Event.display_events(specific_refugee_row)
                #     POP UP WINDOW TO CONFIRM USER WANTS TO DELETE REFUGEE (say it's irreversible?)
                #     root = tk.Tk()
                while True:
                    result = input("\nAre you sure you want to delete this refugee? Enter 'yes' or 'no': ")
                    # result = tk.messagebox.askquestion("Reminder", "Are you sure you want to delete this refugee?")
                    if result == "yes":
                        # Removing 1 from the population of the associated camp
                        camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
                        camp_df = pd.read_csv(camp_csv_path)
                        logging.info("Camp data file loaded successfully when deleting a refugee from the system.")
                        camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
                        row_index_camp = camp_df[camp_df['campID'] == camp_id].index
                        camp_df.at[row_index_camp[0], 'refugeePop'] -= 1
                        #     Deleting the refugee from the database
                        ref_df.drop(ref_df[ref_df['refugeeID'] == int(rid)].index, inplace=True)
                        ref_df.reset_index(drop=True, inplace=True)
                        ref_df.to_csv(refugee_csv_path, index=False)
                        print(
                            f"\nOkay. You have permanently deleted refugee #{rid} from the system. "
                            f"Their old associated camp population has also been adjusted accordingly.")
                        print("\nRefugee table after deletion:")
                        # print(ref_df.to_string(index=False))
                        Event.display_events(ref_df)
                        break
                    elif result == "no":
                        print("\nReturning back to previous menu.\n")
                        return
                    else:
                        print("\nInvalid input. Please enter 'yes' or 'no': ")
            else:
                # print(ref_df.to_string(index=False))
                Event.display_events(ref_df)
                # checking input is valid according to refugee IDs in database
                while True:
                    rid = input(
                        "\nFrom the list above enter the refugee ID for the refugee "
                        "you wish to remove from the system: ")
                    if rid == "RETURN":
                        return
                    elif rid.strip() and rid.strip().isdigit() and ref_df['refugeeID'].eq(int(rid)).any():
                        break
                    else:
                        print("\nSorry - that refugee ID doesn't exist. Pick again.")
                print("Below is the information about this refugee.")
                specific_refugee_row = ref_df[ref_df['refugeeID'] == int(rid)]
                print(specific_refugee_row.to_string(index=False))
                #     POP UP WINDOW TO CONFIRM USER WANTS TO DELETE REFUGEE (say it's irreversible?)
                #     root = tk.Tk()
                while True:
                    result = input("Are you sure you want to delete this refugee? Enter 'yes' or 'no': ")
                    # result = tk.messagebox.askquestion("Reminder", "Are you sure you want to delete this refugee?")
                    if result == "yes":
                        # Removing 1 from the population of the associated camp
                        camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
                        camp_df = pd.read_csv(camp_csv_path)
                        logging.info("Camp data file loaded successfully when deleting a refugee from the system.")
                        camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
                        row_index_camp = camp_df[camp_df['campID'] == camp_id].index
                        camp_df.at[row_index_camp[0], 'refugeePop'] -= 1
                        #     Deleting the refugee from the database
                        ref_df.drop(ref_df[ref_df['refugeeID'] == int(rid)].index, inplace=True)
                        ref_df.reset_index(drop=True, inplace=True)
                        ref_df.to_csv(refugee_csv_path, index=False)
                        print(
                            f"\nOkay. You have permanently deleted refugee #{rid} from the system. "
                            f"Their old associated camp population "
                            f"has also been adjusted accordingly.")
                        print("\nRefugee table after deletion:")
                        # print(ref_df.to_string(index=False))
                        Event.display_events(ref_df)
                        break
                    elif result == "no":
                        print("\nReturning back to previous menu.")
                        return
                    else:
                        print("\nInvalid input. Please enter 'yes' or 'no': ")
                #     tk.messagebox.showinfo("Cancel", "The operation to delete the refugee was canceled.")
                #     break
            # root.mainloop()
            # while True:
            #     user_input = input("Enter RETURN to exit back.")
            #     if user_input.lower() == "RETURN":
            #         return
            #     else:
            #         print("Invalid user entry. Please enter RETURN.")
        except FileNotFoundError as e:
            logging.critical(f"Error: {e}. One of the data files not found when deleting a refugee from system.")
            print(f"\nTraining session data file is not found or is damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n{e}")
        except Exception as e:
            logging.critical(f"Unexpected error: {e}")
            print(f"\nOne of the data files is not found or is damaged when deleting a refugee from the system."
                  f"\nPlease contact admin for further assistance."
                  f"\n{e}")

    def move_refugee_volunteer(self):
        cid = helper.check_vol_assigned_camp(self.user.username)
        while True:
            move_or_delete = input(
                f"\nYou're currently assigned to camp {int(cid)}."
                "\n------------------------------------------"
                "\nVolunteer: Moving & Deleting Refugees"
                "\n------------------------------------------"
                "\n As a volunteer, you can move refugees around within the same event, but you can only"
                " delete a refugee from the system if they are in the camp as that which you are assigned.\n"
                "\nPlease Enter one of the below options: "
                "\n[1] Move a refugee "
                "\n[2] Delete a refugee "
                "\n[3] Return back ")

            if move_or_delete == "3":
                return
            elif move_or_delete == "1":
                helper.move_refugee_helper_method()
            elif move_or_delete.lower() == "2":
                self.delete_refugee()
            else:
                print("Sorry! Didn't catch that. Please try again or enter [3] to exit.\n")

    def move_refugee_admin(self):
        while True:
            move_or_delete = input(
                "\n------------------------------------------"
                "\nAdmin: Moving & Deleting Refugees"
                "\n------------------------------------------"
                "\nPlease Enter one of the below options: "
                "\n[1] Move a refugee "
                "\n[2] Delete a refugee "
                "\n[3] Return back ")
            if move_or_delete == "3":
                return
            elif move_or_delete == "1":
                helper.move_refugee_helper_method()
            elif move_or_delete.lower() == "2":
                self.delete_refugee()
            else:
                print("Sorry! Didn't catch that. Please try again or enter [3] to exit.\n")

    @staticmethod
    def admin_refugee_export():
        print(
            "----------------------------------------------------------------------------------------------------------"
            "\nLooks like you want to print out a CSV record of all the refugees we have in the system across all "
            "camps.\n"
            "---------------------------------------------------------------------------------------------------------")
        helper.admin_export_refugees_to_csv()

    def legal_advice_support(self):
        while True:
            helper.legal_advice_support()
            return

    def refugee_training_sessions(self):
        cid = helper.check_vol_assigned_camp(self.user.username)
        while True:
            create_add_delete = input(
                f"\nYou're currently assigned to camp {int(cid)}."
                "\n------------------------------------------"
                "\nSkills & Training Sessions"
                "\n------------------------------------------"
                "\nPlease Enter one of the below options: "
                "\n[1] Create a session "
                "\n[2] Delete a session "
                "\n[3] Add a refugee to a session "
                "\n[4] Remove a refugee from a session "
                "\n[5] Display all sessions "
                "\n[R] Return back ")

            print(f"You're currently assigned to camp {int(cid)}.")

            if create_add_delete == 'R':
                return
            elif create_add_delete == '1':
                helper.create_training_session()
            elif create_add_delete == '2':
                helper.delete_session()
            elif create_add_delete == '3':
                helper.add_refugee_to_session()
            elif create_add_delete == '4':
                helper.remove_refugee_from_session()
            elif create_add_delete == '5':
                helper.display_training_session()
            else:
                print("\nSorry! Didn't catch that. Please try again or enter [R] to exit. ")

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
                        self.user.password = sha256_crypt.hash(new_password)
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
                          f"\nYour new email is '{self.user.email}'.")
                    break
                elif new_email in all_emails:
                    print("\nSorry, email is already linked to other account.")
                else:
                    print("Invalid email entered.\n"
                          "Only alphabet, numbers and !@#$%^&* are allowed.")
                    continue
        except Exception as e:
            print(f"\nInvalid user input."
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
                else:
                    try:
                        new_phone = int(new_phone)
                        break
                    except ValueError:
                        print("Invalid phone number entered. Only numbers are allowed.")
                        continue

            self.user.phone = new_phone
            # update the csv file
            self.user.update_phone()
            print("\nPhone changed successfully."
                  f"\nYour new phone is '{self.user.phone}")
        except ValueError as e:
            print(f"\nInvalid user input."
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
            print(f"\nInvalid user input."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    """ #### edit refugee for volunteer, volunteer camp dependent #### """

    def vol_edit_refugee(self, r):
        try:
            camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
            df_c = pd.read_csv(camp_csv_path)

            cid = helper.check_vol_assigned_camp(self.user.username)

            ref_pop = df_c.loc[df_c['campID'] == int(cid)]['refugeePop'].tolist()[0]
            user = 'volunteer'

            if ref_pop == 0:
                print("Currently there's no refugee in this camp.")

            ManagementView.refugee_edit_message()
            r.edit_refugee_info(user, cid)
            print(f"You're currently assigned to camp {int(cid)}.")
        except FileNotFoundError as e:
            print(f"\nInvalid user input."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    def vol_display_refugee(self, r):
        user = 'volunteer'
        cid = helper.check_vol_assigned_camp(self.user.username)
        csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        df = pd.read_csv(csv_path)

        if cid == 0:
            print("You're not assigned to a camp! Takinng you back.")
            return
        else:
            if df.loc[df['campID'] == cid]['refugeePop'].tolist()[0] == 0:
                print(f" No refugee(s) in camp {cid}.")
                return

        ManagementView.display_vol_refugee(cid)
        r.display_info(user, cid)
        print(f"You're currently assigned to camp {cid}.")

    def vol_display_camp(self, c):
        user = 'volunteer'
        cid = helper.check_vol_assigned_camp(self.user.username)
        ManagementView.display_vol_camp(cid)
        c.display_info(user, cid)
        print(f"You're currently assigned to camp {int(cid)}.")

    def display_camp_resource(self, c):
        cid = helper.check_vol_assigned_camp(self.user.username)
        ManagementView.display_camp_resource(cid)

        try:
            csv_path = Path(__file__).parents[0].joinpath("data/resourceAllocation.csv")
            df = pd.read_csv(csv_path)
            df = df.loc[df['campID'] == int(cid)]['campID'].tolist()[0]
            print(f"You're currently assigned to camp {int(cid)}.")
            c.display_resinfo(cid)
        except FileNotFoundError as e:
            print(f"\nData file is not found or is damaged."
                  f"\nPlease contact admin for further assistance."
                  f"\n{e}")
            logging.critical(f"{e}")
        except Exception as e:
            print(f"No resources have been allocated to camp {int(cid)} yet.")

    @staticmethod
    def vol_data_visualization(self):
        user_id = self.user.user_id
        user_csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
        # active_index = helper.extract_active_event(camp_csv_path)[0]
        df = pd.read_csv(user_csv_path)
        dff = df[df['userID'] == int(user_id)]
        # event_id = dff.at[1, 'eventID']
        camp_id = dff.at[1, 'campID']

        ManagementView.data_visual_message()
        # AdminView.display_data_visual_menu()

        while True:
            AdminView.display_data_visual_menu()
            try:
                userInput = int(input("Please choose one option: "))
                if userInput == 1:
                    camp_map = visualization_v.DataVisual()
                    camp_map.map()

                elif userInput == 2:
                    gender = gender_distribution
                    gender.gender_pie_chart(camp_id)

                elif userInput == 3:
                    age1 = age_distribution
                    age1.age_bar_chart(camp_id)

                elif userInput == 4:
                    r = resources_distribution
                    r.resources(camp_id)

                elif userInput == 5:
                    medical_info.medical_info(camp_id)

                else:
                    return

            except ValueError as e:
                print("Invalid Input, please try again")
                logging.critical(f"{e}")
