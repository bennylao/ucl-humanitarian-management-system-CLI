class AdminView:
    admin_menu = {
        "1": "Create humanitarian plan",
        "2": "Add camp",
        "3": "Edit volunteer account",
        "4": "Edit humanitarian plan",
        "5": "Activate/deactivate user account",
        "6": "Display plan info",
        "7": "Return to previous page",
        "x": "Exit the system"
    }

    @classmethod
    def display_admin_menu(cls):
        print("")
        for key, value in cls.admin_menu.items():
            print(f"[ {key} ] {value}")

    @classmethod
    def get_admin_options(cls):
        return cls.admin_menu.keys()
