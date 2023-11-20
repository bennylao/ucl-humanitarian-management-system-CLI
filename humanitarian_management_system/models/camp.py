from numpy.core.defchararray import capitalize
from humanitarian_management_system.helper import extract_data, modify_csv_value
import pandas as pd
from pathlib import Path


class Camp:
    """A class to hold information about the size/capacity of the camp,
     and a collective overview of things like the amount of refugees,
      how many are vaccinated, how many need extra medical attention (ie doctors) etc."""
    total_number = 0
    camp_data = []

    # list_of_camp_names = []

    def __init__(self, location, population, capacity, is_camp_available=True):
        # location should be simply a country for simplicity
        self.is_camp_available = is_camp_available
        # option to make the camp unavailable for whatever reason (e.g. it's flooded or infected)
        # by disease and so other refugees shouldn't be added to that camp
        # Location should be a COUNTRY only - for simplicity ?
        self.location = location
        self.capacity = capacity
        self.population = population

        Camp.total_number += 1
        # since we have camp id perhaps name is not necessary? ie. first we refer to an event, from which we can refer
        # to the camp id of that particular event
        # Camp.list_of_camp_names.append(name)

        # Need to think about other methods which might be needed in this class?

    def pass_camp_info(self, select_index, campID):
        country = extract_data("data/eventTesting.csv", "location")
        csv_path = Path(__file__).parents[1].joinpath("data/countries.csv")
        df = pd.read_csv(csv_path)
        # find country id and event id by index
        result = df.loc[df["name"] == capitalize(country.iloc[select_index-1])]['country'].tolist()
        eventID = int(extract_data("data/eventTesting.csv", "eid").iloc[select_index-1])

        # keep track of existing camp num of a particular event
        no_camp = int(extract_data("data/eventTesting.csv", "no_camp").iloc[select_index-1])
        no_camp += 1

        Camp.camp_data = [[campID, eventID, result[0], self.capacity, 0]]
        camp_df = pd.DataFrame(Camp.camp_data, columns=['campID', 'eventID', 'countryID', 'capacity', 'currentPopulation'])
        with open('data/camp.csv', 'a') as f:
            camp_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

        # update camp num of a particular event via linqing's helper function
        modify_csv_value("data/eventTesting.csv", select_index-1, "no_camp", no_camp)

    def __str__(self):
        """

        Returns
        -------

        """
        return "description of camp"

    def location(self):
        pass
