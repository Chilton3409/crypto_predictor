
#!/usr/bin/env python3

import asyncio
import AsyncCryptoV1
from dotenv import load_dotenv
import os
from decimal import Decimal
import logging
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv  
load_dotenv()

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
client = AsyncCryptoV1.CryptoLinkClient(api_key, api_secret)

target = Decimal(10.00)

# Lists to store features and labels
features_list = []
labels_list = []

async def collect_data(tickers):
    for ticker in tickers:
        candles = await client.test_retrieve_candles(ticker)
        if candles.candles:
            # Features
            features = np.array([candles.candles[0].open, candles.candles[0].high, candles.candles[0].low])
            features_list.append(features)

            # Label (e.g., 1 if price increased, 0 otherwise)
            if candles.candles[0].close > candles.candles[0].open:
                labels_list.append(1)
            else:
                labels_list.append(0)

async def calculate_optimal_threshold(features_array, labels_array):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features_array, labels_array, test_size=0.2, random_state=42)

    # Fit the scaler to the training data
    client.scaler.fit(X_train)
    X_test_scaled = client.scaler.transform(X_test)

    # Calculate optimal threshold
    probabilities = client.model.predict_proba(X_test_scaled)[:, 1]
    precision, recall, thresholds = precision_recall_curve(y_test, probabilities)
    optimal_threshold = thresholds[np.argmax(precision + recall)]
    return optimal_threshold

async def test_generate_buy_signals(tickers, optimal_threshold):
    for ticker in tickers:
        candles = await client.test_retrieve_candles(ticker)
        if candles.candles:
            features = np.array([[candles.candles[0].open, candles.candles[0].high, candles.candles[0].low]])
            features_scaled = client.scaler.transform(features)
            prediction = client.model.predict_proba(features_scaled)
            print(f"Prediction for {ticker}: {prediction}")
            if prediction.shape[1] > 1:  # Check if there are multiple classes
                prediction = prediction[0][1]
            else:
                prediction = prediction[0][0]  # If not, use the single class probability
            if prediction > optimal_threshold:  # Use the optimal threshold
                print(f"Buy signal generated for {ticker} with prediction value: {prediction}")
                # create buy order here
                # await client.create_buy_order
            else:
                print(f"Current prediction is too low at {prediction}")

async def main():
    tickers = await client.get_top_gainers() # List of tickers to check
    await collect_data(tickers)

    features_array = np.array(features_list)
    labels_array = np.array(labels_list)
    optimal_threshold = await calculate_optimal_threshold(features_array, labels_array)
    print(f"Optimal threshold: {optimal_threshold}")

    await test_generate_buy_signals(tickers, optimal_threshold)

asyncio.run(main())

