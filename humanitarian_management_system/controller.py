from humanitarian_management_system.models import User, Volunteer, Event
from humanitarian_management_system.views import StartupView, InstructionView, LoginView, AdminView, VolunteerView
from humanitarian_management_system import helper


class Controller:
    def __init__(self):
        self.session = "startup"

    def initialise(self):
        StartupView.display_startup_logo()
        StartupView.display_welcome_message()
        self.startup()

    def startup(self):
        StartupView.display_startup_menu()
        user_selection = helper.validate_user_selection(StartupView.get_startup_options())
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
        username = input("--> Username: ")
        password = input("--> Password: ")
        is_login_valid = User.validate_user(username, password)
        # redirect based on validation
        if is_login_valid:
            AdminView.display_admin_menu()
            user_selection = helper.validate_user_selection(AdminView.get_admin_options())

            if user_selection == "1":
                self.create_event()
            if user_selection == "2":
                pass
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
            print("Invalid username or password! Or the account has been disabled!")
            Controller.login(self)

    def register(self):
        self.session = "register"
        InstructionView.display_registration_message()
        usernames = User.get_all_usernames()
        registration_info = helper.validate_registration(usernames)
        if registration_info is not None:
            v = Volunteer(registration_info[0], registration_info[1], registration_info[2], registration_info[3],
                          registration_info[4], registration_info[5], registration_info[6])
            v.pass_data()
            print("User created.")

        else:
            self.startup()

    def create_event(self):
        InstructionView.event_creation_message()
        event_info = helper.validate_event_input()
        if event_info is not None:
            e = Event(event_info[0], event_info[1], event_info[2], event_info[3], event_info[4], event_info[5])
            e.pass_event_info()
            print("Event created.")
        else:
            self.startup()
