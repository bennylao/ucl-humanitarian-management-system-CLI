import pandas as pd
from pathlib import Path


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def change_username(self):
        pass

    def change_password(self):
        pass

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
        df = pd.read_csv(user_csv_path, dtype="string")
        # row will be empty series if no record is found
        row = df.loc[df['username'] == username]
        # if record is found and password is correct
        if not row.empty and str(row.iat[0, 3]) == password:
            # return user information as pandas series
            return row.squeeze()
        else:
            return pd.Series()
