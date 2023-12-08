from humanitarian_management_system.helper import modify_csv_pandas
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

    def __init__(self, capacity, health_risk, is_camp_available=True):
        # location should be simply a country for simplicity
        self.is_camp_available = is_camp_available
        # option to make the camp unavailable for whatever reason (e.g. it's flooded or infected)
        # by disease and so other refugees shouldn't be added to that camp
        # Location should be a COUNTRY only - for simplicity ?
        # self.current_resource_amount = current_resource_amount
        self.capacity = capacity
        self.health_risk = health_risk

        self.camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        self.cty_csv_path = Path(__file__).parents[1].joinpath("data/country.csv")
        self.event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
        self.res_alloc_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        self.res_type_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")

        # Camp.total_number += 1
        # since we have camp id perhaps name is not necessary? ie. first we refer to an event, from which we can refer
        # to the camp id of that particular event
        # Camp.list_of_camp_names.append(name)

        # Need to think about other methods which might be needed in this class?

    def pass_camp_info(self, select_index, camp_id):
        """if user choose to add a """
        df_e = pd.read_csv(self.event_csv_path)
        country = df_e['location']
        # geo_data = extract_data("data/event.csv","")
        df = pd.read_csv(self.cty_csv_path)
        # find country id and event id by index

        event_country = df_e.loc[df_e['eventID'] == select_index]['location'].tolist()[0]
        countryID = df.loc[df['name'] == event_country.capitalize()]['countryID'].tolist()[0]

        # keep track of existing camp num of a particular event
        no_camp = int(df_e.loc[df_e["eventID"] == int(select_index)]['no_camp'].tolist()[0])
        no_camp += 1

        if self.is_camp_available:
            status = 'open'
        else:
            status = 'closed'

        Camp.camp_data = [[camp_id, int(select_index), countryID, self.capacity, self.health_risk, 0, 0, 1, status]]
        camp_df = pd.DataFrame(Camp.camp_data,
                               columns=['campID', 'eventID', 'countryID', 'refugeeCapacity', 'healthRisk',
                                        'volunteerPop', 'refugeePop', 'avgCriticalLvl', 'status'])

        csv_path2 = Path(__file__).parents[1].joinpath("data/camp.csv")
        with open(csv_path2, 'a', newline='') as f:
            camp_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

        # update camp num for a particular event
        csv_path3 = Path(__file__).parents[1].joinpath("data/event.csv")
        modify_csv_pandas(csv_path3, 'eventID', select_index, 'no_camp', no_camp)

    def display_info(self, user, cid):

        camp_df = pd.read_csv(self.camp_csv_path)
        event_df = pd.read_csv(self.event_csv_path)
        cid_arr = []

        if user == 'admin':
            for i in camp_df['campID'].tolist():
                cid_arr.append(str(i))

        joined_df = pd.merge(camp_df, event_df, on='eventID', how='inner')
        joined_df.columns = ['Camp ID', 'Event ID', 'countryID', 'Refugee capacity', 'Health risk',
                             'Volunteer population', 'Refugee population', 'Average critical level', 'Status',
                             'Ongoing', 'Title', 'Location', 'Description', 'no_camp', 'Start date', 'End date']
        if user == 'volunteer':
            joined_df = joined_df.loc[joined_df['Camp ID'] == int(cid)]

        table_str = joined_df[['Camp ID', 'Refugee capacity', 'Health risk', 'Volunteer population',
                               'Refugee population', 'Average critical level', 'Status']].to_markdown(index=False)
        print("\n" + table_str)

        while True:
            user_input = input("Would you like to access the event profile for a particular camp (yes or no)? ")

            if user_input == 'RETURN':
                return

            if user_input.lower() == 'yes':
                self.display_eventinfo(user, cid, joined_df, cid_arr)

            if user_input.lower() != 'yes' and user_input.lower() != 'no':
                print("Must enter yes or no!")
                continue
            if user_input.lower() == 'no':
                return
            break

    def display_eventinfo(self, user, cid, joined_df, cid_arr):

        if user == 'admin':
            while True:
                id_input = input("Please enter the refugee id whose medical profile you would like to see: ")

                if id_input == 'RETURN':
                    return
                if id_input not in cid_arr:
                    print("Invalid refugee ID entered!")
                    continue
                joined_df = joined_df.loc[joined_df['Camp ID'] == int(id_input)]
                table_str = joined_df[['Camp ID', 'Event ID', 'Title', 'Description', 'Location', 'Ongoing',
                                       'Start date', 'End date']].to_markdown(
                    index=False)
                print("\n" + table_str)
                self.display_end(user, cid)
                return
            return
        else:
            joined_df = joined_df.loc[joined_df['Camp ID'] == int(cid)]
            table_str = joined_df[['Camp ID', 'Event ID', 'Title', 'Description', 'Location', 'Ongoing',
                                   'Start date', 'End date']].to_markdown(
                index=False)
            print("\n" + table_str)
            self.display_end(user, cid)
            return

    def display_resinfo(self, cid):
        camp_df = pd.read_csv(self.camp_csv_path)
        camp_df = camp_df.loc[camp_df['campID'] == cid]
        res_alloc_df = pd.read_csv(self.res_alloc_path)
        res_type_df = pd.read_csv(self.res_type_path)
        # thanks to Jess codes :)
        joined_df = pd.merge(camp_df, res_alloc_df, on='campID', how='inner')
        joined_df = pd.merge(joined_df, res_type_df, on='resourceID', how='inner')
        resource_camp = joined_df.pivot_table(index=['campID'], columns='name',
                                              values='qty', aggfunc='sum').sort_index(level=0)

        table_str = resource_camp.to_markdown(index=False)
        print("\n" + table_str)
        while True:
            user_input = input("Would you like to exit (yes)? ")
            if user_input == 'RETURN':
                return
            if user_input.lower() != 'yes':
                print("Must enter yes or leave it alone!")
                continue
            return

    def display_end(self, user, cid):
        while True:
            user_input = input("Would you like to exit (yes or no)? ")

            if user_input == 'RETURN':
                return
            if user_input.lower() != 'yes' and user_input.lower() != 'no':
                print("Must enter yes or no!")
                continue
            if user_input.lower() == 'no':
                self.display_info(user, cid)
            return
        return

    # def delete_camp(self):
    #     """This part of the code is to delete the camp from the camp.csv"""
    #     InstructionView.camp_deletion_message()
    #     active_index = extract_active_event()[0]
    #
    #     # if there is no active events, return
    #     if len(active_index) == 0:
    #         print("No relevant events to select from")
    #         return
    #     else:
    #         # print the events info for users to choose
    #         csv_path = Path(__file__).parents[0].joinpath("data/event.csv")
    #         df1 = matched_rows_csv(csv_path, "ongoing", True, "eid")
    #         print("\n*The following shows the info of all available events*\n")
    #         print(df1[0])
    #         while True:
    #             try:
    #                 eventID = int(input("\nEnter Event ID: "))
    #                 if eventID not in df1[1]:
    #                     print(f"Invalid input! Please enter an integer from {df1[1]} for Event ID.")
    #                     continue
    #                 else:
    #                     break
    #             except ValueError:
    #                 print(f"Invalid input! Please enter an integer from {df1[1]} for Event ID.")
    #
    #         # print camps info for users to choose
    #         csv_path2 = Path(__file__).parents[0].joinpath("data/camp.csv")
    #         df2 = matched_rows_csv(csv_path2, "eventID", eventID, "campID")
    #         print("\n**The following shows the info of related camps*\n")
    #         print(df2[0])
    #         while True:
    #             try:
    #                 delete_camp = int(input("\nWhich camp do you want to delete? Please enter campID: "))
    #                 if delete_camp not in df2[1]:
    #                     print(f"Invalid input! Please enter an integer from {df2[1]} for Camp ID.")
    #                     continue
    #                 else:
    #                     while True:
    #                         aa = input(f"\nAre you sure to delete camp {delete_camp}? (yes/no): ")
    #                         if aa == "yes":
    #                             # implement the deletion in csv file
    #                             df3 = pd.read_csv(csv_path2)
    #                             df3 = df3[df3["campID"] != delete_camp]
    #                             df3.to_csv(csv_path2, index=False)
    #
    #                             # keep track of existing camp num of a particular event
    #                             no_camp = df1[0].loc[eventID, "no_camp"]
    #                             no_camp -= 1
    #                             df4 = pd.read_csv(csv_path)
    #                             index = df4[df4["eid"] == eventID].index.tolist()
    #                             modify_csv_value(csv_path, index[0], "no_camp", no_camp)
    #                             print("Deletion Successful")
    #                             break
    #                         elif aa == "no":
    #                             break
    #                         else:
    #                             print("Invalid input! Please enter 'yes' or 'no'")
    #                             continue
    #                     break
    #             except ValueError:
    #                 print(f"Invalid input! Please enter an integer from {df2[1]} for Camp ID.")
