import pandas as pd
from humanitarian_management_system.helper import extract_data, modify_csv_value, modify_csv_pandas
from pathlib import Path


# A very basic attempt at resource allocation to camp, it's basically just a manipulation of database/csv files by
# looping through them when necessary
class ResourceTest():
    resource_data = []

    def __init__(self, campID, pop, total_pop):
        self.pop = pop
        self.campID = campID
        self.total_pop = total_pop

    def calculate_resource(self):
        item_id = extract_data("data/resourceType.csv", "resourceID").tolist()

        # extract total refugee pop for all active plans
        csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        df = pd.read_csv(csv_path)
        data = extract_data("data/eventTesting.csv", ['ongoing', 'eid'])
        active_id = []

        for i in range(len(data)):
            if data['ongoing'].iloc[i]:
                active_id.append(data['eid'].iloc[i])

        for i in active_id:
            self.total_pop += int(df.loc[df['eventID'] == i]['refugeePop'].tolist()[0])

        # extract info related to resource item and its current allocation to camp
        csv_path1 = Path(__file__).parents[1].joinpath("data/resourceType.csv")
        csv_path2 = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        csv_path3 = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        df1 = pd.read_csv(csv_path1)
        df2 = pd.read_csv(csv_path2)
        df3 = pd.read_csv(csv_path3)

        for i in item_id:
            priority = df1.loc[df1['resourceID'] == i]['priorityLvl'].tolist()[0]
            stock = df2.loc[df2['resourceID'] == i]['total'].tolist()[0]
            try:
                current_amount = df3.loc[(df3['resourceID'] == i) & (df3['campID'] == self.campID)]['qty'].tolist()[0]
            except:
                current_amount = 0

            if priority == 1:
                try:
                    set_amount = (0.8 * stock + 0.6 * self.pop) // ((0.3 * self.total_pop) + (0.2 * current_amount))
                    new_stock = int(stock) - int(set_amount)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)
                except:
                    set_amount = (0.8 * stock + 0.6 * self.pop)
                    new_stock = int(stock) - int(set_amount)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)

            if priority == 2:
                try:
                    set_amount = (0.7 * stock + 0.6 * self.pop) // ((0.3 * self.total_pop) + (0.2 * current_amount))
                    new_stock = int(stock) - int(set_amount)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)
                except:
                    set_amount = (0.7 * stock + 0.6 * self.pop)
                    new_stock = int(stock) - int(set_amount)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)

            if priority == 3:
                try:
                    set_amount = (0.6 * stock + 0.6 * self.pop) // ((0.3 * self.total_pop) + (0.2 * current_amount))
                    new_stock = int(stock) - int(set_amount)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)
                except:
                    set_amount = (0.6 * stock + 0.6 * self.pop)
                    new_stock = int(stock) - int(set_amount)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)

    def pass_resource_info(self, set_amount, campID, resourceID, new_stock):

        ResourceTest.resource_data = [[resourceID, campID, int(set_amount)]]
        res_df = pd.DataFrame(ResourceTest.resource_data, columns=['resourceID', 'campID', 'qty'])
        p1 = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        p2 = Path(__file__).parents[1].joinpath("data/resourceStock.csv")

        with open(p1, 'a') as f:
            res_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

        modify_csv_pandas("data/resourceStock.csv", 'resourceID', int(resourceID),
                          'total', new_stock )
