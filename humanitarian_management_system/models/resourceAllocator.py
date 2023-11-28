import pandas as pd
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


    def redistribute(self):
        resource_stats_instance = ResourceReport()

        # resource stock total... >> can probably remove the need for this later 
        totalResources = self.totalResources_df

        alloc_ideal = resource_stats_instance.determine_above_below() # how to get this ? 
        alloc_ideal['updated'] = alloc_ideal['current']

        for index, row in alloc_ideal.iterrows():
            if row['status'] != 'balanced':
                alloc_ideal.at[index, 'updated'] = row['ideal_qty'] 
                ### if the status is not balanced, then update the quantity column with the ideal amount 
        
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

        ###### need to write the redistributed amount into the actual CSV
        redistribute_sum_checker = alloc_ideal.groupby('resourceID')['updated'].sum()

        ###### validate the redistributed totals, against the actual totals.
        ###### this is just incase there is any discrepancies from rounding.
        if 'resourceID' in totalResources.columns:
            totalResources.set_index('resourceID', inplace=True)
        comparison_result = redistribute_sum_checker == totalResources['total']
        print(alloc_ideal)
        
        #### write to csv
        alloc_updated = alloc_ideal.iloc[:, :3]
        alloc_updated = alloc_updated.rename(columns={alloc_updated.columns[2]: 'qty'})
        print(alloc_updated)
        alloc_updated.to_csv(self.resource_allocaation_csv_path, index=False)

        ### print success msg
        print("\n ======= ＼(^o^)／ AUTO-REDISTRIBUTION SUCCESSFUL! ＼(^o^)／ ===== \n Check resourceAllocation.csv or [1] View Resource Statistics to see! \n")
        ######## maybe redirect the menus


        ###### note for jess is to do a before and after of the reallocation


        return alloc_ideal, redistribute_sum_checker, comparison_result
    
    def manual_alloc(self):
        # add stuff to deal with unallocated items later bc i think its a bit different. right now i think is just about getting a function that works 
        resource_stats_instance = ResourceReport()
        print("Below is how each resource is currently distributed across the camps: ")
        all_resource_camp_df = resource_stats_instance.resource_report_camp()
        print(all_resource_camp_df)

        move = pd.DataFrame(columns=['resourceID','origin_campID', 'destination_campID', 'moveUnits'])
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
            moveUnits = int(input(f"\n Please enter the amount of *** Resource ID {r_id_select}: {r_name_select} *** to manually re-allocate: "))

            # Ask if the user is done
            done = input("\n Are there any more resources you want to manually allocate? y / n -->  ").strip().lo
            if done == 'n':
                break
            return
        
        ####