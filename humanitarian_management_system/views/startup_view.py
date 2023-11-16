class StartupView:
    startup_options = {
        "1": "Login",
        "2": "Register as a volunteer",
        "x": "Exit the system"
    }

    @staticmethod
    def display_startup_logo():
        print("\n========================================\n"
              "     Group 11 Humanitarian Management System     \n"
              "========================================")

    @staticmethod
    def display_welcome_message():
        print("\nWelcome to the Humanitarian Management System!")


    @classmethod
    def display_startup_menu(cls):
        for key, value in cls.startup_options.items():
            print(f"[ {key} ] {value}")

    @classmethod
    def get_startup_options(cls):
        return cls.startup_options.keys()
