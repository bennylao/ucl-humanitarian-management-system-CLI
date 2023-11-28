from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceAdder import ResourceAdder
from humanitarian_management_system.models.resourceReport import ResourceReport

from pathlib import Path
import pandas as pd


# camp_df = pd.read_csv("humanitarian_management_system/data/camp.csv")

# print(camp_df)

report_instance = ResourceReport()

all_resource_camp_df = report_instance.resource_report_camp().reset_index()

single_resource_camp_df = all_resource_camp_df[all_resource_camp_df['name'] == 'Food']

print(single_resource_camp_df.to_string(index=False))