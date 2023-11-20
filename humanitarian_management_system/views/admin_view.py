class AdminView:
    admin_menu = {
        "1": "Create humanitarian plan",
        "2": "Camp management",
        "3": "Volunteer account management",
        "4": "Edit humanitarian plan",
        "5": "Add resources stock",
        "6": "Display events",
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


class CampView:
    camp_menu = {
        "1": "Add camp",
        "2": "Resources allocation",
        "3": "Edit camp",
        "4": "Return to previous page",
        "x": "Exit the system"
    }

    @classmethod
    def display_camp_menu(cls):
        print("")
        for key, value in cls.camp_menu.items():
            print(f"[ {key} ] {value}")

    @classmethod
    def get_camp_options(cls):
        return cls.camp_menu.keys()


class VolView:
    vol_menu = {
        "1": "Edit volunteer profile",
        "2": "Activate volunteer",
        "3": "Disable volunteer",
        "4": "Return to previous page",
        "x": "Exit the system"
    }

    @classmethod
    def display_vol_menu(cls):
        print("")
        for key, value in cls.vol_menu.items():
            print(f"[ {key} ] {value}")

    @classmethod
    def get_vol_options(cls):
        return cls.vol_menu.keys()
