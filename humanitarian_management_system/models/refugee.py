import pandas as pd
from humanitarian_management_system.helper import modify_csv_pandas, validate_user_selection
from humanitarian_management_system.models import Event
from humanitarian_management_system.views import VolunteerView
from humanitarian_management_system import helper
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

        self.ref_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
        self.camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        self.medinfo_csv_path = Path(__file__).parents[1].joinpath("data/medicalInfo.csv")
        self.medtype_csv_path = Path(__file__).parents[1].joinpath("data/medicalInfoType.csv")
    

    def add_refugee_from_user_input(self, cid):
        """Method to add the information of a newly added refugee in our system to the csv file"""
        # keep track of refugee id
        id_arr = pd.read_csv(self.ref_csv_path)["refugeeID"].tolist()

        if len(id_arr) == 0:
            rid = 0
        else:
            rid = int(id_arr.pop())

        rid += 1

        # keep track of refugee population of a camp
        df = pd.read_csv(self.camp_csv_path)
        ref_pop = df.loc[df['campID'] == cid]['refugeePop'].tolist()[0]

        # pass data to refugee csv
        Refugee.refugee_data = [[rid, int(cid), self.firstName, self.lastName, self.dob, self.gender, self.family_id]]
        ref_df = pd.DataFrame(Refugee.refugee_data,
                              columns=['refugeeID', 'campID', 'firstName', 'lastName', 'dob', 'gender', 'familyID'])

        ref_df.to_csv(self.ref_csv_path, mode='a', index=False, header=False)

        # update refugee population of a camp by 1
        ref_pop += 1
        modify_csv_pandas("data/camp.csv", 'campID', cid, 'refugeePop', ref_pop)

        self.pass_refugee_medical_info(rid, cid)

    def pass_refugee_medical_info(self, rid, cid):

        df = pd.read_csv(self.medinfo_csv_path)

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

        with open(self.medinfo_csv_path, 'a') as f:
            med_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

        self.calculate_avg_critical_lvl(cid)

    def calculate_avg_critical_lvl(self, cid):
        # calculate the average medical critical lvl of a camp based on the individual refugee's critical lvl
        lvl_arr = []
        mid_arr = []
        avg_lvl = 0

        df_r = pd.read_csv(self.ref_csv_path)
        df_m = pd.read_csv(self.medinfo_csv_path)
        df_l = pd.read_csv(self.medtype_csv_path)

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

    def edit_refugee_info(self, user, cid):
        """
        To edit refugee profile except campID as that belongs to Martha's move refugee method.
        """
        id_arr = []
        # use this when comparing user newly input refugee id against existing refugee id
        id_arr_temp = []
        date_format = '%d/%m/%Y'

        df_i = pd.read_csv(self.ref_csv_path)['refugeeID'].tolist()
        df = pd.read_csv(self.ref_csv_path)

        for i in df_i:
            id_arr.append(i)
            id_arr_temp.append(i)

        # if no refugees, exit to menu
        if len(df_i) == 0:
            print("No refugees created yet.")
            return

        if user == 'admin':
            # get all existing active refugees
            print("Here it displays a list of info for all existing refugees")
            Event.display_events(df)
        else:
            # refugees are camp dependent according to volunteer's assigned camp
            filtered_df = df[df['campID'] == cid]
            if filtered_df.empty:
                print("\nNo refugees in this camp yet.")
                return

            df_i = df.loc[df['campID'] == cid]['refugeeID']
            id_arr = df_i.tolist()
            print(f"Here it displays a list of info for all existing refugees in camp {cid}")
            Event.display_events(filtered_df)

        while True:
            try:
                ref_id = input("\nPlease select a refugee ID you would like to change: ")

                if ref_id == 'RETURN':
                    return

                if int(ref_id) not in id_arr:
                    print("Invalid refugee ID entered!")
                    continue
                else:
                    break
            except ValueError:
                print("Invalid refugee ID entered!")
                continue

        VolunteerView.display_edit_refugee_menu()
        user_selection = validate_user_selection(VolunteerView.get_edit_refugee_options())

        # if user_selection == '1':
        #     print("Sorry, you can't change the refugeeID - it's fixed! Taking you back...")
        #     return
            # old_id = df.loc[df['refugeeID'] == int(ref_id)]['refugeeID'].tolist()[0]
            # print(f"Current refugee ID is {old_id}")
            # while True:
            #     try:
            #         new_value = input("\nEnter new refugee ID: ")
            #
            #         if new_value == 'RETURN':
            #             return
            #
            #         if int(new_value) in id_arr_temp:
            #             print("Can't use an existing refugee ID!")
            #             continue
            #         else:
            #             break
            #     except ValueError:
            #         print("Can't use an existing refugee ID!")
            #         continue
            # self.modify_csv("data/refugee.csv", 'refugeeID', int(ref_id), 'refugeeID',
            #                 int(new_value), user, cid)
            # helper.modify_csv_pandas("data/medicalInfo.csv", 'refugeeID', int(old_id),
            #                          'refugeeID', int(new_value))
            #
            # # reorder refugee ID after ID changed
            # csv_path_r = Path(__file__).parents[1].joinpath("data/refugee.csv")
            # df_r = pd.read_csv(csv_path_r)
            #
            # df_r.sort_values('refugeeID', inplace=True)
            # df_r.to_csv(Path(__file__).parents[1].joinpath("data/refugee.csv"), index=False)

        if user_selection == '1':
            print(f"Current refugee first name is {df.loc[df['refugeeID'] == int(ref_id)]['firstName'].tolist()[0]}")
            while True:
                new_value = input("\nEnter new first name: ")

                if new_value == 'RETURN':
                    return

                if not new_value.isalpha():
                    print("Must be alphabetic values!")
                    continue
                else:
                    break
            df_ref = pd.read_csv(Path(__file__).parents[1].joinpath("data/refugee.csv"))
            df_ref.loc[df_ref['refugeeID'] == int(ref_id), 'firstName'] = new_value
            df_ref.to_csv(Path(__file__).parents[1].joinpath("data/refugee.csv"), index=False)

        if user_selection == '2':
            print(f"Current refugee last name is {df.loc[df['refugeeID'] == int(ref_id)]['lastName'].tolist()[0]}")
            while True:
                new_value = input("\nEnter new last name: ")

                if new_value == 'RETURN':
                    return

                if not new_value.isalpha():
                    print("Must be alphabetic values!")
                    continue
                else:
                    break
            df_ref = pd.read_csv(Path(__file__).parents[1].joinpath("data/refugee.csv"))
            df_ref.loc[df_ref['refugeeID'] == int(ref_id), 'lastName'] = new_value
            df_ref.to_csv(Path(__file__).parents[1].joinpath("data/refugee.csv"), index=False)

        if user_selection == '3':
            print(f"Current refugee first DOB is {df.loc[df['refugeeID'] == int(ref_id)]['dob'].tolist()[0]}")
            while True:
                try:
                    # new_value = input("\nEnter date of birth (format: dd/mm/yyyy): ")
                    print("\nEnter date of birth (format: dd/mm/yyyy): ")
                    new_value = helper.not_too_old()
                    if new_value == 'RETURN':
                        return
                    datetime_object = datetime.datetime.strptime(new_value, date_format)
                    if datetime_object > datetime.datetime.now():
                        print("Birth date should be before current date and time")
                        continue
                    new_value = datetime_object.strftime(date_format)
                    break
                except ValueError:
                    print("\nInvalid date format entered.")
                    continue
            df_ref = pd.read_csv(Path(__file__).parents[1].joinpath("data/refugee.csv"))
            df_ref.loc[df_ref['refugeeID'] == int(ref_id), 'dob'] = new_value
            df_ref.to_csv(Path(__file__).parents[1].joinpath("data/refugee.csv"), index=False)

        if user_selection == '4':
            print(f"Current refugee gender is {df.loc[df['refugeeID'] == int(ref_id)]['gender'].tolist()[0]}")
            while True:
                new_value = input("\nEnter new gender (male, female or other): ")

                if new_value == 'RETURN':
                    return

                if new_value != 'male' and new_value != 'female' and new_value != 'other':
                    print("Must enter male, female or other!")
                    continue
                else:
                    break
            df_ref = pd.read_csv(Path(__file__).parents[1].joinpath("data/refugee.csv"))
            df_ref.loc[df_ref['refugeeID'] == int(ref_id), 'gender'] = new_value
            df_ref.to_csv(Path(__file__).parents[1].joinpath("data/refugee.csv"), index=False)

        if user_selection == '5':
            print(f"Current refugee family ID is {df.loc[df['refugeeID'] == int(ref_id)]['familyID'].tolist()[0]}")
            df_ref_display = df[['familyID', 'refugeeID', 'firstName', 'lastName']].sort_values(by=['familyID', 'refugeeID'])
            table = df_ref_display.to_markdown(index=False)
            print("\n" + table)
            while True:
                new_value = input("\nEnter new family ID: ")

                if new_value == 'RETURN':
                    return

                else:
                    try:
                        new_value = int(new_value)
                        break
                    except ValueError:
                        print("Must be a numerical value!")
                        continue
            df_ref = pd.read_csv(Path(__file__).parents[1].joinpath("data/refugee.csv"))
            df_ref.loc[df_ref['refugeeID'] == int(ref_id), 'familyID'] = new_value
            df_ref.to_csv(Path(__file__).parents[1].joinpath("data/refugee.csv"), index=False)

        if user_selection == 'R':
            return

    def modify_csv(self, csv_path, col, col_val, new, new_val, user, cid):
        print("Change has been made successfully!")
        modify_csv_pandas(csv_path, col, col_val, new, new_val)
        print("Is there any other changes you would like to make?")

        while True:
            user_input = input("Yes or No? ")
            if user_input.lower() != 'yes' and user_input.lower() != 'no':
                print("Must enter yes or no!")
                continue
            if user_input == 'yes':
                self.edit_refugee_info(user, cid)
            else:
                return
        return

    def display_info(self, user, cid):

        ref_df = pd.read_csv(self.ref_csv_path)
        medinfo_df = pd.read_csv(self.medinfo_csv_path)
        medtype_df = pd.read_csv(self.medtype_csv_path)

        ref_id_arr = []
        for i in ref_df['refugeeID'].tolist():
            ref_id_arr.append(str(i))

        if user == 'volunteer':
            ref_id_arr = []
            ref_df = ref_df.loc[ref_df['campID'] == cid]
            for i in ref_df['refugeeID'].tolist():
                ref_id_arr.append(str(i))

        joined_df_ref = pd.merge(ref_df, medinfo_df, on='refugeeID', how='inner')
        joined_df_med = pd.merge(medinfo_df, medtype_df, on='medicalInfoTypeID', how='inner')

        joined_df_total = pd.merge(joined_df_ref, joined_df_med, on='refugeeID', how='inner')
        joined_df_total.columns = ['Refugee ID', 'Camp ID', 'First name', 'Last name', 'DOB', 'Gender', 'Family ID',
                                   'medicalInfoID_x', 'medicalInfoTypeID_x', 'Description', 'Is vaccinated?',
                                   'medicalInfoID_y', 'medicalInfoTypeID_y', 'description_y', 'isVaccinated_y',
                                   'Condition', 'Critical level']

        Event.display_events(joined_df_total[['Refugee ID', 'Camp ID', 'First name', 'Last name', 'DOB', 'Gender',
                                              'Family ID']].sort_values('Refugee ID'))

        while True:
            user_input = input("Would you like to access the medical profile for a particular refugee (yes or no)? ")

            if user_input == 'RETURN':
                return

            if user_input.lower() == 'yes':
                self.display_medinfo(user, cid, joined_df_total, ref_id_arr)

            if user_input.lower() != 'yes' and user_input.lower() != 'no':
                print("Must enter yes or no!")
                continue
            if user_input.lower() == 'no':
                return
            break

    def display_medinfo(self, user, cid, joined_df_total, ref_id_arr):
        while True:
            id_input = input("Please enter the refugee ID whose medical profile you would like to see: ")
            if id_input == 'RETURN':
                return

            if id_input not in ref_id_arr:
                print("Invalid refugee ID entered!")
                continue

            df_med = joined_df_total.loc[joined_df_total['Refugee ID'] == int(id_input)]
            Event.display_events(
                df_med[['Refugee ID', 'First name', 'Last name', 'Description', 'Condition',
                        'Is vaccinated?', 'Critical level']].sort_values('Refugee ID'))

            while True:
                user_input = input("Would you like to exit (yes or no)? ")
                if user_input == 'RETURN':
                    return
                if user_input.lower() != 'yes' and user_input.lower() != 'no':
                    print("Must enter yes or no!")
                    continue
                if user_input.lower() == 'no':
                    self.display_info(cid, user)
                return
            return
