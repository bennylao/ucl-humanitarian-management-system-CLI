import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import random
from pathlib import Path


class DataVisual:

    def __init__(self):
        camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
        camp_loc = pd.read_csv(camp_csv_path)
        self.camp_loc = camp_loc

    def map(self):

        fig = px.scatter_mapbox(
            self.camp_loc,
            lat="latitude",
            lon="longitude",
            hover_name=self.camp_loc["campID"].apply(lambda x: f"Camp {x}"),
            hover_data=["eventID", "countryID", "refugeePop", "refugeeCapacity", "status"],
            color='status',
            zoom=0,
            height=800,
            width=None
        )

        fig.update_layout(mapbox_style="carto-positron")
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        fig.update_traces(marker={"size": 10, "symbol": "circle"})
        # fig.update_layout(mapbox_bounds={"west": -10, "east": 2, "south": 49, "north": 60})
        fig.update_layout(mapbox_bounds={"west": -180, "east": 180, "south": -90, "north": 90})
        fig.update_layout(title='Camp locations on map')
        fig.show()

    def charts(self):
        # Create a default pie chart
        refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
        refugee_data = pd.read_csv(refugee_csv_path)
        rd = refugee_data[refugee_data['campID'] == 3]
        labels = ['Male', 'Female', 'Other']
        value1 = rd[rd["gender"] == "female"].shape[0]
        value2 = rd[rd["gender"] == "male"].shape[0]
        value3 = rd[rd["gender"] == "other"].shape[0]
        values = [value2, value1, value3]
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values)])

        # fig_pie.update_layout(title='Pie Chart for Default Camp')
        # Create a dropdown menu
        camp_dropdown = [dict(label=f"Camp {camp}", method="restyle",
                              args=[{"labels": ['Male', 'Female', 'Other'],
                                     "values": [value2, value1, value3]},
                                    {"title": f'Pie Chart for Camp {camp}'}]) for camp in self.camp_loc["campID"]]

        # Add the dropdown menu to the layout
        fig_pie.update_layout(
            updatemenus=[dict(type="dropdown", x=-0.15, y=1.15, showactive=False,
                              buttons=camp_dropdown)])

        fig_pie.show()


if __name__ == '__main__':
    datavisual = DataVisual()
    # datavisual.charts()
    datavisual.map()

# ref:https://plotly.com/python/scatter-plots-on-maps/
