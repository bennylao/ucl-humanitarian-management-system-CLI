import re
import csv
from pathlib import Path
import pandas as pd
import datetime
import logging
from passlib.hash import sha256_crypt

def not_too_old():
    while True:
        date_string = input("--> ")
        try:
            year = int(date_string[-4:])  # Extracts the year
            if year >= 1900:
                return date_string
            else:
                print("Please enter a year of 1900 and afterwards...")
        except ValueError:
            print("Invalid format. Please enter a valid date...")

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
        elif re.match(r'\w', username, re.A):
            break
        else:
            print("Invalid username entered. Only alphabet letter (a-z), numbers (0-9) and underscore(_) are allowed.")
    # check for password
    while True:
        password = input("\nEnter password: ")
        if password == 'RETURN':
            return
        elif re.match(allowed_chars, password):
            password = sha256_crypt.hash(password)
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
                  "Only alphabetic characters are allowed."
                  '(Those characters defined in the Unicode character database as "Letter")')
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
            print("Invalid first name entered.\n"
                  "Only alphabetic characters are allowed."
                  '(Those characters defined in the Unicode character database as "Letter")')
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
        try:
            phone = int(phone)
        except ValueError:
            logging.warning("Invalid phone - phone is numeric but is not a number.")
            print("Invalid phone number entered.\n"
                  "Only numbers are allowed.")
            continue
        break

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

    # ask user to select their role in camp
    try:
        role_type_csv_path = Path(__file__).parent.joinpath("data/roleType.csv")
        df_role = pd.read_csv(role_type_csv_path)
    except FileNotFoundError as e:
        print("\n Data file seems to be damaged. Please contact admin for further assistance")
        logging.critical(e)
        return
    role_id_list = df_role['roleID'].tolist()
    print("\n" + df_role.to_markdown(index=False))
    while True:
        print("Please select a role you want to change to (Enter its index)")
        new_role_id = input("---> ")
        if new_role_id.upper() == "RETURN":
            return
        else:
            try:
                new_role_id = int(new_role_id)
                if new_role_id not in role_id_list:
                    print("You must choose one of the roleID from the list!")
                else:
                    break
            except ValueError:
                print("Only Integer is allowed!")

    return ["volunteer", False, False, username, password, first_name, last_name, email, phone, occupation, new_role_id,
            0]


def validate_event_input():
    try:
        countries_csv_path = Path(__file__).parent.joinpath("data/country.csv")
        df_countries = pd.read_csv(countries_csv_path)
        df_countries['name'] = df_countries['name'].str.lower()
        all_countries = df_countries['name'].tolist()
    except FileNotFoundError as e:
        print(f"\nFile not found."
              f"\nPlease contact admin for further assistance."
              f"\n[Error] {e}")
        logging.critical(f"{e}")
        return

    date_format = '%d/%m/%Y'  # Use for validating user entered date format
    while True:
        title = input("\nPlan title: ")
        if title.lower() == 'return':
            return
        else:
            break

    while True:
        location = input("\nLocation(country): ").lower()
        if location.upper() == 'RETURN':
            return
        elif location not in all_countries:
            print("\nInvalid country name entered.")
            continue
        else:
            country_id = df_countries.loc[df_countries['name'] == location, 'countryID'].values[0]
            df_countries = pd.read_csv(countries_csv_path)
            location = df_countries.loc[df_countries['countryID'] == country_id, 'name'].values[0]
            break

    while True:
        description = input("\nDescription: ")
        if description.upper() == 'RETURN':
            return
        else:
            break

    while True:
        #start_date = input("\nStart date (format dd/mm/yyyy): ")
        print("\nStart date (format dd/mm/yyyy): ")
        start_date = not_too_old()
        if start_date.upper() == 'RETURN':
            return
        try:
            start_date = datetime.datetime.strptime(start_date, date_format)
            break
        except ValueError:
            print("\nInvalid date format entered.")
            continue

    while True:
        end_date = input("\nEstimated end date (format dd/mm/yyyy): ")
        if end_date.upper() == 'RETURN':
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
        ongoing = 'True'
    elif start_date.date() > datetime.date.today():
        ongoing = 'Yet'
    else:
        ongoing = 'False'

    return [ongoing, title, location, description, 0, start_date, end_date]


def validate_camp_input():
    csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
    df = pd.read_csv(csv_path)
    id_arr = df['campID'].tolist()

    if id_arr:
        campID = id_arr.pop() + 1
    else:
        campID = 1

    # while True:
    #     try:
    #         latitude = float(input("\n Enter the latitude of the camp: "))
    #         if latitude == "RETURN":
    #             return
    #         else:
    #             break
    #     except ValueError:
    #         print("Invalid input, Please enter a numerical value")

    # while True:
    #     try:
    #         longitude = float(input("\n Enter the longitude of the camp: "))
    #         if longitude == "RETURN":
    #             return
    #         else:
    #             break
    #     except ValueError:
    #         print("Invalid input, Please enter a numerical value")

    # capacity input
    while True:
        capacity = input("\nEnter capacity: ")

        if capacity == "RETURN":
            return
        if int(capacity) > 0:
            break
        else:
            print("Must be a positive integer!")
            continue

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


def modify_csv_pandas(file_path, select_col, row_value, final_col, new_value):
    try:
        csv_path = Path(__file__).parents[0].joinpath(file_path)
        df = pd.read_csv(csv_path)
        i = df.index[df[select_col] == row_value].tolist()[0]
        modify_csv_value(csv_path, i, final_col, new_value)
    except FileNotFoundError as e:
        logging.critical(f"{e}")
    except IndexError as e:
        logging.critical(f"{e}")


def modify_csv_value(file_path, row_index, column_name, new_value):
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
        rows[row_index][column_name] = new_value
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except FileNotFoundError as e:
        print(f"\n File not found."
              f"\nPlease contact admin for further assistance."
              f"\n[Error] {e}")
        logging.critical(f"{e}")


def matched_rows_csv(file, desired_column, except_value, index):
    """used to extract rows with specific value in a specific column"""
    df = pd.read_csv(file)
    if desired_column in df.columns.tolist():
        if except_value in df[desired_column].tolist():
            dff = df[df[desired_column] != except_value].set_index(index)
            dff_sorted = dff.sort_index()
            return [dff_sorted, dff_sorted.index.tolist()]
        else:
            return f"Value '{except_value}' not found in the {desired_column}."
    else:
        return f"Column '{desired_column}' not found in the CSV file."


def extract_active_event(csv_path):
    '''used to extract event id for active/yet ongoing events'''
    df = pd.read_csv(csv_path, converters={'ongoing': str})
    # ensure we only display camp(s) that are part of an active plan
    data = df[['ongoing', 'eventID']]
    active_id = []

    for i in range(len(data)):
        if data['ongoing'].iloc[i] == 'True' or data['ongoing'].iloc[i] == 'Yet':
            active_id.append(data['eventID'].iloc[i])

    return active_id, df


def display_open_camp_list():
    csv_path = Path(__file__).parents[0].joinpath("data/event.csv")
    active_id = extract_active_event(csv_path)[0]
    df_e = pd.read_csv(csv_path, converters={'ongoing': str})

    csv_path_c = Path(__file__).parents[0].joinpath("data/camp.csv")
    df_c = pd.read_csv(csv_path_c)

    if len(active_id) == 0:
        print("No relevant camps to select from")
        return

    camp_id_active = df_c.loc[df_c['status'] == 'open']['campID'].tolist()
    index = [int(i) for i in camp_id_active]

    table_str = df_c.loc[df_c['status'] == 'open'].to_markdown(index=False)
    print("\n" + table_str)

    return index


def validate_man_resource(index):
    csv_path = Path(__file__).parents[0].joinpath("data/resourceStock.csv")
    df = pd.read_csv(csv_path)

    while True:
        try:
            select_index = int(input("\nEnter camp index: "))

            if select_index not in index:
                print("invalid index option entered!")
                continue
            if select_index == 'RETURN':
                return
            break
        except ValueError:
            print("invalid index option entered!")
            logging.warning("Invalid index option entered!")
            continue

    res_id = pd.read_csv(csv_path)['resourceID'].tolist()

    # display medical condition option list
    for i in res_id:
        name = df.loc[df['resourceID'] == i]['name'].tolist()[0]
        stock = df.loc[df['resourceID'] == i]['total'].tolist()[0]
        print("\n"f''' Index: {i} | Item name: {name} | Stock: {stock} ''')

    while True:
        try:
            select_item = int(input("\nEnter item index: "))
            if select_index == 'RETURN':
                return
            if select_item not in res_id:
                print("invalid index option entered!")
                continue
            break
        except ValueError:
            print("invalid index option entered!")
            logging.warning("Invalid index option entered!")

    while True:
        select_amount = input("\nEnter amount: ")

        if select_index == 'RETURN':
            return
        else:
            try:
                select_amount = int(select_amount)
                if select_amount > int(df.loc[df['resourceID'] == select_item]['total'].tolist()[0]):
                    print("Cannot exceed the stock amount!")
                    continue
            except ValueError:
                logging.info("user input is not numerical value")
                print("Must be a numerical value!")
                continue

    return select_index, select_item, select_amount


def validate_refugee(lvl, cid):
    date_format = "%d/%m/%Y"
    while True:
        f_name = input("\nEnter first name: ")
        if f_name == 'RETURN':
            return
        if not f_name.isalpha():
            print("Must be alphabetic values!")
            continue
        else:
            break

    while True:
        l_name = input("\nEnter last name: ")
        if l_name == 'RETURN':
            return
        if not l_name.isalpha():
            print("Must be alphabetic values!")
            continue
        else:
            break

    while True:
        try:
            # dob = input("\nEnter date of birth (format: dd/mm/yyyy): ")
            print("\nEnter date of birth (format: dd/mm/yyyy): ")
            dob = not_too_old()
            if dob == 'RETURN':
                return
            datetime_object = datetime.datetime.strptime(dob, date_format)
            if datetime_object > datetime.datetime.now():
                print("Birth date should be before current date and time")
                continue
            else:
                dob = datetime_object.strftime(date_format)
                break
        except ValueError:
            print("\nInvalid date format entered.")
            continue

    while True:
        gender = input("\nEnter gender (male, female, other): ")
        if gender.upper() == 'RETURN':
            return
        if (gender != 'male') and (gender != 'female') and (gender != 'other'):
            print("Please enter only male, female or other!")
            continue
        else:
            break

    while True:
        print("\nSelect 1 to create a new family identification, or 2 to join an existing one")
        select = input("\nSelect your option: ")

        csv_path_camp = Path(__file__).parents[0].joinpath("data/camp.csv")
        df_camp = pd.read_csv(csv_path_camp)
        csv_path_ref = Path(__file__).parents[0].joinpath("data/refugee.csv")
        df_ref = pd.read_csv(csv_path_ref)
        all_familyID_list = df_ref['familyID'].drop_duplicates().sort_values().tolist()

        if select == 'RETURN':
            return
        elif select != '1' and select != '2':
            print("Select 1 or 2 only!")
            continue

        if select == '1':
            print("\nCreate a new family identification except these existing ones: ", all_familyID_list)
            while True:
                try:
                    create_id = input("\nEnter family identification: ")
                    if create_id == 'RETURN':
                        return
                    if int(create_id) in all_familyID_list:
                        print("Family ID already exists!")
                        continue
                    else:
                        break
                except ValueError:
                    print("Must be an integer value!")
                    continue
            break
        elif select == '2':
            df_ref_display = df_ref[['familyID', 'refugeeID', 'firstName', 'lastName']].sort_values(by=['familyID', 'refugeeID'])
            table = df_ref_display.to_markdown(index=False)
            print("\n" + table)
            while True:
                try:

                    create_id = input("\nEnter family identification: ")
                    if create_id == 'RETURN':
                        return
                    elif int(create_id) not in all_familyID_list:
                        print("Invalid family ID entered!")
                        continue
                    else:
                        break
                except ValueError:
                    print("Must be an integer value!")
                    continue
            break

    while True:
        vacc = input("\nIs vaccinated? (True or False): ")

        if vacc == "RETURN":
            return

        if (vacc != 'True') and (vacc != 'False'):
            print("Please enter True or False only!")
            continue
        if vacc == 'False' and lvl == 'high':
            print("This camp only accept vaccinated refugee due to health risk concerns!")
            continue
        else:
            break

    csv_path = Path(__file__).parents[0].joinpath("data/medicalInfoType.csv")

    med_id = pd.read_csv(csv_path)["medicalInfoTypeID"].tolist()
    df = pd.read_csv(csv_path)
    df.rename(columns={'medicalInfoTypeID': 'Index'}, inplace=True)
    df.rename(columns={'criticalLvl': 'Critical level'}, inplace=True)
    df = df.loc[:, df.columns != 'Critical level']
    # display medical condition option list
    table_str = df.to_markdown(index=False)
    print("\n" + table_str)
    while True:
        try:
            med = input("\nEnter medical condition: ")
            if med == "RETURN":
                return
            if int(med) not in med_id:
                print("Invalid index option entered!")
                continue
            break
            # if user decided to enter nothing, we just assume the refugee is healthy aka index = 1
        except ValueError:
            print("Invalid index option entered!")
            logging.warning("Invalid index option")

    while True:
        med_des = input("\nEnter medical description (optional): ")
        if len(str(med_des)) == 0:
            med_des = None
        if med_des == "RETURN":
            return
        else:
            break

    return create_id, f_name, l_name, dob, gender, med, med_des, vacc


def move_refugee_helper_method(cid):
    """Moves refugee from one camp to another"""
    # displaying list of all refugees to user
    print("\nYOU ARE REQUESTING TO MOVE A REFUGEE. Enter RETURN if you didn't mean to select this. Otherwise, proceed"
          " as instructed.\n")
    try:
        refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
        ref_df = pd.read_csv(refugee_csv_path)
        logging.info("Refugee file loaded successfully for moving a refugee around camps.")
        camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        camp_df = pd.read_csv(camp_csv_path)
        # print(ref_df.to_markdown(index=False))
        # ---------------------------------------------------
        eventID = camp_df.loc[camp_df['campID'] == int(cid), 'eventID'].iloc[0]
        camps_in_event = camp_df.loc[camp_df['eventID'] == eventID, 'campID'].tolist()
        refugees_in_associated_camps = ref_df[ref_df['campID'].isin(camps_in_event)]
        print(refugees_in_associated_camps.to_markdown(index=False))
        # --------------------------------------------------
        # checking input is valid according to refugee IDs in database
        while True:
            rid = input("\nFrom the list above enter the refugee ID for the refugee you wish to move another camp"
                        "\nREMEMBER: Enter RETURN to go back if no valid options: ")
            if rid.lower() == "return":
                return
            try:
                rid = int(rid)
                if refugees_in_associated_camps['refugeeID'].eq(rid).any():
                    break
                else:
                    print("\nSorry - that refugee ID isn't in your event. Pick again.")
            except ValueError as e:
                logging.info(f"Error {e}with user input for moving a refugee from a camp.")
                print(f"Invalid input with error {e}. Try again with a valid refugee ID.\n")
        camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        camp_df = pd.read_csv(camp_csv_path)
        logging.info("Camp file loaded successfully for moving a refugee around camps.")
        active_camp_df = camp_df[camp_df['status'] == 'open']
        old_camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
        eventID = camp_df.loc[camp_df['campID'] == int(old_camp_id), 'eventID'].iloc[0]
        camps_in_event = camp_df.loc[camp_df['eventID'] == eventID, 'campID'].tolist()
        active_and_in_event = camp_df[(camp_df['status'] == 'open') & (camp_df['campID'].isin(camps_in_event))]
        # checking input is valid according to refugee IDs in database
        if len(active_and_in_event) == 0:
            print("Oh no. There are no other active camps in the same event as this refugee... Redirecting you back!")
            return
        while True:
            print("\n", active_and_in_event.to_markdown(index=False))
            camp_id = input("\nFrom the above list (list of ACTIVE camps which are in the same event as "
                            f"refugee number {rid}'s original camp) enter the campID of the camp "
                            f"you want to move this refugee to: ")
            if camp_id.lower() == "return":
                return
            try:
                camp_id = int(camp_id)
                if camp_id == old_camp_id:
                    print("\nLooks like that's the same camp this refugee is already in. Try again "
                          "or if there are no other camps available, enter RETURN to go back.")
                elif (camp_id in active_camp_df['campID'].values) and (camp_id in camps_in_event):
                    # Need to do a final check to see if new camp's refugeePop + 1 is < new camp's refugeeCapacity
                    row_index_new_camp = camp_df[camp_df['campID'] == int(camp_id)].index
                    new_potential_refugee_pop = (camp_df.at[row_index_new_camp[0], 'refugeePop'])
                    new_camp_capacity = camp_df.at[row_index_new_camp[0], 'refugeeCapacity']
                    if (new_potential_refugee_pop + 1) <= new_camp_capacity:
                        break
                    else:
                        print(
                            "\n\nOh no! The new camp you've selected doesn't have the capacity to handle "
                            "another refugee. "
                            f"Camp {camp_id} has a current population of {new_potential_refugee_pop} and a capacity of "
                            f"{new_camp_capacity}.\nLet's go again.\n")
                else:
                    print("\nSorry - that camp ID doesn't exist (anymore). Pick again.")
            except ValueError:
                print("\nInvalid input. Please enter a valid campID or type RETURN to go back: ")
        # Need to point out to user if this refugee is part of a family. Do they want to move the entire family?
        refugee_family_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'familyID'].iloc[0]
        related_family_members = ref_df[(ref_df['familyID'] == int(refugee_family_id)) & (ref_df['campID'].isin(camps_in_event))]
        total_family_members = len(related_family_members)
        while True:
            if total_family_members > 1:
                print("\n----HOLD ON!---- \nThis refugee is part of a family unit (see below).\n")
                print(related_family_members.to_markdown(index=False))
                user_input = input("\nAre you sure you want to move this refugee alone? Enter YES (to move"
                                   " alone), NO (to move as a family unit), or RETURN (to exit): ")
                if user_input.lower() == 'yes':
                    break
                elif user_input.lower() == 'no':
                    print(
                        "\nOkay. We're going to try to move the family as a unit. However, if capacity in the new camp"
                        " is not enough for the entire family, then we shall abort.")

                    related_family_members_list = related_family_members['refugeeID'].tolist()
                    size_of_family = len(related_family_members_list)
                    row_index_new_camp = camp_df[camp_df['campID'] == int(camp_id)].index
                    new_potential_refugee_family_pop = (camp_df.at[row_index_new_camp[0], 'refugeePop'])
                    new_camp_capacity = camp_df.at[row_index_new_camp[0], 'refugeeCapacity']
                    if (new_potential_refugee_family_pop + size_of_family) > new_camp_capacity:
                        print(
                            f"\n\nSorry. Moving this entire family unit would cause capacity overflow of camp {camp_id}."
                            f"You'll have to move them alone or not at all. Camp {camp_id} has a current population "
                            f"of {new_potential_refugee_family_pop},\n"
                            f"a capacity of {new_camp_capacity}, whilst the family has {size_of_family} members."
                            f"\n\n")
                        return
                    print("\nExcellent. No capacity overflow detected for the new camp!")
                    # print(related_family_members_list)
                    for index, row in related_family_members.iterrows():
                        rid = row['refugeeID']
                        old_camp_id = row['campID']
                        # old_camp_id = ref_df.loc[ref_df['campID'] == int(i), 'campID'].iloc[0]
                        # row_index_old_camp = camp_df[camp_df['campID'] == old_camp_id].index
                        # # print(row_index_camp)
                        # # print(row_index_old_camp)
                        # camp_df.at[row_index_old_camp[0], 'refugeePop'] -= 1
                        # Update the campID for the refugee in refugee CSV
                        row_index_ref = ref_df[ref_df['refugeeID'] == int(rid)].index[0]
                        modify_csv_value(refugee_csv_path, row_index_ref, "campID", camp_id)
                        # Remove 1 from the population of the old camp
                        row_index_old_camp = camp_df[camp_df['campID'] == old_camp_id].index
                        camp_df.at[row_index_old_camp[0], 'refugeePop'] -= 1
                        camp_df.to_csv(camp_csv_path, index=False)
                        # Add one to the population of the camp which the refugee is now in
                        camp_df.at[row_index_new_camp[0], 'refugeePop'] += 1
                        camp_df.to_csv(camp_csv_path, index=False)
                        # camp_df.to_csv(camp_csv_path, mode='a', index=False, header=False)
                        # modify_csv_value(camp_df, row, "refugeePop", camp_id)
                        print(
                            f"\nTransfer for refugee {rid} complete. We have reassigned the refugee from camp {old_camp_id} "
                            f"to camp {camp_id}."
                            f"Additionally, the population of both camps has been adjusted accordingly. See below.")
                        print("\n", camp_df[camp_df['campID'] == int(old_camp_id)].to_markdown(index=False), "\n")
                        print("\n", camp_df[camp_df['campID'] == int(camp_id)].to_markdown(index=False), "\n")
                    print("\n Great. That's all that family transferred as a unit.")
                    row_index_new_camp = camp_df[camp_df['campID'] == int(camp_id)].index
                    new_refugee_pop = (camp_df.at[row_index_new_camp[0], 'refugeePop'])
                    new_camp_capacity = camp_df.at[row_index_new_camp[0], 'refugeeCapacity']
                    if new_refugee_pop > new_camp_capacity:
                        overflow_amount = (new_refugee_pop - new_camp_capacity)
                        print(
                            f"Uh oh! Capacity overflow. You need to remove {overflow_amount} refugee(s) from camp {camp_id}")

                    return
                elif user_input.lower() == 'return':
                    return
                else:
                    print("Sorry. Invalid input. Let's try again.")
            else:
                break
        print("\nThanks - bear with us whilst we make that transfer. This refugee either has no family members in the"
              "system, or you have chosen to move them by themselves."
              "\n\n----------------------------------------------------------------------------------------")
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
        camp_df.at[row_index_new_camp[0], 'refugeePop'] += 1
        camp_df.to_csv(camp_csv_path, index=False)

        recalculate_criticalvl(camp_id)
        # camp_df.to_csv(camp_csv_path, mode='a', index=False, header=False)
        # modify_csv_value(camp_df, row, "refugeePop", camp_id)
        print(f"\nTransfer complete. We have reassigned the refugee from camp {old_camp_id} to camp {camp_id}."
              f"Additionally, the population of both camps has been adjusted accordingly. See below.")
        print("\n", camp_df[camp_df['campID'] == int(old_camp_id)].to_markdown(index=False), "\n")
        print("\n", camp_df[camp_df['campID'] == int(camp_id)].to_markdown(index=False), "\n")
    except FileNotFoundError as e:
        logging.critical(f"Error: {e}. One of the data files not found when moving a refugee around camps.")
        print(f"\nTraining session data file is not found or is damaged."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"\nOne of the data files is not found or is damaged when moving a refugee around camps.."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")


def move_refugee_admin():
    """Moves refugee from one camp to another"""
    # displaying list of all refugees to user
    print("\nYOU ARE REQUESTING TO MOVE A REFUGEE. Enter RETURN if you didn't mean to select this. Otherwise, proceed"
          " as instructed.\n")
    try:
        refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
        ref_df = pd.read_csv(refugee_csv_path)
        logging.info("Refugee file loaded successfully for moving a refugee around camps.")
        # camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        # camp_df = pd.read_csv(camp_csv_path)
        print(ref_df.to_markdown(index=False))
        # --------------------------------------------------
        # checking input is valid according to refugee IDs in database
        while True:
            rid = input("\nFrom the list above enter the refugee ID for the refugee you wish to move another camp"
                        "\nREMEMBER: Enter RETURN to go back if no valid options: ")
            if rid.lower() == "return":
                return
            try:
                rid = int(rid)
                if ref_df['refugeeID'].eq(rid).any():
                    break
                else:
                    print("\nSorry - that refugee ID doesn't exist. Pick again.")
            except ValueError as e:
                logging.info(f"Error {e}with user input for moving a refugee from a camp.")
                print(f"Invalid input with error {e}. Try again with a valid refugee ID.\n")
        camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        camp_df = pd.read_csv(camp_csv_path)
        logging.info("Camp file loaded successfully for moving a refugee around camps.")
        active_camp_df = camp_df[camp_df['status'] == 'open']
        old_camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
        eventID = camp_df.loc[camp_df['campID'] == int(old_camp_id), 'eventID'].iloc[0]
        camps_in_event = camp_df.loc[camp_df['eventID'] == eventID, 'campID'].tolist()
        active_and_in_event = camp_df[(camp_df['status'] == 'open') & (camp_df['campID'].isin(camps_in_event))]
        # checking input is valid according to refugee IDs in database
        if len(active_and_in_event) == 0:
            print("Oh no. There are no other active camps in the same event as this refugee... Redirecting you back!")
            return
        while True:
            print("\n", active_and_in_event.to_markdown(index=False))
            camp_id = input("\nFrom the above list (list of ACTIVE camps which are in the same event as "
                            f"refugee number {rid}'s original camp) enter the campID of the camp "
                            f"you want to move this refugee to: ")
            if camp_id.lower() == "return":
                return
            try:
                camp_id = int(camp_id)
                if camp_id == old_camp_id:
                    print("\nLooks like that's the same camp this refugee is already in. Try again "
                          "or if there are no other camps available, enter RETURN to go back.")
                elif (camp_id in active_camp_df['campID'].values) and (camp_id in camps_in_event):
                    # Need to do a final check to see if new camp's refugeePop + 1 is < new camp's refugeeCapacity
                    row_index_new_camp = camp_df[camp_df['campID'] == int(camp_id)].index
                    new_potential_refugee_pop = (camp_df.at[row_index_new_camp[0], 'refugeePop'])
                    new_camp_capacity = camp_df.at[row_index_new_camp[0], 'refugeeCapacity']
                    if (new_potential_refugee_pop + 1) <= new_camp_capacity:
                        break
                    else:
                        print(
                            "\n\nOh no! The new camp you've selected doesn't have the capacity to handle "
                            "another refugee. "
                            f"Camp {camp_id} has a current population of {new_potential_refugee_pop} and a capacity of "
                            f"{new_camp_capacity}.\nLet's go again.\n")
                else:
                    print("\nSorry - that's not an option. Pick again.")
            except ValueError:
                print("\nInvalid input. Please enter a valid campID or type RETURN to go back: ")
        # Need to point out to user if this refugee is part of a family. Do they want to move the entire family?
        refugee_family_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'familyID'].iloc[0]
        related_family_members = ref_df[(ref_df['familyID'] == int(refugee_family_id)) & (ref_df['campID'].isin(camps_in_event))]
        total_family_members = len(related_family_members)
        while True:
            if total_family_members > 1:
                print("\n----HOLD ON!---- \nThis refugee is part of a family unit (see below).\n")
                print(related_family_members.to_markdown(index=False))
                user_input = input("\nAre you sure you want to move this refugee alone? Enter YES (to move"
                                   " alone), NO (to move as a family unit), or RETURN (to exit): ")
                if user_input.lower() == 'yes':
                    break
                elif user_input.lower() == 'no':
                    print(
                        "\nOkay. We're going to try to move the family as a unit. However, if capacity in the new camp"
                        " is not enough for the entire family, then we shall abort.")

                    related_family_members_list = related_family_members['refugeeID'].tolist()
                    size_of_family = len(related_family_members_list)
                    row_index_new_camp = camp_df[camp_df['campID'] == int(camp_id)].index
                    new_potential_refugee_family_pop = (camp_df.at[row_index_new_camp[0], 'refugeePop'])
                    new_camp_capacity = camp_df.at[row_index_new_camp[0], 'refugeeCapacity']
                    if (new_potential_refugee_family_pop + size_of_family) > new_camp_capacity:
                        print(
                            f"\n\nSorry. Moving this entire family unit would cause capacity overflow of camp {camp_id}."
                            f"You'll have to move them alone or not at all. Camp {camp_id} has a current population "
                            f"of {new_potential_refugee_family_pop},\n"
                            f"a capacity of {new_camp_capacity}, whilst the family has {size_of_family} members."
                            f"\n\n")
                        return
                    print("\nExcellent. No capacity overflow detected for the new camp!")
                    # print(related_family_members_list)
                    for index, row in related_family_members.iterrows():
                        rid = row['refugeeID']
                        old_camp_id = row['campID']
                        # Update the campID for the refugee in refugee CSV
                        row_index_ref = ref_df[ref_df['refugeeID'] == int(rid)].index[0]
                        modify_csv_value(refugee_csv_path, row_index_ref, "campID", camp_id)
                        # Remove 1 from the population of the old camp
                        row_index_old_camp = camp_df[camp_df['campID'] == old_camp_id].index
                        camp_df.at[row_index_old_camp[0], 'refugeePop'] -= 1
                        camp_df.to_csv(camp_csv_path, index=False)
                        # Add one to the population of the camp which the refugee is now in
                        camp_df.at[row_index_new_camp[0], 'refugeePop'] += 1
                        camp_df.to_csv(camp_csv_path, index=False)
                        # camp_df.to_csv(camp_csv_path, mode='a', index=False, header=False)
                        # modify_csv_value(camp_df, row, "refugeePop", camp_id)
                        print(
                            f"\nTransfer for refugee {rid} complete. We have reassigned the refugee from camp {old_camp_id} "
                            f"to camp {camp_id}."
                            f"Additionally, the population of both camps has been adjusted accordingly. See below.")
                        print("\n", camp_df[camp_df['campID'] == int(old_camp_id)].to_markdown(index=False), "\n")
                        print("\n", camp_df[camp_df['campID'] == int(camp_id)].to_markdown(index=False), "\n")
                    print("\n Great. That's all that family transferred as a unit.")
                    row_index_new_camp = camp_df[camp_df['campID'] == int(camp_id)].index
                    new_refugee_pop = (camp_df.at[row_index_new_camp[0], 'refugeePop'])
                    new_camp_capacity = camp_df.at[row_index_new_camp[0], 'refugeeCapacity']
                    if new_refugee_pop > new_camp_capacity:
                        overflow_amount = (new_refugee_pop - new_camp_capacity)
                        print(
                            f"Uh oh! Capacity overflow. You need to remove {overflow_amount} refugee(s) from camp {camp_id}")

                    return
                elif user_input.lower() == 'return':
                    return
                else:
                    print("Sorry. Invalid input. Let's try again.")
            else:
                break
        print("\nThanks - bear with us whilst we make that transfer. This refugee either has no family members in the"
              "system, or you have chosen to move them by themselves."
              "\n\n----------------------------------------------------------------------------------------")
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
        camp_df.at[row_index_new_camp[0], 'refugeePop'] += 1
        camp_df.to_csv(camp_csv_path, index=False)

        recalculate_criticalvl(camp_id)
        # camp_df.to_csv(camp_csv_path, mode='a', index=False, header=False)
        # modify_csv_value(camp_df, row, "refugeePop", camp_id)
        print(f"\nTransfer complete. We have reassigned the refugee from camp {old_camp_id} to camp {camp_id}."
              f"Additionally, the population of both camps has been adjusted accordingly. See below.")
        print("\n", camp_df[camp_df['campID'] == int(old_camp_id)].to_markdown(index=False), "\n")
        print("\n", camp_df[camp_df['campID'] == int(camp_id)].to_markdown(index=False), "\n")
    except FileNotFoundError as e:
        logging.critical(f"Error: {e}. One of the data files not found when moving a refugee around camps.")
        print(f"\nTraining session data file is not found or is damaged."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"\nOne of the data files is not found or is damaged when moving a refugee around camps.."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")


def delete_refugee():
    print("YOU ARE REQUESTING TO DELETE A REFUGEE. Enter RETURN if you didn't mean to select this. Otherwise, proceed"
          " as instructed.")
    try:
        refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
        ref_df = pd.read_csv(refugee_csv_path)
        logging.info("Refugee data file to delete a refugee from system loaded successfully.")
        print(ref_df.to_markdown(index=False))
        # checking input is valid according to refugee IDs in database
        while True:
            rid = input(
                "\nFrom the list above enter the refugee ID for the refugee you wish to remove from the system: ")
            if rid == "RETURN":
                return
            elif rid.strip() and rid.strip().isdigit() and ref_df['refugeeID'].eq(int(rid)).any():
                break
            else:
                print("\nSorry - that refugee ID doesn't exist. Pick again.")
        print("Below is the information about this refugee.")
        specific_refugee_row = ref_df[ref_df['refugeeID'] == int(rid)]
        print(specific_refugee_row.to_markdown(index=False))
        #     POP UP WINDOW TO CONFIRM USER WANTS TO DELETE REFUGEE (say it's irreversible?)
        #     root = tk.Tk()
        while True:
            result = input("Are you sure you want to delete this refugee? Enter 'yes' or 'no': ")
            # result = tk.messagebox.askquestion("Reminder", "Are you sure you want to delete this refugee?")
            if result == "yes":
                # Removing 1 from the population of the associated camp
                camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
                camp_df = pd.read_csv(camp_csv_path)
                logging.info("Camp data file loaded successfully when deleting a refugee from the system.")
                camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
                row_index_camp = camp_df[camp_df['campID'] == camp_id].index
                camp_df.at[row_index_camp[0], 'refugeePop'] -= 1
                camp_df.to_csv(camp_csv_path, index=False)
                #     Deleting the refugee from the database
                ref_df.drop(ref_df[ref_df['refugeeID'] == int(rid)].index, inplace=True)
                ref_df.reset_index(drop=True, inplace=True)
                ref_df.to_csv(refugee_csv_path, index=False)
                recalculate_criticalvl(camp_id)
                print(
                    f"\nOkay. You have permanently deleted refugee #{rid} from the system. Their old associated camp population "
                    f"has also been adjusted accordingly.")
                print("\nRefugee DataFrame after deletion:")
                print(ref_df.to_markdown(index=False))
                break
            elif result == "no":
                print("\nReturning back to previous menu.")
                return
            else:
                print("\nInvalid input. Please enter 'yes' or 'no': ")
            #     tk.messagebox.showinfo("Cancel", "The operation to delete the refugee was canceled.")
            #     break
        # root.mainloop()
        # while True:
        #     user_input = input("Enter RETURN to exit back.")
        #     if user_input.lower() == "RETURN":
        #         return
        #     else:
        #         print("Invalid user entry. Please enter RETURN.")
    except FileNotFoundError as e:
        logging.critical(f"Error: {e}. One of the data files not found when deleting a refugee from system.")
        print(f"\nTraining session data file is not found or is damaged."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"\nOne of the data files is not found or is damaged when deleting a refugee from the system."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")


def legal_advice_support():
    logging.info("Legal Advice Page starts up.")
    print("------------------------------------------------------------------------------\n"
          "                       Legal Advice Support Services\n"
          "------------------------------------------------------------------------------")
    print("\nBelow are links to our partner legal charities to offer legal support to refugees whilst we work on "
          "\nbuilding our own team."
          "\nRight clicking on these links will direct you to a web page. \nYou will have to return back "
          "to the application manually.\n")

    links = [
        ("Refugee Council Legal Advice Site", "https://www.refugeecouncil.org.uk/"),
        ("Red Cross Legal Support", "https://www.redcross.org.uk/"),
        ("Refugee Legal Centre", "https://www.refugee-legal-centre.org.uk/"),
        ('RETURN', '')
    ]
    while True:
        for i, (name, url) in enumerate(links, 1):
            print(f"{i}. {name}: {url}", '\n')
        user_input = input("\nClick on one of the above links or enter RETURN to leave this menu: ")
        if user_input.lower() == "return":
            return
        # Just exit the page whatever they input.
        break


def iterate_through_list(lst1, lst2):
    for element in lst1:
        lst2.append(element)


def display_training_session():
    try:
        training_session_path = Path(__file__).parents[0].joinpath("data/trainingSessions.csv")
        session_df = pd.read_csv(training_session_path)
        length_session_df = pd.read_csv(training_session_path)["sessionID"].tolist()
        logging.info("Training session data successfully loaded.")
        print("\n--------------------------------------------------------------------------------------"
              "\nThese training / skills sessions give refugees the opportunity to pick up new skills."
              "\n--------------------------------------------------------------------------------------")
        while True:
            if len(length_session_df) == 0:
                user_input = input("Oh no! No sessions created yet! Why don't you add one now? "
                                   "\nEnter 1 to create a session or 2 to go back: ")
                if user_input == '1':
                    create_training_session()
                    return
                elif user_input == '2':
                    return
                else:
                    print("\nSorry! Invalid input.")
            else:
                print("\n", session_df.to_markdown(index=False))
                input("\nEnter anything to go back when you're ready. ")
                return
    except FileNotFoundError as e:
        logging.critical(f"Error: {e}. Session data file not found.")
        print(f"\nTraining session data file is not found or is damaged."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"\nTraining session data file is not found or is damaged."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")


def create_training_session():
    try:
        training_session_path = Path(__file__).parents[0].joinpath("data/trainingSessions.csv")
        session_df = pd.read_csv(training_session_path)
        role_type_path = Path(__file__).parents[0].joinpath("data/roleType.csv")
        role_df = pd.read_csv(role_type_path)
        camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        camp_df = pd.read_csv(camp_csv_path)
        refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
        ref_df = pd.read_csv(refugee_csv_path)
        print(role_df['name'].to_markdown(index=False))
        logging.info("All data files have loaded.")
        while True:
            occupation = input("\nFrom the list above enter the role which is closest to your own"
                               " or enter RETURN to exit: ")
            if occupation.lower() == "return":
                return
            elif role_df['name'].eq(occupation.lower()).any():
                break
            else:
                print("\nSorry - that role doesn't exist in our system. Pick again or enter RETURN: ")
        while True:
            topic = input("\nEnter the type of topic you will be discussing in your skills session: ")
            if topic.lower() == "return":
                return
            else:
                break
        while True:
            date_input = input("\nEnter the date of the session (e.g., YYYY-MM-DD): ")
            if date_input.lower() == "return":
                return
            else:
                try:
                    date = datetime.datetime.strptime(date_input, '%Y-%m-%d').date()
                    if date > datetime.datetime.now().date():
                        logging.info("Date for creating a session has been set correctly.")
                        break
                    else:
                        print("Can't select a date in the past! Try again.")
                        logging.info("Date input for creating a session was in the past so invalid.")
                except ValueError:
                    logging.info("Input date for creating a training session was invalid form.")
                    print("\nInvalid date format. Please use the format YYYY-MM-DD. Or enter RETURN to quit.")
        df_c = camp_df.loc[camp_df['status'] == 'open']
        print(df_c.to_markdown(index=False))
        while True:
            camp = input("\nEnter the campID of the camp you will be holding the session at: ")
            if camp.lower() == "return":
                return
            try:
                camp_id = int(camp)
                if camp_id in camp_df.loc[camp_df['status'] == 'open']['campID'].tolist():
                    break
                else:
                    print("\nSorry - that camp doesn't exist or already closed. Pick again or enter RETURN.")
                    continue
            except ValueError as e:
                logging.info("Invalid user input when creating a session")
                print(f"\nInvalid input {e}. Please enter a valid integer for campID or type 'RETURN' to go back.")
        eventID = camp_df.loc[camp_df['campID'] == int(camp), 'eventID'].iloc[0]
        camps_in_event = camp_df.loc[camp_df['eventID'] == eventID, 'campID'].tolist()
        refugees_in_associated_camps = ref_df[ref_df['campID'].isin(camps_in_event)]
        participants = []
        while True:
            print("\n", refugees_in_associated_camps.to_markdown(index=False))
            rid = input(
                "\nFrom the list above of all refugees in the camps which are part of the same event as the camp you "
                "will be holding the session,\none at a time enter a refugee ID for who shall be joining the skills "
                "session. Enter DONE when finished: ")
            if rid.lower() == 'done':
                break
            if rid.lower() == 'return':
                return
            elif int(rid) in participants:
                print("\nYou've already added that refugee!")
            elif rid.strip() and rid.strip().isdigit() and int(rid) in refugees_in_associated_camps['refugeeID'].values:
                participants.append(int(rid))
            elif not ref_df['refugeeID'].eq(int(rid)).any():
                print("\nSorry - that refugee doesn't exist in our system!")
            else:
                print("\nSorry - that refugee isn't in the same 'event' as where this session is hosted. Pick again.")

            #  Now we have all the info we need to create a training session
            # Need to also increment sessionID by 1.
        print(f"\nHere is a confirmed list of the refugees you have selected to attend. You can add more later: ")
        for participant in participants:
            print(participant)
        print("\n\nGreat! That's all the info we need to create a session. Here are the details:\n"
              "---------------------------------------------------------------------------------")
        session_arr = pd.read_csv(training_session_path)["sessionID"].tolist()
        if len(session_arr) == 0:
            sessionID = 0
        else:
            sessionID = int(session_arr.pop())
        sessionID += 1

        training_session_data = [int(sessionID), occupation, topic, date, int(camp), list(participants), eventID]
        session_df.loc[len(session_df)] = training_session_data
        session_df.to_csv(training_session_path, index=False)
        added_session = session_df[session_df['sessionID'] == sessionID]
        print(added_session.to_markdown(index=False))
        print("\n---------------------------------------------------------------------------------")
        return
    except FileNotFoundError as e:
        logging.critical(f"Error: {e}. One of the data files not found.")
        print(f"\nTraining session data file is not found or is damaged."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"\nOne of the data files is not found or is damaged."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")


def delete_session():
    try:
        training_session_path = Path(__file__).parents[0].joinpath("data/trainingSessions.csv")
        session_df = pd.read_csv(training_session_path)
        logging.info("Training session file to delete a session has loaded correctly.")
        print(
            "\nLooks like you want to cancel or delete a session. That's a shame! See current sessions in the system.")
        print("\n", session_df.to_markdown(index=False))
        # session_df.set_index('sessionID', inplace=True)
        while True:
            sessionID = input(
                "Enter RETURN now if you have changed your mind, or enter the sessionID you want to cancel: ")
            if sessionID.lower() == 'return':
                return
            elif sessionID.strip() and sessionID.strip().isdigit() and session_df['sessionID'].eq(int(sessionID)).any():
                break
            else:
                print("\n\nSorry - that's not a valid session ID. Pick again. ")
        sessionID_int = int(sessionID)
        session_date = session_df.loc[session_df['sessionID'] == sessionID_int, 'date'].values[0]
        session_datetime = datetime.datetime.strptime(session_date, '%Y-%m-%d').date()
        if session_datetime < datetime.datetime.now().date():
            logging.info("Date for session to delete is in the past.")
            while True:
                confirm = input("\nYou're about to delete a previously held skills session. "
                                "\nEnter YES to confirm or RETURN to cancel: ")
                if confirm.lower == 'return':
                    return
                elif confirm.lower() == 'yes':
                    break
                else:
                    print("Invalid option. Try again.")
        else:
            logging.info("Date for session to delete is in the future.")
            while True:
                print(session_df[session_df['sessionID'] == sessionID_int])
                confirm = input(f"\nYou're about to cancel skills session {sessionID_int} (displayed"
                                f" above), which HAS NOT yet been given. "
                                "\nAre you sure? Enter YES to confirm or RETURN to cancel: ")
                if confirm.lower() == 'return':
                    break
                elif confirm.lower() == 'yes':
                    break
                else:
                    print("\nInvalid option. Try again.\n")
        if confirm.lower() == 'return':
            return
        # Update CSV files accordingly
        session_df.drop(session_df[session_df['sessionID'] == sessionID_int].index, inplace=True)
        session_df.reset_index(drop=True, inplace=True)
        session_df.to_csv(training_session_path, index=False)
        print(
            f"\n Okay! We've deleted session number {sessionID} from our system. See below for updated list of sessions.\n")
        if len(session_df) != 0:
            print(session_df.to_markdown(index=False))
        else:
            print("No sessions in the system!")
    except FileNotFoundError as e:
        logging.critical(f"Error: {e}. One of the data files not found.")
        print(f"\nTraining session data file is not found or is damaged."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"\nOne of the data files is not found or is damaged."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")


def add_refugee_to_session():
    try:
        refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
        ref_df = pd.read_csv(refugee_csv_path)
        training_session_path = Path(__file__).parents[0].joinpath("data/trainingSessions.csv")
        session_df = pd.read_csv(training_session_path)
        logging.info("Refugee and training session data files loaded successfully to add a refugee to a session.")
        print("It's great another refugee wants to join a skills session!\n")
        length_session_df = pd.read_csv(training_session_path)["sessionID"].tolist()
        if len(length_session_df) == 0:
            print("Oh no! No sessions created yet! Taking you back...")
            return
        print(session_df.to_markdown(index=False))
        while True:
            sessionID = input("\n\nFrom the list above, enter the session ID for the "
                              "skills session you want to add more participants to. Or enter RETURN to go back: ")
            if sessionID.lower() == 'return':
                return
            elif sessionID.strip() and sessionID.strip().isdigit() and session_df['sessionID'].eq(int(sessionID)).any():
                break
            else:
                print("\n\nSorry - that's not a valid session ID. Pick again. ")
        row_index_sessionID = session_df[session_df['sessionID'] == int(sessionID)].index[0]
        registered = session_df.at[row_index_sessionID, 'participants']
        registered = registered.strip("[]").split(", ")
        already_registered = []
        for i in registered:
            if i != '' and isinstance(i, int):
                already_registered.append(int(i))
        eventID = session_df.at[row_index_sessionID, 'eventID']
        camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        camp_df = pd.read_csv(camp_csv_path)
        camps_in_event = camp_df.loc[camp_df['eventID'] == eventID, 'campID'].tolist()
        refugees_in_associated_camps = ref_df[ref_df['campID'].isin(camps_in_event)]
        # ----------  adding only refugees in this event! ---------
        # participants = []
        while True:

            if len(refugees_in_associated_camps) == 0:
                print("\nOh no. There are no other refugees in the event which this session is held."
                      "Taking you back")
                return
            print("\n", refugees_in_associated_camps.to_markdown(index=False))
            # print(refugees_in_associated_camps['refugeeID'])
            rid = input(
                f"\n\nFrom the above list, which are refugees in the same event as that which this session is "
                f"being held,\nenter the Refugee ID for who you want to add to session {sessionID}"
                "\nEnter DONE when you are finished, or return to cancel and go back: ")
            if rid.lower() == "return":
                return
            if rid.lower() == "done":
                break
            try:
                rid = int(rid)
                if rid in already_registered:
                    # print(already_registered)
                    print(f"\nDon't worry. That refugee is already down to attend this session.")
                # elif int(rid) in participants:
                #     print("\nYou've already just added that refugee.")
                elif refugees_in_associated_camps['refugeeID'].eq(int(rid)).any():
                    print(f"\n\nAdding refugee with id {rid} to skills session {sessionID}. \n\n")
                    already_registered.append(rid)
                else:
                    print("\n\nSorry - that refugee ID doesn't exist. Pick again.")
                    input("press Enter to continue...")
            except ValueError as e:
                print("Invalid integer entered!")
                logging.critical(f"{e}")
            except Exception as e:
                logging.critical(f"Unexpected error when adding a refugee to a training session from invalid user"
                                 f"input: {e}")
                print("\nInvalid input. Must enter an integer or one of the specified exit options.")
        # Now we need to add the new "participants" list to the participants list in the csv for the right session
        # already_registered_list = list(map(int, already_registered.split(',')))
        # Combine the two lists using extend
        # combined_attendees = participants.copy()
        # combined_attendees.extend(already_registered_list)
        # already_registered_list = list(already_registered)
        # already_registered_list.extend(participants)
        # combined_attendees = already_registered + participants
        # print(combined_attendees)
        session_df.at[row_index_sessionID, 'participants'] = already_registered
        session_df.to_csv(training_session_path, index=False)
        print(f"\nExcellent! We have added those refugees to session {sessionID}. See below. ")
        print(session_df.to_markdown(index=False))
    except FileNotFoundError as e:
        logging.critical(f"Error: {e}. One of the data files not found when adding a refugee to a session.")
        print(f"\nTraining session data file is not found or is damaged."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"\nOne of the data files is not found or is damaged for adding a refugee to a system."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")


def remove_refugee_from_session():
    try:
        refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
        ref_df = pd.read_csv(refugee_csv_path)
        training_session_path = Path(__file__).parents[0].joinpath("data/trainingSessions.csv")
        session_df = pd.read_csv(training_session_path)
        logging.info("Refugee and session data files loaded successfully when removing a refugee from a session.")
        print("Looks like you're looking to remove a refugee from one of the sessions!")
        length_session_df = pd.read_csv(training_session_path)["sessionID"].tolist()
        if len(length_session_df) == 0:
            print("Oh no! No sessions created yet! Taking you back...")
            return
        print(session_df.to_markdown(index=False))
        while True:
            sessionID = input("\n\nFrom the list above, enter the session ID for the "
                              "skills session you want remove a participant from. Or enter RETURN to go back: ")
            if sessionID.lower() == 'return':
                return
            try:
                if sessionID.strip() and sessionID.strip().isdigit() and session_df['sessionID'].eq(
                        int(sessionID)).any():
                    break
                else:
                    print("\n\nSorry - that's not a valid session ID. Pick again. ")
                logging.info("Successfully converted user input to int type.")
            except ValueError as e:
                logging.info("Invalid user input when selecting session ID")
                print(f"Error: {e}"
                      "\nPlease enter an integer or one of the specified exit options.")
        row_index_sessionID = session_df[session_df['sessionID'] == int(sessionID)].index[0]
        already_registered = session_df.at[row_index_sessionID, 'participants']
        participants = []
        while True:
            print("\n", already_registered)
            rid = input(f"\n\nFrom the above list, enter the Refugee ID for the person you want to remove from session "
                        f"{sessionID}\nEnter DONE when you are finished, or return to cancel and go back: ")
            if rid.lower() == "return":
                return
            if rid.lower() == "done":
                break
            try:
                if rid not in already_registered:
                    print(f"\nThat refugee isn't registered to attend this session, anyway.")
                    continue
                elif rid in participants:
                    print("\nYou've already just removed that refugee from this session.")
                    continue
                logging.info("Successfully converted user input to int type.")
                if rid in already_registered:
                    print(f"\nRemoving refugee with id {rid} from skills session {sessionID}. \n\n")
                    participants.append(rid)
                else:
                    print("\n\nSorry - that refugee ID doesn't exist. Pick again.")
                    continue
            except ValueError as e:
                logging.info("Invalid user input when selecting refugee ID to remove from session.")
                print(f"Error: {e}"
                      "\nPlease enter an integer or one of the specified exit options.")

        # Now we need to remove the new "participants" from the participants list in the csv for the right session
        already_registered_list = list(already_registered)
        print(already_registered)
        combined_string = ''.join(already_registered_list)
        already_registered_cleaned_list = [int(match.group()) for match in re.finditer(r'\d+', combined_string)]
        participants_cleaned = [int(participant.strip("'")) for participant in participants]
        updated_attendees = [num for num in already_registered_cleaned_list if num not in participants_cleaned]
        session_df.at[row_index_sessionID, 'participants'] = updated_attendees
        session_df.to_csv(training_session_path, index=False)
        print(f"\nExcellent! We have removed refugee(s) {participants} from session {sessionID}. See below. ")
        print("\n", session_df.to_markdown(index=False))
    except FileNotFoundError as e:
        logging.critical(f"Error: {e}. One of the data files not found when removing a refugee from a session.")
        print(f"\nTraining session data file is not found or is damaged."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"\nOne of the data files is not found or is damaged for removing a refugee from a session."
              f"\nPlease contact admin for further assistance."
              f"\n{e}")


def get_export_file_path():
    try:
        while True:
            user_input = input(
                "Enter 'X' for us to place your report in our data folder."
                "\n\n***You will see this when you next log back in or after you "
                "stop running the program***\n\n(Or Enter RETURN to go back).\n")

            if user_input.lower() == 'return':
                return None
            elif user_input.lower() == 'x':
                file_path = Path(__file__).parent
                print(file_path)
                index = 1
                file_path = file_path.parent.joinpath(f"refugee_data_export1.csv")
                while file_path.is_file():
                    index += 1
                    file_path = file_path.parent.joinpath(f"refugee_data_export{index}.csv")
                    print(file_path)
                break
            else:
                print("Sorry. Didn't catch that. Try again.")
                break
        return file_path

    except Exception as e:
        logging.info("File path options entered by user causing issue.")
        print(f"Looks like that file path didn't work, causing error {e}. Don't worry - we're redirecting you back.")
        return


def admin_export_refugees_to_csv():
    try:
        file_path = get_export_file_path()
        if file_path == None:
            return
        print(file_path)
        refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
        ref_df = pd.read_csv(refugee_csv_path)
        logging.info("Successfully loaded refugee csv for admin exporting refugee csv file.")
        camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        camp_df = pd.read_csv(camp_csv_path)
        logging.info("Successfully loaded camp csv file for reporting on refugees in event.")
        event_csv_path = Path(__file__).parents[0].joinpath("data/event.csv")
        event_df = pd.read_csv(event_csv_path, converters={'ongoing': str})
        logging.info("Successfully loaded event csv file for reporting on refugees in event.")
        print(ref_df.to_markdown(index=False))
        print("\nWe can print out a report of refugees categorised by event, camp, or report on all refugees "
              "in the system.\n")
        while True:
            ref_filter = input("Please select your preferred filter by entering one of the below options:"
                               "\nEVENT,\nCAMP,\n* (for all),\nor RETURN: ")
            refugees = []
            if ref_filter.lower() == 'return':
                return
            elif ref_filter.lower() == 'camp':
                while True:
                    campID = input("\nEnter the camp that you want a report of refugees on: ")
                    if campID.lower() == 'return':
                        return
                    try:
                        campID = int(campID)
                        if camp_df['campID'].eq(campID).any():
                            break
                        else:
                            print("\nSorry - that camp doesn't exist in our system!")
                    except Exception as e:
                        logging.critical(f"Unexpected error when filtering refugees by camp"
                                         f"for reporting function, with error {e}.")
                        print("\nInvalid input. Must enter an integer or one of the specified exit options.")
                refugees_in_camp = ref_df[ref_df['campID'] == campID]
                print(f"Okay! We're getting all the refugees which are in camps within camp {campID}.\n"
                      f"----------------------------------------------------------------------------------\n")
                for index, row in refugees_in_camp.iterrows():
                    refugee_data = {
                        "refugeeID": row["refugeeID"],
                        "campID": row["campID"],
                        "firstName": row["firstName"],
                        "lastName": row["lastName"],
                        "dob": row["dob"],
                        "gender": row["gender"],
                        "familyID": row["familyID"],
                    }
                    refugees.append(refugee_data)
                break
            elif ref_filter.lower() == 'event':
                print(event_df.to_markdown(index=False))
                while True:
                    eventID = input("Enter the event that you want a report of refugees on: ")
                    if eventID.lower() == 'return':
                        return
                    try:
                        eventID = int(eventID)
                        if event_df['eventID'].eq(eventID).any():
                            break
                        else:
                            print("\nSorry - that event doesn't exist in our system!")
                    except Exception as e:
                        logging.critical(f"Unexpected error when filtering refugees by event"
                                         f"for reporting function, with error {e}.")
                        print("\nInvalid input. Must enter an integer or one of the specified exit options.")
                camps_in_event = camp_df.loc[camp_df['eventID'] == eventID, 'campID'].tolist()
                refugees_in_associated_camps = ref_df[ref_df['campID'].isin(camps_in_event)]
                print(f"Okay! We're getting all the refugees which are in camps within eventID {eventID}. If none"
                      f"exist, you'll get an empty file.\n"
                      f"----------------------------------------------------------------------------------\n")
                for index, row in refugees_in_associated_camps.iterrows():
                    refugee_data = {
                        "refugeeID": row["refugeeID"],
                        "campID": row["campID"],
                        "firstName": row["firstName"],
                        "lastName": row["lastName"],
                        "dob": row["dob"],
                        "gender": row["gender"],
                        "familyID": row["familyID"],
                    }
                    refugees.append(refugee_data)
                break

            elif ref_filter == '*':
                for index, row in ref_df.iterrows():
                    refugee_data = {
                        "refugeeID": row["refugeeID"],
                        "campID": row["campID"],
                        "firstName": row["firstName"],
                        "lastName": row["lastName"],
                        "dob": row["dob"],
                        "gender": row["gender"],
                        "familyID": row["familyID"],
                    }
                    refugees.append(refugee_data)
                break
            else:
                print("Sorry! Didn't quite catch that. Let's try again or enter RETURN to go back.")
            if len(refugees) == 0:
                print("No data on the specified refugees to report on.")
                return
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = refugees[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(refugees)

            print(f"Refugee data exported to {file_path} successfully.")
    except Exception as e:
        logging.critical("Error with file when exporting refugee data to CSV on admin demand.")
        print(f"Error exporting data to CSV: {e}. Redirecting you back!")
        return


def recalculate_criticalvl(camp_id):
    lvl_arr = []
    mid_arr = []
    avg_lvl = 0

    ref_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
    medinfo_csv_path = Path(__file__).parents[0].joinpath("data/medicalInfo.csv")
    medtype_csv_path = Path(__file__).parents[0].joinpath("data/medicalInfoType.csv")

    df_r = pd.read_csv(ref_csv_path)
    df_m = pd.read_csv(medinfo_csv_path)
    df_l = pd.read_csv(medtype_csv_path)

    rid_arr = df_r.loc[df_r['campID'] == int(camp_id)]['refugeeID'].tolist()

    for i in rid_arr:
        mid = df_m.loc[df_m['refugeeID'] == i]['medicalInfoTypeID'].tolist()
        mid_arr += mid
    for j in mid_arr:
        lvl = df_l.loc[df_l['medicalInfoTypeID'] == j]['criticalLvl'].tolist()
        lvl_arr += lvl

    for n in lvl_arr:
        avg_lvl += n

    try:
        avg_lvl = avg_lvl / len(lvl_arr)
    except:
        avg_lvl = 1
    modify_csv_pandas("data/camp.csv", 'campID', int(camp_id), 'avgCriticalLvl', avg_lvl)


def help_center_page():
    while True:
        print("This Humanitarian Management System has been divided into functions for 2 roles: Admin and Volunteer."
              " Below you will find the relevant functions that each have access to & how they work.\n\n"
              "--------------------------------------------------------------------------"
              "--------------------------------------------------------------------------------------------------------"
              "--\n"
              "                                                                                   ADMIN\n"
              "---------------------------------------------------------------------------"
              "--------------------------------------------------------------------------------------------------------"
              "--\n"
              "\n\n1. Humanitarian Plan (Event) Management"
              "\n   - Here is where admin can create new events a.k.a. 'Plans' in the system. Remember to add in the "
              " camps associated with this event, otherwise you can't host any refugees!"
              "\n   - You can also edit all details about the event"
              "\n   - Note the difference between closing an event and deleting an event: Closing an event automatically"
              " closes all camps & deletes all refugees in that event but you can still see the event in\n     "
              "our records. Deleting an event from the system deletes its actual record, deletes refugees,"
              " and closes all associated camps & you cannot edit them."
              "\n   - You can display all events currently in the system"
              "\n\n2. Camp Management"
              "\n   - Only a user with Admin privilege can add new camps to the system. Adding an end date is optional."
              "\n   - A camp can be closed/deleted as a single entity, even if an event is still ongoing. This is in case of "
              "a potential health outbreak in the camp or natural disaster."
              "\n   - Only an Admin can close and delete camps. A camp can ONLY BE DELETED if its status has already been "
              "changed to 'CLOSED' to ensure that all resources have been unallocated from it."
              "\n   - The main difference between closing and deleting a camp is that a closed camp offers you the option"
              " of automatically assigning volunteers to another camp. A closed camp can also be reopened."
              "\n     A deleted camp automatically deletes refugees from the system and unassigns volunteers from any "
              "camp so that they are ready to be assigned to another camp."
              "\n   - Don't forget to check out the sophisticated data visualisation feature in camp management to get a graphical "
              "overview of all the camps, refugees, and resources in the system."
              "\n\n3. Refugee Management"
              "\n"
              "\n   - *** Our organisation believes it is essential to track the information of individual family members"
              " who seek our help so that we can best allocate\n         the resources based on an accurate understanding of"
              " the refugee population's health status, based on individual's conditions rather than over-allocating medical "
              "\n         supplies when they are already precious. We also know that sometimes it isn't possible to "
              "keep refugees together, so our platform can more accurately\n         capture this is ever the case "
              "arises. ***"
              "\n"
              "\n   - An admin can add and delete any refugee held in the system (whilst refugees have restrictions)"
              "\n   - Admins are able to BULK IMPORT a list of refugees using CSV."
              "\n   - An admin move any refugee from camp to camp"
              "\n   - We also encourage refugees to be kept together as a family unit. You may choose to move a refugee alone if"
              " essential, however we will prompt you to keep family units together\n     if the system detects a family unit "
              "and capacity allows for them to stay together."
              "\n   - Please note: Refugees MUST BE VACCINATED to be added to a camp which is of high risk (by policy) & a camp MUST HAVE ENOUGH CAPACITY "
              "to add more refugees to it. These restrictions have been\n     implemented in the system."
              "\n   - An admin is able to EXPORT a CSV file of the refugees in the system, either an entire overview"
              "or filtered by a specific camp or event."
              "\n\n4. Resource Management"
              "\n   - Our resource management section is very sophisticated. It includes:"
              "\n   - A SHOP: where admin adds into the system the resources which they have acquired. This initial "
              "'purchase' of items simply places them in the system, waiting to be allocated to\n            "
              "camps by a specified method."
              "\n   - ALLOCATION: Resources can be allocated either manually or automatically."
              "\n                 - Manual allocation is where admin can specify amounts they wish to allocate and to which camps"
              "\n                 - Auto allocation is where the system's algorithms will calculate the average weighting of "
              "resources in camps as it is, as well as the population of refugees to\n                   ensure resources"
              "  are distributed in a balanced and 'equal' way proportionate to population."
              "\n                   which is the average health rating of its refugee population."
              "\n   - STATISTICS: Admin can see all current statistics on how resources are distributed."
              "\n\n5. Volunteer Account Management"
              "\n   - Admin is able to edit volunteer accounts, display an overview of them, deactivate or remove"
              "volunteer accounts."
              "\n\n6. Display Summary/Statistics"
              "\n   - Here admins can get a tabular overview of all events categorised by current, future and closed."
              "\n\n7/8.Account Edit & View"
              "\n   - Admin can modify their own account details & view them"
              "\n\n9. Open MessageBox"
              "\n   - Users can send and read messages to/from one another using our MessageBox system."
              "\n\n\n\n--------------------------------------------------------------------------"
              "-------------------------------------------------------------------------------------------------------"
              "----\n"
              "                                                                                  VOLUNTEER\n"
              "---------------------------------------------------------------------------"
              "-------------------------------------------------------------------------------------------------------"
              "----\n"
              "\n\n1. Join/Change Camp"
              "\n   - A volunteer MUST join a camp to be able to add/delete a refugee to/from a camp. We also need "
              "to know which camp's resources to display to them. "
              "\n   - If a volunteer is assigned to a camp which is closed, they will be automatically assigned to another"
              " camp by admin or can stay assigned to that original camp if closure is deemed temporary."
              "\n   - If a volunteer is assigned to a camp which is deleted, they will automatically be unassigned from "
              "any camp so that they can join another camp of their choosing."
              "\n\n2. Camp Management"
              "\n   - Volunteer can add refugees ONLY to their own camp. "
              "\n   - Please note: Refugees MUST BE VACCINATED to be added to a camp (by policy) & a camp MUST HAVE ENOUGH CAPACITY "
              "to add more refugees to it. These restrictions have been implemented\n     in the system."
              "\n   - Refugees can only be moved to a camp within the same event as they are currently registred in"
              "\n   - We also encourage refugees to be kept together as a family unit. You may choose to move a refugee alone if"
              " essential, however we will prompt you to keep family units together\n     if the system detects a family unit "
              "and capacity allows for them to stay together."
              "\n   - Volunteer can make amendments to the camp they are assigned to"
              "\n   - Volunteer can display camp information & resources"
              "\n   - Volunteer can ACCESS LEGAL ADVICE links for supporting refugees better "
              "whilst the organisation is building its own legal support team."
              "\n   - REFUGEE SKILLS SESSIONS:"
              "\n                              - Volunteers can register refugee skills sessions where they select a topic and date"
              "\n                                for an informative session to upskill refugees."
              "\n                              - Refugees from any camps within the same event as the hosted session can attend"
              "\n                                However, you cannot add refugees from outside the event."
              "\n                              - Refugees can be added at time of event creation or afterwards. They can also be removed."
              "\n                              - Sessions can be deleted from the system"
              "\n   - Don't forget to check out the sophisticated data visualisation feature in camp management to get a graphical "
              "overview of all the camps, refugees, and resources in the system."
              "\n\n3/4.Edit & View Account Information"
              "\n   - Volunteer can edit and view their own personal account information"
              "\n\n5. Open MessageBox"
              "\n   - Users can send and read messages to/from one another using our MessageBox system."
              "\n\n\n *** Look out for our return prompt instructions throughout the application if ever you change "
              "your mind about a process! ***"

              )

        input("\n\nEnter anything when you're ready to exit this page & return back to the start menu: ")
        return


def check_vol_assigned_camp(username):
    csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
    df = pd.read_csv(csv_path)
    # check if volunteer is already assigned to a camp, if no exit to menu
    cid = df.loc[df['username'] == username]['campID'].tolist()[0]
    # check if volunteer user already join a camp
    if cid == 0:
        print("You must first join a camp!")
    return cid


def edit_vol_end():
    while True:
        user_input = input("Would you like to change other information (yes or no)? ")
        if user_input.lower() != 'yes' and user_input.lower() != 'no':
            print("Must enter yes or no!")
            continue
        if user_input.lower() == 'yes':
            return False
        else:
            return True
