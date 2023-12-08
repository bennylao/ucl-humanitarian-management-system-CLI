import plotly.graph_objects as go
from pathlib import Path
import pandas as pd
from plotly.subplots import make_subplots


def medical_info():
    type_csv_path = Path(__file__).parents[0].joinpath("data/medicalInfoType.csv")
    info_csv_path = Path(__file__).parents[0].joinpath("data/medicalInfo.csv")
    info = pd.read_csv(info_csv_path)
    info_type = pd.read_csv(type_csv_path)
    labels = info_type['condition'].tolist()
    values = []
    for k in range(1, 15):
        value = info[info['medicalInfoTypeID'] == k].shape[0]
        values.append(value)

    label1 = ['vaccinated', 'unvaccinated']
    value1 = info[info['isVaccinated'] == True].shape[0]
    value2 = info[info['isVaccinated'] == False].shape[0]
    value3 = [value1, value2]

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(go.Pie(labels=label1, values=value3, hole=0.3), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=values, hole=0.3), 1, 2)

    fig.update_layout(title_text='Medical Info')

    fig.update_layout(
        annotations=[
            dict(text='Vaccination Status', x=0.17, y=0.5, font_size=14, showarrow=False),
            dict(text='Medical Conditions', x=0.83, y=0.5, font_size=14, showarrow=False)
        ]
    )

    fig.show()


if __name__ == '__main__':
    medical_info()
