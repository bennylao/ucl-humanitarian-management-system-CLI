import re
import csv
from pathlib import Path
import pandas as pd
import datetime


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
    allowed_chars = r"[!@#$%^&*\w]"
    # specify allowed email format
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    # check for username
    while True:
        username = input("\nEnter username: ")
        if username == 'RETURN':
            return
        elif username in usernames:
            print("Sorry, username already exists.")
            continue
        elif username.isalnum():
            break
        else:
            print("Invalid username entered.")
            continue
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
            continue
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
            continue
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
            continue
    # check for email
    while True:
        email = input("\nEnter email: ")
        if email == 'RETURN':
            return
        elif re.fullmatch(email_format, email):
            break
        else:
            print("Invalid email entered.")
            continue
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
            continue
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
            continue

    return [username, password, first_name, last_name, email, phone, occupation]


def validate_event_input():
    country = []
    id_arr = []
    country_data = extract_data("data/countries.csv", "name")
    date_format = '%d/%m/%Y'  # Use for validating user entered date format

    for ele in country_data:
        country.append(ele.lower())
    # keep track of uid and increment it by 1
    try:
        I = extract_data("data/eventTesting.csv", "eid")
    except:
        I = '0'

    for i in I:
        id_arr.append(i)
    eid = 0
    if id_arr:
        eid = id_arr.pop()
    eid = int(eid) + 1

    while True:
        title = input("--> Plan title: ")
        if title == 'RETURN':
            return
        else:
            break

    while True:
        location = input("--> Location(country): ").lower()
        if location == 'RETURN':
            return
        elif location not in country:
            print("Invalid country name entered")
            continue
        else:
            break

    while True:
        description = input("--> Description: ")
        if description == 'RETURN':
            return
        else:
            break

    while True:
        try:
            start_date = input("--> Start date (format dd/mm/yy): ")
            if start_date == 'RETURN':
                return
            start_date = datetime.datetime.strptime(start_date, date_format)
            break
        except ValueError:
            print("Invalid date format entered.")
            continue

    # Maybe not every event has an known end date when it is created,
    # that's why we need an end_event() function to end it or modify its end date.
    while True:
        try:
            end_date = input("--> Estimated end date (format dd/mm/yy): ")
            if end_date == 'RETURN':
                return
            if end_date == 'None':
                end_date = None
                break
            end_date = datetime.datetime.strptime(end_date, date_format)
            if end_date <= start_date:
                print("End date has to be later than start date.")
                continue
            break
        except ValueError:
            print("Invalid date format entered.")
            continue

    return [title, location, description, start_date, end_date, eid]


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


def extract_data(csv, col):
    user_csv_path = Path(__file__).parents[0].joinpath(csv)
    df = pd.read_csv(user_csv_path)
    return df[col].tolist()
