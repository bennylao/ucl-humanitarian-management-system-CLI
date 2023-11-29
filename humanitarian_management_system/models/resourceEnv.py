from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceAdder import ResourceAdder
from humanitarian_management_system.models.resourceReport import ResourceReport

from pathlib import Path
import pandas as pd


# camp_df = pd.read_csv("humanitarian_management_system/data/camp.csv")

# print(camp_df)

test_instance = ResourceAllocator()
test_instance.manual_alloc()

report_instance = ResourceReport()
print(report_instance.resource_report_camp_vs_unallocated())