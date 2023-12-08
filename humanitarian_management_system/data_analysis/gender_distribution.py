import plotly.graph_objects as go
from pathlib import Path
import pandas as pd


def gender_pie_chart(camp_id):
    refugee_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
    rd = pd.read_csv(refugee_csv_path)
    male = rd[(rd['campID'] == camp_id) & (rd['gender'] == 'male')].shape[0]
    female = rd[(rd['campID'] == camp_id) & (rd['gender'] == 'female')].shape[0]
    other = rd[(rd['campID'] == camp_id) & (rd['gender'] == 'other')].shape[0]
    values = [male, female, other]
    labels = ['male', 'female', 'other']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text = f"Gender Distribution for Refugees in Camp {camp_id}")
    fig.show()


if __name__ == '__main__':
    gender_pie_chart(2)
