"""
LSTM Time Series Forecasting for Global Financial Indices

This script fetches historical price data for major global stock indices using yfinance,
then trains and applies an LSTM neural network to predict future monthly closing prices.

Main functionalities:
- Download historical data for indices like S&P 500, NASDAQ, Dow Jones, FTSE 100, Nikkei, and others.
- Prepare the data by resampling to monthly frequency and scaling values.
- Create lagged datasets for supervised learning suitable for LSTM input.
- Define and train an LSTM model to forecast future closing prices.
- Predict future prices for a specified horizon (default 120 months).
- Plot actual historical and predicted future prices, saving plots as PNG files.

Key functions:
- get_finance_data: Returns a dictionary of yfinance Ticker objects and their names.
- create_dataset: Prepares input/output arrays with lagged observations.
- build_lstm_model: Defines and compiles the LSTM model architecture.
- run_lstm_time_series_prediction: Runs the full training, prediction, and plotting pipeline for each index.
- main: Fetches data for all indices, runs predictions sequentially, handling errors and throttling requests.

Dependencies:
- yfinance, numpy, pandas, matplotlib, scikit-learn, tensorflow (keras)

Usage:
Run the script to automatically download data, train models, generate forecasts,
and save the plots to the 'Predict Finance' directory.
"""



import yfinance as yf
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


def get_finance_data():
    """
    Returns a dictionary of Ticker objects for major global indices.
    """
    tickers = {
        "sp500": "^GSPC",
        "nasdaq": "^IXIC",
        "dow_jones": "^DJI",
        "vix": "^VIX",
        "russell_2000": "^RUT",
        "ftse_100": "^FTSE",
        "nikkei_225": "^N225",
        "hang_seng": "^HSI",
        "dax": "^GDAXI",
        "cac_40": "^FCHI",
        "bovespa": "^BVSP",
        "asx_200": "^AXJO",
        "sensex": "^BSESN",
        "kospi": "^KS11",
        "msci_world": "URTH",
        "emerging_markets": "EEM",
        "tsx": "^GSPTSE",
        "smi": "^SSMI",
        "euro_stoxx_50": "^STOXX50E"
    }
    return {name: yf.Ticker(ticker) for name, ticker in tickers.items()}, list(tickers.keys())


def create_dataset(data, n_lags):
    """
    Creates a dataset for LSTM model training.

    :param data: Scaled data array
    :param n_lags: Number of lagged observations
    :return: Tuple of features and target arrays
    """
    X, y = [], []
    for i in range(n_lags, len(data)):
        X.append(data[i - n_lags:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)


def build_lstm_model(input_shape):
    """
    Builds and compiles the LSTM model.

    :param input_shape: Shape of the input data
    :return: Compiled LSTM model
    """
    model = Sequential([
        LSTM(units=50, return_sequences=False, input_shape=input_shape),
        Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def run_lstm_time_series_prediction(df, finance_name, n_months_to_predict=120, n_lags=12):
    """
    Predicts time series of closing prices using an LSTM model.
    Saves the plot as an image in the 'Predict Finance' directory.

    :param df: DataFrame with 'Close' column
    :param finance_name: Name of the index
    :param n_months_to_predict: Number of months to predict
    :param n_lags: Number of lagged observations for training
    """
    os.makedirs("Predict Finance", exist_ok=True)

    # Prepare the data
    df['Date'] = pd.to_datetime(df.index)
    df.set_index('Date', inplace=True)
    df_monthly = df['Close'].resample('M').last().dropna()

    # Scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df_monthly.values.reshape(-1, 1))

    # Create dataset
    X, y = create_dataset(scaled_data, n_lags)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    # Split the data into training and testing sets
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Build and train the model
    model = build_lstm_model((X_train.shape[1], 1))
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

    # Make predictions
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)

    # Future predictions
    input_seq = scaled_data[-n_lags:].reshape(1, n_lags, 1)
    future_predictions = []

    for _ in range(n_months_to_predict):
        next_val = model.predict(input_seq)[0, 0]
        future_predictions.append(next_val)
        input_seq = np.append(input_seq[:, 1:, :], [[[next_val]]], axis=1)

    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

    # Plotting future_dates = pd.date_range(df_monthly.index[-1], periods=n_months_to_predict + 1, freq='M')[1:]
    future_dates = pd.date_range(df_monthly.index[-1], periods=n_months_to_predict + 1, freq='M')[1:]

    plt.figure(figsize=(12, 6))
    plt.plot(df_monthly.index, df_monthly.values, label="Actual")
    plt.plot(future_dates, future_predictions, label="Predicted Future", linestyle='dashed')
    plt.title(f"LSTM Forecast: {finance_name} - Next {n_months_to_predict} Months")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.savefig(f"Predict Finance/{finance_name}_prediction.png")
    plt.close()


def main():
    indices, tickers = get_finance_data()
    for name in tickers:
        try:
            print(f"🔍 Fetching data for {name}...")
            df = indices[name].history(period="max")
            if not df.empty and 'Close' in df.columns:
                print(f"✅ Fetching successful for {name}. Running LSTM prediction...")
                run_lstm_time_series_prediction(df, name)
            else:
                print(f"❌ Error in {name}: No 'Close' column found.")

            # הוספת השהייה של 3 שניות לפני הבקשה הבאה
            time.sleep(3)

        except Exception as e:
            print(f"❌ Error with {name}: {e}")
            time.sleep(10)  # אם קרתה שגיאה, יש להמתין 10 שניות לפני הבקשה הבאה


if __name__ == "__main__":
    main()
