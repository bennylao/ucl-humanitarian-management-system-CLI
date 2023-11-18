import pandas as pd
from pathlib import Path
from humanitarian_management_system.helper import extract_data


def pass_data():
    # Access user enter values from helper function and assign them to Volunteer class

    # keep track of uid and increment it by 1
    I = extract_data('data/user.csv', 'userID')
    return I

print(pass_data())
