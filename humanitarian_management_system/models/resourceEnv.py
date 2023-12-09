from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceReport import ResourceReport
from humanitarian_management_system.models.resourceCampCreateDelete import ResourceCampCreateDelete
import pandas as pd


instance = ResourceCampCreateDelete()
report_instance = ResourceReport()

alloc_instance = ResourceAllocator()

alloc_instance.auto_alloc_debug()


updateTotals = report_instance.resourceStock_generator(report_instance.resourceAllocs_df)
print(updateTotals)
# updateTotals.to_csv(report_instance.resource_stock_csv_path, index=False)

'''
data = [
    [9, "Water", 52, None, 99, "[2] UNASSIGN: camp -> inventory"],
    [10, "Baby Supplies", 55, 57.0, 93, "[3] RE-ASSIGN: camp <-> camp"]
]

# Define the column names.
columns = ["resourceID", "name", "origin_campID", "destination_campID", "moveUnits", "actionInfo"]

# Create the DataFrame. 
df = pd.DataFrame(data, columns=columns)
print(df.transpose().to_string(header = False))
'''

list1 = report_instance.valid_all_camps_with_refugees()
list2 = report_instance.valid_open_camps_with_refugees()

print(list1)
print(list2)