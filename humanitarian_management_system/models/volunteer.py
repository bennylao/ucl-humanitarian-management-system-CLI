import pandas as pd
from pathlib import Path
from .user import User


class Volunteer(User):

    def __init__(self, user_id, username, password, first_name, last_name, email, phone, occupation,
                 role_id, camp_id):
        super().__init__(user_id, username, password, first_name, last_name, email, phone, occupation)
        self.role_id = role_id
        self.camp_id = camp_id

    def show_account_info(self):
        role_type_csv_path = Path(__file__).parents[1].joinpath("data/roleType.csv")
        df_role = pd.read_csv(role_type_csv_path)
        current_role = df_role.loc[df_role['roleID'] == self.role_id, 'name'].iloc[0]
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path, converters={'roleID': str})
        df.loc[df['userID'] == int(self.user_id), 'roleID'] = current_role
        df = df.rename(columns={"roleID": "Role"}, errors="raise")
        sub_df = df.loc[df['userID'] == int(self.user_id), ['username', 'firstName', 'lastName', 'email',
                                                            'phone', 'occupation', 'Role', 'campID']]

        table_str = sub_df.to_markdown(index=False)
        print("\n" + table_str)
        input("\nPress Enter to return...")

    def update_role(self):
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path, converters={'username': str, 'password': str})
        df.loc[df['userID'] == self.user_id, 'roleID'] = self.role_id
        df.to_csv(user_csv_path, index=False)

    @staticmethod
    def create_new_record(registration_info):
        csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        user_id = pd.read_csv(csv_path)['userID'].max() + 1
        # insert user id into registration_info
        registration_info.insert(0, user_id)
        user_df = pd.DataFrame(data=[registration_info])
        # Pass assign values into .csv file
        user_df.to_csv(csv_path, mode='a', index=False, header=False)
