import helper
import volunteer
from admin import Admin


def main():
    """This is the function that will run the app."""
    start_up_logo = ("========================================\n"
                     "Group 11 Humanitarian Management System\n"
                     "========================================\n")
    # Possible menu options for the interface
    menu_optionsA = ("[ 1 ] Login\n"
                     "[ 2 ] Register as a volunteer\n"
                     "[ x ] Exit the system")
    menu_optionsB = ("[ 1 ] Admin\n"
                     "[ 2 ] Volunteer\n"
                     "[ 3 ] Return to main menu\n"
                     "[ x ] Exit the system")
    admin_menu = ("[ 1 ] Create humanitarian plan\n"
                  "[ 2 ] Edit volunteer account\n"
                  "[ 3 ] Edit humanitarian plan\n"
                  "[ 4 ] Activate/deactivate user account\n"
                  "[ 5 ] Return to previous page\n"
                  "[ x ] Exit the system")
    vol_menu = ("[ 1 ] Create refugee profile\n"
                "[ 2 ] Edit personal account\n"
                "[ 3 ] Edit camp profile\n"
                "[ 4 ] Edit refugee profile\n"
                "[ 5 ] Return to previous page\n"
                "[ x ] Exit the system")

    print(start_up_logo)
    print("Welcome to the Humanitarian Management System!")
    print(menu_optionsA + "\n")

    # Initialise register variables for Volunteer
    user_enter = '-1'
    option_arr = ['1', '2', 'x']

    firstName, lastName, userName, occupation = '', '', '', ''
    phone = '-1'
    password = ''
    confirmPassword = '-2'

    # Give error if inappropriate option keyword is entered
    while user_enter not in option_arr:
        user_enter = input("--> ")
        if user_enter not in option_arr:
            print("Invalid option entered.")

    if user_enter == '1':
        helper.login_page(menu_optionsB, option_arr, firstName, lastName, userName, phone, password, occupation)

    elif user_enter == '2':

        helper.reg_validate(firstName, lastName, userName, occupation, phone, password, confirmPassword)
        main()

    elif user_enter == '3':
        exit()


if __name__ == "__main__":
    # Initialise the creation of the default admin account upon starting the app
    A = Admin('admin', '111', '07786471235')
    A.default_account()
    main()


