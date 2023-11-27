from resourceTesting import ResourceTest
from resourceReport import ResourceReport
from resourceAllocator import ResourceAllocator

from pathlib import Path
import pandas as pd

test_instance = ResourceTest(campID=1, pop=100, total_pop=1000)


test_instance.resource_adder()
