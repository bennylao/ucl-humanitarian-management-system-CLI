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
    
    ############################################################################################################################

    ### TOOLBOX - utility-type functions to check data & create valid selection ranges for resources

    ############################################################################################################################
    
    def unalloc_resource_checker(self):
        #### just a checker to see if we have any unallocated resources. Should return just binary outcome
        #### will be useful for other resource functions 
        unalloc = sum(self.unallocResources_df['unallocTotal'])
        if unalloc == 0:
            unalloc_status = False
            unalloc_prompt = "\n ＼(^o^)／ GOOD NEWS ＼(^o^)／ There are no unallocated resources (empty inventory) \n"
        else:
            unalloc_items = self.unallocResources_df[self.unallocResources_df['unallocTotal'] > 0]
            unalloc_status = True
            unalloc_prompt = f"\n =======  ｡•́︿•̀｡  WARNING! THERE ARE THE FOLLOWING UNALLOCATED RESOURCES  ｡•́︿•̀｡  ===== \n \n {unalloc_items.to_string(index = False)} \n"

        return unalloc_status, unalloc_prompt
    
    def valid_new_camps(self):
        #### we detect this by finding camps where: 
        # status = open
        # refugeePop > 0
        # but no assigned resources

        ## camps by status & refugeePop
        condition = (self.camp_df['status'] == 'open') & (self.camp_df['refugeePop'] > 0)
        filtered_df_A = self.camp_df[condition][['campID', 'status', 'refugeePop']].reset_index(drop=True)

        # camps with 
        df_B = self.resource_report_camp() 
        ## note this uses joined_df which is based on the resource mapping -> resourceAllocation... 
        # which should not include any camps that (1) have no resources across the board; (2) but are still open and have non zero refugeePop
        ## hence, the valid camps without any resources ... should not feature here at all; so we need to find the inverse of the intersection
        df_sum = df_B.sum().reset_index(name='resourceSum')
        condition = df_sum['resourceSum'] > 0
        filtered_df_B = df_sum[condition]['campID']

        # Assuming df1 is your first DataFrame and df2 is your second DataFrame
        # And assuming the column in df2 is also named 'campID'

        # Filtering out the rows where campID in df1 is not in df2
        new_camps_df = filtered_df_A[~filtered_df_A['campID'].isin(filtered_df_B)].reset_index(drop=True)

        return new_camps_df  ## use this by finding if not empty list
    
    def valid_closed_camps(self):
        ## only closed camps with resources still unassigned

        ## camps by status
        condition = (self.camp_df['status'] == 'closed')
        filtered_df_A = self.camp_df[condition][['campID', 'status', 'refugeePop']].reset_index(drop=True)

        # camps with resources still
        df_B = self.resource_report_camp() 
        df_sum = df_B.sum().reset_index(name='resourceSum')
        condition = df_sum['resourceSum'] > 0
        filtered_df_B = df_sum[condition]['campID']

        # Find their intersection
        closed_camps_df = filtered_df_A[filtered_df_A['campID'].isin(filtered_df_B)].reset_index(drop=True)

        return closed_camps_df  ## use this by finding if not empty list


    def valid_unalloc_resources(self):
        unalloc_items = self.unallocResources_df[self.unallocResources_df['unallocTotal'] > 0]
        # we only need the resourceID and amount > but do that when calling the function
        return unalloc_items

    
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
    
    def valid_all_camps_with_refugees(self): ####### come back to this!! 
        condition = self.camp_df['status']=='open'
        valid_range = self.camp_df.loc[condition, ['campID', 'refugeePop']]
        return valid_range

    def valid_resources(self):
        valid_range = self.totalResources_df['resourceID'].tolist()
        return valid_range

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

    ############################################################################################################################

    ### STATS - table generation, used to display within GUI & in combo with toolbox functions for involved manipulation of data

    ### JESS NOTES - NEED TO TIDY THIS UP; MAKE BETTER LOOKING... ASK TEAM WHATS GOOD

    ############################################################################################################################

    def resourceStock_generator(self, new_map):
        assigned = self.totalResources_df
        joined_df = pd.merge(assigned.drop(['total'], axis=1, inplace=False), new_map, on='resourceID', how='inner')
        new_stock = joined_df.groupby('resourceID').agg({
                        'name': 'first',  # Keeps the first name for each group
                        'qty': 'sum',  # Sums the qty for each camp >> we ignore the 'total' column in stockManualResources
                        'priorityLvl': 'first',  
                    }).reset_index()
        new_stock.rename(columns={'qty': 'total'}, inplace=True)
        return new_stock

    def resource_report_total(self):
        resource_sum = pd.merge(self.totalResources_df, self.unallocResources_df[['resourceID', 'unallocTotal']], on='resourceID', how='outer').fillna(0)
        ### changing around the columns
        temp = resource_sum['total'].copy()
        resource_sum['total'],  resource_sum['priorityLvl'] = resource_sum['priorityLvl'], temp
        resource_sum.rename(columns={'total': 'priorityLvl', 'priorityLvl': 'assignedTotal'}, inplace=True)
        resource_sum['grandTotal'] = resource_sum['assignedTotal'] + resource_sum['unallocTotal']
        #### sample output
        """       resourceID                   name  priorityLvl  assignedTotal  unallocTotal  grandTotal
        0            1                  Blankets            2          10084             0       10084
        1            2                  Clothing            1           2850             0        2850
        2            3                      Toys            3             65          1200        1265
        3            4                  Medicine            1            102             0         102
        4            5                  Vitamins            2             84             0          84
        5            6                      Food            1            102             0         102
        6            7                    Snacks            3             65             0          65
        7            8                Toiletries            2             84             0          84
        8            9                     Water            1            202             0         202
        9           10             Baby Supplies            1            102             0         102
        10          11  General Tools & Supplies            3          50096             0       50096 """
        return resource_sum

    def resource_report_camp(self):
        resource_camp = self.joined_df.pivot_table(index=['resourceID', 'name', 'priorityLvl'], columns='campID', values='qty', aggfunc='sum').sort_index(level=0)

        ## is this helpful? maybe add in population as well ? 
        ## add something into allow view of selected resources only... ?? or not... idm 
        """ campID                                          3      5     6     9     11
        resourceID name                     priorityLvl                                
        1          Blankets                 2             2292   5500   917   917   458
        2          Clothing                 1              648   1555   259   259   130
        3          Toys                     3              288    691   115   115    58
        4          Medicine                 1               31     75    12    12     6
        5          Vitamins                 2               19     46     8     8     4
        6          Food                     1               23     56     9     9     5
        7          Snacks                   3               15     36     6     6     3
        8          Toiletries               2               19     46     8     8     4
        9          Water                    1               46    110    18    18     9
        10         Baby Supplies            1               23     56     9     9     5
        11         General Tools & Supplies 3            11385  27325  4554  4554  2277 """
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

        #################### this includes closed camps too ! 
        return joined_df_unalloc_camp
    
    def report_closed_camp_with_resources(self):
        master_df = self.resource_report_camp_vs_unallocated()
        valid_range_df = self.valid_closed_camps()
        camp_half_df = master_df[valid_range_df['campID'].to_list()]
        info_half_df = master_df.iloc[:, :4]
        return pd.concat([info_half_df, camp_half_df], axis=1)
    

    ############################################################################################################################

    ### EQUILIBRIUM STATS - used in auto-allocation; but will be good for report generation too

    ############################################################################################################################

    # Setting the gold standard for what should be the 'equilibrium' level
    def calculate_resource_jess(self):

        # resource stock total...
        
        totalResources = self.totalResources_df

        # resource stock total...
        # extract total refugee population
        camp = self.camp_df
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
        resourceID = totalResources['resourceID'].tolist()

        # Find the non-zero camps... aka the camps with refugees
        # second_column = camp.loc[camp['refugeePop'] > 0, 'campID'].tolist()
        valid_camps_df = self.valid_open_camps_with_refugees()
        second_column = valid_camps_df['campID'].tolist()
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