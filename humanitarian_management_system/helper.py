import re
import csv
from pathlib import Path
import pandas as pd
import datetime
import math
import logging




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

    return ["volunteer", "FALSE", "FALSE", username, password, first_name, last_name, email, phone, occupation, 0, 0, 0]


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
        if location.upper() == 'RETURN':
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
    csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
    df = pd.read_csv(csv_path)
    id_arr = df['campID'].tolist()

    if id_arr:
        campID = id_arr.pop() + 1
    else:
        campID = 1

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
    csv_path = Path(__file__).parents[0].joinpath("data/roleType.csv")
    index = pd.read_csv(csv_path)["roleID"].tolist()
    role = pd.read_csv(csv_path)["name"]

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
    df = pd.read_csv(csv_path)
    # ensure we only display camp(s) that are part of an active plan
    data = df[['ongoing', 'eventID']]
    active_id = []

    for i in range(len(data)):
        if data['ongoing'].iloc[i] == 'True' or data['ongoing'].iloc[i] == 'Yet':
            active_id.append(data['eventID'].iloc[i])

    return active_id, df


def display_camp_list():
    index = []

    csv_path = Path(__file__).parents[0].joinpath("data/eventTesting.csv")
    active_id = extract_active_event(csv_path)[0]
    df_e = pd.read_csv(csv_path)

    csv_path_c = Path(__file__).parents[0].joinpath("data/camp.csv")
    df_c = pd.read_csv(csv_path_c)

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
    csv_path = Path(__file__).parents[0].joinpath("data/resourceStock.csv")
    df = pd.read_csv(csv_path)

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

    res_id = pd.read_csv(csv_path)['resourceID'].tolist()

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
            dob = input("\nEnter date of birth (format: dd/mm/yyyy): ")
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

    csv_path = Path(__file__).parents[0].joinpath("data/medicalInfoType.csv")

    med_id = pd.read_csv(csv_path)["medicalInfoTypeID"].tolist()
    df = pd.read_csv(csv_path)
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
    print("\nYOU ARE REQUESTING TO MOVE A REFUGEE. Enter RETURN if you didn't mean to select this. Otherwise, proceed"
          " as instructed.\n")
    try:
        refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
        ref_df = pd.read_csv(refugee_csv_path)
        logging.info("Refugee file loaded successfully for moving a refugee around camps.")
        print(ref_df.to_string(index=False))
        # checking input is valid according to refugee IDs in database
        while True:
            rid = input("\nFrom the list above enter the refugee ID for the refugee you wish to move another camp: ")
            if rid == "RETURN":
                return
            elif rid.strip() and rid.strip().isdigit() and ref_df['refugeeID'].eq(int(rid)).any():
                break
            else:
                print("\nSorry - that refugee ID doesn't exist. Pick again.")
        camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        camp_df = pd.read_csv(camp_csv_path)
        logging.info("Camp file loaded successfully for moving a refugee around camps.")
        active_camp_df = camp_df[camp_df['status'] == 'open']
        old_camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
        eventID = camp_df.loc[camp_df['campID'] == int(old_camp_id), 'eventID'].iloc[0]
        camps_in_event = camp_df.loc[camp_df['eventID'] == eventID, 'campID'].tolist()
        active_and_in_event = camp_df[(camp_df['status'] == 'open') & (camp_df['campID'].isin(camps_in_event))]
        # checking input is valid according to refugee IDs in database
        while True:
            print("\n", active_and_in_event.to_string(index=False))
            camp_id = input("\nFrom the above list, which is a list of ACTIVE camps\n"
                            "which are part of the same event as this refugee's original camp,\n"
                            "enter the campID of the camp you want to move this refugee to: ")
            if camp_id.lower() == "return":
                return
            try:
                camp_id = int(camp_id)
                if camp_id == old_camp_id:
                    print("\nLooks like that's the same camp this refugee is already in. Try again "
                          "or if there are no other camps\navailable, enter RETURN to go back.")
                elif (camp_id in active_camp_df['campID'].values) and (camp_id in camps_in_event):
                    # Need to do a final check to see if new camp's refugeePop + 1 is < new camp's refugeeCapacity
                    row_index_new_camp = camp_df[camp_df['campID'] == int(camp_id)].index
                    new_potential_refugee_pop = (camp_df.at[row_index_new_camp[0], 'refugeePop'])
                    new_camp_capacity = camp_df.at[row_index_new_camp[0], 'refugeeCapacity']
                    if (new_potential_refugee_pop + 1) <= new_camp_capacity:
                        break
                    else:
                        print("\n\nOh no! The new camp you've selected doesn't have the capacity to handle another refugee. "
                              f"Camp {camp_id} has a current population of {new_potential_refugee_pop} and a capacity of "
                              f"{new_camp_capacity}.\nLet's go again.\n")
                else:
                    print("\nSorry - that camp ID doesn't exist (anymore). Pick again.")
            except ValueError:
                print("\nInvalid input. Please enter a valid campID or type RETURN to go back: ")
        # Need to point out to user if this refugee is part of a family. Do they want to move the entire family?
        refugee_family_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'familyID'].iloc[0]
        related_family_members = ref_df[ref_df['familyID'] == int(refugee_family_id)]
        total_family_members = len(related_family_members)
        while True:
            if total_family_members != 0:
                print("\n----HOLD ON!---- \nThis refugee is part of a family unit (see below).\n")
                print(related_family_members.to_string(index=False))
                user_input = input("\nAre you sure you want to move this refugee alone? Enter YES (to move"
                                   " alone), NO (to move as a family unit), or RETURN (to exit): ")
                if user_input.lower() == 'yes':
                    break
                elif user_input.lower() == 'no':
                    print("Okay. We're going to move the family as a unit."
                          "\n****We're going to allow the whole family to move together, regardless of capacity. However,"
                          "please remember to manually remove some refugees from\nthis camp to a less populated one "
                          "if capacity is maxed out! We'll show you how many to remove if needed at the end.****\n")
                    related_family_members_list = related_family_members['refugeeID'].tolist()
                    # print(related_family_members_list)
                    for index, row in related_family_members.iterrows():
                        rid = row['refugeeID']
                        old_camp_id = row['campID']
                        # old_camp_id = ref_df.loc[ref_df['campID'] == int(i), 'campID'].iloc[0]
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
                        # camp_df.to_csv(camp_csv_path, mode='a', index=False, header=False)
                        # modify_csv_value(camp_df, row, "refugeePop", camp_id)
                        print(
                            f"\nTransfer for refugee {rid} complete. We have reassigned the refugee from camp {old_camp_id} "
                            f"to camp {camp_id}."
                            f"Additionally, the population of both camps has been adjusted accordingly. See below.")
                        print("\n", camp_df[camp_df['campID'] == int(old_camp_id)].to_string(index=False), "\n")
                        print("\n", camp_df[camp_df['campID'] == int(camp_id)].to_string(index=False), "\n")
                    print("\n Great. That's all that family transferred as a unit.")
                    row_index_new_camp = camp_df[camp_df['campID'] == int(camp_id)].index
                    new_refugee_pop = (camp_df.at[row_index_new_camp[0], 'refugeePop'])
                    new_camp_capacity = camp_df.at[row_index_new_camp[0], 'refugeeCapacity']
                    if new_refugee_pop > new_camp_capacity:
                        overflow_amount = (new_refugee_pop - new_camp_capacity)
                        print(f"Uh oh! Capacity overflow. You need to remove {overflow_amount} refugee(s) from camp {camp_id}")
                    else:
                        print("Great. No capacity overflow detected.")
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
        # camp_df.to_csv(camp_csv_path, mode='a', index=False, header=False)
        # modify_csv_value(camp_df, row, "refugeePop", camp_id)
        print(f"\nTransfer complete. We have reassigned the refugee from camp {old_camp_id} to camp {camp_id}."
              f"Additionally, the population of both camps has been adjusted accordingly. See below.")
        print("\n", camp_df[camp_df['campID'] == int(old_camp_id)].to_string(index=False), "\n")
        print("\n", camp_df[camp_df['campID'] == int(camp_id)].to_string(index=False), "\n")
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
        print(ref_df.to_string(index=False))
        # checking input is valid according to refugee IDs in database
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
                #     Deleting the refugee from the database
                ref_df.drop(ref_df[ref_df['refugeeID'] == int(rid)].index, inplace=True)
                ref_df.reset_index(drop=True, inplace=True)
                ref_df.to_csv(refugee_csv_path, index=False)
                print(
                    f"\nOkay. You have permanently deleted refugee #{rid} from the system. Their old associated camp population "
                    f"has also been adjusted accordingly.")
                print("\nRefugee DataFrame after deletion:")
                print(ref_df)
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
    logging.debug("Legal Advice Page starts up.")
    print("Below are links to our partner legal charities to offer legal support to refugees whilst we work on "
          "\nbuilding our own team."
          "\nClicking on these links will direct you to a web page. \nYou will have to return back "
          "to the application manually.")

    links = [
        ("Refugee Council Legal Advice Site", "https://www.refugeecouncil.org.uk/"),
        ("Red Cross Legal Support", "https://www.redcross.org.uk/"),
        ("Refugee Legal Centre", "https://www.refugee-legal-centre.org.uk/"),
        ('RETURN', '')
    ]
    while True:
        for i, (name, url) in enumerate(links, 1):
            print(f"{i}. {name}: {url}")
        user_input = input("Click on one of the above links or enter RETURN to leave this menu: ")
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
                elif user_input == '2':
                    return
                else:
                    print("\nSorry! Invalid input.")
            else:
                print("\n", session_df.to_string(index=False))
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
        print(role_df['name'].to_string(index=False))
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
                        logging.debug("Date input for creating a session was in the past so invalid.")
                except ValueError:
                    logging.debug("Input date for creating a training session was invalid form.")
                    print("\nInvalid date format. Please use the format YYYY-MM-DD. Or enter RETURN to quit.")
        while True:
            camp = input("\nEnter the campID of the camp you will be holding the session at: ")
            if camp.lower() == "return":
                return
            try:
                camp_id = int(camp)
                if camp_df['campID'].eq(camp_id).any():
                    break
                else:
                    print("\nSorry - that camp doesn't exist in our system. Pick again or enter RETURN.")
            except ValueError:
                print("\nInvalid input. Please enter a valid integer for campID or type 'RETURN' to go back.")
        eventID = camp_df.loc[camp_df['campID'] == int(camp), 'eventID'].iloc[0]
        camps_in_event = camp_df.loc[camp_df['eventID'] == eventID, 'campID'].tolist()
        refugees_in_associated_camps = ref_df[ref_df['campID'].isin(camps_in_event)]
        participants = []
        while True:
            print("\n", refugees_in_associated_camps.to_string(index=False))
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

        training_session_data = [int(sessionID), occupation, topic, date, camp, participants, eventID]
        session_df.loc[len(session_df)] = training_session_data
        session_df.to_csv(training_session_path, index=False)
        added_session = session_df[session_df['sessionID'] == sessionID]
        print(added_session.to_string(index=False))
        print("\n---------------------------------------------------------------------------------")
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
        print("\nLooks like you want to cancel or delete a session. That's a shame! See current sessions in the system.")
        print("\n", session_df.to_string(index=False))
        # session_df.set_index('sessionID', inplace=True)
        while True:
            sessionID = input("Enter RETURN now if you have changed your mind, or enter the sessionID you want to cancel: ")
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
            print(session_df.to_string(index=False))
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
        print(session_df.to_string(index=False))
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
        already_registered = session_df.at[row_index_sessionID, 'participants']
        eventID = session_df.at[row_index_sessionID, 'eventID']
        camp_csv_path = Path(__file__).parents[0].joinpath("data/camp.csv")
        camp_df = pd.read_csv(camp_csv_path)
        camps_in_event = camp_df.loc[camp_df['eventID'] == eventID, 'campID'].tolist()
        refugees_in_associated_camps = ref_df[ref_df['campID'].isin(camps_in_event)]
        # ----------  adding only refugees in this event! ---------
        participants = []
        while True:
            try:
                print("\n",refugees_in_associated_camps.to_string(index=False))
                rid = input(f"\n\nFrom the above list, which are refugees in the same event as that which this session is "
                            f"being held,\nenter the Refugee ID for who you want to add to session {sessionID}"
                            "\nEnter DONE when you are finished, or return to cancel and go back: ")
                if rid.lower() == "return":
                    return
                if rid.lower() == "done":
                    break
                elif rid in already_registered:
                    print(f"\nDon't worry. That refugee is already down to attend this session.")
                elif int(rid) in participants:
                    print("\nYou've already just added that refugee.")
                elif rid.strip() and rid.strip().isdigit() and ref_df['refugeeID'].eq(int(rid)).any():
                    print(f"\n\nAdding refugee with id {rid} to skills session {sessionID}. \n\n")
                    participants.append(int(rid))
                else:
                    print("\n\nSorry - that refugee ID doesn't exist. Pick again.")
            except Exception as e:
                logging.critical(f"Unexpected error when adding a refugee to a training session from invalid user"
                                 f"input: {e}")
                print("\nInvalid input. Must enter an integer or one of the specified exit options.")
        # Now we need to add the new "participants" list to the participants list in the csv for the right session
        # already_registered_list = list(map(int, already_registered.split(',')))
        # Combine the two lists using extend
        # combined_attendees = participants.copy()
        # combined_attendees.extend(already_registered_list)
        combined_attendees = [already_registered] + participants
        session_df.at[row_index_sessionID, 'participants'] = combined_attendees
        session_df.to_csv(training_session_path, index=False)
        print(f"\nExcellent! We have added refugee(s) {participants} to session {sessionID}. See below. ")
        print(session_df.to_string(index=False))
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
        print(session_df.to_string(index=False))
        while True:
            sessionID = input("\n\nFrom the list above, enter the session ID for the "
                              "skills session you want remove a participant from. Or enter RETURN to go back: ")
            if sessionID.lower() == 'return':
                return
            elif sessionID.strip() and sessionID.strip().isdigit() and session_df['sessionID'].eq(int(sessionID)).any():
                break
            else:
                print("\n\nSorry - that's not a valid session ID. Pick again. ")
        row_index_sessionID = session_df[session_df['sessionID'] == int(sessionID)].index[0]
        already_registered = session_df.at[row_index_sessionID, 'participants']
        participants = []
        while True:
            try:
                print("\n",already_registered)
                rid = input(f"\n\nFrom the above list, enter the Refugee ID for the person you want to remove from session "
                            f"{sessionID}\nEnter DONE when you are finished, or return to cancel and go back: ")
                if rid.lower() == "return":
                    return
                if rid.lower() == "done":
                    break
                elif rid not in already_registered and ref_df['refugeeID'].eq(int(rid)).any():
                    print(f"\nThat refugee isn't registered to attend this session, anyway.")
                elif any(participant == int(rid) for participant in participants):
                    print("\nYou've already just removed that refugee from this session.")
                elif rid.strip() and rid.strip().isdigit() and ref_df['refugeeID'].eq(int(rid)).any():
                    print(f"\nRemoving refugee with id {rid} from skills session {sessionID}. \n\n")
                    participants.append(int(rid))
                else:
                    print("\n\nSorry - that refugee ID doesn't exist. Pick again.")
            except Exception as e:
                logging.critical(f"Unexpected error when removing refugee from training session from invalid user"
                                 f"input: {e}")
                print("\nInvalid input. Must enter an integer or one of the specified exit options.")
        # Now we need to remove the new "participants" from the participants list in the csv for the right session
        already_registered_list = list(already_registered)
        print(already_registered)
        combined_as_string = ''.join(already_registered_list)
        already_registered_cleaned_list = [int(match.group()) for match in re.finditer(r'\d+', combined_as_string)]
        # participants_cleaned = [int(participant.strip("'")) for participant in participants]
        updated_attendees = [num for num in already_registered_cleaned_list if num not in participants]
        session_df.at[row_index_sessionID, 'participants'] = updated_attendees
        session_df.to_csv(training_session_path, index=False)
        print(f"\nExcellent! We have removed refugee(s) {participants} from session {sessionID}. See below. ")
        print("\n", session_df.to_string(index=False))
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


def check_vol_assigned_camp(username):
    csv_path = Path(__file__).parents[0].joinpath("data/user.csv")
    df = pd.read_csv(csv_path)
    # check if volunteer is already assigned to a camp, if no exit to menu
    cid = df.loc[df['username'] == username]['campID'].tolist()[0]
    # check if volunteer user already join a camp
    if math.isnan(cid):
        print("You must first join a camp!")
        return
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
