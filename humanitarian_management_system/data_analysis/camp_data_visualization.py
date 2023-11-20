from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import webbrowser
import random
import plotly.graph_objs as go
from pathlib import Path

user_csv_path = Path(__file__).parents[1].joinpath("data/location_data.csv")
camp_loc = pd.read_csv(user_csv_path)

app = Dash(__name__)
# Create a scatter map showing locations of camps
fig = px.scatter_mapbox(
    camp_loc,
    lat="latitude",
    lon="longitude",
    hover_name="name",
    hover_data=["city", "population"],
    color_discrete_sequence=["fuchsia"],
    zoom=11,
    height=600,
    width=700
)
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_traces(marker={"size": 10, "symbol": "circle", "color": "green"})
fig.update_layout(mapbox_bounds={"west": -0.510375, "east": 0.273515, "south": 51.106760, "north": 51.654290})

# Create a pie chart
pie_chart = dcc.Graph(id='pie-chart')

app.layout = html.Div([
    html.Div([
        html.H1("Camp Locations on Map"),
        dcc.Graph(id='scatter-map', figure=fig)],
        style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        html.H1("Location Data"),
        dcc.Dropdown(
            options=[
                {'label': 'Pie Chart', 'value': 'pie'},
                {'label': 'Bar Chart', 'value': 'bar'}],
            value='pie',
            id='chart_type'
        ),

        dcc.Graph(id='pie-chart', config={'displayModeBar': False})],

        style={'width': '50%', 'display': 'inline-block'}),
])


# Callback to update the pie chart when hovering over a location
@app.callback(
    Output('pie-chart', 'figure'),
    Input('scatter-map', 'hoverData'),
    Input('chart_type', 'value')
)
def update_pie_chart(hoverData,chart_type):
    #if hoverData is None:
        #eturn {}
    if not hoverData or not hoverData['points']:
        # If no hover data, show a default pie chart
        labels_default = ['Default Category 1', 'Default Category 2', 'Default Category 3']
        values_default = [random.randint(1, 10) for _ in range(3)]

        default_pie_chart = go.Figure(data=[go.Pie(labels=labels_default, values=values_default)])
        default_pie_chart.update_layout(title='Default Pie Chart')

        return default_pie_chart
    # Extract the city name from hoverData
    city_name = hoverData['points'][0]['hovertext']

    labels = ['Category A', 'Category B', 'Category C']
    values = [random.randint(1, 10) for _ in range(3)]

    if chart_type == 'pie':
        chart_fig = {
            'data': [go.Pie(labels=labels, values=values)],
            'layout': {'title': f'Pie Chart for {city_name}'}
        }
    else:
        chart_fig = {
            'data': [go.Bar(x=labels, y=values)],
            'layout': {'title': f'Bar Chart for {city_name}'}
        }

    return chart_fig


if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:8050/")
    app.run_server(debug=True, use_reloader=False)
