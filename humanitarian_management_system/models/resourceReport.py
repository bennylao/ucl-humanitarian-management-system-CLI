import pandas as pd
from humanitarian_management_system.helper import (extract_data, modify_csv_value, modify_csv_pandas, extract_data_df,
                                                   extract_active_event)
from pathlib import Path


class ResourceReport():
    def __init__(self):
        self.totalResources_df = extract_data_df("data/resourceStock.csv")
        self.resourceAllocs_df = extract_data_df("data/resourceAllocation.csv")
        self.unallocResources = extract_data_df("data/resourceUnallocatedStock.csv")
        self.joined_df = pd.merge(self.totalResources_df, self.resourceAllocs_df, on='resourceID', how='inner')
    
    def unalloc_resource_checker(self):
        #### just a checker to see if we have any unallocated resources. Should return just binary outcome
        #### will be useful for other resource functions 
        unalloc = sum(self.unallocResources['unallocTotal'])
        if unalloc == 0:
            unalloc_status = False
            unalloc_prompt = "======= ＼(^o^)／ There are no unallocated resources ~ All good! ＼(^o^)／ ===== \n"
        else:
            unalloc_items = self.unallocResources[self.unallocResources['unallocTotal'] > 0]
            unalloc_status = True
            unalloc_prompt = f"=======  ｡•́︿•̀｡  WARNING! THERE ARE THE FOLLOWING UNALLOCATED RESOURCES  ｡•́︿•̀｡  ===== \n \n {unalloc_items} \n"

        return unalloc_status, unalloc_prompt


    def resource_report_total(self):
        ################ there seems to have been some divergence on the data here since i last worked on reporting
        ################ previously, i just had resourcedType, where the total was calculated by the aggregation below
        ##### now the total is printed out in resourceStock seperately. What are the implications?
        # My first thoughts are that this might be less robust (incase we need to update the totals.)... but happy to keep going and see whats going on
        resource_sum = self.joined_df.groupby('resourceID').agg({
            'name': 'first',  # Keeps the first name for each group
            'priorityLvl': 'first',  # Keeps the first priorityLvl for each group
            'qty': 'sum'  # Sums the allocatedQuantity for each group
        }).reset_index()
        return resource_sum

    def resource_report_camp(self):
        resource_camp = self.joined_df.pivot_table(index=['name', 'priorityLvl'], columns='campID', values='qty', aggfunc='sum').sort_index(level=1)

        ## is this helpful? maybe add in population as well ? 
        return resource_camp
    
    ############## comparing our current resource levels to a caculated equilibirum level

    # Setting the gold standard for what should be the 'equilibrium' level
    def calculate_resource_jess(self):

        # resource stock total...
        totalResources = extract_data_df("data/resourceStock.csv")

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

        ### creating the base for the alloc_ideal dataframe

        # Define the range for the first column (numbers 1 to 11)
        numbers = list(range(1, 12))
        resourceID = totalResources['resourceID'].tolist()

        # Find the non-zero camps... aka the camps with refugees
        second_column = camp.loc[camp['refugeePop'] > 0, 'campID'].tolist()
        resourceID_repeated = resourceID * len(second_column)

        # Repeat each number 11 times to match the length of each block in the first column
        second_column_repeated = [num for num in second_column for _ in range(len(resourceID))]

        # Creating the DataFrame
        alloc_ideal = pd.DataFrame({
            'resourceID': resourceID_repeated,
            'campID': second_column_repeated,
            'ideal_qty': [0] * len(second_column_repeated)
        })
        print(alloc_ideal)


        for index, row in alloc_ideal.iterrows():
            # going through each row of the dataframe...
            r_id = row['resourceID'] # use this to get the corresponding total in resourceStock
            r_stock_amt = totalResources.loc[totalResources['resourceID'] == r_id, 'total'].iloc[0]

            c_id = row['campID'] # use this to get the corresponding total in camp
            c_refugee_amt = camp.loc[camp['campID'] == c_id, 'refugeePop'].iloc[0]

            # Calculate what the ideal amount should be...
            ideal_qty_value = round((c_refugee_amt / totalRefugees) * r_stock_amt)

            """ # Printing out the details in a readable format
            print(f"Row Index: {index}")
            print(f"Resource ID: {r_id}, Stock Amount: {r_stock_amt}")
            print(f"Camp ID: {c_id}, Refugee Amount: {c_refugee_amt}")
            print(f"Ideal Quantity Value: {ideal_qty_value}")
            print("-" * 50)  # Separator for readability """

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

        ## need to index the below, as right now just resting on good faith that the resourceIDs are in the same order
        # alloc_ideal['current'] = alloc_current['qty']
        for index, row in alloc_ideal.iterrows():
            # going through each row of the dataframe... creating a pair search key each row
            r_id_ideal = row['resourceID'] 
            c_id_ideal = row['campID']
            pairmatch_condition = (alloc_current['resourceID'] == r_id_ideal) & (alloc_current['campID'] == c_id_ideal)

            # finding the qty where the two cols of alloc_current match that of the current alloc_ideal
            if not alloc_current.loc[pairmatch_condition, 'qty'].empty:
                matched_current_qty = alloc_current.loc[pairmatch_condition, 'qty'].iloc[0]
            else:
                matched_current_qty = 0  

            alloc_ideal.at[index, 'current'] = matched_current_qty ## creatung the current column here for alloc_ideal

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