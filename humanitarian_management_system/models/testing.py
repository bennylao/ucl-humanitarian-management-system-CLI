import pandas as pd
from pathlib import Path

from numpy.core.defchararray import capitalize

from humanitarian_management_system.helper import extract_data


def pass_data():

    user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
    df = pd.read_csv(user_csv_path)
    i = df.index[df['username'] == 'volunteer2'].tolist()
    t = df.iloc[i]['userType'].tolist()

    return t[0]

print(pass_data())






















