import pandas as pd
from pathlib import Path
from .resourceReport import ResourceReport

######## adding to the net amount
######## should be admin only 

class ResourceAdder():
    def __init__(self):
        
        resource_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
        resource_allocaation_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
        self.resource__nallocated_stock_csv_path = Path(__file__).parents[1].joinpath("data/resourceUnallocatedStock.csv")
        self.totalResources_df = pd.read_csv(resource_stock_csv_path)
        self.resourceAllocs_df = pd.read_csv(resource_allocaation_csv_path)
        self.unallocResources_df = pd.read_csv(self.resource__nallocated_stock_csv_path)
        self.joined_df = pd.merge(self.totalResources_df, self.resourceAllocs_df, on='resourceID', how='inner')

    def resource_adder(self):
        report_instance = ResourceReport()
        grandTotal = report_instance.resource_report_total()
        ## admin only but deal with later
        ## adds to the total amount of resources available

        # welcome to the resource store! please enter how many of each object you would like to add
        # totalResources = extract_data_df("data/resourceStock.csv")
        # unallocResources = extract_data_df("data/resourceUnallocatedStock.csv")
        ################ might need to change this to unallocated...
        totalResources = self.totalResources_df
        unallocResources = self.unallocResources_df

        ### menu bit
        print(f"""==========================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ Hi Admin! Welcome to the Resource Shop ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
==========================================================================\n
        Any purchased items will be in your unallocated inventory, pending your assignment to camps\n
        Below is your current stock levels:\n
{grandTotal.to_string(index = False)} \n"""
        ) 
        basket = pd.DataFrame(columns=['resourceID','buyUnits'])
        basket_id_list = []
        basket_units_list = []
        ### can give user an option to leave the shop rn. come back to this 
        while True:
            # add error handling in the last stage / later ... 
            # r_id_select = int(input("\nPlease enter the resourceID of the item you would like to purchase: --> "))
            prompt = "\nPlease enter the resourceID of the item you would like to purchase: --> "    
            valid_range = report_instance.valid_resources()
            r_id_select = report_instance.input_validator(prompt, valid_range)  
            r_name_select = totalResources.loc[totalResources['resourceID'] == r_id_select, 'name'].iloc[0]

            prompt = f"Please enter the number of units of *** Resource ID {r_id_select}: {r_name_select} *** which you would like to buy: --> "
            r_id_units = report_instance.input_validator(prompt, list(range(10000)), 'Invalid selection. Please enter an integer quantity between 0 to 9999.')  

            basket_id_list.append(r_id_select)
            basket_units_list.append(r_id_units)

            # Ask if the user is done
            done = input("\n Are you done shopping? y / n -->  ").strip()
            if done == 'y':
                break
            #### need to

        # insert the two lists into the basket dataframe
        basket['resourceID'] = basket_id_list
        basket['buyUnits'] = basket_units_list
        # could add in edit basket option but come back to this 
        print(f"""==========================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ Below is your shopping basket: ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
==========================================================================\n
{basket.to_string(index = False)} \n"""
        )
        confirm_shop = input("Proceed to checkout? \n [y] Yes; \n [x] Abandon cart \n --> ")
        if confirm_shop == 'y':
            ## logic to loop thru this and add to the unallocated dataframe
            ## actually esier to do join
            result_df = pd.merge(unallocResources, basket, on='resourceID', how='left').fillna(0)
            result_df['unallocTotal'] = result_df['unallocTotal'].astype(int) + result_df['buyUnits'].astype(int)
            result_df.drop('buyUnits', axis=1, inplace=True)
            result_df.to_csv(self.resource__nallocated_stock_csv_path, index=False)

            print("Checkout successful! Below is your updated stock levels:\n")
            report_instance_AFTER = ResourceReport()
            grandTotal_AFTER = report_instance_AFTER.resource_report_total()
            print(grandTotal_AFTER.to_string(index = False))
            print("\n ======= ＼(^o^)／ Thanks for Shopping! Come Again Soon! ＼(^o^)／ ===== \n")
        ######## maybe redirect the menus
        return result_df
 ## what after this? new unallocated resources

 ## 