class VolunteerView:

    vol_menu = {
        "1": "Join/change camp",
        "2": "Edit personal account",
        "3": "Camp management",
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

class CampViewV:
    camp_menu = {
        "1": "Add refugee",
        "2": "Edit camp profile",
        "3": "Return to previous page",
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



