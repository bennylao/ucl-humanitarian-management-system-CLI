class ManagementView:
    """
    This class contains all the messages that shared between volunteer and admin after login.
    """

    admin_manage_account_menu = (
        ("1", "Change Username"),
        ("2", "Change Password"),
        ("3", "Change Name"),
        ("4", "Change Email"),
        ("5", "Change Phone Number"),
        ("6", "Change Occupation"),
        ("R", "Return to previous page"),
        ("L", "Logout")
    )

    volunteer_manage_account_menu = (
        ("1", "Change Username"),
        ("2", "Change Password"),
        ("3", "Change Name"),
        ("4", "Change Email"),
        ("5", "Change Phone Number"),
        ("6", "Change Occupation"),
        ("7", "Change Role"),
        ("R", "Return to previous page"),
        ("L", "Logout")
    )

    @classmethod
    def admin_display_account_menu(cls):
        print("\n===== Account Edit Menu =====")
        for key, value in cls.admin_manage_account_menu:
            print(f"[ {key} ] {value}")

    @classmethod
    def admin_get_account_options(cls):
        return [options[0] for options in cls.admin_manage_account_menu]

    @classmethod
    def volunteer_display_account_menu(cls):
        print("\n===== Account Edit Menu =====")
        for key, value in cls.volunteer_manage_account_menu:
            print(f"[ {key} ] {value}")

    @classmethod
    def volunteer_get_account_options(cls):
        return [options[0] for options in cls.volunteer_manage_account_menu]

    @staticmethod
    def display_summary_message():
        print("\n========================================\n"
              "                 SUMMARY\n"
              "========================================\n"
              "More detailed information, please refer to the corresponding menu.")

    @staticmethod
    def event_creation_message():
        print("\n========================================\n"
              "              Event CREATION\n"
              "========================================\n"
              "Please fill in all the following information below.\n"
              "The end date is optional. Enter 'NONE' to skip for now.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def event_edit_message():
        print("\n========================================\n"
              "             Event MODIFICATION\n"
              "========================================\n"
              "Please fill in all the following information below.\n"
              "The end date is optional. Enter 'NONE' to skip for now.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def event_close_message():
        print("\n========================================\n"
              "               Event CLOSE\n"
              "========================================\n"
              "Please fill in all the following information below.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def event_delete_message():
        print("\n========================================\n"
              "               Event DELETION\n"
              "========================================\n"
              "Please fill in all the following information below.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def camp_main_message():
        print("\n========================================\n"
              "           Camp MANAGEMENT\n"
              "========================================\n"
              "Please select an option from the following.")

    @staticmethod
    def camp_init_message():
        print("\n========================================\n"
              "            Event CREATION\n"
              "========================================\n"
              "Please select a plan by its index.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def camp_creation_message():
        print("\n========================================\n"
              "             Camp CREATION\n"
              "========================================\n"
              "Please fill in all the following information below.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def camp_modification_message():
        print("\n========================================\n"
              "             Camp MODIFICATION\n"
              "========================================\n"
              "Please fill in all the following information below.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def camp_deletion_message():
        print("\n========================================\n"
              "             Camp DELETION\n"
              "========================================\n"
              "Please fill in all the following information below.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def camp_close_message():
        print("\n========================================\n"
              "             Camp CLOSURE\n"
              "========================================\n"
              "Please fill in all the following information below.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def vol_main_message():
        print("\n========================================\n"
              "      Volunteer account MANAGEMENT\n"
              "========================================\n"
              "Please select an option from the following.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def resource_alloc_main_message():
        print("\n==========================================================\n"
              "\n✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ [ 4.1 ] RESOURCE ALLOCATION ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n"
              "\n==========================================================\n"
              "[ 1 ] Manual    - user select one by one \n"
              "[ 2 ] Automatic - all camps rebalanced based on refugee count\n\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def man_resource_message():
        print("\n========================================\n"
              "         Allocating manually\n"
              "========================================\n"
              "Please select a camp by its index.\n"
              "Follow by the index of the resource type.\n"
              "And finally the amount you want.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def auto_resource_message():
        print("\n========================================\n"
              "       Allocating automatically\n"
              "========================================\n"
              "Please select a camp by its index.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def resource_report_message():
        print("""\n==========================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ [ 4.3 ] RESOURCE STATS VIEWER ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
==========================================================================\n
[1] View all resource stats \n
[2] View only unbalanced resources\n """)

    @staticmethod
    def join_camp_message():
        print("\n========================================\n"
              "            Join/change CAMP\n"
              "========================================\n"
              "Please select a camp by its index to join\n"
              "Or to change your current camp to that instead.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def create_refugee_message():
        print("\n========================================\n"
              "            Refugee CREATION\n"
              "========================================\n"
              "Please fill in all the following information below.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def refugee_edit_message():
        print("\n========================================\n"
              "               Refugee EDIT\n"
              "========================================\n"
              "Please fill in all the following information below.\n"
              "Or enter 'RETURN' to go back to admin menu page.")

    @staticmethod
    def display_admin_refugee():
        print("\n========================================\n"
              "       All refugee information \n"
              "==========================================")

    @staticmethod
    def display_vol_refugee(cid):
        print("\n========================================\n"
              f"     Refugee information in camp {int(cid)} \n"
              "==========================================")

    @staticmethod
    def display_admin_camp():
        print("\n==========================================\n"
              "        All camp information \n"
              "==========================================")

    @staticmethod
    def display_vol_camp(cid):
        print("\n==========================================\n"
              f"        Camp {int(cid)} information \n"
              "==========================================")

    @staticmethod
    def display_camp_resource(cid):
        print("\n==========================================\n"
              f"     Camp {int(cid)} resources information \n"
              "==========================================")

    @staticmethod
    def display_admin_vol():
        print("\n==========================================\n"
              "         All volunteer information \n"
              "==========================================")

    @staticmethod
    def display_activate():
        print("\n==========================================\n"
              "   Activate/deactivate volunteer accounts \n"
              "==========================================")

    @staticmethod
    def data_visual_message():
        print("\n==========================================\n"
              "           Data Visualization \n"
              "==========================================")

    @staticmethod
    def messageBox():
        print("\n==========================================\n"
              "          Welcome to Message Box \n"
              "==========================================")

