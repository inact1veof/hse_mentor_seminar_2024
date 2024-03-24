from prophet import Prophet


def run_prophet(df, value_column, time_column):

    df = df.rename(columns={value_column: 'y', time_column: 'ds'})

    model = Prophet(growth='linear',
                    seasonality_mode='additive',
                    n_changepoints=2
                    )
    model.add_country_holidays(country_name='US')
    model.fit(df)

    future = model.make_future_dataframe(periods=65, freq='B')
    forecast = model.predict(future)
    forecast = forecast.rename(columns={'ds': time_column, 'yhat': value_column})

    return forecast

