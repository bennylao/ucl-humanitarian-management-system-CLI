class VolunteerView:
    """
    This class contains all the messages that volunteer might see.
    """

    main_menu = (
        ("1", "Join/Change Camp"),
        ("2", "Camp Management"),
        ("3", "Edit Account Information"),
        ("4", "View Account Information"),
        ("5", "Open MessageBox"),
        ("L", "Logout")
    )

    manage_camp_menu = (
        ("1", "Add refugee"),
        ("2", "Edit refugee"),
        ("3", "Move/remove refugee(s)"),
        ("4", "Edit camp profile"),
        ("5", "Display refugees information"),
        ("6", "Display camp information"),
        ("7", "Display camp resources"),
        ("8", "Legal Advice Services"),
        ("9", "Refugee Skills Sessions Management"),
        ("10", "Camp/Refugee data visualization"),
        ("R", "Return to previous page"),
        ("L", "Logout")
    )

    change_refugee_menu = (
        ("1", "Change First name"),
        ("2", "Change Last name"),
        ("3", "Change DOB"),
        ("4", "Change Gender"),
        ("5", "Change Family ID"),
        ("R", "Return to previous page"),
    )

    @staticmethod
    def display_login_message(username):
        print("\n========================================\n"
              f"         Welcome back {username}\n"
              "========================================\n"
              "Please select an option from the following.")

    @classmethod
    def display_main_menu(cls):
        print("\n===== Volunteer Main Menu =====")
        for key, value in cls.main_menu:
            print(f"[ {key} ] {value}")

    @classmethod
    def get_main_options(cls):
        return [options[0] for options in cls.main_menu]

    @classmethod
    def display_camp_menu(cls):
        print("")
        for key, value in cls.manage_camp_menu:
            print(f"[ {key} ] {value}")

    @classmethod
    def get_camp_options(cls):
        return [options[0] for options in cls.manage_camp_menu]

    @classmethod
    def display_edit_refugee_menu(cls):
        print("")
        for key, value in cls.change_refugee_menu:
            print(f"[ {key} ] {value}")

    @classmethod
    def get_edit_refugee_options(cls):
        return [options[0] for options in cls.change_refugee_menu]
