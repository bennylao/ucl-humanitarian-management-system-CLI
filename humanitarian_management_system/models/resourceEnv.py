from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceAdder import ResourceAdder

from pathlib import Path
import pandas as pd


camp_df = pd.read_csv("humanitarian_management_system/data/camp.csv")

print(camp_df)

