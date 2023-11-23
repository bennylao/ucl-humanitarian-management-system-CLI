import pandas as pd
from humanitarian_management_system.helper import extract_data, modify_csv_value, modify_csv_pandas, extract_data_df
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
        self.rid = rid
        # Refugee.total_number += 1

    def add_refugee_from_user_input(self, cid):
        """Method to add the information of a newly added refugee in our system to the csv file"""
        # keep track of refugee id
        id_arr = extract_data("data/refugee.csv", "refugeeID").tolist()
        if len(id_arr) == 0:
            rid = 0
        else:
            rid = int(id_arr.pop())

        rid += 1

        # keep track of refugee population of a camp
        df = extract_data_df("data/camp.csv")
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
        id_arr = extract_data("data/medicalInfo.csv", "medicalInfoID").tolist()
        if len(id_arr) == 0:
            mid = 0
        else:
            mid = int(id_arr.pop())
        mid += 1

        # pass data to medicalinfo csv
        Refugee.med_data = [[mid, rid, self.medical_condition_id, self.medical_description, self.is_vaccinated]]
        med_df = pd.DataFrame(Refugee.med_data,
                              columns=['medicalInfoID', 'refugeeID', 'medicalInfoTypeID', 'description', 'isVaccinated'])
        csv_path_a = Path(__file__).parents[1].joinpath("data/medicalInfo.csv")
        with open(csv_path_a, 'a') as f:
            med_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

        self.calculate_avg_critical_lvl(cid)

    def calculate_avg_critical_lvl(self, cid):
        # calculate the average medical critical lvl of a camp based on the individual refugee's critical lvl
        lvl_arr = []
        mid_arr = []
        avg_lvl = 0
        df_r = extract_data_df("data/refugee.csv")
        df_m = extract_data_df("data/medicalInfo.csv")
        df_l = extract_data_df("data/medicalInfoType.csv")
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



    # def vaccinate_refugee(self):
    #     # How do we add logic here? Do we need to subtract one from the vaccines available
    #     # to this specific camp? Ie we've distributed our resource across our camps,
    #     # we can see what is available to this camp, and we want to use one of the
    #     # vaccinations to vaccinate a refugee. We should probably include logic to
    #     # subtract one vaccine from those available to the camp which this refugee belongs to
    #     pass

    def move_refugee(self):
        new_camp = int(input("Please enter the campID for the camp you wish to move this refugee to: "))
        ref_df = pd.read_csv("data/refugee.csv")
        camp_df = pd.read_csv('data/camp.csv')
        if camp_df['campID'].eq(new_camp).any():
            row_index = ref_df[ref_df['refugeeID'] == self.rid].index[0]
            with open("data/refugee.csv", 'a') as f:
                ref_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
        # modify_csv_value(file_path, row_index, column_name, new_value)
                modify_csv_value("data/refugee.csv", self.rid+1, "campID", new_camp)
        else:
            print("Sorry. That campID doesn't exist.")
            self.move_refugee()


