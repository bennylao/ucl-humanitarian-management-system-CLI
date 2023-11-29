import pandas as pd
from pathlib import Path

from humanitarian_management_system.helper import modify_csv_pandas
from .resourceReport import ResourceReport


# A very basic attempt at resource allocation to camp, it's basically just a manipulation of database/csv files by
# looping through them when necessary
class ResourceTest():
    resource_data = []

    def __init__(self, campID, pop, total_pop):
        self.pop = pop
        self.campID = campID
        self.total_pop = total_pop
        self.resource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        self.resource_allocaation_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        self.resource__nallocated_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceUnallocatedStock.csv")
        self.totalResources_df = pd.read_csv(self.resource_stock_csv_path)
        self.resourceAllocs_df = pd.read_csv(self.resource_allocaation_csv_path)
        self.unallocResources_df = pd.read_csv(self.resource__nallocated_stock_csv_path)
        self.joined_df = pd.merge(self.totalResources_df, self.resourceAllocs_df, on='resourceID', how='inner')

    def calculate_resource(self):
        # get id of resources
        resource_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        df2 = pd.read_csv(resource_csv_path)
        item_id = df2['resourceID'].tolist()

        # extract total refugee pop for all active plans
        camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        df = pd.read_csv(camp_csv_path)
        # extract average medical critical level for a camp
        avg_lvl = df.loc[df['campID'] == int(self.campID)]['avgCriticalLvl'].tolist()[0]

        # extract total refugee population
        pop_arr = df['refugeePop'].tolist()
        for i in pop_arr:
            self.total_pop += i

        # extract info related to resource item and its current allocation to camp
        resource_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        df3 = pd.read_csv(resource_csv_path)

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
        resource_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        totalResources = pd.read_csv(resource_csv_path)

        # resource stock total...
        camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        camp = pd.read_csv(camp_csv_path)

        # extract total refugee population
        camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        df = pd.read_csv(camp_csv_path)
        pop_arr = df['refugeePop'].tolist()
        totalRefugees = sum(pop_arr)

        # this is the current allocation. not the gold standard one..
        resource_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        alloc_current = pd.read_csv(resource_csv_path)

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
        resource_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        alloc_current = pd.read_csv(resource_csv_path)

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
        resource_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        totalResources = pd.read_csv(resource_csv_path)

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
        csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        df = pd.read_csv(csv_path)
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
        # totalResources = extract_data_df("data/resourceStock.csv")
        # unallocResources = extract_data_df("data/resourceUnallocatedStock.csv")
        ################ might need to change this to unallocated...
        resource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        totalResources = pd.read_csv(resource_stock_csv_path)

        unresource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceUnallocatedStock.csv")
        unallocResources = pd.read_csv(unresource_stock_csv_path)

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
        print(f"""==========================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ Below is your shopping basket: ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
==========================================================================\n
{basket} \n"""
        )
        confirm_shop = input("Proceed to checkout? \n [y] Yes; \n [x] Abandon cart \n --> ")
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
    def manual_alloc(self):
        # add stuff to deal with unallocated items later bc i think its a bit different. right now i think is just about getting a function that works 
        resource_stats_instance = ResourceReport()
        print("Below is how each resource is currently distributed across the camps: ")
        all_resource_camp_df = resource_stats_instance.resource_report_camp()
        print(all_resource_camp_df)

        move = pd.DataFrame(columns=['resourceID', 'name', 'origin_campID', 'destination_campID', 'moveUnits'])
        move_id_list = []
        move_name_list = []
        move_origin_camp_list = []
        nove_dest_camp_list = []
        move_units_list = []

        while True: 
            ###################################################################
            # select single resource
            r_id_select = int(input("\nPlease enter the resourceID of the item you would like to manually redistribute: --> "))
            r_name_select = self.totalResources_df.loc[self.totalResources_df['resourceID'] == r_id_select, 'name'].iloc[0]

            # how much of this resource is allocated in each camp currently (does not yet include unallocated)
            all_resource_camp_df = resource_stats_instance.resource_report_camp().reset_index()
            single_resource_camp_df = all_resource_camp_df[all_resource_camp_df['resourceID'] == r_id_select]
            print(f"\n*** Resource ID {r_id_select}: {r_name_select} *** is currently distributed in the following camps: \n")
            print(single_resource_camp_df.to_string(index=False))

            # get the user to select the origin & destination camp:
            origin_c_id = int(input(f"\nPlease enter the ORIGIN campID (from the above) where you would like to REMOVE *** Resource ID {r_id_select}: {r_name_select} *** from: "))
            destination_c_id = int(input(f"\nPlease enter the DESTINATION campID (from any campID) where you would like to ADD *** Resource ID {r_id_select}: {r_name_select} *** to: "))
            
            # get unit number. ######## Note to self / team!!!! PROBABLY NEED TO ADD VALIDATION LATER!!!! #########
            move_units = int(input(f"\n Please enter the amount of *** Resource ID {r_id_select}: {r_name_select} *** to manually re-allocate: "))

            move_id_list.append(r_id_select)
            move_name_list.append(r_name_select)
            move_origin_camp_list.append(origin_c_id)
            nove_dest_camp_list.append(destination_c_id)
            move_units_list.append(move_units)

            # Ask if the user is done
            done = input("\n Are there any more resources you want to manually allocate? y / n -->  ").strip()
            if done == 'n':
                break
            
        
        move['resourceID'] = move_id_list
        move['name'] = move_name_list
        move['origin_campID'] = move_origin_camp_list
        move['destination_campID'] = nove_dest_camp_list
        move['moveUnits'] = move_units_list
        
        
        print(f"""==========================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ Below are your selected manual re-allocations: ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
==========================================================================\n
        {move.to_string(index=False)} \n"""
        )
        confirm_move = input("Proceed to re-allocate? \n [y] Yes; \n [x] Abandon manual allocation \n --> ")
        if confirm_move == 'y':
            resourceManualAllocs = self.resourceAllocs_df

            for index, row in move.iterrows():
                # to make the manual moves, we need to identify (resource_id, campID) pairs for origin & destination
                # Assuming df is your DataFrame
                origin_condition = (resourceManualAllocs['resourceID'] == row['resourceID']) & (resourceManualAllocs['campID'] == row['origin_campID'])
                print(origin_condition.any())
                print(resourceManualAllocs.loc[origin_condition, 'qty'])
                resourceManualAllocs.loc[origin_condition, 'qty'] -= row['moveUnits'] ### substract / remove from the origin camp
                ###### error handling ---> assumess there is only 1 unique pairwwise combo. does not consider if the pair is in the table twice 

                dest_condition = (resourceManualAllocs['resourceID'] == row['resourceID']) & (resourceManualAllocs['campID'] == row['destination_campID'])
                if dest_condition.any():
                    resourceManualAllocs.loc[dest_condition, 'qty'] += row['moveUnits'] 
                    ### add to the destination camp
                else:
                    # create the row in resourceAllocator if it does not exist
                    new_row_resourceAllocs = {'resourceID': row['resourceID'], 'campID': row['destination_campID'], 'qty': row['moveUnits']}
                    resourceManualAllocs = resourceManualAllocs.append(new_row_resourceAllocs, ignore_index=True)
                    
            #### we should now have the updated data, resourceManualAllocs for resourceAllocation.csw
            # print(resourceManualAllocs)
            resourceManualAllocs.to_csv(self.resource_allocaation_csv_path, index=False)

            #### write it in; and then run the report generator again to create an after table grouped by campID 
            resource_stats_instance_AFTER = ResourceReport()
            post_manual_alloc_camp_df = resource_stats_instance_AFTER.resource_report_camp()

            print(f"""\n ======= ＼(^o^)／ Manual Re-allocation Successful! ＼(^o^)／ ===== \n
Below are the before vs. current resource allocations by camp: \n"""
        )
            print("BEFORE: \n")
            print(all_resource_camp_df.to_string(index=False))
            print("\nAFTER: \n")
            print(post_manual_alloc_camp_df)



        return resourceManualAllocs
    

    def manual_unallocated_only(self):
        # add stuff to deal with unallocated items later bc i think its a bit different. right now i think is just about getting a function that works 
        resource_stats_instance = ResourceReport()
        print("Below is how each resource is currently unallocated vs. how many is distributed across the camps: ")
        all_resource_camp_camp_vs_unallocated = resource_stats_instance.resource_report_camp_vs_unallocated()
        print(all_resource_camp_camp_vs_unallocated)

        print("Below is how each resource is currently distributed across the camps: ")

        move = pd.DataFrame(columns=['resourceID', 'name', 'action', 'campID', 'moveUnits'])
        move_id_list = []
        move_name_list = []
        move_action_list = []
        nove_camp_list = []
        move_units_list = []

        while True: 
            ###################################################################
            # select single resource
            r_id_select = int(input("\nPlease enter the resourceID of the UNALLOCATED item you would like to manually redistribute: --> "))
            r_name_select = self.unallocResources_df.loc[self.unallocResources_df['resourceID'] == r_id_select, 'name'].iloc[0]

            # get the user to select the origin & destination camp:
            c_id = int(input(f"\nPlease enter the relevant campID for the *** Resource ID {r_id_select}: {r_name_select} *** : --> "))

            action = input(f"Would you like to assign the unallocated resource to campID {c_id}; or unassign the resource from campID {c_id} back into unallocated ? \nassign / unassign -->")
            
            # get unit number. ######## Note to self / team!!!! PROBABLY NEED TO ADD VALIDATION LATER!!!! #########
            move_units = int(input(f"\n Please enter the amount of *** Resource ID {r_id_select}: {r_name_select} *** to manually re-allocate: "))

            move_id_list.append(r_id_select)
            move_name_list.append(r_name_select)
            nove_camp_list.append(c_id)
            move_action_list.append(action)
            move_units_list.append(move_units)

            # Ask if the user is done
            done = input("\n Are there any more resources you want to manually allocate? y / n -->  ").strip()
            if done == 'n':
                break
            
        
        move['resourceID'] = move_id_list
        move['name'] = move_name_list
        move['action'] = move_action_list
        move['campID'] = nove_camp_list
        move['moveUnits'] = move_units_list
        
        
        print(f"""==========================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ Below are your selected manual re-allocations between unallocated resources: ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
==========================================================================\n
        {move.to_string(index=False)} \n"""
        )
        confirm_move = input("Proceed to re-allocate? \n [y] Yes; \n [x] Abandon manual allocation \n --> ")
        if confirm_move == 'y':
            ### here, we will need to print to two or multiple csvs, as opposed to just one - as the net amount is changing
            resourceManualAllocs = self.resourceAllocs_df
            unallocManualResources = self.unallocResources_df
            for index, row in move.iterrows():
                # to make the manual moves, we need to identify (resource_id, campID) pairs for origin & destination
                condition = (resourceManualAllocs['resourceID'] == row['resourceID']) & (resourceManualAllocs['campID'] == row['campID'])

                if row['action'] == 'assign':
                    # assigning unallocated resources to camps 
                    # the camp can either already have some of that resource - in which case the (resourceID, campID) pair should already exist in 'resourceAllocation'
                    # or it may not have that resource at all, in which case we need to insert a new row 
                    ############ FOR JESS TO COME BACK TO: NEED TO ADD CHECKER FOR IF CAMP OPENED / CLOSED
                    # 1) add qty to resourceAllocation
                    if condition.any():
                        ###
                        resourceManualAllocs.loc[condition, 'qty'] += row['moveUnits'] 
                    else:
                        ###
                        new_row_resourceAllocs = {'resourceID': row['resourceID'], 'campID': row['destination_campID'], 'qty': row['moveUnits']}
                        resourceManualAllocs = resourceManualAllocs.append(new_row_resourceAllocs, ignore_index=True)
                    # 2) subtract qty from resourceUballocatedStock
                    unallocManualResources.loc[unallocManualResources['resourceID'] == row['resourceID'], 'unallocTotal'] -= row['moveUnits']
                    ############ ERROR HANDLING: CHECK FOR LEGAL VALUES TO TAKE AWAY AND SUBTRACT
                    
                elif row['action'] == 'remove':
                    ### removing items from a camp and putting it into unallocated stock
                    ### the (resourceID, campID) pair should always already exist in 'resourceAllocation'
                    resourceManualAllocs.loc[condition, 'qty'] -= row['moveUnits'] ### 1) subtract from allocated
                    unallocManualResources.loc[unallocManualResources['resourceID'] == row['resourceID'], 'unallocTotal'] += row['moveUnits'] ### 2) add to unallocated
                else:
                    print("Erorr: unidentified allocation action")

                ###### error handling ---> assumess there is only 1 unique pairwwise combo. does not consider if the pair is in the table twice 
                    
            ### We will need to update all 3 files:
            # 1) resourceAllocs - changes in camp inventory resource assignment as above
            resourceManualAllocs.to_csv(self.resource_allocaation_csv_path, index=False)
            # 2) unallocResources - changes in unallocated inventory as above
            unallocManualResources.to_csv(self.resource_allocaation_csv_path, index=False)
            # 3) since the net total amount has now changed... we also need to recalculate the totals in resourceStock:
            totalManualResources = self.totalResources_df ### the total numbers in this are out of date and we need to update them using resourceManualAllocs
            ## use resourceID as the match key 
            joined_df = pd.merge(totalManualResources, resourceManualAllocs, on='resourceID', how='inner')
            resource_sum = joined_df.groupby('resourceID').agg({
                'name': 'first',  # Keeps the first name for each group
                'qty': 'sum',  # Sums the qty for each camp >> we ignore the 'total' column in totalManualResources
                'priorityLvl': 'first',  
            }).reset_index()
            resource_sum.to_csv(self.resource_stock_csv_path, index=False)
            

            #### write it in; and then run the report generator again to create an after table grouped by campID 
            resource_stats_instance_AFTER = ResourceReport()
            post_manual_alloc_camp_df = resource_stats_instance_AFTER.resource_report_camp_vs_unallocated()

            print(f"""\n ======= ＼(^o^)／ Manual Re-allocation of Unallocated Resources Successful! ＼(^o^)／ ===== \n
Below are the before vs. current resource allocations by camp & unllocated resources: \n"""
        )
            print("BEFORE: \n")
            print(all_resource_camp_camp_vs_unallocated.to_string(index=False))
            print("\nAFTER: \n")
            print(post_manual_alloc_camp_df)



        return resourceManualAllocs