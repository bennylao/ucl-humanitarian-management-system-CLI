import pandas as pd
from humanitarian_management_system.helper import (extract_data, modify_csv_value, modify_csv_pandas, extract_data_df,
                                                   extract_active_event)
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
        item_id = extract_data("data/resourceStock.csv", "resourceID").tolist()

        # extract total refugee pop for all active plans
        df = extract_data_df("data/camp.csv")
        # extract average medical critical level for a camp
        avg_lvl = df.loc[df['campID'] == int(self.campID)]['avgCriticalLvl'].tolist()[0]

        # extract total refugee population
        pop_arr = extract_data("data/camp.csv", "refugeePop").tolist()
        for i in pop_arr:
            self.total_pop += i

        # extract info related to resource item and its current allocation to camp
        df2 = extract_data_df("data/resourceStock.csv")
        df3 = extract_data_df("data/resourceAllocation.csv")

        for i in item_id:
            priority = df2.loc[df2['resourceID'] == i]['priorityLvl'].tolist()[0]
            stock = df2.loc[df2['resourceID'] == i]['total'].tolist()[0]
            try:
                current_amount = df3.loc[(df3['resourceID'] == i) & (df3['campID'] == self.campID)]['qty'].tolist()[0]
            except:
                current_amount = 0
            # higher priority item means we need to distribute more of it
            if priority == 1:
                try:
                    set_amount = (0.5 * stock + 0.3 * self.pop) * avg_lvl // ((0.5 * self.total_pop)
                                                                              + (0.1 * current_amount))
                    new_stock = int(stock) - int(set_amount)

                    if set_amount == 0:
                        self.pass_resource_info(int(stock), self.campID, i, 0)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)
                except:
                    set_amount = (0.5 * stock + 0.3 * self.pop) * avg_lvl // 2
                    new_stock = int(stock) - int(set_amount)

                    if set_amount == 0:
                        self.pass_resource_info(int(stock), self.campID, i, 0)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)

            if priority == 2:
                try:
                    set_amount = (0.4 * stock + 0.3 * self.pop) * avg_lvl // ((0.5 * self.total_pop)
                                                                              + (0.1 * current_amount))
                    new_stock = int(stock) - int(set_amount)

                    if set_amount == 0:
                        self.pass_resource_info(int(stock), self.campID, i, 0)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)
                except:
                    set_amount = (0.4 * stock + 0.3 * self.pop) * avg_lvl // 2
                    new_stock = int(stock) - int(set_amount)

                    if set_amount == 0:
                        self.pass_resource_info(int(stock), self.campID, i, 0)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)

            if priority == 3:
                try:
                    set_amount = (0.3 * stock + 0.3 * self.pop) * avg_lvl // ((0.5 * self.total_pop)
                                                                              + (0.1 * current_amount))
                    new_stock = int(stock) - int(set_amount)

                    if set_amount == 0:
                        self.pass_resource_info(int(stock), self.campID, i, 0)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)
                except:
                    set_amount = (0.3 * stock + 0.3 * self.pop) * avg_lvl // 2
                    new_stock = int(stock) - int(set_amount)

                    if set_amount == 0:
                        self.pass_resource_info(int(stock), self.campID, i, 0)
                    self.pass_resource_info(set_amount, self.campID, i, new_stock)

    def pass_resource_info(self, set_amount, campID, resourceID, new_stock):

        ResourceTest.resource_data = [[resourceID, campID, int(set_amount)]]
        res_df = pd.DataFrame(ResourceTest.resource_data, columns=['resourceID', 'campID', 'qty'])
        p1 = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")

        with open(p1, 'a') as f:
            res_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
        # update stock after resources have been distributed
        modify_csv_pandas("data/resourceStock.csv", 'resourceID', int(resourceID),
                          'total', new_stock)

    def manual_resource(self, set_amount, resourceID):
        df = extract_data_df("data/resourceStock.csv")
        stock = df.loc[df['resourceID'] == resourceID]['total'].tolist()[0]

        ResourceTest.resource_data = [[resourceID, self.campID, int(set_amount)]]
        res_df = pd.DataFrame(ResourceTest.resource_data, columns=['resourceID', 'campID', 'qty'])
        p1 = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")

        new_stock = int(stock) - int(set_amount)

        with open(p1, 'a') as f:
            res_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
        # update stock after resources have been distributed
        modify_csv_pandas("data/resourceStock.csv", 'resourceID', int(resourceID),
                          'total', new_stock)


