from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceReport import ResourceReport
from humanitarian_management_system.models.resourceCampCreateDelete import ResourceCampCreateDelete


instance = ResourceCampCreateDelete()
report_instance = ResourceReport()

alloc_instance = ResourceAllocator()

table = report_instance.master_resource_stats()
pretty_table = report_instance.PRETTY_PIVOT_CAMP(table)

print(pretty_table.to_string(index=False).replace('.0', '  '))
