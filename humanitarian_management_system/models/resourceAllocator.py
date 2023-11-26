import pandas as pd
from humanitarian_management_system.helper import (extract_data, modify_csv_value, modify_csv_pandas, extract_data_df,
                                                   extract_active_event)
from pathlib import Path
from resourceReport import ResourceReport


# A very basic attempt at resource allocation to camp, it's basically just a manipulation of database/csv files by
# looping through them when necessary
class ResourceAllocator():
    def __init__(self):
        
        self.resourceLibrary_df = extract_data_df("data/resourceStock.csv")
        self.resourceAllocs_df = extract_data_df("data/resourceAllocation.csv")
        self.joined_df = pd.merge(self.resourceLibrary_df, self.resourceAllocs_df, on='resourceID', how='inner')

    def redistribute(self):
        resource_stats_instance = ResourceReport()
        # resource stock total... >> can probably remove the need for this later 
        totalResources = extract_data_df("data/resourceStock.csv")

        alloc_ideal = resource_stats_instance.determine_above_below() # how to get this ? 
        alloc_ideal['updated'] = alloc_ideal['current']

        for index, row in alloc_ideal.iterrows():
            if row['status'] != 'balanced':
                row['updated'] = row['ideal_qty']
        
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
        return redistribute_sum_checker, comparison_result