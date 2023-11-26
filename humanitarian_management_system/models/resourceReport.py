import pandas as pd
from humanitarian_management_system.helper import (extract_data, modify_csv_value, modify_csv_pandas, extract_data_df,
                                                   extract_active_event)
from pathlib import Path


# A very basic attempt at resource allocation to camp, it's basically just a manipulation of database/csv files by
# looping through them when necessary
class ResourceReport():
    def __init__(self):
        self.resourceLibrary_df = extract_data_df("data/resourceStock.csv")
        self.resourceAllocs_df = extract_data_df("data/resourceAllocation.csv")
        self.joined_df = pd.merge(self.resourceLibrary_df, self.resourceAllocs_df, on='resourceID', how='inner')

    def resource_report_total(self):
        resourceSum_df = self.joined_df.groupby('resourceID').agg({
            'name': 'first',  # Keeps the first name for each group
            'priorityLvl': 'first',  # Keeps the first priorityLvl for each group
            'qty': 'sum'  # Sums the allocatedQuantity for each group
        }).reset_index()
        return resourceSum_df

    def resource_report_camp(self):
        pivot_df = self.joined_df.pivot_table(index=['name', 'priorityLvl'], columns='campID', values='qty', aggfunc='sum')
        return pivot_df