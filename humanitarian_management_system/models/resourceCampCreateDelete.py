import pandas as pd
from pathlib import Path
from .resourceAdder import ResourceAdder
from .resourceReport import ResourceReport

#### this will deal with resource changes with new camp creation or deletion

class ResourceCampCreateDelete():
    def __init__(self):
        
        resource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        resource_allocaation_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        self.resource__nallocated_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceUnallocatedStock.csv")
        self.totalResources_df = pd.read_csv(resource_stock_csv_path)
        self.resourceAllocs_df = pd.read_csv(resource_allocaation_csv_path)
        self.unallocResources_df = pd.read_csv(self.resource__nallocated_stock_csv_path)
        self.joined_df = pd.merge(self.totalResources_df, self.resourceAllocs_df, on='resourceID', how='inner')

    def remove_camp_resources(self):
        ### we need to get the campid from somewhere, for now lets just set it ourselves,

        ### this should be able to be called on multiple camps at once, just run it several times :) 
        c_id = 1 ### change to input
        report_instance = ResourceReport()
        resource_camp = report_instance.resource_report_camp()
        resource_camp.reset_index(inplace=True)

        # we take vertical slice of the resource allocations per camp, and then add this to unalloc resource.
        resource_c_id = resource_camp[['resourceID','name', c_id]]
        print(f"\nHerer are the resources from the closed camp {c_id}, which will be unassgined back into inventory...\n")
        print(resource_c_id(index=False))

        # need to recalculate all 3 sheets 

        # first calculate...
        # unallocated stock - add the above to each resource. do mapping to be on safe side 
        inventory = self.unallocResources_df ## will always have more or equal 
        joined_df = pd.merge(inventory, resource_c_id, on='resourceID', how='outer').fillna(0) #join and then add... 
        joined_df['unallocTotal'] = joined_df[c_id] + joined_df['unallocTotal']
        new_unalloc = joined_df.drop(3, axis=1)

        # for allocations & totals = remove it from the map first, and then recalculate the sum 
        map = self.resourceAllocs_df
        remove = map['campID'] == c_id
        new_map = map[~remove]

        # recalc the sum
        assigned = self.totalResources_df
        joined_df = pd.merge(assigned.drop(['total'], axis=1, inplace=False), new_map, on='resourceID', how='inner')
        new_assigned = joined_df.groupby('resourceID').agg({
                        'name': 'first',  # Keeps the first name for each group
                        'qty': 'sum',  # Sums the qty for each camp >> we ignore the 'total' column in stockManualResources
                        'priorityLvl': 'first',  
                    }).reset_index()
        new_assigned.rename(columns={'qty': 'total'}, inplace=True)


        ### need to overwrite these ! for now just print is ok 

        print(pd.merge(new_unalloc, new_assigned, [['resourceID', 'unallocTotal']], on='resourceID', how='outer').fillna(0))

        pass

    def new_camp_resources(self, new_camp):
        map = self.totalResources_df
        ### assume we get a df input like the below 
        """     +-------------+------------+
                | new camp id | refugeepop |
                +-------------+------------+
                | 100         | 5          |
                | 101         | 6          |
                +-------------+------------+
        """

        ### mechanism to calculate starting amounts >> discuss w team how this is done! >> families etc? 
        # for now just do basics. 10 x refugeePop amount for each resource
        resourceID_val = map['resourceID'].unique().tolist()
        l = len(resourceID_val)
        for index, row in new_camp.iterrow():
            p = row['refugeePop']
            campID_list =+ [row['campID']] * l
            qty_list =+ [p*10] * l
        pd.DataFrame(map['resourceID'].unique())
        
        pass