import pandas as pd
from humanitarian_management_system.helper import modify_csv_pandas, validate_user_selection
from humanitarian_management_system.models import Event
from humanitarian_management_system.views import VolunteerView
import datetime

from pathlib import Path


class Refugee:
    refugee_data = []
    med_data = []

    def __init__(self, family_id, firstName, lastName, dob, gender, medical_condition_id, medical_description,
                 is_vaccinated):
        """Need to prompt user to fill in camp ID, medical condition, family name.
        Refugee is instantiated as not_vaccinated unless they are specified as True
        (something to add in User Manual??)"""
        self.firstName = firstName
        self.lastName = lastName
        self.dob = dob
        self.gender = gender
        self.family_id = family_id
        self.medical_condition_id = medical_condition_id
        self.medical_description = medical_description
        self.is_vaccinated = is_vaccinated
        # self.rid = rid
        # Refugee.total_number += 1

    def add_refugee_from_user_input(self, cid):
        """Method to add the information of a newly added refugee in our system to the csv file"""
        # keep track of refugee id
        csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
        id_arr = pd.read_csv(csv_path)["refugeeID"].tolist()

        if len(id_arr) == 0:
            rid = 0
        else:
            rid = int(id_arr.pop())

        rid += 1

        # keep track of refugee population of a camp
        csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        df = pd.read_csv(csv_path)
        ref_pop = df.loc[df['campID'] == cid]['refugeePop'].tolist()[0]

        # pass data to refugee csv
        Refugee.refugee_data = [[rid, int(cid), self.firstName, self.lastName, self.dob, self.gender, self.family_id]]
        ref_df = pd.DataFrame(Refugee.refugee_data,
                              columns=['refugeeID', 'campID', 'firstName', 'lastName', 'dob', 'gender', 'familyID'])
        csv_path_a = Path(__file__).parents[1].joinpath("data/refugee.csv")
        with open(csv_path_a, 'a') as f:
            ref_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

        # update refugee population of a camp by 1
        ref_pop += 1
        modify_csv_pandas("data/camp.csv", 'campID', cid, 'refugeePop', ref_pop)

        self.pass_refugee_medical_info(rid, cid)

    def pass_refugee_medical_info(self, rid, cid):
        csv_path = Path(__file__).parents[0].joinpath("data/medicalInfo.csv")
        df = pd.read_csv(csv_path)

        id_arr = df["medicalInfoID"].tolist()
        if len(id_arr) == 0:
            mid = 0
        else:
            mid = int(id_arr.pop())
        mid += 1

        # pass data to medical info csv
        Refugee.med_data = [[mid, rid, self.medical_condition_id, self.medical_description, self.is_vaccinated]]
        med_df = pd.DataFrame(Refugee.med_data,
                              columns=['medicalInfoID', 'refugeeID', 'medicalInfoTypeID', 'description',
                                       'isVaccinated'])
        csv_path_a = Path(__file__).parents[1].joinpath("data/medicalInfo.csv")
        with open(csv_path_a, 'a') as f:
            med_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

        self.calculate_avg_critical_lvl(cid)

    def calculate_avg_critical_lvl(self, cid):
        # calculate the average medical critical lvl of a camp based on the individual refugee's critical lvl
        lvl_arr = []
        mid_arr = []
        avg_lvl = 0

        csv_path_r = Path(__file__).parents[1].joinpath("data/refugee.csv")
        df_r = pd.read_csv(csv_path_r)

        csv_path_m = Path(__file__).parents[1].joinpath("data/medicalInfo.csv")
        df_m = pd.read_csv(csv_path_m)

        csv_path_l = Path(__file__).parents[1].joinpath("data/medicalInfoType.csv")
        df_l = pd.read_csv(csv_path_l)

        rid_arr = df_r.loc[df_r['campID'] == int(cid)]['refugeeID'].tolist()

        for i in rid_arr:
            mid = df_m.loc[df_m['refugeeID'] == i]['medicalInfoTypeID'].tolist()
            mid_arr += mid
        for j in mid_arr:
            lvl = df_l.loc[df_l['medicalInfoTypeID'] == j]['criticalLvl'].tolist()
            lvl_arr += lvl

        for n in lvl_arr:
            avg_lvl += n

        avg_lvl = avg_lvl / len(lvl_arr)
        modify_csv_pandas("data/camp.csv", 'campID', int(cid), 'avgCriticalLvl', avg_lvl)

    @staticmethod
    def edit_refugee_info(user, cid):
        """
        To edit refugee profile except campID as that belongs to Martha's move refugee method.
        """
        id_arr = []
        date_format = '%d/%m/%Y'

        csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
        df_i = pd.read_csv(csv_path)['refugeeID'].tolist()
        df = pd.read_csv(csv_path)

        # if no refugees, exit to menu
        if len(df_i) == 0:
            print("No refugees created yet.")
            return

        if user == 'admin':
            # get all existing active refugees
            for i in df_i:
                id_arr.append(i)
            print("Here it displays a list of info for all existing refugees")
            Event.display_events(df)
        else:
            # refugees are camp dependent according to volunteer's assigned camp
            filtered_df = df[df['campID'] == cid]
            if filtered_df.empty:
                print("\nNo refugees in this camp yet.")
                return

            df_i = df.loc[df['campID'] == cid]['refugeeID'].tolist()

            for i in df_i:
                id_arr.append(i)
            print(f"Here it displays a list of info for all existing refugees in camp {cid}")
            Event.display_events(filtered_df)

        while True:
            try:
                ref_id = int(input("\nPlease select a refugee ID you would like to change: "))
                if ref_id not in id_arr:
                    print("Invalid refugee ID entered!")
                    continue
                if ref_id == 'RETURN':
                    return
                else:
                    break
            except:
                return

        VolunteerView.display_edit_refugee_menu()
        user_selection = validate_user_selection(VolunteerView.get_edit_refugee_options())

        if user_selection == '1':
            while True:
                try:
                    new_value = int(input("\nEnter new refugee ID "))
                    if new_value in id_arr:
                        print("Can't use an existing refugee ID!")
                        continue
                    if new_value == 'RETURN':
                        return
                    else:
                        break
                except:
                    return
            modify_csv_pandas("data/refugee.csv", 'refugeeID', ref_id, 'refugeeID', new_value)

        if user_selection == '2':
            while True:
                new_value = input("\nEnter new first name ")
                if not new_value.isalpha():
                    print("Must be alphabetic values!")
                    continue
                if new_value == 'RETURN':
                    return
                else:
                    break
            modify_csv_pandas("data/refugee.csv", 'refugeeID', ref_id, 'firstName', new_value)

        if user_selection == '3':
            while True:
                new_value = input("\nEnter new last name ")
                if not new_value.isalpha():
                    print("Must be alphabetic values!")
                    continue

                if new_value == 'RETURN':
                    return
                else:
                    break
            modify_csv_pandas("data/refugee.csv", 'refugeeID', ref_id, 'lastName', new_value)

        if user_selection == '4':
            while True:
                try:
                    new_value = input("\nEnter date of birth (format: dd/mm/yy): ")
                    if new_value == 'RETURN':
                        return
                    new_value = datetime.datetime.strptime(new_value, date_format)
                    break
                except ValueError:
                    print("\nInvalid date format entered.")
                    continue
            modify_csv_pandas("data/refugee.csv", 'refugeeID', ref_id, 'dob', new_value)

        if user_selection == '5':
            while True:
                new_value = input("\nEnter new gender (male, female or other) ")
                if new_value != 'male' or new_value != 'female' or new_value != 'other':
                    print("Must enter male, female or other!")
                    continue
                if new_value == 'RETURN':
                    return
                else:
                    break
            modify_csv_pandas("data/refugee.csv", 'refugeeID', ref_id, 'gender', new_value)

        if user_selection == '6':
            while True:
                try:
                    new_value = input("\nEnter new family ID ")
                    if not new_value.isnumeric():
                        print("Must be a numerical value!")
                        continue
                    if new_value == 'RETURN':
                        return
                    else:
                        break
                except:
                    return
            modify_csv_pandas("data/refugee.csv", 'refugeeID', ref_id, 'familyID', new_value)

        if user_selection == 'R':
            return

    @staticmethod
    def modify_csv(csv_path, col, col_val, new, new_val):
        print("Change has been made successfully!")
        modify_csv_pandas(csv_path, col, col_val, new, new_val)
        return


