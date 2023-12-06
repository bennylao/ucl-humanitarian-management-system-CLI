# from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import webbrowser
import random
import plotly.graph_objs as go
from pathlib import Path
from threading import Thread

class Dashboard:
    def __init__(self):
        self.app = Dash(__name__)
        self.setup_layout()

    def setup_layout(self):

        camp_csv_path = Path(__file__).parents[0].joinpath("data/campTest.csv")
        refugee_csv_path = Path(__file__).parents[0].joinpath("data/refugee.csv")
        camp_loc = pd.read_csv(camp_csv_path)
        refugee_data = pd.read_csv(refugee_csv_path)

        # Create a scatter map showing locations of camps
        fig = px.scatter_mapbox(
            camp_loc,
            lat="lat",
            lon="long",
            hover_name=camp_loc["campID"].apply(lambda x: f"Camp {x}"),
            hover_data=["eventID", "countryID",  "status"],
            color_discrete_sequence=["fuchsia"],
            zoom=11,
            height=600,
            width=700
        )
        fig.update_layout(mapbox_style="carto-positron")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_traces(marker={"size": 10, "symbol": "circle", "color": "green"})
        # fig.update_layout(mapbox_bounds={"west": -0.510375, "east": 0.273515, "south": 51.106760, "north": 51.654290})
        fig.update_layout(mapbox_bounds={"west": -10, "east": 2, "south": 49, "north": 60})

        # pie_chart = dcc.Graph(id='pie-chart')

        self.app.layout = html.Div([
            html.Div([
                html.H1("Camp Locations on Map"),
                dcc.Graph(id='scatter-map', figure=fig)],
                style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                html.H1("Location Data"),
                dcc.Dropdown(
                    options=[
                        {'label': 'Gender Pie Chart', 'value': 'pie'},
                        {'label': 'Pop Bar Chart', 'value': 'bar'}],
                    value='pie',
                    id='chart_type'
                ),
                dcc.Graph(id='pie-chart', config={'displayModeBar': False})],
                style={'width': '50%', 'display': 'inline-block'}),
        ])

        # Callback to update the pie chart when hovering over a location
        @self.app.callback(
            Output('pie-chart', 'figure'),
            Input('scatter-map', 'hoverData'),
            Input('chart_type', 'value')
        )
        def update_pie_chart(hoverData, chart_type):
            if not hoverData or not hoverData['points']:
                # If no hover data, show a default pie chart
                rd = refugee_data[refugee_data['campID'] == 2]
                labels = ['Male', 'Female', 'Other']
                value1 = rd[rd["gender"] == "female"].shape[0]
                value2 = rd[rd["gender"] == "male"].shape[0]
                value3 = rd[rd["gender"] == "other"].shape[0]
                values = [value2, value1, value3]
                # gender_pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values)])
                # gender_pie_chart.update_layout(title='Gender Pie Chart for ')

                chart_fig = {
                    'data': [go.Pie(labels=labels, values=values)],
                    'layout': {'title': f'Pie Chart for camp 2'}
                }

                return chart_fig

            camp_id = hoverData['points'][0]['hovertext']
            camp_name = f"camp: {camp_id}"

            gender_labels = ['Male', 'Female', 'Other']
            rd = refugee_data[refugee_data['campID'] == int(camp_id.split(' ')[1])]
            value1 = rd[rd["gender"] == "female"].shape[0]
            value2 = rd[rd["gender"] == "male"].shape[0]
            value3 = rd[rd["gender"] == "other"].shape[0]

            gender_values = [value2, value1, value3]

            labels = ['Category A', 'Category B', 'Category C']
            values = [random.randint(1, 10) for _ in range(3)]

            if chart_type == 'pie':
                chart_fig = {
                    'data': [go.Pie(labels=gender_labels, values=gender_values)],
                    'layout': {'title': f'Pie Chart for {camp_id}'}
                }
            else:
                chart_fig = {
                    'data': [go.Bar(x=labels, y=values)],
                    'layout': {'title': f'Bar Chart for {camp_name}'}
                }

            return chart_fig

    def run(self):
        thread = Thread(target=self.app.run_server, kwargs={'debug': False, 'use_reloader': False})
        thread.start()
        webbrowser.open("http://127.0.0.1:8050/")


if __name__ == '__main__':
    dashboard = Dashboard()
    dashboard.run()

