import pandas as pd
from pathlib import Path
from humanitarian_management_system.views import AdminView

class ResourceReport():
    def __init__(self):
        resource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        resource_allocaation_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        self.resource__nallocated_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceUnallocatedStock.csv")
        self.camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        self.camp_df = pd.read_csv(self.camp_csv_path)
        self.totalResources_df = pd.read_csv(resource_stock_csv_path)
        self.resourceAllocs_df = pd.read_csv(resource_allocaation_csv_path)
        self.unallocResources_df = pd.read_csv(self.resource__nallocated_stock_csv_path)
        self.joined_df = pd.merge(self.totalResources_df, self.resourceAllocs_df, on='resourceID', how='inner')
    
    def unalloc_resource_checker(self):
        #### just a checker to see if we have any unallocated resources. Should return just binary outcome
        #### will be useful for other resource functions 
        unalloc = sum(self.unallocResources_df['unallocTotal'])
        if unalloc == 0:
            unalloc_status = False
            unalloc_prompt = "\n ======= ＼(^o^)／ There are no unallocated resources ~ All good! ＼(^o^)／ ===== \n"
        else:
            unalloc_items = self.unallocResources_df[self.unallocResources_df['unallocTotal'] > 0]
            unalloc_status = True
            unalloc_prompt = f"\n =======  ｡•́︿•̀｡  WARNING! THERE ARE THE FOLLOWING UNALLOCATED RESOURCES  ｡•́︿•̀｡  ===== \n \n {unalloc_items} \n"

        return unalloc_status, unalloc_prompt
    
    #### the resource Map in its oiginal state, only displays camps with allocated resources. So there may be camps that have refugees, but no resources...
    #### how likely is this? ony if we remove all resources... 
    #### think we can just use the open camps with refugees actually. 
    #### if the resource is zero; we csn just prompt another selection... (?)
    
    def valid_open_camps(self):
        condition = self.camp_df['status']=='open'
        valid_range = self.camp_df.loc[condition, ['campID', 'refugeePop']]
        return valid_range

    def valid_open_camps_with_refugees(self):
        condition = (self.camp_df['refugeePop']>0) & (self.camp_df['status']=='open')
        valid_range = self.camp_df.loc[condition, ['campID', 'refugeePop']]
        return valid_range
    

    def valid_resources(self):
        valid_range = self.totalResources_df['resourceID'].tolist()
        return valid_range
    
    def valid_pairwise_camp_resources(self):
        resourceMap = self.resourceAllocs_df
        valid_range12_df = resourceMap.loc[resourceMap['qty']>0, ['campID', 'resourceID']]
        columns = valid_range12_df.columns
        valid_range12 = set(zip(valid_range12_df[columns[0]], valid_range12_df[columns[1]]))
        return valid_range12

    def input_validator(self, prompt_msg, valid_range, error_msg = 'Invalid selection. Please try again.'):
        # for usage in resources - validates the form inputs
        while True:
            user_input = input(prompt_msg)

            if user_input.lower() == 'return':
                break

            # Check if the input is a digit and convert it to an integer if it is
            if user_input.isdigit():
                user_input = int(user_input)

            # Check if the input (either integer or string) is in the valid range
            if user_input in valid_range:
                return user_input  # Return if the input is in the valid range

            else:
                print(error_msg)  # Print error message for input out of range
        AdminView.manage_resource_menu()


    # for campID and resource pairing - resource must be above zero and campID must be an open one with refugees
    def pairwise_input_validator(self, prompt_msg1, prompt_msg2, valid_range1, valid_range2, valid_range12, error_msg='Invalid combination. Please try again.'):
        while True:
            user_input1 = self.input_validator(prompt_msg1, valid_range1)

            # Get the second input using the existing input_validator
            user_input2 = self.input_validator(prompt_msg2, valid_range2)

            # Check if the combination of user_input_1 and user_input_2 is valid
            ### note the column order must match / be identical !! 
            if (user_input1, user_input2) in valid_range12:
                return user_input1, user_input2
            else:
                print(error_msg)


    def resource_report_total(self):
        resource_sum = pd.merge(self.totalResources_df, self.unallocResources_df[['resourceID', 'unallocTotal']], on='resourceID', how='outer').fillna(0)
        return resource_sum

    def resource_report_camp(self):
        resource_camp = self.joined_df.pivot_table(index=['resourceID', 'name', 'priorityLvl'], columns='campID', values='qty', aggfunc='sum').sort_index(level=0)

        ## is this helpful? maybe add in population as well ? 
        ## add something into allow view of selected resources only... ?? or not... idm 
        return resource_camp
    
    def resource_report_camp_vs_unallocated(self):
        unallocResources_df = pd.read_csv(self.resource__nallocated_stock_csv_path)
        resource_camp = self.joined_df.pivot_table(index=['resourceID', 'name', 'priorityLvl'], columns='campID', values='qty', aggfunc='sum').sort_index(level=0)
        joined_df_unalloc_camp = pd.merge(unallocResources_df, resource_camp, on='resourceID', how='inner')
        temp = joined_df_unalloc_camp['unallocTotal'].copy()

        joined_df_unalloc_camp['unallocTotal'],  joined_df_unalloc_camp['priorityLvl'] = joined_df_unalloc_camp['priorityLvl'], temp
        joined_df_unalloc_camp.rename(columns={'unallocTotal': 'priorityLvl', 'priorityLvl': 'unallocTotal'}, inplace=True)

        ## is this helpful? maybe add in population as well ? 
        ## add something into allow view of selected resources only... ?? or not... idm 
        return joined_df_unalloc_camp
    
    ############## comparing our current resource levels to a caculated equilibirum level

    # Setting the gold standard for what should be the 'equilibrium' level
    def calculate_resource_jess(self):

        # resource stock total...
        
        totalResources = self.totalResources_df

        # resource stock total...
        # extract total refugee population
        camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        camp = pd.read_csv(camp_csv_path)
        pop_arr = camp['refugeePop'].tolist()
        totalRefugees = sum(pop_arr)

        # this is the current allocation. not the gold standard one..
        resource_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        alloc_current = pd.read_csv(resource_csv_path)

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
        # print(alloc_ideal)


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
        alloc_current = self.resourceAllocs_df

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