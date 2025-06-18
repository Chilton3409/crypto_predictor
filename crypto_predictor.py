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
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
from sklearn.metrics import precision_recall_curve
import time
import joblib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

client = AsyncCryptoV1.CryptoLinkClient(api_key, api_secret)
target = Decimal(10.00)


async def test_retrieve_candles(ticker):
    try:
        candles = await client.get_candles(ticker=ticker)
        return candles
    except Exception as e:
        logging.exception(msg=e)


    
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
            
            #scale the data using minmax scaler
            scaler = MinMaxScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            n_estimators = trial.suggest_int('n_estimators', 90, 200)
            max_depth = trial.suggest_int('max_depth', 5, 15)
            # Create and train a random forest classifier
            clf = RandomForestClassifier(n_estimators=n_estimators,max_depth=max_depth, random_state=42)
            clf.fit(X_train_scaled, y_train)
            
            # Make predictions on the test set
            predictions = clf.predict(X_test_scaled)
            print(predictions)
            # Evaluate the model
            accuracy = clf.score(X_test_scaled, y_test)
            print(f"current prediction: {predictions}. Current accuraccy: {accuracy}")
            precision = precision_score(y_test, predictions)
            print(f"current precision is at: {precision}")
            
            recall = recall_score(y_test, predictions)
            print(f"current recall score is at: {recall}")
            
            f1 = f1_score(y_test, predictions)
            print(f"current f1 score is: {f1}")
            
            # Calculate probabilities for AUC-ROC
            probabilities = clf.predict_proba(X_test_scaled)[:, 1]
            print(f"current probabilitie: {probabilities}")
            
            auc_roc = roc_auc_score(y_test, probabilities)
            print(f"current auc_roc is: {auc_roc}")
            
            return accuracy
    except Exception as e:
        logging.exception(msg=e)
        
def generate_buy_signals(model, tickers):
    
    try:
        for ticker in tickers:
            print(f"processing ticker: {ticker}")
            candle_data = asyncio.run(test_retrieve_candles(ticker=ticker))
            if candle_data.candles:
                features = [candle_data.candles[0].open, candle_data.candles[0].high, candle_data.candles[0].low]
                prediction = model.predict_proba([features])
                print(f"Prediction for {ticker}: {prediction}")
                if prediction.shape[1] > 1:  # Check if there are multiple classes
                    prediction = prediction[0][1]
                else:
                    prediction = prediction[0][0]  # If not, use the single class probability

                
                if prediction > 0.8:  # Threshold for buy signal
                
                    print(f"Buy signal generated for {ticker} with prediction value: {prediction}")
                    #create buy order here
                    asyncio.run(client.create_buy_order(ticker=ticker))
                else:
                    print(f"current prediction is to low at {prediction}")
                    
                
                
    except Exception as e:
        logging.exception(msg=e)

    
def main():
    
    try:
        
        
        study = optuna.create_study(study_name="crypto predictor",direction='maximize')
        study.optimize(objective, n_trials=50)
        if study.best_trial:
            best_params = study.best_params
            best_accuracy = study.best_value
            print(f"Best parameters: {best_params}")
            print(f"Best accuracy: {best_accuracy:.2f}")
        
            #train a new model with the optimized parameters
            gainers = asyncio.run(client.get_top_gainers())
            data = []
            labels = []
            for gainer in gainers:
                candle_data = asyncio.run(test_retrieve_candles(ticker=gainer))
                if candle_data.candles:
                    data.append([candle_data.candles[0].open, candle_data.candles[0].high, candle_data.candles[0].low])
                    # Label: 1 if price went up, 0 if price went down or stayed the same
                    labels.append(1 if candle_data.candles[0].close > candle_data.candles[0].open else 0)
            if data and len(data) > 1:
                    
                X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
                scaler = MinMaxScaler()
                X_trained_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                best_model = RandomForestClassifier(n_estimators=best_params['n_estimators'], max_depth=best_params['max_depth'], random_state=42)
                best_model.fit(X_trained_scaled, y_train)
                joblib.dump((best_model, scaler), 'crypto_predictor.joblib')

        """
         
            
            while True:
                
                tickers = asyncio.run(client.get_top_gainers())
                
                #generate buy signals
                
                buy_signals = generate_buy_signals(best_model, tickers)
            
            
                #begin sell logic
                spots = asyncio.run(client.get_spot_positions())
                for ticker in tickers:
                
                    asyncio.run(client.sell_logic(spots, ticker=ticker))
                """
    except Exception as e:
        logging.exception(msg=e)
if __name__=='__main__':
    main()
    
    
    
    