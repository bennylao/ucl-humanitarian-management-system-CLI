import re
import csv
from pathlib import Path
import pandas as pd
import datetime
import tkinter as tk
import tkinter.messagebox
import numpy as np


def validate_user_selection(options):
    while True:
        selection = input("--> ")
        if selection in options:
            break
        else:
            print("Invalid option entered.")
    return selection


def validate_registration(usernames):
    # specify allowed characters for passwords
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
        elif username.isalnum():
            break
        else:
            print("Invalid username entered. Only alphabet letter (a-z) and numbers (0-9) are allowed.")
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
            # remove extra whitespaces between words in first name
            # for example: "  Chon   Hou  " -> "Chon Hou"
            first_name = ' '.join(first_name.split())
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
            # remove extra whitespaces between words in last name
            last_name = ' '.join(last_name.split())
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

    return ["volunteer", "TRUE", username, password, first_name, last_name, email, phone, occupation, 0, 0, 0]


def validate_event_input():
    countries_csv_path = Path(__file__).parent.joinpath("data/country.csv")
    all_countries = pd.read_csv(countries_csv_path)['name'].tolist()

    date_format = '%d/%m/%Y'  # Use for validating user entered date format
    while True:
        title = input("\nPlan title: ")
        if title == 'RETURN':
            return
        else:
            break

    while True:
        location = input("\nLocation(country): ").title()
        if location == 'RETURN':
            return
        elif location not in all_countries:
            print("Invalid country name entered.")
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
        start_date = input("\nStart date (format dd/mm/yyyy): ")
        if start_date == 'RETURN':
            return
        try:
            start_date = datetime.datetime.strptime(start_date, date_format)
            break
        except ValueError:
            print("\nInvalid date format entered.")
            continue

    while True:
        end_date = input("\nEstimated end date (format dd/mm/yyyy): ")
        if end_date == 'RETURN':
            return
        elif end_date == 'NONE':
            end_date = None
            break
        try:
            end_date = datetime.datetime.strptime(end_date, date_format)
            if end_date <= start_date:
                print("\nEnd date has to be later than start date.")
                continue
            elif end_date <= datetime.datetime.today():
                print("\nEnd date has to be later than today.")
                continue
            break
        except ValueError:
            print("\nInvalid date format entered.")
            continue

    if ((end_date == None and start_date.date() <= datetime.date.today())
            or (start_date.date() <= datetime.date.today() and end_date.date() >= datetime.date.today())):
        ongoing = True
    elif start_date.date() > datetime.date.today():
        ongoing = 'Yet'
    else:
        ongoing = False

    return [ongoing, title, location, description, 0, start_date, end_date]


def validate_camp_input():
    try:
        csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        id_arr = extract_data(csv_path, "campID").tolist()
    except:
        id_arr = ['0']

    campID = 0
    if id_arr:
        campID = id_arr.pop()
    campID = int(campID) + 1

    # capacity input
    while True:
        try:
            capacity = input("\nEnter capacity: ")
            if capacity == "RETURN":
                break
            elif int(capacity) > 0:
                break
            else:
                print("Must be a positive integer!")
                continue
        except ValueError:
            print("Must be a positive integer!!")

    # while True:
    #     try:
    #         resource = input("\nEnter resources amount: ")
    #         if capacity == "RETURN":
    #             break
    #         elif int(resource) > 0:
    #             break
    #         else:
    #             print("Must be a positive integer!")
    #             continue
    #     except ValueError:
    #         print("Must be a positive integer!!")

    # risk input
    while True:
        risk = input("\nEnter health risk level (low or high): ")
        if risk == 'RETURN':
            return
        elif (risk != 'low') and (risk != 'high'):
            print("Must enter low or high")
            continue
        else:
            break

    return campID, capacity, risk


def validate_join():  # volunteer joining a camp
    index = extract_data("data/roleType.csv", "roleID").tolist()
    role = extract_data("data/roleType.csv", "name")

    print("Please select a camp role by its index.")
    for i in index:
        print(f''' index: {i} | {role.iloc[i - 1]} ''')
    while True:
        user_input = input("\nEnter index: ")
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


def matched_rows_csv(file, desired_column, desired_value, index):
    """used to extract rows with specific value in a specific column"""
    df = pd.read_csv(file)
    if desired_column in df.columns.tolist():
        if desired_value in df[desired_column].tolist():
            dff = df[df[desired_column] == desired_value].set_index(index)
            dff_sorted = dff.sort_index()
            return [dff_sorted, dff_sorted.index.tolist()]
        else:
            return f"Value '{desired_value}' not found in the {desired_column}."
    else:
        return f"Column '{desired_column}' not found in the CSV file."


def extract_data(csv_path, col):
    df = pd.read_csv(csv_path)
    return df[col]


def extract_data_df(csv_path):
    df = pd.read_csv(csv_path)
    return df


def extract_active_event(csv_path):
    df = pd.read_csv(csv_path)
    # ensure we only display camp(s) that are part of an active plan
    data = extract_data(csv_path, ['ongoing', 'eid'])
    active_id = []

    for i in range(len(data)):
        if data['ongoing'].iloc[i] == 'True' or data['ongoing'].iloc[i] == 'Yet':
            active_id.append(data['eid'].iloc[i])

    return active_id, df


def display_camp_list():
    index = []

    csv_path = Path(__file__).parents[0].joinpath("data/eventTesting.csv")
    active_id = extract_active_event(csv_path)[0]
    df_e = pd.read_csv(csv_path)

    csv_path_c = Path(__file__).parents[0].joinpath("data/camp.csv")
    df_c = extract_data_df(csv_path_c)

    if len(active_id) == 0:
        print("No relevant camps to select from")
        return

    for i in active_id:
        camp_id = df_c.loc[df_c['eventID'] == i]['campID'].tolist()
        for j in camp_id:
            capacity = df_c.loc[df_c['campID'] == j]['refugeeCapacity'].tolist()[0]
            r_pop = df_c.loc[df_c['campID'] == j]['refugeePop'].tolist()[0]
            health_risk = df_c.loc[df_c['campID'] == j]['healthRisk'].tolist()[0]
            plan_title = df_e.loc[df_e['eid'] == i]['title'].tolist()[0]
            description = df_e.loc[df_e['eid'] == i]['description'].tolist()[0]
            location = df_e.loc[df_e['eid'] == i]['location'].tolist()[0]
            end_date = df_e.loc[df_e['eid'] == i]['endDate'].tolist()[0]
            index.append(j)

            print(f'''
                * Index: {j}  | Health risk level: {health_risk} | Plan title: {plan_title} | description: {description} 
                | location: {location} | Capacity: {capacity} | Refugee population: {r_pop} | End date: {end_date} * ''')

    return index


def validate_man_resource(index):
    df = extract_data_df("data/resourceStock.csv")
    while True:
        select_index = int(input("\nEnter camp index: "))

        if select_index not in index:
            print("invalid index option entered!")
            continue
        try:
            if select_index == 'RETURN':
                return
        except:
            return
        break

    res_id = extract_data("data/resourceStock.csv", "resourceID").tolist()
    # display medical condition option list
    for i in res_id:
        name = df.loc[df['resourceID'] == i]['name'].tolist()[0]
        stock = df.loc[df['resourceID'] == i]['total'].tolist()[0]
        print("\n"f''' Index: {i} | Item name: {name} | Stock: {stock} ''')

    while True:
        select_item = int(input("\nEnter item index: "))

        if select_item not in res_id:
            print("invalid index option entered!")
            continue
        try:
            if select_index == 'RETURN':
                return
        except:
            return
        break

    while True:
        select_amount = input("\nEnter amount: ")

        if int(select_amount) > int(df.loc[df['resourceID'] == select_item]['total'].tolist()[0]):
            print("Cannot exceed the stock amount!")
            continue
        if not select_amount.isnumeric():
            print("Must be a numerical value!")
            continue

        if select_index == 'RETURN':
            return
        else:
            break

    return select_index, select_item, select_amount


def validate_refugee(lvl):
    date_format = '%d/%m/%Y'

    while True:
        f_name = input("\nEnter first name: ")
        if not f_name.isalpha():
            print("Must be alphabetic values!")
            continue
        if f_name == 'RETURN':
            return
        else:
            break

    while True:
        l_name = input("\nEnter last name: ")
        if not l_name.isalpha():
            print("Must be alphabetic values!")
            continue
        if l_name == 'RETURN':
            return
        else:
            break

    while True:
        try:
            dob = input("\nEnter date of birth (format: dd/mm/yy): ")
            if dob == 'RETURN':
                return
            dob = datetime.datetime.strptime(dob, date_format)
            break
        except ValueError:
            print("\nInvalid date format entered.")
            continue

    while True:
        gender = input("\nEnter gender (male, female, other): ")

        if (gender != 'male') and (gender != 'female') and (gender != 'other'):
            print("Please enter only male, female or other!")
            continue
        if gender == 'RETURN':
            return
        else:
            break

    while True:
        family_id = input("\nEnter family identification: ")
        if not family_id.isnumeric():
            print("Must be a numerical value!")
            continue
        if family_id == 'RETURN':
            return
        else:
            break

    while True:
        vacc = input("\nIs vaccinated? (True or False): ")
        if (vacc != 'True') and (vacc != 'False'):
            print("Please enter True or False only!")
            continue
        if vacc == 'False' and lvl == 'high':
            print("This camp only accept vaccinated refugee due to health risk concerns!")
            continue
        if vacc == "RETURN":
            return
        else:
            break

    med_id = extract_data("data/medicalInfoType.csv", "medicalInfoTypeID").tolist()
    df = extract_data_df("data/medicalInfoType.csv")
    # display medical condition option list
    for i in med_id:
        cond = df.loc[df['medicalInfoTypeID'] == i]['condition'].tolist()[0]
        lvl = df.loc[df['medicalInfoTypeID'] == i]['criticalLvl'].tolist()[0]
        print("\n"f''' Index: {i} | Condition: {cond} | Critical level: {lvl} ''')

    while True:
        try:
            med = input("\nEnter medical condition (optional): ")
            if int(med) not in med_id:
                print("Invalid index option entered!")
            # if user decided to enter nothing, we just assume the refugee is healthy aka index = 1
            elif med == '':
                med = 1
            if med == "RETURN":
                return
        except:
            return
        break

    while True:
        med_des = input("\nEnter medical description (optional): ")
        if len(str(med_des)) == 0:
            med_des = None
        if med_des == "RETURN":
            return
        else:
            break

    return family_id, f_name, l_name, dob, gender, int(med), med_des, vacc


def move_refugee_helper_method():
    """Moves refugee from one camp to another"""
    # displaying list of all refugees to user
    print("YOU ARE REQUESTING TO MOVE A REFUGEE. Enter RETURN if you didn't mean to select this. Otherwise, proceed"
          "as instructed.")
    refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
    ref_df = pd.read_csv(refugee_csv_path)
    print(ref_df)
    # checking input is vaild according to refugee IDs in database
    while True:
        rid = input("\nFrom the list above enter the refugee ID for the refugee you wish to move another camp: ")
        if rid == "RETURN":
            return
        elif rid.strip() and rid.strip().isdigit() and ref_df['refugeeID'].eq(int(rid)).any():
            break
        else:
            print("\nSorry - that refugee ID doesn't exist. Pick again.")
    old_camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
    # Displaying list of all ACTIVE camps to user
    camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
    camp_df = pd.read_csv(camp_csv_path)
    active_camp_df = camp_df[camp_df['status'] == 'open']
    print("\n", active_camp_df)
    # checking input is vaild according to refugee IDs in database
    while True:
        camp_id = input("\nGreat! Now, from the above list, enter the campID of "
                        "the camp you want to move this refugee to: ")
        if camp_id == "RETURN":
            return
        elif camp_id.strip() and camp_id.strip().isdigit() and active_camp_df['campID'].eq(int(camp_id)).any():
            break
        else:
            print("\nSorry - that camp ID doesn't exist (anymore). Pick again.")
    # Minus one from the population of the camp originally associated with the refugee
    # print(camp_id)
    row_index_old_camp = camp_df[camp_df['campID'] == old_camp_id].index
    # print(row_index_camp)
    # print(row_index_old_camp)
    camp_df.at[row_index_old_camp[0], 'refugeePop'] -= 1
    # Update the campID for the refugee in refugee CSV
    row_index_ref = ref_df[ref_df['refugeeID'] == int(rid)].index[0]
    modify_csv_value(refugee_csv_path, row_index_ref, "campID", camp_id)
    # Add one to the population of the camp which the refugee is now in
    row_index_new_camp = camp_df[camp_df['campID'] == int(camp_id)].index
    # print("row_index_new_camp:", row_index_new_camp)
    # print(row_index_new_camp)
    camp_df.at[row_index_new_camp[0], 'refugeePop'] += 1
    # camp_df.to_csv(camp_csv_path, mode='a', index=False, header=False)
    # modify_csv_value(camp_df, row, "refugeePop", camp_id)
    print(f"Transfer complete. We have reassigned the refugee from camp {old_camp_id} to camp {camp_id}."
          f"Additionally, the population of both camps has been adjusted accordingly.")
    return
# Just need to add some extra logic to the above in case the event also changes....


def delete_refugee():
    print("YOU ARE REQUESTING TO DELETE A REFUGEE. Enter RETURN if you didn't mean to select this. Otherwise, proceed"
          " as instructed.")
    refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
    ref_df = pd.read_csv(refugee_csv_path)
    print(ref_df)
    # checking input is vaild according to refugee IDs in database
    while True:
        rid = input("\nFrom the list above enter the refugee ID for the refugee you wish to remove from the system: ")
        if rid == "RETURN":
            return
        elif rid.strip() and rid.strip().isdigit() and ref_df['refugeeID'].eq(int(rid)).any():
            break
        else:
            print("\nSorry - that refugee ID doesn't exist. Pick again.")
    print("Below is the information about this refugee.")
    specific_refugee_row = ref_df[ref_df['refugeeID'] == int(rid)]
    print(specific_refugee_row)
#     POP UP WINDOW TO CONFIRM USER WANTS TO DELETE REFUGEE (say it's irreversible?)

    root = tk.Tk()
    result = tk.messagebox.askquestion("Reminder", "Are you sure you want to delete this refugee?")
    if result == "yes":
        # Removing 1 from the population of the associated camp
        camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        camp_df = pd.read_csv(camp_csv_path)
        camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
        row_index_camp = camp_df[camp_df['campID'] == camp_id].index
        camp_df.at[row_index_camp[0], 'refugeePop'] -= 1
        #     Deleting the refugee from the database
        ref_df.drop(ref_df[ref_df['refugeeID'] == int(rid)].index, inplace=True)
        ref_df.to_csv(refugee_csv_path, index=False)
        tk.messagebox.showinfo(
            f"Okay. You have permanently deleted refugee #{rid} from the system. Their old associated camp population "
            f"has also been adjusted accordingly.")

    else:
        tk.messagebox.showinfo("Cancel", "The operation to delete the event was canceled.")
    root.mainloop()

# # Removing 1 from the population of the associated camp
#     camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
#     camp_df = pd.read_csv(camp_csv_path)
#     camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
#     row_index_camp = camp_df[camp_df['campID'] == camp_id].index
#     camp_df.at[row_index_camp[0], 'refugeePop'] -= 1
#     #     Deleting the refugee from the database
#     ref_df.drop(ref_df[ref_df['refugeeID'] == int(rid)].index, inplace=True)
#     ref_df.to_csv(refugee_csv_path, index=False)
#     tk.messagebox.showinfo(f"Okay. You have permanently deleted refugee #{rid} from the system. Their old associated camp population has "
#           f"also been adjusted accordingly.")


# Also add a method to edit info for a refugee?
# Borrow functions
#     Use while loop instead of calling function again  - break if valid and continue if not valid
#
# Also put a try and except
#     Display list of refugees in camps
# get user to input refugee id
# Display list of camps to move refugee to
# Update both populations
#       user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
#         df = pd.read_csv(user_csv_path)
#         sub_df = df.loc[df['userID'] == int(self.user_id), ['username', 'firstName', 'lastName', 'email',
#                                                             'phone', 'occupation', 'roleID', 'eventID', 'campID']]
#         table_str = sub_df.to_markdown(index=False)
#         print("\n" + table_str)
