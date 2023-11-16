import pandas as pd
from pathlib import Path


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def get_all_usernames():
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path)
        return df["username"].tolist()

    @staticmethod
    def get_all_login_info():
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path)
        return df["username"].tolist()

    @staticmethod
    def validate_user(username, password):
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path)
        row = df.loc[df['username'] == username, 'password']

        if not row.empty and str(row.iloc[0]) == password:
            return True
        else:
            return False
