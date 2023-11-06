# A place for possible helper functions?
# I think it's better and easier to manage to have one csv file for each table for our database
from volunteer import Volunteer
import main


def reg_validate(firstName, lastName, userName, occupation, phone, password, confirmPassword):
    """ A very basic validation of user entered values """
    while len(firstName) == 0:
        firstName = input("First name: ")
    while len(lastName) == 0:
        lastName = input("Last name: ")

    # Check if username already exists
    V = Volunteer(firstName, lastName, userName, phone, password, occupation)
    U = V.read_data(V)
    while len(userName) == 0:
        userName = input("User name: ")
        for ele in U[0]:
            if userName == ele:
                print("Sorry, username already exists.")
                userName = ''
                continue

    while len(occupation) == 0:
        occupation = input("User occupation: ")
    while len(phone) != 11:
        phone = input("Phone number: ")
        if len(phone) != 11:
            print("Number must be of length 11.")
    while len(password) == 0:
        password = input("Password: ")
    while len(password) != len(confirmPassword):
        confirmPassword = input("Confirm password: ")
        if len(password) != len(confirmPassword):
            print("Password does not match!")

    # Pass user enter values to Volunteer class as they're ready to be stored into .csv file
    V = Volunteer(firstName, lastName, userName, phone, password, occupation)
    V.pass_data()
    print("An account has been successfully created!")


def login_page(menu_optionsB, option_arr, firstName, lastName, userName, phone, password, occupation):
    """ Display login page menu options...work in progress """
    V = Volunteer(firstName, lastName, userName, phone, password, occupation)
    U = V.read_data(V)
    user, pwd = '', ''

    # fetch username and password values from .csv file and assign them here
    tmpA, tmpB = [], []
    for i in U[0]:
        tmpA.append(i)
    for j in U[1]:
        tmpB.append(j)

    print(menu_optionsB + "\n")
    user_enter = '-1'
    option_arr.append('3')
    while user_enter not in option_arr:
        user_enter = input("--> ")
        if user_enter not in option_arr:
            print("Invalid option entered.")

        if user_enter == '1':
            while len(user) == 0 or len(pwd) == 0:
                # check if admin login info match the data that was fetched from the .csv file
                user = input("--> Username: ")
                pwd = input("--> Password: ")
                if user not in tmpA or pwd not in str(tmpB):
                    print("Incorrect username/password, or account does not exist.")
                    user, pwd = '', ''
                    continue

        elif user_enter == '2':
            while len(user) == 0 or len(pwd) == 0:
                # check if volunteer login info match the data that was fetched from the .csv file
                user = input("--> Username: ")
                pwd = input("--> Password: ")
                if user not in tmpA or pwd not in str(tmpB):
                    print("Incorrect username/password, or account does not exist.")
                    user, pwd = '', ''
                    continue

        elif user_enter == '3':
            main.main()


def admin_page():
    pass
