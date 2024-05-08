import requests
import json
import pandas as pd
import os

path = os.path.dirname(os.path.abspath(__file__))
path_file = os.path.join(path, 'credentials.json')

with open(path_file, 'r') as f:
    headers = json.load(f)
    
def indicator_data(indicator = 71, start_date = '2021-12-14', end_date = '2022-12-14', time_trunc='hour'):

    url_indicator = f'https://api.esios.ree.es/indicators/{indicator}'
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'time_trunc': time_trunc,
    }
    
    res = requests.get(url_indicator, params, headers=headers)
    
    data = res.json()
    
    return data


def dataframe_p48(data):
    
    data_values = data['indicator']['values']
    df = pd.DataFrame(data_values)

    col_name = data['indicator']['short_name']
    df = df.rename({'value': col_name}, axis=1)

    df.datetime = pd.to_datetime(df.datetime, utc=True, format='ISO8601').dt.tz_convert('Europe/Madrid')
    df = df[['datetime', col_name]].drop_duplicates().copy()
    df = df.set_index('datetime')
    
    return df