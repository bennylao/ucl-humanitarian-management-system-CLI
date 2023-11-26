from pathlib import Path
import pandas as pd
from .user import User


class Admin(User):
    def __init__(self, user_id, username, password, first_name, last_name, email, phone, occupation):
        super().__init__(user_id, username, password, first_name, last_name, email, phone, occupation)

    def show_account_info(self):
        user_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
        df = pd.read_csv(user_csv_path)
        sub_df = df.loc[df['userID'] == int(self.user_id), ['username', 'firstName', 'lastName', 'email',
                                                            'phone', 'occupation']]
        table_str = sub_df.to_markdown(index=False)
        print("\n" + table_str)

    def edit_volunteer_account(self, volunteer_name):
        pass

    def allocate_resource(self):
        # should this just call from resources class?
        pass

    def deactivate_user(self):
        pass

    def create_humanitarian_plan(self):
        pass

    def end_event(self):
        pass

    def edit_plan(self):
        pass

    def display_humanitarian_plan(self):
        pass
