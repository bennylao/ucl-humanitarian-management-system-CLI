# A place for possible helper functions?
# I think it's better and easier to manage to have one csv file for each table for our database
import pandas as pd
import re
import csv


def validate_user_selection(options):
    while True:
        selection = input("--> ")
        if selection in options:
            break
        else:
            print("Invalid option entered.")
    return selection


def validate_registration(usernames):
    # specify allowed characters for username
    allowed_chars = "[!@#$%^&*\w]"
    # specify allowed email format
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    # check for username
    while True:
        username = input("\nEnter username: ")
        if username == 'RETURN':
            return
        elif username in usernames:
            print("Sorry, username already exists.")
        elif username.isalnum():
            break
        else:
            print("Invalid username entered.")
    # check for password
    while True:
        password = input("\nEnter password: ")
        if password == 'RETURN':
            return
        elif re.match(allowed_chars, password):
            break
        else:
            print("Invalid password entered.\n"
                  "Only alphabet, numbers and !@#$%^&* are allowed.")
    # check for first name
    while True:
        first_name = input("\nEnter first name: ")
        if first_name == 'RETURN':
            return
        elif first_name.replace(" ", "").isalpha():
            break
        else:
            print("Invalid first name entered.\n"
                  "Only alphabet are allowed.")
    # check for last name
    while True:
        last_name = input("\nEnter last name: ")
        if last_name == 'RETURN':
            return
        elif last_name.replace(" ", "").isalpha():
            break
        else:
            print("Invalid last name entered.\n"
                  "Only alphabet are allowed.")
    # check for email
    while True:
        email = input("\nEnter email: ")
        if email == 'RETURN':
            return
        elif re.fullmatch(email_format, email):
            break
        else:
            print("Invalid email entered.")
    # check for phone
    while True:
        phone = input("\nEnter phone number: ")
        if phone == 'RETURN':
            return
        elif phone.isnumeric():
            break
        else:
            print("Invalid phone number entered.\n"
                  "Only numbers are allowed.")
    # check for occupation
    while True:
        occupation = input("\nEnter occupation: ")
        if occupation == 'RETURN':
            return
        elif occupation.replace(" ", "").isalpha():
            break
        else:
            print("Invalid occupation entered.\n"
                  "Only alphabet are allowed.")

    return [username, password, first_name, last_name, email, phone, occupation]


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
