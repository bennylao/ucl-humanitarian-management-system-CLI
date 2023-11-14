import helper
import event
from admin import Admin


def main():
    """This is the function that will run the app."""
    start_up_logo = ("========================================\n"
                     "Group 11 Humanitarian Management System\n"
                     "========================================\n")
    event.Event.update_ongoing()  # update 'ongoing' in event csv file
    # Possible menu options for the interface
    menu_optionsA = ("[ 1 ] Login\n"
                     "[ 2 ] Register as a volunteer\n"
                     "[ x ] Exit the system")
    menu_optionsB = ("[ 1 ] Admin\n"
                     "[ 2 ] Volunteer\n"
                     "[ 3 ] Return to main menu\n"
                     "[ x ] Exit the system")

    admin_menu = ("[ 1 ] Create humanitarian plan\n"
                  "[ 2 ] End an event\n"
                  "[ 3 ] Add camp\n"
                  "[ 4 ] Edit volunteer account\n"
                  "[ 5 ] Edit humanitarian plan\n"
                  "[ 6 ] Activate/deactivate user account\n"
                  "[ 7 ] Display plan info\n"
                  "[ 8 ] Return to previous page\n"
                  "[ x ] Exit the system")
    vol_menu = ("[ 1 ] Create refugee profile\n"
                "[ 2 ] Join camp\n"
                "[ 3 ] Edit personal account\n"
                "[ 4 ] Edit camp profile\n"
                "[ 5 ] Edit refugee profile\n"
                "[ 6 ] Return to previous page\n"
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
    user_enter = helper.option_valid(user_enter, option_arr)

    if user_enter == '1':
        helper.login_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
                          password, occupation)

    elif user_enter == '2':

        helper.reg_validate(firstName, lastName, userName, occupation, phone, password, confirmPassword)
        main()

    elif user_enter == '3':
        exit()


if __name__ == "__main__":
    # Initialise the creation of the default admin account upon starting the app
    A = Admin('admin', '111', 'xxxxxxxxxxx')
    A.default_account()
    main()


