from resourceTesting import ResourceTest
from resourceReport import ResourceReport
from resourceAllocator import ResourceAllocator

from humanitarian_management_system.helper import (extract_data, modify_csv_value, modify_csv_pandas, extract_data_df)
from pathlib import Path
import pandas as pd

test_instance = ResourceTest(campID=1, pop=100, total_pop=1000)


allocator_instance = ResourceAllocator()

#print(allocator_instance.add_unalloc_resource())
alloc_ideal, redistribute_sum_checker, comparison_result = allocator_instance.redistribute()

print(redistribute_sum_checker)
print(comparison_result)


test_instance.resource_adder()
