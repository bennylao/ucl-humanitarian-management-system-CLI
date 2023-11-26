from resourceTesting import ResourceTest
from resourceReport import ResourceReport

from humanitarian_management_system.helper import (extract_data, modify_csv_value, modify_csv_pandas, extract_data_df)
from pathlib import Path
import pandas as pd

test_instance = ResourceTest(campID=1, pop=100, total_pop=1000)

# print(test_instance.calculate_resource_jess())

""" alloc_ideal = test_instance.calculate_resource_jess()
alloc_ideal = test_instance.determine_above_below(threshold = 0.10)
redistribute_sum_checker = test_instance.redistribute()

print(alloc_ideal.groupby('resourceID')['current'].sum())
print(redistribute_sum_checker)

print("hi all good")


resource_report = ResourceReport()
print(resource_report.resource_report_camp()) """

test_instance.resource_adder()

df1 = extract_data_df("data/resourceStock.csv")
df2 = extract_data_df("data/resourceUnallocatedStock.csv")

result_df = pd.merge(df1, df2[['resourceID', 'total']], on='resourceID', how='left')
print(result_df)
