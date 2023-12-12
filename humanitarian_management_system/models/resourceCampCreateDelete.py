import pandas as pd
from pathlib import Path
from .resourceAdder import ResourceAdder
from .resourceReport import ResourceReport

#### this will deal with resource changes with new camp creation or deletion

class ResourceCampCreateDelete():
    def __init__(self):
        
        self.resource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        self.resource_allocaation_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        self.resource__nallocated_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceUnallocatedStock.csv")
        self.totalResources_df = pd.read_csv(self.resource_stock_csv_path)
        self.resourceAllocs_df = pd.read_csv(self.resource_allocaation_csv_path)
        self.unallocResources_df = pd.read_csv(self.resource__nallocated_stock_csv_path)
        self.joined_df = pd.merge(self.totalResources_df, self.resourceAllocs_df, on='resourceID', how='inner')

    def remove_camp_resources(self, valid_range_list):
        ### we need to get the campid from somewhere, for now lets just set it ourselves,

        ### this should be able to be called on multiple camps at once, just run it several times :) 
        report_instance = ResourceReport()
        resource_camp = report_instance.resource_report_camp()
        resource_camp.reset_index(inplace=True)
        sum_df = pd.DataFrame()
        sum_df['resourceID'] = resource_camp['resourceID']
        sum_df['sum'] = resource_camp[valid_range_list].sum(axis=1)
        ##### and now we need to add them all together!!

        # need to recalculate all 3 sheets 

        # first calculate...
        # unallocated stock - add the above to each resource. do mapping to be on safe side 
        inventory = self.unallocResources_df ## will always have more or equal 
        joined_df = pd.merge(inventory, sum_df, on='resourceID', how='outer').fillna(0) #join and then add... 
        joined_df['unallocTotal'] = joined_df['sum'] + joined_df['unallocTotal']
        new_unalloc = joined_df.drop('sum', axis=1)
        new_unalloc.to_csv(self.resource__nallocated_stock_csv_path, index=False)
        # for allocations & totals = remove it from the map first, and then recalculate the sum 
        map = self.resourceAllocs_df
        remove = remove = map['campID'].isin(valid_range_list)
        new_map = map[~remove]
        new_map.to_csv(self.resource_allocaation_csv_path, index=False)
        # recalc the sum
        new_assigned = report_instance.resourceStock_generator(new_map)
        new_assigned.to_csv(self.resource_stock_csv_path, index=False)

        return new_unalloc

 
    def closed_camp_resources_interface(self):
        ### do the same but opposite basically of new_camp!
        report_instance = ResourceReport()
        closed_camps_df = report_instance.valid_closed_camps()
        valid_range_list = closed_camps_df['campID'].to_list()
        # print(after_pretty.to_string(index=False).replace('.0', '  '))
        if not closed_camps_df.empty:
            closed_camp_resource_stats = report_instance.report_closed_camp_with_resources()
            pretty_closed_stats = report_instance.PRETTY_PIVOT_CAMP(closed_camp_resource_stats)
            print(f"""\033[91m\n
✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖ !!!  SOS   ｡•́︿•̀｡  SOS !!! ✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖  \n
CHECK 2:\n
The below CLOSED camps still have resources allocated... \n
==============================================================\033[0m\n
{pretty_closed_stats.to_string(index=False).replace('.0', '  ')} \n
    Unassign / unallocate resources from all closed camps, and move to inventory? [ y ]\n
            """)

            user_select = report_instance.input_validator('--> ', ['y'], "\033[91mSorry, you don't have a choice here... \nIt is not good to leave resources assigned to closed camps...Please enter y\033[0m")
            if user_select == 'RETURN':
                return
            if user_select == 'y':
                self.remove_camp_resources(valid_range_list)
                print(f"\033[92m===== ＼(^o^)／ All resources from campIDs {valid_range_list} successfully unallocated & moved to inventory ＼(^o^)／ =====\033[0m")
                print(f"\nAFTER:\n")
                report_instance_AFTER = ResourceReport()
                closed_camp_resource_AFTER = report_instance_AFTER.report_closed_camp_with_resources()
                print(closed_camp_resource_AFTER)
        else:
            print("\n\033[92m＼(^o^)／ GOOD NEWS ＼(^o^)／ CHECK 2: There are no closed camps with assigned resources \033[0m")


    def new_camp_resources(self):
        #### we will have a new_camps_list .. 
        report_instance = ResourceReport()
        new_camps_df = report_instance.valid_new_camps()
        resource_range = report_instance.valid_resources()

        ### assume we get a df input like the below 
        """     +-------------+------------+
                | new camp id | refugeepop |
                +-------------+------------+
                | 100         | 5          |
                | 101         | 6          |
                +-------------+------------+
        """

        ### mechanism to calculate starting amounts >> discuss w team how this is done! >> families etc? 
        new_alloc_df = pd.DataFrame(columns=['resourceID','campID','qty'])

        # Iterate over the base DataFrame
        for index, row in new_camps_df.iterrows():
            # Create a temporary DataFrame for each camp
            temp_df = pd.DataFrame({
                'resourceID': resource_range,
                'campID': row['campID'],
                'qty': row['refugeePop'] * 10
            }) ## this will have values... all non zero

            new_alloc_df = new_alloc_df.dropna(axis=1, how='all')
            temp_df = temp_df.dropna(axis=1, how='all')
            new_alloc_df = pd.concat([new_alloc_df, temp_df], ignore_index=True)
        
        map = self.resourceAllocs_df
        map = map[map['qty'] != 0]


        new_map = pd.concat([map, new_alloc_df], ignore_index=True)
        new_map.to_csv(self.resource_allocaation_csv_path, index=False)
        # use this to create the updated stock / assigned resources table
        new_assigned = report_instance.resourceStock_generator(new_map)
        new_assigned.to_csv(self.resource_stock_csv_path, index=False)

        ## now need to overwrite the both of them into csv files

        print("\nSuccess!")
        
        return new_map, new_assigned
    

    def new_camp_resources_interface(self):
        #### this only needs ot run, if new_camps_df is not empty 
        report_instance = ResourceReport()
        new_camps_df = report_instance.valid_new_camps()
        if not new_camps_df.empty:
            print(f"""\033[91m
    ✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖ !!!  SOS   ｡•́︿•̀｡  SOS !!! ✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖✖  \n
    CHECK 1:\n
    There are newly open camp(s) with refugees...\n
    but NO RESOURCES OF ANY TYPE! \n
    ==============================================================\033[0m\n
    {new_camps_df.to_string(index=False)} \n
    The starter resource pack for new camps is 10 of each resource per refugee.\n
    Proceed to buy & assign this for all camps above? [ y / n ]\n

    Note: if 'n', you will still have the option of assigning resources to these newly opened & resourceless but populated camps,
    via other channels: \n
        >> these camps will be automatically be included in [4.1] Resource Allocation -> [4.1.2] Auto-Distribute
        >> manually assign existing resources from inventory & other camps via [4.1] Resource Allocation -> [4.1.1] Manual
            """)  ######### this should be slightly different for volunteer

            user_select = report_instance.input_validator('--> ', ['y', 'n'])
            if user_select == 'RETURN':
                return
            before_camp_vs_unallocated = report_instance.master_resource_stats()

            #### can add something more interactive here
            

            if user_select == 'y':
                self.new_camp_resources()
                print("\nAll new camps have now been assigned a starter resource pack.\n ")
                print("\nBEFORE:")
                before_pretty = report_instance.PRETTY_PIVOT_CAMP(before_camp_vs_unallocated)
                print(before_pretty.to_string(index=False).replace('.0', '  '))
                print("\nAFTER:\n")
                report_instance_AFTER = ResourceReport()
                after_camp_vs_unallocated = report_instance_AFTER.master_resource_stats()
                after_pretty = report_instance_AFTER.PRETTY_PIVOT_CAMP(after_camp_vs_unallocated)
                print(after_pretty.to_string(index=False).replace('.0', '  '))
                print("\n ======= ＼(^o^)／ Thanks for Shopping! Come Again Soon! ＼(^o^)／ ===== \n")
        else:
            print("\n\033[92m＼(^o^)／ GOOD NEWS ＼(^o^)／ CHECK 1: There are open camps with refugees, that have no resources\033[0m")