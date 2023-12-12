import pandas as pd
import numpy as np
from pathlib import Path
from .resourceReport import ResourceReport
import time


class ResourceAllocator():
    def __init__(self):
        
        self.resource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        self.resource_allocaation_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        self.resource__nallocated_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceUnallocatedStock.csv")
        self.totalResources_df = pd.read_csv(self.resource_stock_csv_path)
        self.resourceAllocs_df = pd.read_csv(self.resource_allocaation_csv_path)
        self.unallocResources_df = pd.read_csv(self.resource__nallocated_stock_csv_path)
        self.joined_df = pd.merge(self.totalResources_df, self.resourceAllocs_df, on='resourceID', how='inner')

    def jess_funky_timer(self, multiple):
        for i in range(multiple):
            print('... ┌(;･_･)┘ LOADING ... ')
            time.sleep(0.15)
            print('... └(･_･;)┐ LOADING ... ') 
            print("\n")
            time.sleep(0.15)

    def auto_alloc_interface(self):
        report_instance = ResourceReport()
        # POSSIBLY REMOVE BUT OVERWRITING THE TOTALS ! 
        # updateTotals = report_instance.resourceStock_generator(self.resourceAllocs_df)
        # updateTotals.to_csv(self.resource_stock_csv_path, index=False)
        #
        before_auto_alloc = report_instance.master_resource_stats() 
        ## run an instance of the table before modifying the source data to include unallocated soruces, if the user so wishes
        ## this is so that our table will pick up the before of unallocated resource integration

        unalloc_status, prompt = report_instance.unalloc_resource_checker()
        if unalloc_status == True:
            # user can choose if they want to do this manually or automatically, same as above actually
            # is there a way we can reuse the same code ?? <- if we merge it into the same files....
            include_unassigned = report_instance.input_validator('Do you want to include unallocated resources in the auto-distribution? y / n --> ', ['y', 'n'])
            if include_unassigned == 'y':
                self.add_unalloc_resource()  # ## add the unassigned resources to the
                # totalResources, ready for assignment by running auto_alloc immediately after
                self.jess_funky_timer(2)
                print("\nUnallocated resources from inventory will be included in auto-allocation to valid camps.\n")
                self.jess_funky_timer(2)
            elif include_unassigned == 'RETURN':
                return
            else:
                self.jess_funky_timer(2)
                print("\nSkipping addition of unallocated resources.\n")
                self.jess_funky_timer(2)
        else:
            print("\nCheck complete: No unallocated resources found, proceeding with auto-allocation...\n")
            self.jess_funky_timer(2)

        print(f"""\n================================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ [ 4.1.2 ] RESOURCE AUTO-ALLOCATION ACROSS ALL CAMPS ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
================================================================================\n
""")
        self.auto_alloc()  
        ### print success msg
        self.jess_funky_timer(2)
        print("\n======= ＼(^o^)／ AUTO-REDISTRIBUTION SUCCESSFUL! ＼(^o^)／ ===== \n \nBelow are the before & after auto-allocation: \n")
        ######## maybe redirect the menus
        report_instance_AFTER = ResourceReport()
        print("BEFORE: \n")
        before_pretty = report_instance_AFTER.PRETTY_PIVOT_CAMP(before_auto_alloc)
        print(before_pretty.to_string(index=False).replace('.0', '  '))
        print("\nAFTER: \n")
        
        after = report_instance_AFTER.master_resource_stats()
        after_pretty = report_instance_AFTER.PRETTY_PIVOT_CAMP(after)
        print(after_pretty.to_string(index=False).replace('.0', '  '))

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
        r_inst = ResourceReport()
        status, prompt = r_inst.unalloc_resource_checker() # how to get this ? 
        
        if status == False:
            print("\n ======= ＼(^o^)／ Unallocated Resources Ready for Allocation! ＼(^o^)／ ===== \n")
            pass
        else:
            print("Error: adding unallocated resources unsuccessful...")
        return self.totalResources_df

    def adjust_auto_alloc(self, alloc_ideal):
        redistribute_sum_checker = alloc_ideal.groupby('resourceID')['updated'].sum()
        comparison_result = redistribute_sum_checker == self.totalResources_df['total']

        for resource_id, is_equal in comparison_result.items():
            if not is_equal:
                delta = redistribute_sum_checker[resource_id] - self.totalResources_df['total'][resource_id]
                resource_id_match_df = alloc_ideal[alloc_ideal['resourceID'] == resource_id]
                max_qty_r_id =  resource_id_match_df['updated'].max()
                row_indices = resource_id_match_df[resource_id_match_df['updated'] == max_qty_r_id].index

                delta_per_row = delta / len(row_indices)
                for row_index in row_indices:
                    adjusted_value = max(alloc_ideal.loc[row_index, 'updated'] - delta_per_row, 0)
                    alloc_ideal.loc[row_index, 'updated'] = adjusted_value

        return alloc_ideal

    def auto_alloc(self):
        r_inst = ResourceReport()
        ### the adding is done before in a different function, so by the time it  makes it here, we have already added to the auto_alloc.... so need to get the unallocTotal elsewhere. 

        totalResources = self.totalResources_df

        try:
            alloc_ideal = r_inst.determine_above_below()
            self.jess_funky_timer(2)
            print("\n...STEP 1: successfully calculated ideal allocation levels for all open camps with refugees...\n")
            time.sleep(0.5)
            print("\nideal resource per camp = camp refugee population / total refugees in all open camps X total amount of that resource\n")
            time.sleep(0.5)
            self.jess_funky_timer(2)
            print("\n...STEP 2: comparing current quantity to ideal quantity each resource per camp...\n")
            # print(alloc_ideal)
            for line in alloc_ideal.to_string(index = False).split('\n'):
                print(line)
                time.sleep(0.05)
            print("\n...see allocation map above...\n")
        except Exception as e:
            print(f"An error occurred : {e}")
        alloc_ideal['updated'] = alloc_ideal['current']

        for index, row in alloc_ideal.iterrows():
            if row['status'] != 'balanced':
                alloc_ideal.at[index, 'updated'] = row['ideal_qty'] 
                ### if the status is not balanced, then update the quantity column with the ideal amount 
        '''
        self.jess_funky_timer(2)
        print("\n...STEP 3: for balanced resources within +/-10% threshold of ideal, leave them be...\n")
        self.jess_funky_timer(2)
        print("\n...STEP 4: for unbalanced resources (any above / below), update the current quantity to match the ideal quantity...\n")
        # print(alloc_ideal) ###### intermediary checks 
        
        self.jess_funky_timer(2)
        print("\n...STEP 5: check against total per resource included in this auto-allocation...\n")
        self.jess_funky_timer(2)
        print("\n...due to the threshold range & rounding in calculations; we need to make small adjustments to ensure the totals are the same before & after auto-allocation...\n")
        # Now need to check, how the sum compares to the total amounts and make small tweaks... 
        '''
        redistribute_sum_checker = alloc_ideal.groupby('resourceID')['updated'].sum()


        '''
        # print(totalResources)
        comparison_result = redistribute_sum_checker == totalResources['total']
        print(comparison_result)
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
        '''
        '''
        # recheck the balanced...
        self.jess_funky_timer(2)
        print("\n...successfully checked that totals match...\n")
        '''

        ###### validate the redistributed totals, against the actual totals.
        ###### this is just incase there is any discrepancies from rounding.
        if 'resourceID' in totalResources.columns:
            totalResources.set_index('resourceID', inplace=True)
        comparison_result = redistribute_sum_checker == totalResources['total']
        # print(alloc_ideal)
        alloc_ideal = self.adjust_auto_alloc(alloc_ideal)
        #### write to csv
        alloc_updated = alloc_ideal[['resourceID', 'campID', 'updated']]
        alloc_updated = alloc_updated.rename(columns={alloc_updated.columns[2]: 'qty'})
        # print(alloc_updated)
        alloc_updated.to_csv(self.resource_allocaation_csv_path, index=False)

        #print(alloc_updated)
        #print(r_inst.resourceStock_generator(alloc_updated))


        return alloc_ideal, redistribute_sum_checker, comparison_result
    
    def manual_alloc(self):
        # add stuff to deal with unallocated items later bc i think its a bit different. right now i think is just about getting a function that works 
        print(f"""\n==========================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ [ 4.1.1 ] MANUAL RESOURCE ALLOCATOR ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
==========================================================================\n""")
        r_inst = ResourceReport()
        print("Below is how each resource is currently unallocated vs. how many is distributed across the camps: \n")
        master_table = r_inst.master_resource_stats()
        master_table_pretty = r_inst.PRETTY_PIVOT_CAMP(master_table)
        print(master_table_pretty.to_string(index=False).replace('.0', '  '))

        status, unalloc_prompt = r_inst.unalloc_resource_checker()

        move = pd.DataFrame(columns=['resourceID', 'name', 'origin_campID', 'destination_campID', 'moveUnits', 'action', 'actionInfo'])
        do_not_calc = False

        already_selected = []

        while True: 
            ################ Begin with asking the user what type of manual allocation they want to make:
            action_string_list = ["[1] ASSIGN:    inventory ->  camp", "[2] UNASSIGN:  camp      ->  inventory", "[3] RE-ASSIGN: camp      <-> camp"]
            print("\nWhat type of manual allocation would you like to make? Enter 1, 2, 3 or RETURN to exit.")
            for action_string in action_string_list:
                print(action_string)

            prompt = "--> "
            action_select = r_inst.input_validator(prompt, [1,2,3])
            if action_select == 'RETURN':
                return
            action_string = [item for item in action_string_list[action_select-1].split(' ') if item.strip()]
            action_string_pretty = (" ").join(action_string)
            print(f"\n\033[95mYou have selected: {action_string_pretty}\033[0m\n")

            ###################################################################
            # Give user different form prompts depending on choice
            # select single resource
            #if action_select.lower() == 'return':
                #return
            ###### if user chooses 1 then... first check that there are unallocated resources. kick them out if not. 
            if action_select == 1:
                if status == False: 
                    ### if there are no unallocated resources, then no inventory to move from camp, tell the user this and ask them to select another option
                    print('\nThere are no unallocated resources here for you to assign to camps, taking you back to resource mgmt menu... ')
                    do_not_calc = True
                    break 


            ### the resourceID valid range is different depending on origin
            if action_select == 1: # should be only if there are unallocated resources... 
                unalloc_items = r_inst.valid_unalloc_resources()
                print(f"\nHere are the current unallocated resources: \n{unalloc_items.to_string(index=False)}\n")
                print("\nPlease enter the resourceID:")
                if already_selected: # if not empty 
                    print(f"Note you have already made selection(s) for Resource IDs: {set(already_selected)} ")   
                #r_id_select = r_inst.input_validator(prompt, valid_range)
                #if r_id_select == 'RETURN':
                    #return
                r_id_select = r_inst.input_validator_2range_resources("--> ", already_selected, move, 'manual_alloc')
                if r_id_select == 'RETURN':
                    return
                r_name_select = self.unallocResources_df.loc[self.unallocResources_df['resourceID'] == r_id_select, 'name'].iloc[0]
                already_selected.append(r_id_select)
                pass
            else: # where the origin is a camp (action 2 & 3) - the valid ranges & displays are different
                # r_id_select = int(input("\nPlease enter the resourceID of the item: --> "))
                print("\nPlease enter the resourceID:")
                if already_selected: # if not empty 
                    print(f"fNote you have already made selection(s) for Resource IDs: [{set(already_selected)}]. ")   
                #print(move)
                r_id_select = r_inst.input_validator_2range_resources("--> ", already_selected, move, 'manual_alloc')  ############# validation begins immediately... 
                if r_id_select == 'RETURN':
                    return
                r_name_select = self.unallocResources_df.loc[self.unallocResources_df['resourceID'] == r_id_select, 'name'].iloc[0]
                # how much of this resource is allocated in each camp & uallocated currently 
                already_selected.append(r_id_select)
                
                print(f"\n\033[93m*** Resource ID {r_id_select}: {r_name_select} *** is currently distributed as below: \033[0m\n")
                single_resource = r_inst.PRETTY_RESOURCE(master_table, [r_id_select])
                print(single_resource.to_string(index=False).replace('.0', '  '))

            if action_select == 3: 
                # [3] RE-ASSIGN: camp <-> camp /// two camps need to be identified - origin & destination
                # origin_c_id = int(input(f"\nPlease enter the ORIGIN campID (from the above) where you would like to REMOVE *** Resource ID {r_id_select}: {r_name_select} *** from: ")
                
                valid_range = r_inst.valid_origin_camp_single_resource(r_id_select)[1]
                print(f"\nPlease enter the \033[95mORIGIN campID to REMOVE \033[0mResource ID {r_id_select}: {r_name_select} from: ")
                print(f"\033[92mValid campIDs are any currently with resources: {valid_range}\033[0m")

                origin_c_id = r_inst.input_validator("--> ", valid_range, '\033[91mPlease select a camp that both: has at least 1 unit of the resource AND is open with refugees.\033[0m') 
                if origin_c_id == 'RETURN':
                    return

                ### ask user what resource id they want to move... maybe just do the quantity checker later. or can do right now... 


                # destination_c_id = int(input(f"\nPlease enter the DESTINATION campID (from any open campID) where you would like to ADD *** Resource ID {r_id_select}: {r_name_select} *** to: "))
                valid_range = r_inst.valid_open_camps_with_refugees()
                valid_range = valid_range['campID'].tolist()
                print(f"\nPlease enter the \033[95mDESTINATION campID to ADD \033[0mResource ID {r_id_select}: {r_name_select} to: ")
                print(f"\033[92mValid campIDs are open & has at least one refugee: {valid_range}\033[0m")
                destination_c_id = r_inst.input_validator("--> ", valid_range, '\033[91mPlease select a valid camp.\033[0m') 
                if destination_c_id == 'RETURN':
                    return
            
            else: 
                ##################### [1] & [2] movement between inventory
                # get corresponding camp:
                prompt = f"\nPlease enter the relevant \033[95mcampID\033[0m for the Resource ID {r_id_select}: {r_name_select}: --> "
                if action_select == 1:
                    # [1] ASSIGN: inventory -> camp
                    origin_c_id = np.nan
                    valid_range = r_inst.valid_open_camps_with_refugees()
                    valid_range = valid_range['campID'].tolist()
                    destination_c_id = r_inst.input_validator(prompt, valid_range, 'Please select a valid camp that is open and has refugees.')
                    if destination_c_id == 'RETURN':
                        return  
                elif action_select == 2:
                    # [2] UNASSIGN: camp -> inventory
                    valid_range = r_inst.valid_origin_camp_single_resource(r_id_select)[1] ######################
                    origin_c_id = r_inst.input_validator(prompt, valid_range, 'Please select a camp that both: has at least 1 unit of the resource AND is open with refugees. ') 
                    if origin_c_id == 'RETURN':
                        return
                    destination_c_id = np.nan
                else:
                    print("Error")

            ### seperate loop for validating entries. Action 2 & 3 are grouped together as they invole taking away a resource from a camp, so the amount must not exced that in stock for the camp
            ### Action 1's valid range is the unallocated resources levels 
            # get unit number. ######## RESOURCE FORM VALIDATION: PROBABLY NEED TO ADD VALIDATION LATER!!!! ######### - might need to move these into the loops

            if action_select == 1:
                upper_limit = self.unallocResources_df.loc[self.unallocResources_df['resourceID']==r_id_select, 'unallocTotal'].iloc[0]
            else:
                single_resource_stats = r_inst.valid_origin_camp_single_resource(r_id_select)[0]
                r_id_qty = single_resource_stats.iloc[:, 4:] ### how to get quantity?? 
                upper_limit = r_id_qty[origin_c_id].iloc[0]
                
            # building the valid range4 - which is... for that selected camp are moving FROM (origin), the moveUnits must not exceed the resource already there
            # do this by reusing the single_stats_instance
            valid_range = list(range(0, int(upper_limit)+1))
            error_msg = f"Please enter an amount between 0 and {int(upper_limit)} for this resource.\033[0m"
            prompt = f"\n\033[91mPlease enter the \033[95mAMOUNT\033[0m of Resource ID {r_id_select}: {r_name_select} to move [between 0 and {int(upper_limit)}]: "
            move_units = r_inst.input_validator(prompt, valid_range, error_msg)
            if move_units == 'RETURN':
                return

            new_row = pd.DataFrame({'resourceID': [r_id_select], 
                                    'name':[r_name_select], 
                                    'origin_campID':[origin_c_id], 
                                    'destination_campID':[destination_c_id], 
                                    'moveUnits':[move_units], 
                                    'action':[action_select], 
                                    'actionInfo':[action_string_pretty]})
            move = pd.concat([move, new_row], ignore_index=True)

            # Ask if the user is done
            # done = input("\n Are there any more resources you want to manually allocate? y / n -->  ").strip()

            done = r_inst.input_validator("\nAre there any more resources you want to manually allocate? y / n \n-->  ", ['y', 'n'])
            if done == 'n':
                break # exit the loop
            elif done == 'RETURN':
                return # exit the function
            else:
                pass
            
        if do_not_calc == False:
            self.manual_alloc_calc(move, master_table)

        return move
        
    def manual_alloc_calc(self, move: pd.DataFrame, master_table):
        ##### this is more like part 2 of the function. the calculator; vs. previous was the input forms. 
        ###  dont need to execute this if user selects 1 & from above and there are no unallocated resources 

        ### how to run this conditionally, depending whats in the function in layer above ? 
        r_inst = ResourceReport()
        move_print = move[['resourceID', 'name', 'origin_campID', 'destination_campID', 'moveUnits', 'actionInfo']]

        print(f"""\n=============================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ Below are your selected manual re-allocations: ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
=============================================================================\n
        \n{move_print.transpose().to_string(header = False)} \n"""
        )
        confirm_move = r_inst.input_validator("Proceed to re-allocate? \n [y] Yes; \n [x] Abandon manual allocation \n --> ", ['y','x'])
        if confirm_move == 'RETURN':
                return
        if confirm_move == 'y':
            ### there are potentially changes needed to be written to all 3 resource CSVs
            ### the specific changes depends on the action
            resourceCampMap = self.resourceAllocs_df
            unallocManualResources = self.unallocResources_df

            for index, row in move.iterrows():

                if row['action'] == 3: 
                    # [3] RE-ASSIGN: camp <-> camp
                    origin_condition = (resourceCampMap['resourceID'] == row['resourceID']) & (resourceCampMap['campID'] == row['origin_campID'])
                    # print(origin_condition.any())
                    # print(resourceCampMap.loc[origin_condition, 'qty'])
                    resourceCampMap.loc[origin_condition, 'qty'] -= row['moveUnits'] ### substract / remove from the origin camp
                    ###### error handling ---> assumess there is only 1 unique pairwwise combo. does not consider if the pair is in the table twice 

                    dest_condition = (resourceCampMap['resourceID'] == row['resourceID']) & (resourceCampMap['campID'] == row['destination_campID'])
                    if dest_condition.any():
                        resourceCampMap.loc[dest_condition, 'qty'] += row['moveUnits'] 
                        ### add to the destination camp
                    else:
                        # create the row in resourceAllocator if it does not exist
                        new_row = {'resourceID': row['resourceID'], 'campID': row['destination_campID'], 'qty': row['moveUnits']}
                        #print(type(resourceCampMap))
                        #resourceCampMap = resourceCampMap.append(new_row, ignore_index=True)
                        resourceCampMap = pd.concat([resourceCampMap, pd.DataFrame([new_row])], ignore_index=True)
                    
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
                            print(type(resourceCampMap))
                            # resourceCampMap = resourceCampMap.append(new_row, ignore_index=True)
                            resourceCampMap = pd.concat([resourceCampMap, pd.DataFrame([new_row])], ignore_index=True)
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
            r_inst_AFTER = ResourceReport()
            master_after = r_inst_AFTER.master_resource_stats()
            

            print(f"""\n ======= ＼(^o^)／ Manual Re-allocation of Resources Successful! ＼(^o^)／ ===== \n
Below are the before vs. current allocations of the impacted resources: \n"""
        )
            print("BEFORE: \n")
            ### be cleaner & only print the rows that have been changed, 
            
            selected_before_pretty = r_inst_AFTER.PRETTY_RESOURCE(master_table, move['resourceID'].tolist())  ## note it doesnt matter so much here we are using the AFTER instance on before data
            print(selected_before_pretty.to_string(index=False).replace('.0', '  '))
            print("\nAFTER: \n")
            selected_after_pretty = r_inst_AFTER.PRETTY_RESOURCE(master_after, move['resourceID'].tolist())
            print(selected_after_pretty.to_string(index=False).replace('.0', '  '))
            return resourceCampMap
        
        ####


