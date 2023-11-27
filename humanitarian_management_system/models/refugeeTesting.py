import re
import csv
from pathlib import Path
import pandas as pd
from humanitarian_management_system import helper

def move_refugee_helper_method():
    """Moves refugee from one camp to another"""
    # displaying list of all refugees to user
    refugee_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
    ref_df = pd.read_csv(refugee_csv_path)
    print(ref_df)
    # checking input is vaild according to refugee IDs in database
    while True:
        rid = input("\nFrom the list above enter the refugee ID for the refugee you wish to move another camp: ")
        if rid == "RETURN":
            return
        elif ref_df['refugeeID'].eq(int(rid)).any():
            break
        else:
            print("\nSorry - that refugee ID doesn't exist. Pick again.")
    # old_camp_id = ref_df[ref_df['refugeeID'] == int(rid), 'campID'].index[0]
    old_camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
    print(old_camp_id)
    # print(old_camp_id)
    # old_camp_id = ref_df.loc[ref_df['refugeeID'] == rid, 'campID'].iloc[0]
    # camp_id_value = df.loc[df['refugeeID'] == refugee_id_value, 'campID'].values[0]
    # Displaying list of all ACTIVE camps to user
    camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
    camp_df = pd.read_csv(camp_csv_path)
    active_camp_df = camp_df[camp_df['status'] == 'open']
    print("\n", active_camp_df)
    # checking input is vaild according to refugee IDs in database
    while True:
        camp_id = input("\nGreat! Now, from the above list, enter the campID of "
                        "the camp you want to move this refugee to: ")
        if camp_id == "RETURN":
            return
        elif active_camp_df['campID'].eq(int(camp_id)).any():
            break
        else:
            print("\nSorry - that camp ID doesn't exist (anymore). Pick again.")
    # Minus one from the population of the camp originally associated with the refugee
    # print(camp_id)
    row_index_old_camp = camp_df[camp_df['campID'] == old_camp_id].index
    # print(row_index_camp)
    # print(row_index_old_camp)
    # refugee_pop = row_index_camp['refugeePop'].iloc[0]
    # row_index_camp = camp_df[ref_df['campID'] == old_camp_id].index[0]
    camp_df.at[row_index_old_camp[0], 'refugeePop'] -= 1
    # Update the campID for the refugee in refugee CSV
    row_index_ref = ref_df[ref_df['refugeeID'] == int(rid)].index[0]
    # print(row_index_ref)
    # ref_df.to_csv(refugee_csv_path, mode='a', index=False, header=False)
    helper.modify_csv_value(refugee_csv_path, row_index_ref, "campID", camp_id)
    # Add one to the population of the camp which the refugee is now in
    row_index_new_camp = camp_df[camp_df['campID'] == int(camp_id)].index
    # print("row_index_new_camp:", row_index_new_camp)
    # print(row_index_new_camp)
    camp_df.at[row_index_new_camp[0], 'refugeePop'] += 1
    # camp_df.to_csv(camp_csv_path, mode='a', index=False, header=False)
    # modify_csv_value(camp_df, row, "refugeePop", camp_id)
    print(f"Transfer complete. We have reassigned the refugee from camp {old_camp_id} to camp {camp_id}."
          f"Additionally, the population of both camps has been adjusted accordingly.")
    return

move_refugee_helper_method()