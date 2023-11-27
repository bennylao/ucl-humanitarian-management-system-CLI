import pandas as pd
from humanitarian_management_system.helper import (extract_data, modify_csv_value, modify_csv_pandas, extract_data_df,
                                                   extract_active_event)
from pathlib import Path
from resourceReport import ResourceReport


# A very basic attempt at resource allocation to camp, it's basically just a manipulation of database/csv files by
# looping through them when necessary
class ResourceAllocator():
    def __init__(self):
        resource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        resource_allocaation_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        resource__nallocated_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceUnallocatedStock.csv")
        self.totalResources_df = pd.read_csv(resource_stock_csv_path)
        self.resourceAllocs_df = pd.read_csv(resource_allocaation_csv_path)
        self.unallocResources_df = pd.read_csv(resource__nallocated_stock_csv_path)
        self.joined_df = pd.merge(self.totalResources_df, self.resourceAllocs_df, on='resourceID', how='inner')

    def add_unalloc_resource(self):
        # adding unallocated resources to the total resources dataframe, preparing it for the (auto) distribution... 
        # note that i think this is only relevant to automatic reallocation only... 

        ## THIS IS AN INTERMEDIATE FUNCTION: AFTER WE DO THIS, THE TOTAL WILL NO LONGER MATCH THE TOTAL
        ## OF RESOURCEALLOCATION.CSV !!!!!!! AKA IT IS IMPORTANT WE RE RUN THE DISTRIBUTOR IMMEDIATELY AFTER

        self.totalResources_df['total'] = self.totalResources_df['total'] + self.unallocResources_df['unallocTotal']
        # overwrite total resource amounts
        self.totalResources_df.to_csv("humanitarian_management_system/data/resourceStock.csv", index=False)
        # overwrite unallocated resources to all zeros
        self.unallocResources_df['unallocTotal'] = 0
        self.unallocResources_df.to_csv("humanitarian_management_system/data/resourceUnallocatedStock.csv", index=False)

        ## to be robust, can call ResourceReport.unalloc_resource_checker(self) to check? 
        resource_stats_instance = ResourceReport()
        status, prompt = resource_stats_instance.unalloc_resource_checker() # how to get this ? 
        if status == False:
            #print(prompt)
            pass
        else:
            print("Error: adding unallocated resources unsuccessful...")
        return self.totalResources_df


    def redistribute(self):
        resource_stats_instance = ResourceReport()
        # resource stock total... >> can probably remove the need for this later
        resource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        totalResources = pd.read_csv(resource_stock_csv_path)

        alloc_ideal = resource_stats_instance.determine_above_below() # how to get this ? 
        alloc_ideal['updated'] = alloc_ideal['current']

        for index, row in alloc_ideal.iterrows():
            if row['status'] != 'balanced':
                alloc_ideal.at[index, 'updated'] = row['ideal_qty'] ### if the status is not balanced, then update the quantity column with the ideal amount 
        
        print(alloc_ideal)
        
        # Now need to check, how the sum compares to the total amounts and make small tweaks... 
        redistribute_sum_checker = alloc_ideal.groupby('resourceID')['updated'].sum()

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


                ###### need to write the redistributed amount into the actual CSV
        return alloc_ideal, redistribute_sum_checker, comparison_result