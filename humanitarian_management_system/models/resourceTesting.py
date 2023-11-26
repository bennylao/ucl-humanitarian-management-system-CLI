import pandas as pd
from humanitarian_management_system.helper import (extract_data, modify_csv_value, modify_csv_pandas, extract_data_df)
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
        # get id of resources 
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

    # Setting the gold standard for what should be the 'equilibrium' level
    def calculate_resource_jess(self):

        # resource stock total...
        totalResources = extract_data_df("data/resourceStock.csv")#

        # resource stock total...
        camp = extract_data_df("data/camp.csv")

        # extract total refugee population
        pop_arr = extract_data("data/camp.csv", "refugeePop").tolist() # per camp
        totalRefugees = sum(pop_arr)

        # this is the current allocation. not the gold standard one.. 
        alloc_current = extract_data_df("data/resourceAllocation.csv")

        # but we can overwrite ... 
        alloc_ideal = alloc_current
        alloc_ideal.columns.values[2] = 'ideal_qty'

        for index, row in alloc_ideal.iterrows():
            # going through each row of the dataframe...
            r_id = row['resourceID'] # use this to get the corresponding total in resourceStock
            r_stock_amt = totalResources.loc[totalResources['resourceID'] == r_id, 'total'].iloc[0]

            c_id = row['campID'] # use this to get the corresponding total in camp
            c_refugee_amt = camp.loc[camp['campID'] == c_id, 'refugeePop'].iloc[0]
            # print(c_refugee_amt / totalRefugees * r_stock_amt)

            # Calculate what the ideal amount should be...
            ideal_qty_value = round((c_refugee_amt / totalRefugees) * r_stock_amt)

            # Printing out the details in a readable format
            print(f"Row Index: {index}")
            print(f"Resource ID: {r_id}, Stock Amount: {r_stock_amt}")
            print(f"Camp ID: {c_id}, Refugee Amount: {c_refugee_amt}")
            print(f"Ideal Quantity Value: {ideal_qty_value}")
            print("-" * 50)  # Separator for readability

            # Assign the calculated value to the specific row in 'ideal_qty' column
            alloc_ideal.at[index, 'ideal_qty'] = ideal_qty_value
        
        return alloc_ideal # this is the ideal allocation which we will reference to. 

    #########
    def determine_above_below(self, threshold = 0.10):

        alloc_ideal = self.calculate_resource_jess()

        # this is the current allocation. not the gold standard one.. 
        # can probably refactor this code later on...
        alloc_current = extract_data_df("data/resourceAllocation.csv")

        alloc_ideal['upper'] = round(alloc_ideal['ideal_qty'] * (1 + threshold))
        alloc_ideal['lower'] = round(alloc_ideal['ideal_qty'] * (1 - threshold))
        alloc_ideal['current'] = alloc_current['qty']

        # create new column to indicate if resources greater or less than..
        # Function to determine the new column value
        def condititon_resource(row):
            if row['current'] > row['upper']:
                return 'above'
            elif row['current'] < row['lower']:
                return 'below'
            else:
                return 'balanced'

        # Applying the function to create the new column
        alloc_ideal['status'] = alloc_ideal.apply(condititon_resource, axis=1)

        return alloc_ideal
    
    def redistribute(self):

        # resource stock total... >> can probably remove the need for this later 
        totalResources = extract_data_df("data/resourceStock.csv")

        alloc_ideal = self.determine_above_below()
        alloc_ideal['updated'] = alloc_ideal['current']

        for index, row in alloc_ideal.iterrows():
            if row['status'] != 'balanced':
                row['updated'] = row['ideal_qty']
        
        # Now need to check, how the sum compares to the total amounts and make small tweaks... 
        redistribute_sum_checker = alloc_ideal.groupby('resourceID')['updated'].sum()

        # if redistribute_sum_checker == alloc_ideal.groupby('resourceID')['current'].sum():
            #print("all good")
            # otherwise, take 1 or 2 off the top ... 

        ###### validate the redistributed totals, against the actual totals.
        ###### this is just incase there is any discrepancies from rounding.
        totalResources.set_index('resourceID', inplace=True)
        comparison_result = redistribute_sum_checker == totalResources['total']
        # Assuming comparison_result is the Series obtained from the comparison

        for resource_id, is_equal in comparison_result.items():
            if is_equal:
                pass
            else:
                print(f"The sum for resourceID {resource_id} is different post distribution.")
                ########### need to add logic for what to do, basically just adjust it from the camps with the most of that item, but this is an edge case, don't need to worry about it for now


        return redistribute_sum_checker, comparison_result

    # writes in the allocations - i think the allocations are just overwritten basically... 
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


    def resource_adder(self):
        ## admin only but deal with later
        ## adds to the total amount of resources available

        # welcome to the resource store! please enter how many of each object you would like to add
        totalResources = extract_data_df("data/resourceStock.csv")
        unallocResources = extract_data_df("data/resourceUnallocatedStock.csv")
        ################ might need to change this to unallocated...
        

        ### menu bit
        print(f"""==========================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ Hi Admin! Welcome to the Resource Shop ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
==========================================================================\n
        Below is your current inventory:\n
{totalResources} \n"""
        )
        basket = pd.DataFrame(columns=['resourceID','buyUnits'])
        basket_id_list = []
        basket_units_list = []
        ### can give user an option to leave the shop rn. come back to this 
        while True:
            # add error handling in the last stage / later ... 
            r_id_select = int(input("Please enter the resourceID of the item you would like to purchase: --> "))
            r_name_select = totalResources.loc[totalResources['resourceID'] == r_id_select, 'name'].iloc[0]
            r_id_units = int(input(f"Please enter the number of units of *** Resource ID {r_id_select}: {r_name_select} *** which you would like to buy: --> "))

            basket_id_list.append(r_id_select)
            basket_units_list.append(r_id_units)

            # Ask if the user is done
            done = input("Type 'DONE' if you are done shopping; otherwise type anything else to carry on: ").strip().upper()
            if done == 'DONE':
                break

        # insert the two lists into the basket dataframe
        basket['resourceID'] = basket_id_list
        basket['buyUnits'] = basket_units_list
        # could add in edit basket option but come back to this 
        print(f"""Below is your shopping basket: \n {basket} \n"""
        )
        confirm_shop = input("Proceed to checkout? [y] Yes; [x] Abandon cart")
        if confirm_shop == 'y':
            ## logic to loop thru this and add to the unallocated dataframe
            ## actually esier to do join
            result_df = pd.merge(unallocResources, basket, on='resourceID', how='left').fillna(0)
            result_df['unallocTotal'] = result_df['unallocTotal'].astype(int) + result_df['buyUnits'].astype(int)
            result_df.drop('buyUnits', axis=1, inplace=True)
        #result_df.to_csv('resourceUnallocatedStock.csv', index=False)
            print(result_df)
 ## what after this? new unallocated resources

 ## 
