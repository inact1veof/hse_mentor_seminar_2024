import pandas as pd
import json

from DataLoader import DBLoader
from models.Prophet import run_prophet
from models.LR import run_lr
from metrics import calculate_mae
from metrics import calculate_f1

loader = DBLoader()

file_path = 'data.csv'  # cleared and filled input data

df = pd.read_csv(file_path)

df = df.rename(columns={'дата': 'date', 'выход': 'value_main', 'направление': 'value_binary'})

df['value_main'] = df['value_main'].str.replace(',', '.').astype(float)
df['value_binary'] = df['value_binary'].str.replace('л', '1')
df['value_binary'] = df['value_binary'].str.replace('ш', '0')
df['value_binary'] = df['value_binary'].astype(int)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

df_2 = pd.read_excel('Данные.xlsx', sheet_name='Прогноз')  # forecast dates
df_2 = df_2.rename(columns={'дата': 'date'})
dates = df_2['date']

forecast_float = run_prophet(df, 'value_main', 'date')
forecast_all = run_lr(forecast_float, 'value_binary', 'date', df)

# 1002-1065 = all indexes of period
df = forecast_all.loc[1002:1065, ['date', 'value_main', 'value_binary']]
df = df[df['date'].isin(dates)]

with open('forecast_value.json', 'w') as file:
    json.dump(df['value_main'].to_list(), file)

with open('forecast_class.json', 'w') as file:
    json.dump(df['value_binary'].to_list(), file)
