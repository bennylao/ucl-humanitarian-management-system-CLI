import numpy as np
from pathlib import Path
import pandas as pd
import plotly.express as px


def num_camp():
    camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
    camp_loc = pd.read_csv(camp_csv_path)

    eventList = set(camp_loc['eventID'].tolist())

    closed_camps = [camp_loc[(camp_loc['eventID'] == i) & (camp_loc['status'] == 'closed')].shape[0] for i in eventList]
    open_camp = [camp_loc[(camp_loc['eventID'] == i) & (camp_loc['status'] == 'open')].shape[0] for i in eventList]

    data = {"Event ID": list(eventList),
            "open": open_camp,
            "closed": closed_camps}

    df = pd.DataFrame(data)
    fig = px.bar(df, x="Event ID", y=["closed", "open"], title="Camps in each event")
    fig.update_xaxes(tickvals=df["Event ID"])
    fig.update_layout(xaxis_title='Event ID', yaxis_title='Number of Camps')
    fig.show()


if __name__ == '__main__':
    num_camp()

