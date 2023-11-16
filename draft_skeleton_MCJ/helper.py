# A place for possible helper functions?
# I think it's better and easier to manage to have one csv file for each table for our database
from volunteer import Volunteer
from event import Event
import pandas as pd
import main
import csv

def reg_validate(firstName, lastName, userName, occupation, phone, password, confirmPassword):
    """ A very basic validation of user entered values """
    while len(firstName) == 0:
        firstName = input("First name: ")
        if firstName == 'RETURN':
            main.main()
    while len(lastName) == 0:
        lastName = input("Last name: ")
        if lastName == 'RETURN':
            main.main()

    # Check if username already exists
    try:
        U = extract_data("data/userTesting.csv")['userName']
    except:
        U = ''

    # By entering the keyword 'RETURN' user can exit the current session and return to the previous page
    while len(userName) == 0:
        userName = input("User name: ")
        if userName == 'RETURN':
            main.main()

        for ele in U[0]:
            if userName == ele:
                print("Sorry, username already exists.")
                userName = ''
                continue

    while len(occupation) == 0:
        occupation = input("User occupation: ")
        if occupation == 'RETURN':
            main.main()

    while len(phone) != 11:
        phone = input("Phone number: ")
        if phone == 'RETURN':
            main.main()

        if len(phone) != 11:
            print("Phone number must be of length 11.")
        if not phone.isnumeric():
            print("Must be numeric.")
            phone = '-1'
            continue

    while len(password) == 0:
        password = input("Password: ")
        if password == 'RETURN':
            main.main()

    while len(password) != len(confirmPassword):
        confirmPassword = input("Confirm password: ")
        if confirmPassword == 'RETURN':
            main.main()

        if len(password) != len(confirmPassword):
            print("Password does not match!")

    # Pass user enter values to Volunteer class as they're ready to be stored into .csv file
    V = Volunteer(firstName, lastName, userName, phone, password, occupation)
    V.pass_data()
    print("An account has been successfully created!")


def login_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
               password, occupation):
    """ Display login page menu options...work in progress """
    V = Volunteer(firstName, lastName, userName, phone, password, occupation)
    user, pwd = '', ''
    arr = ['4', '5', '6']
    login = False  # keep track of if user has login successfully

    # fetch username and password values from .csv file and assign them here

    try:
        U1 = extract_data("data/userTesting.csv")['userName']
        U2 = extract_data("data/userTesting.csv")['password']
    except:
        U1, U2 = '', ''

    tmpA, tmpB = [], []
    tmpA.extend(U1)
    tmpB.extend(U2)

    print(menu_optionsB + "\n")
    user_enter = '-1'
    option_arr.append('3')
    user_enter = option_valid(user_enter, option_arr)

    if user_enter == '1':
        while len(user) == 0 or len(pwd) == 0:
            # check if admin login info match the data that was fetched from the .csv file
            user = input("--> Username: ")
            # By entering the keyword 'RETURN' user can exit the current session and return to the previous page
            if user == 'RETURN':
                login_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
                           password, occupation)

            pwd = input("--> Password: ")
            if pwd == 'RETURN':
                login_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
                           password, occupation)

            if user not in tmpA or pwd not in str(tmpB):
                print("Incorrect username/password, or account does not exist.")
                user, pwd = '', ''
                continue
            login = True
        if login:
            print("You have login successfully!")
            admin_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
                       password, occupation, arr)

    elif user_enter == '2':

        while len(user) == 0 or len(pwd) == 0:
            # check if volunteer login info match the data that was fetched from the .csv file
            user = input("--> Username: ")
            # By entering the keyword 'RETURN' user can exit the current session and return to the previous page
            if user == 'RETURN':
                login_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
                           password, occupation)

            # extract user active status from .csv by entered userName
            pos = ''
            cnt = -1
            df = pd.read_csv('data/userTesting.csv')
            for ele in tmpA:
                cnt += 1
                if user == ele:
                    pos = cnt
                    status = df.at[df.index[pos], 'active']
                    if not status:
                        print("Sorry, your account has been disabled.")
                        login_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName,
                                   phone, password, occupation)

            pwd = input("--> Password: ")
            # By entering the keyword 'RETURN' user can exit the current session and return to the previous page
            if pwd == 'RETURN':
                login_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
                           password, occupation)

            if user not in tmpA or pwd not in str(tmpB):
                print("Incorrect username/password, or account does not exist.")
                user, pwd = '', ''
                continue

            login = True
        if login:
            print("You have login successfully!")
            vol_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
                     password, occupation, arr)

    elif user_enter == '3':
        main.main()
    else:
        exit()


def admin_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
               password, occupation, arr):
    option_arr.extend(arr)
    option_arr.append('7')

    user_enter = -1
    print(admin_menu)
    user_enter = option_valid(user_enter, option_arr)

    title, location, description, start_date, end_date = '', '', '', '', ''
    E = Event(title, location, description, start_date, end_date)

    if user_enter == '1':
        E.pass_event_info()
        admin_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
                   password, occupation, arr)
    elif user_enter == '2':
        pass
    elif user_enter == '3':
        pass
    elif user_enter == '4':
        E.edit_event_info()
        admin_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
                   password, occupation, arr)
    elif user_enter == '5':
        pass
    elif user_enter == '6':
        pass
    elif user_enter == '7':
        login_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
                   password, occupation)
    else:
        exit()


def vol_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
             password, occupation, arr):
    option_arr.extend(arr)

    user_enter = -1
    print(vol_menu)
    user_enter = option_valid(user_enter, option_arr)

    if user_enter == '1':
        pass
    elif user_enter == '2':
        pass
    elif user_enter == '3':
        pass
    elif user_enter == '4':
        pass
    elif user_enter == '5':
        pass
    elif user_enter == '6':
        login_page(menu_optionsB, admin_menu, vol_menu, option_arr, firstName, lastName, userName, phone,
                   password, occupation)
    else:
        exit()


# Validating user entered option keyword
def option_valid(user_enter, option_arr):
    while user_enter not in option_arr:
        user_enter = input("--> ")
        if user_enter not in option_arr:
            print("Invalid option entered.")
    return user_enter


def extract_data(file_path):
    df = pd.read_csv(file_path)
    return df


def modify_csv_value(file_path, row_index, column_name, new_value):
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    rows[row_index][column_name] = new_value
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)