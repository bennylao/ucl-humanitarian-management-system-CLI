from humanitarian_management_system.models.resourceAllocator import ResourceAllocator
from humanitarian_management_system.models.resourceReport import ResourceReport
from humanitarian_management_system.models.resourceCampCreateDelete import ResourceCampCreateDelete
import pandas as pd
import pathlib as Path


csv_path = Path(__file__).parents[0].joinpath("data/event.csv")
df = pd.read_csv(csv_path)

print(df)