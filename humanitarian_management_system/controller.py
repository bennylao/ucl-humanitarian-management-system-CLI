from .models import User
from .views import StartupView, RegistrationView, LoginView, AdminView, VolunteerView
from . import helper


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

    def register(self):
        self.session = "register"
        RegistrationView.display_registration_message()
        usernames = User.get_all_usernames()
        registration_info = helper.validate_registration(usernames)
        if registration_info is not None:
            print("create User")
            print(registration_info)
        else:
            self.startup()
