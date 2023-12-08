import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import pandas as pd


def resources(camp_id):
    resourceA_csv_path = Path(__file__).parents[1].joinpath("data/resourceAllocation.csv")
    resourceS_csv_path = Path(__file__).parents[1].joinpath("data/resourceStock.csv")
    rs = pd.read_csv(resourceS_csv_path)
    ra = pd.read_csv(resourceA_csv_path)
    labels = rs['name'].tolist()
    values = ra[ra['campID'] == camp_id]['qty'].tolist()

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title=f'Resources in Camp {camp_id}')
    fig.show()


if __name__ == '__main__':
    resources(2)

