# crypto_predictor
This project is a cryptocurrency trading bot that uses machine learning to predict price movements and generate buy signals. 

It consists of two main scripts:


Model Training Script: Trains a machine learning model using historical data to predict price movements.
Trading Bot Script: Uses the trained model to generate buy signals and execute trades.



Features

Machine Learning-based Prediction: Uses a RandomForestClassifier model to predict price movements based on historical data.
Automated Trading: Generates buy signals and executes trades based on predictions.
Risk Management: Includes features for taking profits and stopping losses.



Requirements

Python 3.x: This project is built using Python 3.x.
Required Libraries: scikit-learn, numpy, pandas, and other dependencies listed in requirements.txt.
Coinbase API: Requires an API key and secret to interact with the cryptocurrency market.



Usage

Clone the repository and install the required dependencies.
Run the Model Training Script to train the machine learning model.
Set your API key and secret as environment variables.
Run the Trading Bot Script to start the automated trading bot.



Notes

This project is for educational purposes only and should not be used for actual trading without proper testing and validation.
The bot's performance may vary depending on market conditions and the quality of the API data.

