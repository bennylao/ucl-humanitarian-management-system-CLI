class GeneralView:
    """
    This class contains all the messages that user might see before login.
    """

    startup_menu = (
        ("1", "Login"),
        ("2", "Register as a volunteer"),
        ("x", "Exit the system"),
        ("H", "Help Center")
    )

    @classmethod
    def display_startup_menu(cls):
        print("")
        for option, description in cls.startup_menu:
            print(f"[ {option} ] {description}")

    @classmethod
    def get_startup_options(cls):
        return [options[0] for options in cls.startup_menu]

    @staticmethod
    def display_startup_logo():
        print("\n==================================================\n"
              "     Group 11 Humanitarian Management System     \n"
              "==================================================")

    @staticmethod
    def display_welcome_message():
        print("\nWelcome to the Humanitarian Management System!")

    @staticmethod
    def display_login_message():
        print("\n==================================================\n"
              "          LOGIN PAGE\n"
              "==================================================\n"
              "Please enter your username and password.\n"
              "Or enter 'RETURN' to go back to main page.")

    @staticmethod
    def display_registration_message():
        print("\n========================================\n"
              "        USER REGISTRATION\n"
              "========================================\n"
              "Please fill in all the following information below.\n"
              "Or enter 'RETURN' to go back to main page.")
