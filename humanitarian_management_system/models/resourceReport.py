import pandas as pd
from pathlib import Path
import numpy as np


class ResourceReport():
    def __init__(self):
        self.resource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        resource_allocaation_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        self.resource__nallocated_stock_csv_path = Path(__file__).parents[1].joinpath(
            "data/resourceUnallocatedStock.csv")
        self.camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        self.camp_df = pd.read_csv(self.camp_csv_path)
        self.totalResources_df = pd.read_csv(self.resource_stock_csv_path)
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
            unalloc_prompt = "\n\033[92m＼(^o^)／ GOOD NEWS ＼(^o^)／ CHECK 3: There are no unallocated resources ... aka all resources are currently assigned to camps \033[0m\n"
        else:
            unalloc_items = self.unallocResources_df[self.unallocResources_df['unallocTotal'] > 0]
            unalloc_status = True
            #unalloc_prompt = f"\n =======  ｡•́︿•̀｡  WARNING! THERE ARE THE FOLLOWING UNALLOCATED RESOURCES  ｡•́︿•̀｡  ===== \n \n {unalloc_items.to_string(index=False)} \n"

            unalloc_prompt = f"""\033[91m\n
✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖ !!!  SOS   ｡•́︿•̀｡  SOS !!! ✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖  \n
CHECK 3:\n
THERE ARE THE FOLLOWING UNALLOCATED RESOURCES... \n
==============================================================\033[0m\n
{unalloc_items.to_string(index=False)} \n
            """

        return unalloc_status, unalloc_prompt

    def valid_new_camps(self):
        #### we detect this by finding camps where: 
        # status = open
        # refugeePop > 0
        #  but no assigned resources

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
        condition = self.camp_df['status'] == 'open'
        valid_range = self.camp_df.loc[condition, ['campID', 'refugeePop']]
        return valid_range

    def valid_open_camps_with_refugees(self):
        # subset of all_camps_with_refugees
        condition = (self.camp_df['refugeePop'] > 0) & (self.camp_df['status'] == 'open')
        valid_range = self.camp_df.loc[condition, ['campID', 'refugeePop']]
        return valid_range

    def valid_all_camps_with_refugees(self):  ####### come back to this!!
        condition = self.camp_df['refugeePop'] > 0
        valid_range = self.camp_df.loc[condition, ['campID', 'refugeePop']]
        return valid_range

    def valid_resources(self):
        valid_range = self.totalResources_df['resourceID'].tolist()
        return valid_range

    def valid_origin_camp_single_resource(self, r_id_select):
        # built for origin_camps to move a single resource from... basically, its the r in the master table where the total is above zero
        master_table = self.master_resource_stats()
        single_resource_stats = master_table[master_table['resourceID'] == r_id_select]
        cols_above_zero = single_resource_stats.iloc[:, 4:].columns[(single_resource_stats.iloc[:, 4:] > 0).all()]

        return single_resource_stats, cols_above_zero.tolist()  ## print the actual range

    def input_validator(self, prompt_msg, valid_range, error_msg='\033[91mInvalid selection. Please try again.\033[0m'):
        # for usage in resources - validates the form inputs
        while True:
            user_input = input(prompt_msg)

            # if user_input.lower() == 'return':
            # break

            if user_input == 'RETURN':
                print('Returning user to resource mgmt menu...')
                return user_input

            # Check if the input is a digit and convert it to an integer if it is
            if user_input.isdigit():
                user_input = int(user_input)

            # Check if the input (either integer or string) is in the valid range
            if user_input in valid_range:
                return user_input  # Return if the input is in the valid range
            else:
                print(error_msg)  # Print error message for input out of range
        # AdminView.manage_resource_menu()

    def input_validator_2range_resources(self, prompt_msg: str, 
                                         used_range: list, # this needs to be appended on the outside... 
                                         move_basket: pd.DataFrame,
                                         mode: str,
                                         error_msg='\033[91mInvalid selection. Please try again.\033[0m'):
        # for usage in resources - validates the form inputs
        all_resources = self.valid_resources()
        used_range = list(set(used_range)) # get unique only 
        not_used = [item for item in all_resources if item not in used_range] ## the list of resources not in use 

        while True:
            user_input = input(prompt_msg)

            if user_input == 'RETURN':
                print('Returning user to resource mgmt menu...')
                return user_input

            # Check if the input is a digit and convert it to an integer if it is
            if user_input.isdigit():
                user_input = int(user_input)

            if user_input in not_used:
                return user_input  # Return if the input is in the valid range

            # if we have some records already...
            if len(used_range) > 0:
                # Check if the input (either integer or string) is in the valid range
                if user_input in not_used:
                    return user_input
                # Check if the input is in the second valid range... 
                # in practice this will be mutually exclusive due to usage in resources... 
                elif user_input in used_range:
                    move_basket_row = move_basket.loc[move_basket['resourceID'] == user_input] ## this is the row of the previous selection...
                    if mode == 'manual_alloc':
                        move_basket_print = move_basket_row[['resourceID', 'name', 'origin_campID', 'destination_campID', 'moveUnits', 'actionInfo']]
                        print("\033[91mYou can only specify one instruction per resource, per submission of the manual allocator form. \nCurrently you have already specified the below for this resource...\n")
                        print(move_basket_print.transpose().to_string(header = False))
                        print("\nDo you want to override your selection? \n(Note that you can make multiple manual changes to a resource, by submitting this form and going into the manual allocator again)\033[0m \n ")
                    elif mode == 'shop':
                        move_basket_print = move_basket_row
                        print("\033[91mREMINDER: You can only specify one buy instruction per resource, per shopping basket. \nCurrently you have already specified the below for this resource...\n")
                        print(move_basket_print.transpose().to_string(header = False))
                        print("\nDo you want to update the quantity with your current selection? \033[0m \n ")
                    else:
                        print("Error with move_basket")
                    
                    ## replace with input validator later
                    user_override = self.input_validator("y / n -->  \n", ['y', 'n'])
                    if user_override == 'y':
                        # remove row from move... 
                        move_row_index = move_basket.loc[move_basket['resourceID'] == user_input].index
                        move_basket.drop(move_row_index, inplace = True)
                        print('\033[91mOverriding your previous selection...\033[0m')
                        return user_input
                    elif user_override == 'n':
                        print('Please select another resourceID...')
                    else:
                        print("Override selection error...")
                    # if yes -> need to overwrite it in move dataframe somehow.... 
                    # if no, then need to ask to select another... aka. loop again... ... how to differentiate this? essentially... they just 
                else:
                    print(error_msg)  # Print error message for input out of range ... this essentially means they need to enter something else... 
        # AdminView.manage_resource_menu()

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
        resource_sum = pd.merge(self.totalResources_df, self.unallocResources_df[['resourceID', 'unallocTotal']],
                                on='resourceID', how='outer').fillna(0)
        ### changing around the columns
        temp = resource_sum['total'].copy()
        resource_sum['total'], resource_sum['priorityLvl'] = resource_sum['priorityLvl'], temp
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
        resource_camp = self.joined_df.pivot_table(index=['resourceID', 'name', 'priorityLvl'], columns='campID',
                                                   values='qty', aggfunc='sum').sort_index(level=0)

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

    def master_resource_stats(self):
        unallocResources_df = pd.read_csv(self.resource__nallocated_stock_csv_path)
        ### this table is primarily create based on the joined_df that uses the resource alloc map
        ### this means tho, if the resource is not on the map, then it wont come up on the table; so
        ### currently new camps with nothing allocated to it wont be on the table....
        ### so lets add it to the table :) - dont need to write this in; can just be an extra step done here
        ### i think even just cosmetically is ok? 
        resource_camp = self.joined_df.pivot_table(index=['resourceID', 'name', 'priorityLvl'], columns='campID',
                                                   values='qty', aggfunc='sum').sort_index(level=0)
        
        joined_df_unalloc_camp = pd.merge(unallocResources_df, resource_camp, on='resourceID', how='inner')
        temp = joined_df_unalloc_camp['unallocTotal'].copy()

        joined_df_unalloc_camp['unallocTotal'], joined_df_unalloc_camp['priorityLvl'] = joined_df_unalloc_camp[
            'priorityLvl'], temp
        joined_df_unalloc_camp.rename(columns={'unallocTotal': 'priorityLvl', 'priorityLvl': 'unallocTotal'},
                                      inplace=True)
        
        master_table = joined_df_unalloc_camp ## renaming bc messy 

        ### find extra columms aka. open camps with refugees, but no resources assigned to it....
        captured_camps = list(master_table.columns[4:])
        valid_open_camps_df = self.valid_open_camps_with_refugees() ## note any closed camps with resources will be captured already so no need to check for this 
        valid_open_camps = valid_open_camps_df['campID'].tolist() 
        uncaptured_camps = [item for item in valid_open_camps if item not in captured_camps]

        for item in uncaptured_camps:
            master_table[item] = np.nan
            ## need to sort these in the pretty table...

        if len(uncaptured_camps) != 0:
            sort_cols = sorted(master_table.columns[4:], key=lambda x: pd.to_numeric(x))
            first_4_cols = list(master_table.columns[:4])
            new_order = first_4_cols + sort_cols
            master_table = master_table[new_order]

        ## is this helpful? maybe add in population as well ? 
        ## add something into allow view of selected resources only... ?? or not... idm 

        #################### this includes closed camps too ! includes anything with resources... 
        return master_table

    def report_closed_camp_with_resources(self):
        master_df = self.master_resource_stats()
        valid_range_df = self.valid_closed_camps()
        camp_half_df = master_df[valid_range_df['campID'].to_list()]
        info_half_df = master_df.iloc[:, :4]
        return pd.concat([info_half_df, camp_half_df], axis=1)

    def PRETTY_PIVOT_CAMP(self, table: pd.DataFrame):
        ## incase strings, force into numbers
        for column in table.columns:
            table[column] = pd.to_numeric(table[column], errors='ignore')

        #### this works for tables of this format, split out by camps... 

        """ resourceID                      name  priorityLvl  unallocTotal      3      5     6     9    11
        0            1                  Blankets            2             0   2292   5500   917   917   458
        1            2                  Clothing            1             0    648   1555   259   259   130
        2            3                      Toys            3             0     16     38     6     6     3
        3            4                  Medicine            1             0     23     56     9     9     5
        4            5                  Vitamins            2             0     19     46     8     8     4
        5            6                      Food            1             0     23     56     9     9     5
        6            7                    Snacks            3             0     15     36     6     6     3
        7            8                Toiletries            2             0     19     46     8     8     4
        8            9                     Water            1             0     46    110    18    18     9
        9           10             Baby Supplies            1             0     23     56     9     9     5
        10          11  General Tools & Supplies            3             0  11385  27325  4554  4554  2277 """

        table['resourceID'] = table['resourceID'].astype(int)
        table['unallocTotal'] = table['unallocTotal'].astype(int)
        table_camp_range = table[4:]  # get the campIDs, which are from col 5 onwards due to labels

        # 1) rename the camp columns from just their ID int to 'camp ID X'
        for col in table.columns[4:]:
            table = table.rename(columns={col: 'campID ' + str(col)})  ## the col selects the right column

        # 2) summing horizontally to create the vertical sum column
        num_cols = table.columns[3:]
        ### getting the horizontal sums
        h_sum = table[num_cols].sum(axis=1)
        table['resourceTotal'] = h_sum.astype(int)

        # 3) building the extra horizontal rows 
        v_sum = table[num_cols].sum().tolist()  ## total resource per camp
        sum_row_vector = [np.nan, np.nan, 'total per camp ->'] + v_sum

        # rows for camp info
        condition = self.camp_df['campID'].isin(table_camp_range)
        status_vector = self.camp_df.loc[condition, 'status'].tolist()
        status_vector = [np.nan, np.nan, 'camp status ->'] + [np.nan] + status_vector + [np.nan]

        pop_vector = self.camp_df.loc[condition, 'refugeePop'].tolist()
        pop_vector = [np.nan, np.nan, 'refugeePop ->'] + [np.nan] + pop_vector + [np.nan]

        # 4) putting it all together
        new_rows_df = pd.DataFrame([sum_row_vector, pop_vector, status_vector], columns=table.columns)
        table = pd.concat([table, new_rows_df], ignore_index=True)

        # Convert to integers...
        table['resourceID'] = table['resourceID'].fillna('').astype(str)
        table['resourceTotal'] = table['resourceTotal'].fillna('').astype(str)
        table['unallocTotal'] = table['unallocTotal'].fillna('').astype(str)
        table['name'] = table['name'].fillna('').astype(str)

        return table

    def PRETTY_RESOURCE(self, table: pd.DataFrame, valid_r: list):
        all = self.PRETTY_PIVOT_CAMP(table)
        valid_r_str = [str(integer)+'.0' for integer in valid_r] # convert into a list of strings due to rendering ...
        # Assuming r_id_select is a list of resource IDs
        # Filter rows where 'resourceID' is in the list of r_id_select
        filtered_rows = all[all['resourceID'].isin(valid_r_str)]
        last_two_rows = all.tail(2)

        # Concatenate the filtered rows and the last two rows
        combined_resources = pd.concat([filtered_rows, last_two_rows])

        return combined_resources

    ############################################################################################################################

    ### EQUILIBRIUM STATS - used in auto-allocation; but will be good for report generation too

    ############################################################################################################################

    # Setting the gold standard for what should be the 'equilibrium' level
    def calc_ideal_resource(self):

        # resource stock total...

        totalResources = self.totalResources_df

        # resource stock total...
        # extract total refugee population  ### right now... this is messing up because we will have 
        camp = self.camp_df
        valid_camps_df = self.valid_open_camps_with_refugees()
        valid_range_refugeePop = valid_camps_df['refugeePop'].tolist()
        totalRefugees = sum(valid_range_refugeePop)

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
            r_id = row['resourceID']  # use this to get the corresponding total in resourceStock
            r_stock_amt = totalResources.loc[totalResources['resourceID'] == r_id, 'total'].iloc[0]

            c_id = row['campID']  # use this to get the corresponding total in camp
            c_refugee_amt = camp.loc[camp['campID'] == c_id, 'refugeePop'].iloc[0]

            # Calculate what the ideal amount should be...
            #####################################################################
            # THE ACTUAL ALGO !!!! 
            ideal_qty_value = round((c_refugee_amt / totalRefugees) * r_stock_amt)
            #####################################################################

            # Assign the calculated value to the specific row in 'ideal_qty' column
            alloc_ideal.at[index, 'ideal_qty'] = ideal_qty_value

        return alloc_ideal  # this is the ideal allocation which we will reference to.

    #########
    def determine_above_below(self, threshold=0.10):

        alloc_ideal = self.calc_ideal_resource()

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

            alloc_ideal.at[index, 'current'] = matched_current_qty  ## creatung the current column here for alloc_ideal

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

    def ALLOC_IDEAL_OUTPUT(self):
        ideal = self.determine_above_below()
        unbalanced = ideal[ideal['status'] != 'balanced'].copy()
        unbalanced['delta'] = 0

        for index, row in unbalanced.iterrows():
            if row['status'] == 'above':
                unbalanced.at[index, 'delta'] = row['current'] - row['ideal_qty']
            elif row['status'] == 'below':
                unbalanced.at[index, 'delta'] = row['ideal_qty'] - row['current']

        unbalanced = unbalanced.drop(['upper', 'lower'], axis=1)
        unbalanced['current'] = unbalanced['current'].astype(int)

        return unbalanced

