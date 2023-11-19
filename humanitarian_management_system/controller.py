from humanitarian_management_system.helper import (extract_data, validate_event_input, validate_registration,
                                                   validate_user_selection, validate_camp_input)
from humanitarian_management_system.models import User, Volunteer, Event, Camp
from humanitarian_management_system.views import StartupView, InstructionView, LoginView, AdminView, VolunteerView


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
            # exit()
            pass

    def login(self):
        self.session = "login"
        LoginView.display_login_message()
        username = input("\nUsername: ")
        password = input("\nPassword: ")
        is_login_valid = User.validate_user(username, password)
        # redirect based on validation
        self.login_success(is_login_valid)

    def login_success(self, is_login_valid):
        if is_login_valid:
            AdminView.display_admin_menu()
            user_selection = validate_user_selection(AdminView.get_admin_options())

            if user_selection == "1":
                self.create_event()
            if user_selection == "2":
                self.create_camp()
            if user_selection == "3":
                pass
            if user_selection == "4":
                pass
            if user_selection == "5":
                pass
            if user_selection == "6":
                pass
            if user_selection == "x":
                # exit()
                pass
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

    def create_camp(self):
        InstructionView.camp_init_message()
        # print out selection list, perhaps someone could improve its presentation, coz i'm really bad at this :P
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
