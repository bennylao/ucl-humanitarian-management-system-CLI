from numpy.core.defchararray import capitalize
from humanitarian_management_system.helper import extract_data, modify_csv_value, modify_csv_pandas
import pandas as pd
from pathlib import Path


class Camp:
    """A class to hold information about the size/capacity of the camp,
     and a collective overview of things like the amount of refugees,
      how many are vaccinated, how many need extra medical attention (ie doctors) etc."""
    total_number = 0
    camp_data = []
    # Is  camp data the same as list of camp names? Need for resources
    # list_of_camp_names = []

    def __init__(self, capacity, health_risk, current_resource_amount, is_camp_available=True):
        # location should be simply a country for simplicity
        self.is_camp_available = is_camp_available
        # option to make the camp unavailable for whatever reason (e.g. it's flooded or infected)
        # by disease and so other refugees shouldn't be added to that camp
        # Location should be a COUNTRY only - for simplicity ?
        self.current_resource_amount = current_resource_amount
        self.capacity = capacity
        self.health_risk = health_risk

        Camp.total_number += 1
        # since we have camp id perhaps name is not necessary? ie. first we refer to an event, from which we can refer
        # to the camp id of that particular event
        # Camp.list_of_camp_names.append(name)

        # Need to think about other methods which might be needed in this class?

    def pass_camp_info(self, select_index, camp_id):
        """if user choose to add a """

        country = extract_data("data/eventTesting.csv", "location")
        # geo_data = extract_data("data/eventTesting.csv","")
        csv_path = Path(__file__).parents[1].joinpath("data/countries.csv")
        df = pd.read_csv(csv_path)
        # find country id and event id by index
        result = df.loc[df["name"] == capitalize(country.iloc[select_index-1])]['country'].tolist()
        event_id = int(extract_data("data/eventTesting.csv", "eid").iloc[select_index-1])

        # keep track of existing camp num of a particular event
        no_camp = int(extract_data("data/eventTesting.csv", "no_camp").iloc[select_index-1])
        no_camp += 1

        Camp.camp_data = [[camp_id, event_id, result[0], self.capacity, self.health_risk, 0, 0, 1, self.is_camp_available]]
        camp_df = pd.DataFrame(Camp.camp_data, columns=['campID', 'eventID', 'countryID', 'refugeeCapacity', 'healthRisk',
                                                        'volunteerPop', 'refugeePop', 'avgCriticalLvl', 'status'])
        with open('data/camp.csv', 'a') as f:
            camp_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

        # update camp num for a particular event
        modify_csv_pandas("data/eventTesting.csv", 'eid', select_index, 'no_camp', int(no_camp))

    def __str__(self):
        """

        Returns
        -------

        """
        return "description of camp"

    def location(self):
        pass
