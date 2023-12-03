from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceAdder import ResourceAdder
from humanitarian_management_system.models.resourceReport import ResourceReport

from pathlib import Path
import pandas as pd


# camp_df = pd.read_csv("humanitarian_management_system/data/camp.csv")

# print(camp_df)



resource_stats_instance = ResourceReport()
all_resource_camp_vs_unallocated = resource_stats_instance.resource_report_camp_vs_unallocated()




filtered_df = all_resource_camp_vs_unallocated[all_resource_camp_vs_unallocated['resourceID'] == 1]
df = filtered_df.iloc[:, 4:]

print(df[5].iloc[0])
