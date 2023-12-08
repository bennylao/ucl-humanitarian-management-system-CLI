import plotly.graph_objects as go
from pathlib import Path
import pandas as pd
from plotly.subplots import make_subplots


def medical_info(camp_id):
    type_csv_path = Path(__file__).parents[1].joinpath("data/medicalInfoType.csv")
    info_csv_path = Path(__file__).parents[1].joinpath("data/medicalInfo.csv")
    refugee_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
    info = pd.read_csv(info_csv_path)
    info_type = pd.read_csv(type_csv_path)
    refugee = pd.read_csv(refugee_csv_path)

    dff = pd.merge(info, refugee, on='refugeeID', how='inner')

    dff = dff[dff['campID'] == camp_id]

    dff2 = pd.merge(dff, info_type, on='medicalInfoTypeID', how='inner')

    labels = dff2['condition'].tolist()
    # for i in labels:
    values = [dff2[dff2['condition'] == i].shape[0] for i in labels]

    label1 = ['vaccinated', 'unvaccinated']
    value1 = dff2[dff2['isVaccinated'] == True].shape[0]
    value2 = dff2[dff2['isVaccinated'] == False].shape[0]
    value3 = [value1, value2]

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(go.Pie(labels=label1, values=value3, hole=0.3), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=values, hole=0.3), 1, 2)

    fig.update_layout(title_text=f'Medical Info of refugees in camp {camp_id}')

    fig.update_layout(
        annotations=[
            dict(text='Vaccination Status', x=0.17, y=0.5, font_size=14, showarrow=False),
            dict(text='Medical Conditions', x=0.83, y=0.5, font_size=14, showarrow=False)
        ]
    )

    fig.show()


if __name__ == '__main__':
    medical_info(3)
