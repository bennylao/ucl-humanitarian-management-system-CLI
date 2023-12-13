import pandas as pd
from pathlib import Path
from passlib.hash import sha256_crypt


class User:
    def __init__(self, user_id, username, password, first_name, last_name, email, phone, occupation):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.occupation = occupation

    def update_username(self):
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path, converters={'username': str, 'password': str})
        df.loc[df['userID'] == self.user_id, 'username'] = self.username
        df.to_csv(user_csv_path, index=False)

    def update_password(self):
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path, converters={'username': str, 'password': str})
        df.loc[df['userID'] == self.user_id, 'password'] = self.password
        df.to_csv(user_csv_path, index=False)

    def update_name(self):
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path, converters={'username': str, 'password': str})
        df.loc[df['userID'] == self.user_id, 'firstName'] = self.first_name
        df.loc[df['userID'] == self.user_id, 'lastName'] = self.last_name
        df.to_csv(user_csv_path, index=False)

    def update_email(self):
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path, converters={'username': str, 'password': str})
        df.loc[df['userID'] == self.user_id, 'email'] = self.email
        df.to_csv(user_csv_path, index=False)

    def update_phone(self):
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path, converters={'username': str, 'password': str})
        df.loc[df['userID'] == self.user_id, 'phone'] = self.phone
        df.to_csv(user_csv_path, index=False)

    def update_occupation(self):
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path, converters={'username': str, 'password': str})
        df.loc[df['userID'] == self.user_id, 'occupation'] = self.occupation
        df.to_csv(user_csv_path, index=False)

    @staticmethod
    def get_all_usernames():
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path, converters={'username': str, 'password': str})
        return df["username"].tolist()

    @staticmethod
    def get_all_emails():
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path)
        return df["email"].tolist()

    @staticmethod
    def validate_user(username, password):
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path, converters={'username': str, 'password': str})
        # row will be empty series if no record is found
        row = df.loc[df['username'] == username]
        # if record is found and password is correct
        if not row.empty and sha256_crypt.verify(password, row.iloc[0]['password']):
            # return user information as pandas series
            return row.squeeze()
        else:
            return pd.Series()
