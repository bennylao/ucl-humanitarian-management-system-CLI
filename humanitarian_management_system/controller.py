from humanitarian_management_system.helper import (extract_data, validate_event_input, validate_registration,
                                                   validate_user_selection, validate_camp_input)
from humanitarian_management_system.models import User, Volunteer, Event, Camp
from humanitarian_management_system.views import (StartupView, InstructionView, LoginView, AdminView, CampView,
                                                  VolunteerView)
from pathlib import Path
import pandas as pd


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
        # redirect based on validation
        while is_login_valid:
            if t[0] == 'admin':
                AdminView.display_admin_menu()
                user_selection = validate_user_selection(AdminView.get_admin_options())

                if user_selection == "1":
                    self.create_event()
                if user_selection == "2":
                    self.camp_main()
                if user_selection == "3":
                    pass
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
                    pass
                if user_selection == "2":
                    pass
                if user_selection == "3":
                    pass
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
            e = Event(event_info[0], event_info[1], event_info[2], event_info[3], event_info[4])
            e.pass_event_info(event_info[5])
            print("Event created.")
        else:
            self.startup()

    @staticmethod
    def edit_event():
        InstructionView.event_edit_message()
        df = pd.read_csv('data/eventTesting.csv')
        if df.empty:
            print("\nNo events to edit.")
        else:
            e = Event('','','','','')
            e.edit_event_info()

    def camp_main(self):
        InstructionView.camp_main_message()
        CampView.display_camp_menu()
        user_selection = validate_user_selection(CampView.get_camp_options())
        if user_selection == "1":
            self.create_camp()
        if user_selection == "2":
            pass
        if user_selection == "3":
            pass
        if user_selection == "4":
            pass
        if user_selection == "x":
            exit()

    def create_camp(self):
        InstructionView.camp_init_message()
        # print out selection list, perhaps someone could improve its presentation, coz i'm really bad at this :P
        # only display active event(s) to user
        data_arr = extract_data("data/eventTesting.csv", "ongoing")
        active_index = []

        for i in range(len(data_arr)):
            if data_arr[i]:
                active_index.append(i)

        for i in active_index:
            id = extract_data("data/eventTesting.csv", 'eid').iloc[i]
            title = extract_data("data/eventTesting.csv", 'title').iloc[i]
            location = extract_data("data/eventTesting.csv", 'location').iloc[i]
            description = extract_data("data/eventTesting.csv", 'description').iloc[i]
            endDate = extract_data("data/eventTesting.csv", 'endDate').iloc[i]

            print(f'''
            | {id}  | {title}| {location} | {description} | {endDate} |
            ''')
        # validate input for user select index
        while True:
            select_index = int(input("\nindex: "))
            if (select_index - 1) not in active_index:
                print("Invalid index entered!")
                continue
            else:
                break
        InstructionView.camp_creation_message()
        # prompt for user capacity input
        camp_info = validate_camp_input()
        if camp_info is not None:
            c = Camp('', '', camp_info[0])
            c.pass_camp_info(select_index, camp_info[1])
            print("Camp created.")
        else:
            self.startup()
