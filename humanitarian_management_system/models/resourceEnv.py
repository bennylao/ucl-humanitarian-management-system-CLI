from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceReport import ResourceReport
from humanitarian_management_system.models.resourceAdder import ResourceAdder
from humanitarian_management_system.models.resourceCampCreateDelete import ResourceCampCreateDelete
import pandas as pd
import pathlib as Path


r_inst = ResourceCampCreateDelete()
#print(r_inst.joined_df)

print(r_inst.totalResources_df['resourceID'].dtype)
print(r_inst.resourceAllocs_df['resourceID'].dtype) ### as an object, but shouldnt be! 
