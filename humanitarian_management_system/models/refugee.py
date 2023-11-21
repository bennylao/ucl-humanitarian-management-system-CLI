# Create refugee profile for each refugee including their family. Each
# refugee must be logged with: their camp identification, medical
# condition, etc. Keep it simple, you can assume a family is a singular
# entity, rather than their constituent members. <-- what does this mean?
import pandas as pd
from pathlib import Path
from humanitarian_management_system.helper import extract_data, modify_csv_value, modify_csv_pandas

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

    def pass_refugee_info(self, refugeeID, campID, firstName, lastName, dob, gender, familyID):
        Refugee.refugee_data = [[refugeeID, campID, firstName, lastName, dob, gender, familyID]]
        # ref_df = pd.DataFrame(Refugee.refugee_data, columns=['refugeeID', 'campID', 'firstName', 'lastName', 'dob', 'gender', 'familyID'])
        csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
        ref_df = pd.read_csv(csv_path)
        data = extract_data()
        with open(csv_path, 'a') as f:
            ref_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

        modify_csv_pandas("data/refugee.csv", 'resourceID', int(resourceID),
                          'total', new_stock )

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
            self.associated_camp = new_camp
        else:
            print("Sorry. That campID doesn't exist.")
            self.move_refugee()
