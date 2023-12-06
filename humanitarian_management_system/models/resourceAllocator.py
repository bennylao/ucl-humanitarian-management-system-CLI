import pandas as pd
import numpy as np
from pathlib import Path
from .resourceReport import ResourceReport


class ResourceAllocator():
    def __init__(self):
        
        self.resource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        self.resource_allocaation_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        self.resource__nallocated_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceUnallocatedStock.csv")
        self.totalResources_df = pd.read_csv(self.resource_stock_csv_path)
        self.resourceAllocs_df = pd.read_csv(self.resource_allocaation_csv_path)
        self.unallocResources_df = pd.read_csv(self.resource__nallocated_stock_csv_path)
        self.joined_df = pd.merge(self.totalResources_df, self.resourceAllocs_df, on='resourceID', how='inner')

    def add_unalloc_resource(self):
        # adding unallocated resources to the total resources dataframe, preparing it for the (auto) distribution... 
        # note that i think this is only relevant to automatic reallocation only... 

        ## THIS IS AN INTERMEDIATE FUNCTION: AFTER WE DO THIS, THE TOTAL WILL NO LONGER MATCH THE TOTAL
        ## OF RESOURCEALLOCATION.CSV !!!!!!! AKA IT IS IMPORTANT WE RE RUN THE DISTRIBUTOR IMMEDIATELY AFTER

        self.totalResources_df['total'] = self.totalResources_df['total'] + self.unallocResources_df['unallocTotal']
        # overwrite total resource amounts
        self.totalResources_df.to_csv(self.resource_stock_csv_path, index=False)
        # overwrite unallocated resources to all zeros
        self.unallocResources_df['unallocTotal'] = 0
        self.unallocResources_df.to_csv(self.resource__nallocated_stock_csv_path, index=False)

        ## to be robust, can call ResourceReport.unalloc_resource_checker(self) to check? 
        resource_stats_instance = ResourceReport()
        status, prompt = resource_stats_instance.unalloc_resource_checker() # how to get this ? 
        
        if status == False:
            print("\n ======= ＼(^o^)／ Unallocated Resources Ready for Allocation! ＼(^o^)／ ===== \n")
            pass
        else:
            print("Error: adding unallocated resources unsuccessful...")
        return self.totalResources_df


    def auto_alloc(self):
        resource_stats_instance = ResourceReport()
        all_resource_camp_vs_unallocated = resource_stats_instance.resource_report_camp_vs_unallocated() ### the adding is done before in a different function, so by the time it  makes it here, we have already added to the auto_alloc.... so need to get the unallocTotal elsewhere. 

        """         BEFORE: 

            resourceID                      name  priorityLvl  unallocTotal      3      5     6     9    11
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
        10          11  General Tools & Supplies            3             0  11385  27325  4554  4554  2277

        AFTER: 

            resourceID                      name  priorityLvl  unallocTotal      3      5     6     9    11
        0            1                  Blankets            2             0   2292   5500   917   917   458
        1            2                  Clothing            1             0    648   1555   259   259   130
        2            3                      Toys            3             0    288    691   115   115    58
        3            4                  Medicine            1             0     31     75    12    12     6
        4            5                  Vitamins            2             0     19     46     8     8     4
        5            6                      Food            1             0     23     56     9     9     5
        6            7                    Snacks            3             0     15     36     6     6     3
        7            8                Toiletries            2             0     19     46     8     8     4
        8            9                     Water            1             0     46    110    18    18     9
        9           10             Baby Supplies            1             0     23     56     9     9     5
        10          11  General Tools & Supplies            3             0  11385  27325  4554  4554  2277 """


        # resource stock total... >> can probably remove the need for this later 
        totalResources = self.totalResources_df

        try:
            alloc_ideal = resource_stats_instance.determine_above_below()
            print("\n...successfully calculated equilibrium allocation levels...\n")
        except Exception as e:
            print(f"An error occurred : {e}")
        alloc_ideal['updated'] = alloc_ideal['current']

        for index, row in alloc_ideal.iterrows():
            if row['status'] != 'balanced':
                alloc_ideal.at[index, 'updated'] = row['ideal_qty'] 
                ### if the status is not balanced, then update the quantity column with the ideal amount 
        print("\n...successfully updated qty of unbalanced resource allocations...\n")
        # print(alloc_ideal) ###### intermediary checks 
        
        # Now need to check, how the sum compares to the total amounts and make small tweaks... 
        redistribute_sum_checker = alloc_ideal.groupby('resourceID')['updated'].sum()

        ###### validate the redistributed totals, against the actual totals.
        ###### this is just incase there is any discrepancies from rounding.
        if 'resourceID' in totalResources.columns:
            totalResources.set_index('resourceID', inplace=True)

        # print(totalResources)
        comparison_result = redistribute_sum_checker == totalResources['total']
        # will output the resource_ids that are different 

        for resource_id, is_equal in comparison_result.items():
            if is_equal:
                #print("Success! Writing auto-redistributed to csv...")
                pass
            else:
                delta = redistribute_sum_checker[resource_id] - totalResources['total'][resource_id]
                # delta is positive if the refdistributed amount is higher than total <- means we need to subtract it 
                # delta is negative if the redistir5bute4d amount is lower than the true total, means we need to increase the amount. subtracting a negative number will do the trick. 
                # so should always be subtract eetla. 

                #print(f"The sum for resourceID {resource_id} is different by {delta} post distribution.")
                #print("Correcting...")

                ########### need to add logic for what to do, basically just adjust it from the camps with the most of that item, but this is an edge case, don't need to worry about it for now


                # get the ids whos totals do not match; and get the delta amount between the 2 tables; and then take this off the camp with the highest of that resource_id
                
                # Specified ID and adjustment value

                # Filter the alloc_ideal by the specific resource_id that isn't matching
                resource_id_match_df = alloc_ideal[alloc_ideal['resourceID'] == resource_id]
                # print(resource_id_match_df)
                # Find the maximum value in column 'c'
                max_qty_r_id =  resource_id_match_df['updated'].max()
                # print(max_qty_r_id)
                # Find the row with this maximum value
                row_index = alloc_ideal[(alloc_ideal['resourceID'] == resource_id) & (alloc_ideal['updated'] == max_qty_r_id)].index

                # Adjust the value in the original DataFrame
                alloc_ideal.loc[row_index, 'updated'] -= delta
                # print(alloc_ideal.loc[row_index, 'updated'])

        # recheck the balanced...
        print("\n...successfully checked that totals match...\n")

        ###### need to write the redistributed amount into the actual CSV
        redistribute_sum_checker = alloc_ideal.groupby('resourceID')['updated'].sum()

        ###### validate the redistributed totals, against the actual totals.
        ###### this is just incase there is any discrepancies from rounding.
        if 'resourceID' in totalResources.columns:
            totalResources.set_index('resourceID', inplace=True)
        comparison_result = redistribute_sum_checker == totalResources['total']
        # print(alloc_ideal)
        
        #### write to csv
        alloc_updated = alloc_ideal.iloc[:, :3]
        alloc_updated = alloc_updated.rename(columns={alloc_updated.columns[2]: 'qty'})
        # print(alloc_updated)
        alloc_updated.to_csv(self.resource_allocaation_csv_path, index=False)

        resource_stats_instance_AFTER = ResourceReport()
        post_manual_alloc_camp_df = resource_stats_instance_AFTER.resource_report_camp_vs_unallocated()

        ### print success msg
        print("\n ======= ＼(^o^)／ AUTO-REDISTRIBUTION SUCCESSFUL! ＼(^o^)／ ===== \n Below are the before & after auto-allocation: \n")
        ######## maybe redirect the menus


        ###### note for jess is to do a before and after of the reallocation
        print("BEFORE: \n")
        print(all_resource_camp_vs_unallocated)
        print("\nAFTER: \n")
        print(post_manual_alloc_camp_df)


        return alloc_ideal, redistribute_sum_checker, comparison_result
    
    def manual_alloc(self):
        # add stuff to deal with unallocated items later bc i think its a bit different. right now i think is just about getting a function that works 
        print(f"""\n==========================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ MANUAL RESOURCE ALLOCATOR ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
==========================================================================\n""")
        resource_stats_instance = ResourceReport()
        print("Below is how each resource is currently unallocated vs. how many is distributed across the camps: \n")
        all_resource_camp_vs_unallocated = resource_stats_instance.resource_report_camp_vs_unallocated()
        all_resource_camp_vs_unallocated.reset_index(inplace=True)
        print(all_resource_camp_vs_unallocated.to_string(index=False))

        status, unalloc_prompt = resource_stats_instance.unalloc_resource_checker()

        print("Below are the refugee populations of the camps that are currently open: \n")
        print(resource_stats_instance.valid_open_camps_with_refugees())

        move = pd.DataFrame(columns=['resourceID', 'name', 'origin_campID', 'destination_campID', 'moveUnits', 'action', 'actionInfo'])
        move_id_list = []
        move_name_list = []
        move_action_list = []
        move_origin_camp_list = []
        move_dest_camp_list = []
        move_units_list = []
        move_action_info_list = []
        do_not_calc = False

        while True: 
            ################ Begin with asking the user what type of manual allocation they want to make:
            action_string_list = ["[1] ASSIGN:    inventory ->  camp", "[2] UNASSIGN:  camp      ->  inventory", "[3] RE-ASSIGN: camp      <-> camp"]
            print("\nWhat type of manual allocation would you like to make? Enter 1, 2, 3 or RETURN to exit.")
            for action_string in action_string_list:
                print(action_string)

            prompt = "--> "
            action_select = resource_stats_instance.input_validator(prompt, [1,2,3])
            print(f"\nYou have selected: {action_string_list[action_select-1]}\n")

            ###################################################################
            # Give user different form prompts depending on choice
            # select single resource
            if action_select.lower() == 'return':
                return
            ###### if user chooses 1 then... first check that there are unallocated resources. kick them out if not. 
            if action_select == 1:
                if status == False: 
                    ### if there are no unallocated resources, then no inventory to move from camp, tell the user this and ask them to select another option
                    print('\nThere are no unallocated resources here for you to assign to camps, taking you back to resources menu... ')
                    do_not_calc = True
                    break 


            ### the resourceID valid range is different depending on origin
            if action_select == 1: # should be only if there are unallocated resources... 
                unalloc_items = resource_stats_instance.valid_unalloc_resources()
                print(f"\nHere are the current unallocated resources: \n{unalloc_items.to_string(index=False)}\n")
                prompt = "\nPlease enter the resourceID of the item: --> "    
                valid_range = unalloc_items['resourceID'].tolist()
                r_id_select = resource_stats_instance.input_validator(prompt, valid_range)
                r_name_select = self.unallocResources_df.loc[self.unallocResources_df['resourceID'] == r_id_select, 'name'].iloc[0]
                pass
            else: # where the origin is a camp (action 2 & 3) - the valid ranges & displays are different
                # r_id_select = int(input("\nPlease enter the resourceID of the item: --> "))
                prompt = "\nPlease enter the resourceID of the item: --> "    
                valid_range = resource_stats_instance.valid_resources()
                r_id_select = resource_stats_instance.input_validator(prompt, valid_range)  ############# validation begins immediately... 
                r_name_select = self.unallocResources_df.loc[self.unallocResources_df['resourceID'] == r_id_select, 'name'].iloc[0]
                # how much of this resource is allocated in each camp & uallocated currently 
                
                single_resource_stats = all_resource_camp_vs_unallocated[all_resource_camp_vs_unallocated['resourceID'] == r_id_select]
                print(f"\n*** Resource ID {r_id_select}: {r_name_select} *** is currently distributed as below: \n")
                print(single_resource_stats.to_string(index=False))

            print("\nBelow are the refugee populations & the camps that are currently open: \n")
            print(resource_stats_instance.valid_open_camps_with_refugees()) ### there should not be any camps with zero refugees. 

            if action_select == 3: 
                # [3] RE-ASSIGN: camp <-> camp /// two camps need to be identified - origin & destination
                # origin_c_id = int(input(f"\nPlease enter the ORIGIN campID (from the above) where you would like to REMOVE *** Resource ID {r_id_select}: {r_name_select} *** from: ")
                
                columns_with_all_values_above_zero = single_resource_stats.iloc[:, 4:].columns[(single_resource_stats.iloc[:, 4:] > 0).all()]
                valid_range = columns_with_all_values_above_zero.tolist()
                prompt = f"\nPlease enter the ORIGIN campID where you would like to REMOVE *** Resource ID {r_id_select}: {r_name_select} *** from: "
                origin_c_id = resource_stats_instance.input_validator(prompt, valid_range, 'Please select a valid camp where the resource is in stock.') ########### need to change this. is it those with refugees? or with non zero resources? 

                ### ask user what resource id they want to move... maybe just do the quantity checker later. or can do right now... 


                # destination_c_id = int(input(f"\nPlease enter the DESTINATION campID (from any open campID) where you would like to ADD *** Resource ID {r_id_select}: {r_name_select} *** to: "))
                prompt = f"\nPlease enter the DESTINATION campID where you would like to ADD *** Resource ID {r_id_select}: {r_name_select} *** to: "
                valid_range = resource_stats_instance.valid_open_camps_with_refugees()
                valid_range = valid_range['campID'].tolist()
                destination_c_id = resource_stats_instance.input_validator(prompt, valid_range, 'Please select a valid camp that is open and has refugees.') ########### need to change this. is it those with refugees? or with non zero resources? 
            else: 
                ##################### [1] & [2] movement between inventory
                # get corresponding camp:
                prompt = f"\nPlease enter the relevant campID for the *** [ Resource ID #{r_id_select}: {r_name_select} ] *** : --> "
                if action_select == 1:
                    # [1] ASSIGN: inventory -> camp
                    origin_c_id = np.nan
                    valid_range = resource_stats_instance.valid_open_camps_with_refugees()
                    valid_range = valid_range['campID'].tolist()
                    destination_c_id = resource_stats_instance.input_validator(prompt, valid_range, 'Please select a valid camp that is open and has refugees.')
                elif action_select == 2:
                    # [2] UNASSIGN: camp -> inventory
                    columns_with_all_values_above_zero = single_resource_stats.iloc[:, 4:].columns[(single_resource_stats.iloc[:, 4:] > 0).all()]
                    valid_range = columns_with_all_values_above_zero.tolist()
                    origin_c_id = resource_stats_instance.input_validator(prompt, valid_range, 'Please select a valid camp where there is at least 1 unit of the resource. ') 
                    destination_c_id = np.nan
                else:
                    print("Error")

            ### seperate loop for validating entries. Action 2 & 3 are grouped together as they invole taking away a resource from a camp, so the amount must not exced that in stock for the camp
            ### Action 1's valid range is the unallocated resources levels 
            # get unit number. ######## RESOURCE FORM VALIDATION: PROBABLY NEED TO ADD VALIDATION LATER!!!! ######### - might need to move these into the loops
            prompt = f"\nPlease enter the amount of *** [ Resource ID #{r_id_select}: {r_name_select} ] *** to move: "

            if action_select == 1:
                upper_limit = self.unallocResources_df.loc[self.unallocResources_df['resourceID']==r_id_select, 'unallocTotal'].iloc[0]
            else:
                r_id_qty = single_resource_stats.iloc[:, 4:] # remove first 4 columns (not relevant)
                upper_limit = r_id_qty[origin_c_id].iloc[0]
                
            # building the valid range4 - which is... for that selected camp are moving FROM (origin), the moveUnits must not exceed the resource already there
            # do this by reusing the single_stats_instance
            valid_range = list(range(1, int(upper_limit)+1))
            error_msg = f"Please enter an amount betwen 0 and {upper_limit} for this resource."
            move_units = resource_stats_instance.input_validator(prompt, valid_range, error_msg)

            move_id_list.append(r_id_select)
            move_name_list.append(r_name_select)
            move_origin_camp_list.append(origin_c_id)
            move_dest_camp_list.append(destination_c_id)
            move_action_list.append(action_select)
            move_units_list.append(move_units)

            # Ask if the user is done
            done = input("\n Are there any more resources you want to manually allocate? y / n -->  ").strip()
            if done == 'n':
                break
            
        
        move['resourceID'] = move_id_list
        move['name'] = move_name_list
        move['action'] = move_action_list
        move['origin_campID'] = move_origin_camp_list
        move['destination_campID'] = move_dest_camp_list
        move['moveUnits'] = move_units_list

        for action_num in move_action_list:
            move_action_info_list.append(action_string_list[action_num-1])
        move['actionInfo'] = move_action_info_list

        if do_not_calc == False:
            self.manual_alloc_calc(move, all_resource_camp_vs_unallocated)

        return move
        
    def manual_alloc_calc(self, move, all_resource_camp_vs_unallocated):
        ##### this is more like part 2 of the function. the calculator; vs. previous was the input forms. 
        ###  dont need to execute this if user selects 1 & from above and there are no unallocated resources 

        ### how to run this conditionally, depending whats in the function in layer above ? 

        print(f"""\n==========================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ Below are your selected manual re-allocations: ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
==========================================================================\n
        {move[['resourceID', 'name', 'origin_campID', 'destination_campID', 'moveUnits', 'actionInfo']]} \n"""
        )
        confirm_move = input("Proceed to re-allocate? \n [y] Yes; \n [x] Abandon manual allocation \n --> ")
        if confirm_move == 'y':
            ### there are potentially changes needed to be written to all 3 resource CSVs
            ### the specific changes depends on the action
            resourceCampMap = self.resourceAllocs_df
            unallocManualResources = self.unallocResources_df

            for index, row in move.iterrows():

                if row['action'] == 3: 
                    # [3] RE-ASSIGN: camp <-> camp
                    origin_condition = (resourceCampMap['resourceID'] == row['resourceID']) & (resourceCampMap['campID'] == row['origin_campID'])
                    print(origin_condition.any())
                    print(resourceCampMap.loc[origin_condition, 'qty'])
                    resourceCampMap.loc[origin_condition, 'qty'] -= row['moveUnits'] ### substract / remove from the origin camp
                    ###### error handling ---> assumess there is only 1 unique pairwwise combo. does not consider if the pair is in the table twice 

                    dest_condition = (resourceCampMap['resourceID'] == row['resourceID']) & (resourceCampMap['campID'] == row['destination_campID'])
                    if dest_condition.any():
                        resourceCampMap.loc[dest_condition, 'qty'] += row['moveUnits'] 
                        ### add to the destination camp
                    else:
                        # create the row in resourceAllocator if it does not exist
                        new_row = {'resourceID': row['resourceID'], 'campID': row['destination_campID'], 'qty': row['moveUnits']}
                        resourceCampMap = resourceCampMap.append(new_row, ignore_index=True)
                    
                else:
                    ##################### [1] & [2] movement between inventory
                    if row['action'] == 1: 
                        # [1] ASSIGN: inventory -> camp /////////// 
                        # to make the manual moves, we need to identify (resource_id, campID) pairs for origin & destination
                        condition = (resourceCampMap['resourceID'] == row['resourceID']) & (resourceCampMap['campID'] == row['destination_campID']) ### or 
                        # assigning unallocated resources to camps 
                        # the camp can either already have some of that resource - in which case the (resourceID, campID) pair should already exist in 'resourceAllocation'
                        # or it may not have that resource at all, in which case we need to insert a new row 
                        ############ FOR JESS TO COME BACK TO: NEED TO ADD CHECKER FOR IF CAMP OPENED / CLOSED
                        # 1) add qty to resourceAllocation
                        if condition.any():
                            ###
                            resourceCampMap.loc[condition, 'qty'] += row['moveUnits'] 
                        else:
                            ###
                            new_row = {'resourceID': row['resourceID'], 'campID': row['destination_campID'], 'qty': row['moveUnits']}
                            resourceCampMap = resourceCampMap.append(new_row, ignore_index=True)
                        # 2) subtract qty from resourceUballocatedStock
                        unallocManualResources.loc[unallocManualResources['resourceID'] == row['resourceID'], 'unallocTotal'] -= row['moveUnits']
                        ############ ERROR HANDLING: CHECK FOR LEGAL VALUES TO TAKE AWAY AND SUBTRACT
                        
                    elif row['action'] == 2:
                        ### removing items from a camp and putting it into unallocated stock
                        ### the (resourceID, campID) pair should always already exist in 'resourceAllocation'
                        condition = (resourceCampMap['resourceID'] == row['resourceID']) & (resourceCampMap['campID'] == row['origin_campID'])
                        resourceCampMap.loc[condition, 'qty'] -= row['moveUnits'] ### 1) subtract from allocated
                        unallocManualResources.loc[unallocManualResources['resourceID'] == row['resourceID'], 'unallocTotal'] += row['moveUnits'] ### 2) add to unallocated
                    else:
                        print("Erorr: unidentified allocation action")

                ###### RESOURCE ERROR HANDLING ---> assumess there is only 1 unique pairwwise combo. does not consider if the pair is in the table twice 
                    
            ### We will need to update all 3 files:
            # 1) resourceAllocs - changes in camp inventory resource assignment as above
            resourceCampMap.to_csv(self.resource_allocaation_csv_path, index=False)
            # 2) unallocResources - changes in unallocated inventory as above
            unallocManualResources.to_csv(self.resource__nallocated_stock_csv_path, index=False)
            # 3) since the net total amount has now changed... we also need to recalculate the totals in resourceStock:
            stockManualResources = self.totalResources_df ### the total numbers in this are out of date and we need to update them using resourceCampMap
            ## use resourceID as the match key 
            # print(stockManualResources)
            joined_df = pd.merge(stockManualResources.drop(['total'], axis=1, inplace=False), resourceCampMap, on='resourceID', how='inner')
            resource_sum = joined_df.groupby('resourceID').agg({
                'name': 'first',  # Keeps the first name for each group
                'qty': 'sum',  # Sums the qty for each camp >> we ignore the 'total' column in stockManualResources
                'priorityLvl': 'first',  
            }).reset_index()
            resource_sum.rename(columns={'qty': 'total'}, inplace=True)
            resource_sum.to_csv(self.resource_stock_csv_path, index=False)
            

            #### write it in; and then run the report generator again to create an after table grouped by campID 
            resource_stats_instance_AFTER = ResourceReport()
            post_manual_alloc_camp_df = resource_stats_instance_AFTER.resource_report_camp_vs_unallocated()

            print(f"""\n ======= ＼(^o^)／ Manual Re-allocation of Resources Successful! ＼(^o^)／ ===== \n
Below are the before vs. current resource allocation: \n"""
        )
            print("BEFORE: \n")
            print(all_resource_camp_vs_unallocated)
            print("\nAFTER: \n")
            print(post_manual_alloc_camp_df)


        return resourceCampMap
        
        ####
