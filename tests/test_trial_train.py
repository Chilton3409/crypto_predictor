#!/usr/bin/env python3
#New file created
import AsyncCryptoV1
from dotenv import load_dotenv
load_dotenv()
import numpy as np
import optuna
import os
import asyncio
from decimal import Decimal
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

client = AsyncCryptoV1.CryptoLinkClient(api_key, api_secret)
target = Decimal(10.00)


async def test_retrieve_candles(ticker):
    
    candles = await client.get_candles(ticker=ticker)
    return candles

    
def objective(trial):
    try:
        
        
        gainers = asyncio.run(client.get_top_gainers())
        data =[]
        labels = []
        
        for gainer in gainers:
            candle_data = asyncio.run(test_retrieve_candles(ticker=gainer))
            if candle_data.candles:
                
                data.append([candle_data.candles[0].open, candle_data.candles[0].high, candle_data.candles[0].low])
                # Label: 1 if price went up, 0 if price went down or stayed the same
                labels.append(1 if candle_data.candles[0].close > candle_data.candles[0].open else 0)         
        if data:
            
            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
            
            n_estimators = trial.suggest_int('n_estimators', 90, 200)
            max_depth = trial.suggest_int('max_depth', 5, 15)
            # Create and train a random forest classifier
            clf = RandomForestClassifier(n_estimators=100, random_state=42)
            clf.fit(X_train, y_train)
            
            # Make predictions on the test set
            predictions = clf.predict(X_test)
            print(predictions)
            # Evaluate the model
            accuracy = clf.score(X_test, y_test)
            return accuracy
    except Exception as e:
        logging.exception(msg=e)
        

    
def main():
    try:
        
        study = optuna.create_study(study_name="crypto predictor",direction='maximize')
        study.optimize(objective, n_trials=50)
        best_params = study.best_params
        best_accuracy = study.best_value
        print(f"Best parameters: {best_params}")
        print(f"Best accuracy: {best_accuracy:.2f}")
    except Exception as e:
        logging.exception(msg=e)
if __name__=='__main__':
    main()
    
    