class AdminView:
    """
    This class contains all the messages that admin might see.
    """

    main_menu = (
        ("1", "Humanitarian Plan Management"),
        ("2", "Camp Management"),
        ("3", "Volunteer Account Management"),
        ("4", "Resource Management"),
        ("5", "Display Summary/Statistics"), # ben: idk what exactly this will be, it depends on what Yuan can do
        ("6", "Edit Account Settings and Personal Information"),
        ("L", "Logout")
    )

    manage_event_menu = (
        ("1", "Create new event"),
        ("2", "Edit event"),
        ("3", "Remove event"),
        ("4", "Display all events"),
        ("R", "Return to previous page"),
        ("L", "Logout")
    )

    manage_camp_menu = (
        ("1", "Add new camp"),
        ("2", "Edit camp"),
        ("3", "Remove camp"),
        ("4", "Resources allocation"),
        ("5", "Add refugees"),
        ("6", "Move/remove refugee(s)"),
        ("7", "Display all camps"),
        ("R", "Return to previous page"),
        ("L", "Logout")
    )

    manage_volunteer_menu = (
        ("1", "Edit volunteer profile"),
        ("2", "Deactivate/reactivate volunteer"),
        ("3", "Remove volunteer"),
        ("R", "Return to previous page"),
        ("L", "Logout")
    )

    manage_resource_menu = (
        ("1", "Add resource"),
        # ben: idk what else we can have. jessica please add this
        ("R", "Return to previous page"),
        ("L", "Logout")
    )

    manage_account_menu = (
        ("1", "Change Username"),
        ("2", "Change Password"),
        ("3", "Change Name"),
        ("4", "Change Email"),
        ("5", "Change Phone Number"),
        ("6", "Change Occupation"),
        ("R", "Return to previous page"),
        ("L", "Logout")
    )

    @staticmethod
    def admin_login_message():
        print("\n========================================\n"
              "           Welcome back ADMIN\n"
              "========================================\n"
              "Please select an option from the following.")

    @classmethod
    def display_menu(cls):
        print("")
        for key, value in cls.main_menu:
            print(f"[ {key} ] {value}")

    @classmethod
    def get_main_options(cls):
        return [options[0] for options in cls.main_menu]

    @classmethod
    def display_event_menu(cls):
        print("")
        for key, value in cls.manage_event_menu:
            print(f"[ {key} ] {value}")

    @classmethod
    def get_event_options(cls):
        return [options[0] for options in cls.manage_event_menu]

    @classmethod
    def display_camp_menu(cls):
        print("")
        for key, value in cls.manage_camp_menu:
            print(f"[ {key} ] {value}")

    @classmethod
    def get_camp_options(cls):
        return [options[0] for options in cls.manage_camp_menu]

    @classmethod
    def display_volunteer_menu(cls):
        print("")
        for key, value in cls.manage_volunteer_menu:
            print(f"[ {key} ] {value}")

    @classmethod
    def get_volunteer_options(cls):
        return [options[0] for options in cls.manage_volunteer_menu]

    @classmethod
    def display_resource_menu(cls):
        print("")
        for key, value in cls.manage_resource_menu:
            print(f"[ {key} ] {value}")

    @classmethod
    def get_resource_options(cls):
        return [options[0] for options in cls.manage_resource_menu]

    @classmethod
    def display_account_menu(cls):
        print("")
        for key, value in cls.manage_account_menu:
            print(f"[ {key} ] {value}")

    @classmethod
    def get_account_options(cls):
        return [options[0] for options in cls.manage_account_menu]
