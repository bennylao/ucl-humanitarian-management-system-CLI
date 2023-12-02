from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceAdder import ResourceAdder
from humanitarian_management_system.models.resourceReport import ResourceReport

from pathlib import Path
import pandas as pd


# camp_df = pd.read_csv("humanitarian_management_system/data/camp.csv")

# print(camp_df)

report_instance = ResourceReport()
valid_range = ['y','n']  # or any list of integers, strings, or a mix of both
prompt_message = "Enter a number between 1 and 9, or a specific string: "
report_instance.input_validator(prompt_message, valid_range)