import numpy as np
from pathlib import Path
import pandas as pd
from datetime import datetime
import plotly.express as px


def age_bar_chart(camp_id):
    refugee_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
    rd = pd.read_csv(refugee_csv_path)
    rd = rd[rd['campID'] == camp_id]

    ageList = rd['dob'].tolist()
    age10 = age20 = age30 = age40 = age50 = age60 = age70 = age80 = 0

    if ageList:
        for k in ageList:
            day, moth, year = k.split('/')
            current_year = datetime.now().year
            age = current_year - int(year)
            if age < 10:
                age10 += 1
            elif (age >= 10) and (age < 20):
                age20 += 1
            elif (age >= 20) and (age < 30):
                age30 += 1
            elif (age >= 30) and (age < 40):
                age40 += 1
            elif (age >= 40) and (age < 50):
                age50 += 1
            elif (age >= 50) and (age < 60):
                age60 += 1
            elif (age >= 60) and (age < 70):
                age70 += 1
            else:
                age80 += 1

    values = [age10, age20, age30, age40, age50, age60, age70, age80]
    labels = ['<10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '>70']

    fig = px.bar(x=labels, y=values, title=f'Age Distribution of refugees in camp {camp_id}', labels={'x': 'Age', 'y': 'Population'})

    fig.show()


if __name__ == '__main__':
    age_bar_chart(48)




