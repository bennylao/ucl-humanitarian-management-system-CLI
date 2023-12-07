from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceAdder import ResourceAdder
from humanitarian_management_system.models.resourceReport import ResourceReport
from humanitarian_management_system.models.resourceCampCreateDelete import ResourceCampCreateDelete
from humanitarian_management_system.models.camp import Camp

from pathlib import Path
import pandas as pd
import numpy as np

instance = ResourceCampCreateDelete()
report_instance = ResourceReport()

alloc_instance = ResourceAllocator()



table = report_instance.master_resource_stats()
pretty_table = report_instance.PRETTY_PIVOT_CAMP(table)

print(pretty_table.to_string(index=False).replace('.0', '  '))