import numpy as np
from sklearn.linear_model import LogisticRegression


def prepare_data(df, time_column):
    df['diff'] = df['value_main'].diff()
    df['diff'] = df['diff'].fillna(0)

    df['MA_5'] = df['value_main'].rolling(window=5).mean()
    df['MA_10'] = df['value_main'].rolling(window=10).mean()
    df['MA_30'] = df['value_main'].rolling(window=30).mean()

    delta = df['value_main'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))
    df['RSI'] = RSI

    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month

    df['lag_1'] = df['value_main'].shift(1)
    df['lag_3'] = df['value_main'].shift(3)
    df['lag_7'] = df['value_main'].shift(7)

    df = df.fillna(0)

    df = df.drop(columns=[time_column])
    res = np.array(df)
    return res


def run_lr(df, value_column, time_column, main_df):
    y_train = main_df['value_binary'].values

    X = prepare_data(df, time_column)
    X_train = X[0:1001]
    X_forecast = X[1001:]

    model = LogisticRegression(max_iter=5000)
    model.fit(X_train, y_train)

    y_pred_temp = list(model.predict(X_train))
    y_pred = list(model.predict(X_forecast))

    y_pred_temp.extend(y_pred)
    df[value_column] = y_pred_temp

    return df
