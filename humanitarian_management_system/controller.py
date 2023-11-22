from humanitarian_management_system.helper import (extract_data, validate_event_input, validate_registration,
                                                   validate_user_selection, validate_camp_input, extract_active_event,
                                                   display_camp_list, validate_join, extract_data_df, validate_refugee,
                                                   validate_man_resource, matched_rows_csv)
from humanitarian_management_system.models import User, Volunteer, Event, Camp, ResourceTest, Refugee
from humanitarian_management_system.views import (StartupView, InstructionView, LoginView, AdminView, CampView,
                                                  VolunteerView, VolView, CampViewV)
from pathlib import Path
import pandas as pd
import math


class Controller:
    def __init__(self):
        self.session = "startup"

    def initialise(self):
        StartupView.display_startup_logo()
        StartupView.display_welcome_message()
        self.startup()

    def startup(self):
        StartupView.display_startup_menu()
        user_selection = validate_user_selection(StartupView.get_startup_options())
        if user_selection == "1":
            self.login()
        if user_selection == "2":
            self.register()
        if user_selection == "x":
            exit()

    def login(self):
        self.session = "login"
        LoginView.display_login_message()
        username = input("\nUsername: ")
        if username == 'RETURN':
            self.startup()
        password = input("\nPassword: ")
        if username == 'RETURN':
            self.startup()
        is_login_valid = User.validate_user(username, password)

        # checking usertype
        user_csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path)
        i = df.index[df['username'] == username].tolist()
        t = df.iloc[i]['userType'].tolist()
        # redirect based on validation and usertype - admin or volunteer
        while is_login_valid:
            if t[0] == 'admin':
                AdminView.display_admin_menu()
                user_selection = validate_user_selection(AdminView.get_admin_options())

                if user_selection == "1":
                    self.create_event()
                if user_selection == "2":
                    self.camp_main()
                if user_selection == "3":
                    self.vol_man()
                if user_selection == "4":
                    self.edit_event()
                if user_selection == "5":
                    pass
                if user_selection == "6":
                    pass
                if user_selection == "7":
                    self.startup()
                if user_selection == "x":
                    exit()

            else:
                VolunteerView.display_vol_menu()
                user_selection = validate_user_selection(VolunteerView.get_vol_options())
                if user_selection == "1":
                    self.join_camp(username)
                if user_selection == "2":
                    pass
                if user_selection == "3":
                    self.camp_man(username)
                if user_selection == "4":
                    pass
                if user_selection == "5":
                    pass
                if user_selection == "6":
                    self.startup()
                if user_selection == "x":
                    exit()

        else:
            print("Invalid username or password!\n"
                  "Or the account has been disabled!")
            Controller.login(self)

    def register(self):
        self.session = "register"
        InstructionView.display_registration_message()
        usernames = User.get_all_usernames()
        registration_info = validate_registration(usernames)
        if registration_info is not None:
            v = Volunteer(registration_info[0], registration_info[1], registration_info[2], registration_info[3],
                          registration_info[4], registration_info[5], registration_info[6])
            v.pass_data()
            print("User created.")

        else:
            self.startup()

    def create_event(self):
        InstructionView.event_creation_message()
        event_info = validate_event_input()
        if event_info is not None:
            e = Event(event_info[0], event_info[1], event_info[2], event_info[3], event_info[4], event_info[5])
            e.pass_event_info(event_info[6])
            print("Event created.")
        else:
            return

    @staticmethod
    def edit_event():
        InstructionView.event_edit_message()
        Event.edit_event_info()

    def camp_main(self):
        InstructionView.camp_main_message()
        CampView.display_camp_menu()
        user_selection = validate_user_selection(CampView.get_camp_options())
        if user_selection == "1":
            self.create_camp()

        if user_selection == "2":
            self.delete_camp()

        if user_selection == "3":
            pass
            # self.edit_camp()

        if user_selection == "4":
            self.resource_main()

        if user_selection == "5":
            return
        if user_selection == "x":
            exit()

    # camp management for admin
    def create_camp(self):
        InstructionView.camp_creation_message()
        active_index = extract_active_event()[0]

        # check if active event is 0
        if len(active_index) == 0:
            print("No relevant events to select from.")
            return
        else:
            # read the event csv file and extract all available events
            csv_path = Path(__file__).parents[0].joinpath("data/eventTesting.csv")
            df1 = matched_rows_csv(csv_path, "ongoing", True, "eid")
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

        InstructionView.camp_creation_message()
        # prompt for user capacity input
        camp_info = validate_camp_input()
        if camp_info is not None:
            c = Camp(camp_info[0], camp_info[2], '')
            c.pass_camp_info(eventID, camp_info[1])
            print("Camp created.")
        else:
            self.startup()

    def delete_camp(self):
        """This part of the code is to delete the camp from the camp.csv"""
        InstructionView.camp_deletion_message()
        active_index = extract_active_event()[0]

        # if there is no active events, return
        if len(active_index) == 0:
            print("No relevant events to select from")
            return
        else:
            # print the events info for users to choose
            csv_path = Path(__file__).parents[0].joinpath("data/eventTesting.csv")
            df1 = matched_rows_csv(csv_path, "ongoing", True, "eid")
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
            df2 = matched_rows_csv(csv_path2, "eventID", eventID, "campID")
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





    def resource_main(self):
        InstructionView.resource_main_message()
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
        InstructionView.man_resource_message()
        index = display_camp_list()
        res_man_info = validate_man_resource(index)

        if res_man_info is not None:
            r = ResourceTest(res_man_info[0], '', '')
            r.manual_resource(res_man_info[2], res_man_info[1])
            print("Resource allocated as request.")
        else:
            return

    def auto_resource(self):
        InstructionView.auto_resource_message()
        index = display_camp_list()

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

        df = extract_active_event()[1]
        select_pop = df.loc[df['campID'] == select_index]['refugeePop'].tolist()[0]

        r = ResourceTest(select_index, select_pop, 0)
        r.calculate_resource()
        print("Auto resource allocation completed")

    def join_camp(self, username):
        csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        df = pd.read_csv(csv_path)

        InstructionView.join_camp_message()
        index = display_camp_list()

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
        join_info = validate_join()
        if join_info is not None:
            v = Volunteer(username, '', '', '', '', '', '', join_info)
            v.join_camp(event_id, select_index)
        return

    # camp management for volunteer
    def camp_man(self, username):
        InstructionView.camp_main_message()
        CampViewV.display_camp_menu()

        user_selection = validate_user_selection(CampViewV.get_camp_options())
        if user_selection == '1':
            self.add_refugee(username)
        if user_selection == '2':
            pass
        if user_selection == '3':
            return
        if user_selection == 'x':
            exit()

    def add_refugee(self, username):
        df = extract_data_df("data/user.csv")
        cid = df.loc[df['username'] == username]['campID'].tolist()[0]
        # check if volunteer user already join a camp
        if math.isnan(cid):
            print("You must first join a camp!")
            return
        print(f'''\nYou're currently assigned to camp {int(cid)}.''', end='')
        InstructionView.create_refugee_message()
        df_c = extract_data_df("data/camp.csv")
        # health risk level of volunteer's camp
        lvl = df_c.loc[df_c['campID'] == cid]['healthRisk'].tolist()[0]

        refugee_info = validate_refugee(lvl)
        if refugee_info is not None:
            r = Refugee(refugee_info[0], refugee_info[1], refugee_info[2], refugee_info[3], refugee_info[4],
                        refugee_info[5], refugee_info[6], refugee_info[7])
            r.add_refugee_from_user_input(cid)
        else:
            return
        print("Refugee created.")

    def vol_man(self):
        InstructionView.vol_main_message()
        VolView.display_vol_menu()
        return

