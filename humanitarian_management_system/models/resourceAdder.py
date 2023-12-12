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
        r_inst = ResourceReport()
        grandTotal = r_inst.resource_report_total()
        grandTotal['assignedTotal'] = grandTotal['assignedTotal'].astype(int)
        grandTotal['grandTotal'] = grandTotal['grandTotal'].astype(int)
        ## admin only but deal with later
        ## adds to the total amount of resources available

        # welcome to the resource store! please enter how many of each object you would like to add
        # totalResources = extract_data_df("data/resourceStock.csv")
        # unallocResources = extract_data_df("data/resourceUnallocatedStock.csv")
        ################ might need to change this to unallocated...
        totalResources = self.totalResources_df
        unallocResources = self.unallocResources_df

        ### menu bit
        print(f"""=============================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ [ 4.2 ] Hi Admin! Welcome to the Resource Shop ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
=============================================================================\n
        Any purchased items will be in your unallocated inventory, pending your assignment to camps\n
        Below is your current stock levels:\n
{grandTotal.to_string(index = False)} \n"""
        ) 
        basket = pd.DataFrame(columns=['resourceID', 'name', 'buyUnits'])
        basket_id_list = []
        basket_units_list = []

        already_selected = []

        ### can give user an option to leave the shop rn. come back to this 
        while True:
            # add error handling in the last stage / later ... 
            # r_id_select = int(input("\nPlease enter the resourceID of the item you would like to purchase: --> "))
            '''
            prompt = "\nPlease enter the resourceID of the item you would like to purchase: \n--> "    
            valid_range = r_inst.valid_resources()
            r_id_select = r_inst.input_validator(prompt, valid_range)  
            if r_id_select == 'RETURN':
                return
            '''
            
            print("\nPlease enter the resourceID:")
            if already_selected: # if not empty 
                print(f"Note you have already made selection(s) for Resource IDs: {set(already_selected)} ")   
            r_id_select = r_inst.input_validator_2range_resources("--> ", already_selected, basket, 'shop')
            if r_id_select == 'RETURN':
                return
            
            r_name_select = totalResources.loc[totalResources['resourceID'] == r_id_select, 'name'].iloc[0]
            already_selected.append(r_id_select)

            prompt = f"Please enter how many units of \033[93mResource ID {r_id_select}: {r_name_select}\033[0m which you would like to buy: \n--> "
            r_id_units = r_inst.input_validator(prompt, list(range(10000)), 
                                                '\033[91mInvalid selection. Please enter an integer quantity between 0 to 9999. \n(If you need more than 9999 please checkout & enter the excess in a second basket)\033[0m')  
            if r_id_units == 'RETURN':
                return

            # basket_id_list.append(r_id_select)
            # basket_units_list.append(r_id_units)

            new_row = pd.DataFrame({'resourceID': [r_id_select], 
                                    'name': [r_name_select],
                                    'buyUnits':[r_id_units]})
            basket = pd.concat([basket, new_row], ignore_index=True)

            # Ask if the user is done
            done = r_inst.input_validator("\nAre you done shopping? y / n \n--> ", ['y', 'n'])
            if done == 'y':
                break # exit the loop
            elif done == 'RETURN':
                return # exit the function
            else:
                pass
            #### need to

        # insert the two lists into the basket dataframe
        # basket['resourceID'] = basket_id_list
        # basket['buyUnits'] = basket_units_list
        # could add in edit basket option but come back to this 
        print(f"""==========================================================================\n
✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮ Below is your shopping basket: ✩°｡⋆⸜ ✮✩°｡⋆⸜ ✮\n
==========================================================================\n
{basket.to_string(index = False)} \n"""
        )
        # confirm_shop = input("Proceed to checkout? \n [y] Yes; \n [x] Abandon cart \n --> ")
        confirm_shop = r_inst.input_validator("Proceed to checkout? \n [y] Yes; \n [x] Abandon cart \n--> ", ['y', 'x'])
        if confirm_shop == 'RETURN':
            return
        if confirm_shop == 'x':
            print("\nAbandoning cart & leaving shop... bye bye!\n")
        if confirm_shop == 'y':
            ## logic to loop thru this and add to the unallocated dataframe
            ## actually esier to do join
            # Dropping the 'name' column from basket, don't need it anymore after print! 
            basket = basket.drop('name', axis=1)
            result_df = pd.merge(unallocResources, basket, on='resourceID', how='left').fillna(0)
            result_df['unallocTotal'] = result_df['unallocTotal'].astype(int) + result_df['buyUnits'].astype(int)
            result_df.drop('buyUnits', axis=1, inplace=True)
            result_df.to_csv(self.resource__nallocated_stock_csv_path, index=False)

            print("Checkout successful! Below is your updated stock levels:\n")
            r_inst_AFTER = ResourceReport()
            grandTotal_AFTER = r_inst_AFTER.resource_report_total()
            print(grandTotal_AFTER.to_string(index = False))
            print("\n ======= ＼(^o^)／ Thanks for Shopping! Come Again Soon! ＼(^o^)／ ===== \n")
        ######## maybe redirect the menus
            return result_df
 ## what after this? new unallocated resources

 ## 