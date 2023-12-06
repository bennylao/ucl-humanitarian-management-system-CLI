from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceAdder import ResourceAdder
from humanitarian_management_system.models.resourceReport import ResourceReport
from humanitarian_management_system.models.resourceCampCreateDelete import ResourceCampCreateDelete

from pathlib import Path
import pandas as pd

instance = ResourceCampCreateDelete()
report_instance = ResourceReport()

valid_range_df = report_instance.valid_closed_camps()
valid_range_list = valid_range_df['campID'].to_list()
df = instance.closed_camp_resources_interface()

print(df)