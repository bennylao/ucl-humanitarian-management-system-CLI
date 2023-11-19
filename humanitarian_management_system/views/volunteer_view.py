class VolunteerView:
    vol_menu = {
        "1": "Create refugee profile",
        "2": "Join camp",
        "3": "Edit personal account",
        "4": "Edit camp profile",
        "5": "Edit refugee profile",
        "6": "Return to previous page",
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
