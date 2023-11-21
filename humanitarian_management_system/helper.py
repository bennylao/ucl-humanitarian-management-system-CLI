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
    country_data = extract_data("data/countries.csv", "name")
    date_format = '%d/%m/%Y'  # Use for validating user entered date format

    for ele in country_data:
        country.append(ele.lower())
    # keep track of uid and increment it by 1
    try:
        id_arr = extract_data("data/eventTesting.csv", "eid").tolist()
    except:
        id_arr = '0'

    eid = 0
    if id_arr:
        eid = id_arr.pop()
    eid = int(eid) + 1

    while True:
        title = input("\nPlan title: ")
        if title == 'RETURN':
            return
        else:
            break

    while True:
        location = input("\nLocation(country): ").lower()
        if location == 'RETURN':
            return
        elif location not in country:
            print("Invalid country name entered")
            continue
        else:
            break

    while True:
        description = input("\nDescription: ")
        if description == 'RETURN':
            return
        else:
            break

    while True:
        try:
            no_camp = input("\nCamp Number (positive integers separated by commas): ")
            if no_camp == 'RETURN':
                return
            elif no_camp == 'NONE':
                no_camp = None
                break
            else:
                num_list = [int(num) for num in no_camp.split(',')]
                if all(num > 0 for num in num_list):
                    ## Also no_camp cannot exceed the total number of camps
                    ## Add it after camp.py finished.
                    num_list = sorted(set(num_list))
                    no_camp = ','.join(map(str, num_list))
                    break
                else:
                    print("\nInvalid camp number entered.")
                    continue
        except ValueError:
            print("\nInvalid camp number entered.")
            continue

    while True:
        try:
            start_date = input("\nStart date (format dd/mm/yy): ")
            if start_date == 'RETURN':
                return
            start_date = datetime.datetime.strptime(start_date, date_format)
            break
        except ValueError:
            print("\nInvalid date format entered.")
            continue

    while True:
        try:
            end_date = input("\nEstimated end date (format dd/mm/yy): ")
            if end_date == 'RETURN':
                return
            if end_date == 'NONE':
                end_date = None
                break
            end_date = datetime.datetime.strptime(end_date, date_format)
            if end_date <= start_date:
                print("\nEnd date has to be later than start date.")
                continue
            break
        except ValueError:
            print("\nInvalid date format entered.")
            continue

    return [title, location, description, no_camp, start_date, end_date, eid]


def validate_camp_input():
    try:
        id_arr = extract_data("data/camp.csv", "campID").tolist()
    except:
        id_arr = '0'

    campID = 0
    if id_arr:
        campID = id_arr.pop()
    campID = int(campID) + 1

    while True:
        capacity = input("\nCapacity: ")
        if capacity == 'RETURN':
            return
        elif not capacity.isnumeric():
            print("Must be a numerical input!")
            continue
        else:
            break

    while True:
        risk = input("\nHealth risk level(low or high): ")
        if capacity == 'RETURN':
            return
        elif risk != 'low' or risk != 'high':
            print("Must enter low or high")
            continue
        else:
            break

    return capacity, campID, risk


def validate_join():
    index = extract_data("data/roleType.csv", "roleID").tolist()
    role = extract_data("data/roleType.csv", "name")

    print("Please select a camp role by its index.")
    for i in index[1:]:
        print(f''' index: {i} | {role.iloc[i]} ''')
    while True:
        user_input = input("\nIndex: ")
        if int(user_input) not in index[1:]:
            print("Invalid index option entered!")
            continue
        if user_input == "RETURN":
            return
        else:
            break
    return user_input


def modify_csv_pandas(file_path, select_col, row_value, final_col, new_value):
    csv_path = Path(__file__).parents[0].joinpath(file_path)
    df = pd.read_csv(csv_path)
    i = df.index[df[select_col] == row_value].tolist()[0]
    modify_csv_value(csv_path, i, final_col, new_value)


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
    return df[col]


def extract_active_event():
    csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
    df = pd.read_csv(csv_path)
    # ensure we only display camp(s) that are part of an active plan
    data = extract_data("data/eventTesting.csv", ['ongoing', 'eid'])
    active_id = []

    for i in range(len(data)):
        if data['ongoing'].iloc[i]:
            active_id.append(data['eid'].iloc[i])

    return active_id, df


def display_camp_list():
    index = []

    active_id = extract_active_event()[0]
    df = extract_active_event()[1]
    csv_path = Path(__file__).parents[0].joinpath("data/eventTesting.csv")
    df_e = pd.read_csv(csv_path)

    if len(active_id) == 0:
        print("No relevant camps to select from")
        return

    for i in active_id:
        camp_id = df.loc[df['eventID'] == i]['campID'].tolist()
        for j in camp_id:
            capacity = df.loc[df['campID'] == j]['capacity'].tolist()[0]
            r_pop = df.loc[df['campID'] == j]['refugeePop'].tolist()[0]
            health_risk = df.loc[df['campID'] == j]['healthRisk'].tolist()[0]
            plan_title = df_e.loc[df_e['eid'] == i]['title'].tolist()[0]
            description = df_e.loc[df_e['eid'] == i]['description'].tolist()[0]
            location = df_e.loc[df_e['eid'] == i]['location'].tolist()[0]
            end_date = df_e.loc[df_e['eid'] == i]['endDate'].tolist()[0]
            index.append(j)

            print(f'''
                        * Index: {j}  | Health risk level: {health_risk} | Plan title: {plan_title} | description: {description} 
                        | location: {location} | Capacity: {capacity} | Refugee population: {r_pop} | End date: {end_date} * ''')

    return index
