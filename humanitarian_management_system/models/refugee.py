import pandas as pd
# from helper. import extract_data, modify_csv_value, modify_csv_pandas
from pathlib import Path


class Refugee:
    refugee_data = []
    # total_number = 0

    def __init__(self, refugeeID, campID, firstName, lastName, dob, gender, familyID, medical_condition=None, is_vaccinated=False):
        """Need to prompt user to fill in camp ID, medical condition, family name.
        Refugee is instantiated as not_vaccinated unless they are specified as True
        (something to add in User Manual??)"""
        self.refugeeID = refugeeID
        self.campID = campID
        self.firstName = firstName
        self.lastName = lastName
        self.dob = dob
        self.gender = gender
        self.familyID = familyID
        self.medical_condition = medical_condition
        self.is_vaccinated = is_vaccinated
        # Refugee.total_number += 1

    @classmethod
    def add_refugee_from_user_input(cls):
        """Method to add the information of a newly added refugee in our system to the csv file"""
        refugeeID = input("Enter Refugee ID: ")
        campID = input("Enterr Camp ID: ")
        firstName = input("Enter First Name: ")
        lastName = input("Enter Last Name: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")
        gender = input("Enter Gender: ")
        familyID = input("EEnter Family ID: ")
        medical_condition = input("Entere Medical Condition(Optional): ")
        is_vaccinated = input("Is the refugee vaccinated? (True/False): ").lower
        new_refugee = cls(refugeeID, campID, firstName, lastName, dob, gender, familyID, medical_condition, is_vaccinated)
        cls.refugee_data.append(
            [new_refugee.refugeeID, new_refugee.campID, new_refugee.firstName, new_refugee.lastName, new_refugee.dob,
             new_refugee.gender, new_refugee.familyID])
        csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
        ref_df = pd.read_csv(csv_path)
        new_refugee_df = pd.DataFrame(cls.refugee_data, columns=['refugeeID', 'campID', 'firstName', 'lastName', 'dob', 'gender', 'familyID'])
        ref_df = pd.concat([ref_df, new_refugee_df], ignore_index=True)
        ref_df.to_csv(csv_path, index=False)

        print(ref_df)

    # def pass_refugee_info(self, refugeeID, campID, firstName, lastName, dob, gender, familyID):
    #     Refugee.refugee_data = [[refugeeID, campID, firstName, lastName, dob, gender, familyID]]
    #     # ref_df = pd.DataFrame(Refugee.refugee_data, columns=['refugeeID', 'campID', 'firstName', 'lastName', 'dob', 'gender', 'familyID'])
    #     csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
    #     ref_df = pd.read_csv(csv_path)
    #     # with open(csv_path, 'a') as f:
    #     #     ref_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
    #     # print(ref_df)
    #
    #     # modify_csv_pandas("data/refugee.csv", 'resourceID', int(resourceID),
    #     #                   'total', new_stock )

    def vaccinate_refugee(self):
        # How do we add logic here? Do we need to subtract one from the vaccines available
        # to this specific camp? Ie we've distributed our resource across our camps,
        # we can see what is available to this camp, and we want to use one of the
        # vaccinations to vaccinate a refugee. We should probably include logic to
        # subtract one vaccine from those available to the camp which this refugee belongs to
        pass

    def move_refugee(self):
        new_camp = input("Please enter the campID for the camp you wish to move this refugee to: ")
        df = pd.read_csv('camp.csv')
        if df['campID'].eq(new_camp).any():

            with open(csv_path, 'a') as f:
                ref_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
        #Sorry. Couldn't work out how to use the helper method to actually update these bits for the campID of the refugee in CSV/pandas
        #modify_csv_pandas(file_path, select_col, row_value, final_col, new_value)
        # modify_csv_pandas("data/refugee.csv", 'campID', int(campID),
        #     #                   'total', new_stock )
        # modify_csv_value(file_path, row_index, column_name, new_value)
        else:
            print("Sorry. That campID doesn't exist.")
            self.move_refugee()


Refugee.add_refugee_from_user_input()