class StartupView:
    startup_menu = {
        "1": "Login",
        "2": "Register as a volunteer",
        "x": "Exit the system"
    }

    @staticmethod
    def display_startup_logo():
        print("\n==================================================\n"
              "     Group 11 Humanitarian Management System     \n"
              "==================================================")

    @staticmethod
    def display_welcome_message():
        print("\nWelcome to the Humanitarian Management System!")

    @classmethod
    def display_startup_menu(cls):
        print("")
        for key, value in cls.startup_menu.items():
            print(f"[ {key} ] {value}")

    @classmethod
    def get_startup_options(cls):
        return cls.startup_menu.keys()
