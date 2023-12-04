import re
import csv
from pathlib import Path
import pandas as pd
from humanitarian_management_system import helper
import tkinter as tk
import tkinter.messagebox

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
    camp_df.to_csv(camp_csv_path, index=False)
    # camp_df.to_csv(camp_csv_path, mode='a', index=False, header=False)
    # modify_csv_value(camp_df, row, "refugeePop", camp_id)
    print(f"Transfer complete. We have reassigned the refugee from camp {old_camp_id} to camp {camp_id}."
          f"Additionally, the population of both camps has been adjusted accordingly.")
    return

# move_refugee_helper_method()


# def delete_refugee():
#     print("YOU ARE REQUESTING TO DELETE A REFUGEE. Enter RETURN if you didn't mean to select this. Otherwise, proceed"
#           "as instructed.")
#     refugee_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
#     ref_df = pd.read_csv(refugee_csv_path)
#     print(ref_df)
#     # checking input is vaild according to refugee IDs in database
#     while True:
#         rid = input("\nFrom the list above enter the refugee ID for the refugee you wish to remove from the system: ")
#         if rid == "RETURN":
#             return
#         elif rid.strip() and rid.strip().isdigit() and ref_df['refugeeID'].eq(int(rid)).any():
#             break
#         else:
#             print("\nSorry - that refugee ID doesn't exist. Pick again.")
#     print("Below is the information about this refugee.")
#     specific_refugee_row = ref_df[ref_df['refugeeID'] == int(rid)]
#     print(specific_refugee_row)
#     #     POP UP WINDOW TO CONFIRM USER WANTS TO DELETE REFUGEE (say it's irreversible?)
#     # Removing 1 from the population of the associated camp
#     camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
#     camp_df = pd.read_csv(camp_csv_path)
#     camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
#     row_index_camp = camp_df[camp_df['campID'] == camp_id].index
#     camp_df.at[row_index_camp[0], 'refugeePop'] -= 1
#     #     Deleting the refugee from the database
#     ref_df = ref_df.drop(ref_df[ref_df['refugeeID'] == rid].index)
#     print(f"Okay. You have permanently deleted refugee #{rid} from the system. Their old associated camp pop has "
#           f"also been adjusted accordingly.")

def delete_refugee():
    print("YOU ARE REQUESTING TO DELETE A REFUGEE. Enter RETURN if you didn't mean to select this. Otherwise, proceed"
          "as instructed.")
    refugee_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
    ref_df = pd.read_csv(refugee_csv_path)
    print(ref_df)
    # checking if input is valid according to refugee IDs in database
    while True:
        rid = input("\nFrom the list above enter the refugee ID for the refugee you wish to remove from the system: ")
        if rid == "RETURN":
            return
        elif rid.strip() and rid.strip().isdigit() and ref_df['refugeeID'].eq(int(rid)).any():
            break
        else:
            print("\nSorry - that refugee ID doesn't exist. Pick again.")
    print("Below is the information about this refugee.")
    specific_refugee_row = ref_df[ref_df['refugeeID'] == int(rid)]
    print(specific_refugee_row)
    #     POP UP WINDOW TO CONFIRM USER WANTS TO DELETE REFUGEE (say it's irreversible?)

    root = tk.Tk()
    result = tk.messagebox.askquestion("Reminder", "Are you sure you want to delete this refugee?")
    if result == "yes":
        # Removing 1 from the population of the associated camp
        camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        camp_df = pd.read_csv(camp_csv_path)
        camp_id = ref_df.loc[ref_df['refugeeID'] == int(rid), 'campID'].iloc[0]
        row_index_camp = camp_df[camp_df['campID'] == camp_id].index
        camp_df.at[row_index_camp[0], 'refugeePop'] -= 1
        #     Deleting the refugee from the database
        ref_df.drop(ref_df[ref_df['refugeeID'] == int(rid)].index, inplace=True)
        ref_df.to_csv(refugee_csv_path, index=False)
        print(
            f"Okay. You have permanently deleted refugee #{rid} from the system. Their old associated camp population "
            f"has also been adjusted accordingly.")
        print("\nRefugee DataFrame after deletion:")
        print(ref_df)
    else:
        tk.messagebox.showinfo("Cancel", "The operation to delete the refugee was canceled.")
    root.mainloop()


# delete_refugee()

                prompt_msg1 = f"\n Please enter the amount of *** [ Resource ID #{r_id_select}: {r_name_select} ] *** to move: "
                prompt_msg2 = f"\nPlease enter the ORIGIN campID where you would like to REMOVE *** Resource ID {r_id_select}: {r_name_select} *** from: "
                valid_range1 = resource_stats_instance.valid_open_camps_with_refugees()
                valid_range1 = valid_range1['campID'].tolist()
                valid_range2 = resource_stats_instance.valid_resources()
                valid_range12 = resource_stats_instance.valid_pairwise_camp_resources()

                resource_stats_instance.pairwise_input_validator(prompt_msg1, prompt_msg2, valid_range1, valid_range2, valid_range12)