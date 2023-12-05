from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceAdder import ResourceAdder
from humanitarian_management_system.models.resourceReport import ResourceReport

from pathlib import Path
import pandas as pd

# report_instance = ResourceReport()
# report_instance.determine_above_below()


test_instance = ResourceAllocator()
test_instance.add_unalloc_resource()
test_instance.auto_alloc()