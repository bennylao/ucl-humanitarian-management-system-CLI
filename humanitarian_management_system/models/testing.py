import pandas as pd
from pathlib import Path

from numpy.core.defchararray import capitalize

from humanitarian_management_system.helper import extract_data


def pass_data():

    s = extract_data("data/eventTesting.csv", "eid").iloc[2]
    return s

print(pass_data())






















