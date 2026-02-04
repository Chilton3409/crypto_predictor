#!/usr/bin/env python3
#New file created
from multiprocessing import Pool, Manager
import os
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve

from dotenv import load_dotenv

from decimal import Decimal


from coinbase.rest import RESTClient
from decimal import Decimal
import uuid
load_dotenv()
import time
import datetime
import asyncio
import logging
import joblib
from sklearn.preprocessing import MinMaxScaler
import numpy as np
class CryptoLinkClient():
    def __init__(self, api_key, api_secret):

        #first create ref to the client
        self.client = RESTClient(api_key=api_key, api_secret=api_secret)


        self.ticker_list = []
        self.garbage = []
        self.top_performers = []

        self.profit_threshold = Decimal('.02')
       
        self.stop_loss_threshold = Decimal('-.05')
        #self.model, self.scaler = joblib.load('crypto/crypto_predictor.joblib')
        self.model, self.scaler = joblib.load('crypto_predictor.joblib')

        self.features_list = []
        self.labels_list = []
        self.pnl = float()
        self.profitable_positions = []
        self.observed_max_drawdown = Decimal('.08')
        self.peak_balance = Decimal('0.00')
    async def init(self):

        self.client = RESTClient(api_key=self.api_key, api_secret=self.api_secret)



    async def get_coin_info(self):

        """
        this will return all us dollar related pairs
        """
        try:

            products = self.client.get_products(get_tradability_status=True,)
            test = products.products
            test = [product for product in test if product.quote_name =="US Dollar"]
            return test
        except Exception as e:
            logging.error(f"an error occured in the get coin info function: {e}")
            logging.exception(msg=e, stack_info=True)

    async def update_drawdown_metrics(self):
    """
    Tracks the peak-to-trough drop in real-time.
    Formula: (Current - Peak) / Peak
    """
    current_balance = await self.get_trading_balance()
    
    # 1. Update the lifetime peak
    if current_balance > self.peak_balance:
        self.peak_balance = current_balance
        print(f"New All-Time High balance: {self.peak_balance}")

    # 2. Calculate current drawdown if we are below peak
    if self.peak_balance > 0:
        current_drawdown = (current_balance - self.peak_balance) / self.peak_balance
        
        # 3. Update Max Drawdown record
        if current_drawdown < self.max_observed_drawdown:
            self.max_observed_drawdown = current_drawdown
            
        print(f"Current DD: {current_drawdown*100:.2f}% | Max DD: {self.max_observed_drawdown*100:.2f}%")
        
        # Optional: Safety stop if dip exceeds promised 8%
        if current_drawdown <= Decimal('-0.08'):
            logging.critical("CRITICAL: Promised 8% Drawdown threshold hit. Halting trades.")
            # self.stop_all_trading() 

    async def get_top_gainers(self):
        """

        returns a list of the top gainers on the coinbase leaderboard
        sorted first by percent change, if percent change is equal, then then the higher volume gets preference
        Can be changed, filtered, and sorted and stores them in
        the top gainers list as USD-BTC for easy retrieval

        """
        print("collecting data on top 25 gainers")
        try:
            test = await self.get_coin_info()
            sorted_test = sorted(test, key=lambda x: (float(x.price_percentage_change_24h) if x.price_percentage_change_24h else 0,
                                               float(x.volume_percentage_change_24h) if x.volume_percentage_change_24h else 0),
                        reverse=True)

            top_gainers_last_day = sorted_test[:25]  # Get the top 5 gainers
            top_gainers_tickers = [gainer.product_id for gainer in top_gainers_last_day]

            self.ticker_list.extend(top_gainers_tickers)


            return top_gainers_tickers
        except Exception as e:
          logging.error(f"error occurred in the find top 5 gainers: {e}")

    async def create_watchlist(self):
        """
        return the watchlist with favorited tickers
        """
        try:
            pass


        except Exception as e:
            logging.exception(msg=e)

    async def get_price(self, ticker:str) -> str:
        """
        Retrieves the price of a single coin
        args: ticker:str
        returns a string of the current assets price

        """
        try:

            asset = self.client.get_product(ticker)
            price = asset.price
            return price
        except Exception as e:
            logging.error(f"an error occured in the get price function: {e}")
            logging.exception(msg=e, stack_info=True)

    async def get_info(self, ticker: str) -> list:
        """
        returns a list on information about a single coin
        """
        try:

            info = self.client.get_products(product_ids=[ticker])
            #returns info on a single coin
            return info
        except Exception as e:
            logging.error(f"an error occured in the get info function: {e}")
            logging.exception(msg=e, stack_info=True)

    async def get_order_book(self, ticker: str):

        """
        returns order bookk information about a specific ticker
        """
        try:

            #order book for a single ticker
            order_book = self.client.get_product_book(ticker)
            return order_book

        except Exception as e:
            logging.error(f"an error occcured in the get order book function: {e}")
            logging.exception(msg=e, stack_info=True)
            
    async def get_best_bid_price(self, ticker):
        try:
            pass
        
        except Exception as e:
            logging.exception(msg=e)

    async def get_bid_price(self, ticker: str) -> str:
        """
        returns a big price for a specific ticker
        args: ticker: str

        """
        try:

            order_book = await self.get_order_book(ticker)
            
            bid_price = order_book.pricebook.bids[0].price
            return bid_price
        except Exception as e:
            logging.error(f"an error occurre in the get bid price function: {e}")
            logging.exception(msg=e, stack_info=True)

    async def get_ask_price(self, ticker: str) -> str:
        """
        returns an ask price for a single ticker
        args: ticker: str
        """
        try:

            order_book = await self.get_order_book(ticker)
            ask_price = order_book.pricebook.asks[0].price
            return ask_price
        except Exception as e:
            logging.error(f"an error occurred in the get bid price function: {e}")
            logging.exception(msg=e, stack_info=True)


    async def get_candles(self, ticker: str):

        """
        looks as the one min chart and returns candle information for a single ticker

        """

        try:
            #dont forget to set the unix date, time, and granularity for the charts
            start_time = datetime.datetime.now()-datetime.timedelta(seconds=60)
            start_time_unix = int(datetime.datetime.timestamp(start_time))
            end_time = datetime.datetime.now()
            end_time_unix = int(datetime.datetime.timestamp(end_time))
            candles = self.client.get_candles(ticker, start=start_time_unix,end=end_time_unix,granularity="1")
            return candles

        except Exception as e:
            logging.error(f"an error occurred in the get candles function")
            logging.exception(msg=e, stack_info=True)

    async def test_retrieve_candles(self, ticker):

        try:
            candles = await self.get_candles(ticker=ticker)
            return candles
        except Exception as e:
            logging.exception(msg=e)

    async def get_fills(self, ticker: str):
        """
        returns the latest filled order

        """
        try:

            fills = self.client.get_fills(product_ids=ticker)
            if fills.fills:
                latest_order = fills.fills[-1]
                return latest_order
            else:
                return []#no orders yet.

        except Exception as e:
            logging.error(f"an error occured in the get fills function: {e}")
            logging.exception(msg=e, stack_info=True)

    async def get_a_single_order(self, order_id):
        """
        take an order id to retreive a single order.
        idea: use after placing order to ensure that the status is filled before moving on

        """
        try:
            order = self.client.get_order(order_id=order_id)
            if order.order:
                #if there is an order, return it
                print(order.order.status)
                return order.order
        except Exception as e:
            logging.exception(msg=e)

    async def get_order_status(self, order):
        """
        take an order and retrieve thje
        """
    async def get_latest_filled_size(self, ticker:str) -> str:
        """
        returns the size of the latest filled order as a string
        """
        try:
            latest_buy = await self.get_fills(ticker=ticker)
            if latest_buy.side == 'BUY':
                latest_buy_size = latest_buy.size
                return latest_buy_size

        except Exception as e:
            logging.error(f" an error occured in the get latest filled size: {e}")
            logging.exception(msg=e, stack_info=True)

    async def fetch_orders_by_ticker(self, ticker):
        try:
            orders = self.client.list_orders(order_status='OPEN', product_ids=ticker)
            if orders.orders:

                return orders.orders



        except Exception as e:
            logging.exception(msg=e)

    async def fetch_open_orders(self):

        try:
            orders = self.client.list_orders(order_status='OPEN')
            if orders:

                return orders.orders

        except Exception as e:
            logging.exception(msg=e)


    async def get_latest_buy(self, ticker:str) -> str:
        """
        returns the latest buy orders price as a str


        """

        try:

            latest_order = await self.get_fills(ticker=ticker)
            if latest_order:
                if latest_order.side == "BUY":
                    latest_buy_price = latest_order.price
                    return latest_buy_price

        except Exception as e:
            logging.error(f"error in the get latest buy function: {e}")
            logging.exception(msg=e, stack_info=True)

    async def check_account_balance(self):

        """
        returns the current usd account balance as str
        """
        try:
            summary = self.client.get_futures_balance_summary()
            total_usd_balance= summary.balance_summary['total_usd_balance']['value']
            total_usd_balance = Decimal(total_usd_balance)
            total = str(total_usd_balance)
            print(total)
            return total
        except Exception as e:
            logging.error(f"an error occurred in the check account balance function")
            logging.exception(msg=e, stack_info=True)

    async def open_orders_hold_amount(self):
        try:
            balances = self.client.get_futures_balance_summary()
            if balances.balance_summary.total_open_orders_hold_amount:

                return balances.balance_summary.total_open_orders_hold_amount['value']

        except Exception as e:
            logging.exception(msg=e)

    async def create_sell_order(self, ticker: str, trade_amount: str):
        """
        args: takes ticker as an argument to create a sell order
        checks to make sure the order is open or filled
        then appends it the list

        """
        try:


            ask_price = await self.get_ask_price(ticker=ticker)

            #get the trade amount
            print(f"the current trade amount for ticker: {ticker} is {trade_amount}")


            #create a unique order id
            client_id = str(uuid.uuid4())

            #create the order
            self.client.limit_order_gtc_sell(
            client_order_id=client_id, product_id=ticker, base_size=str(trade_amount),limit_price=str(ask_price))

            print("sell order created successfully")
            await asyncio.sleep(1.50)
            return

        except Exception as e:
            logging.error(f"an error occurred in the create order: {e}")
            logging.exception(msg=e, stack_info=True)


    async def create_buy_order(self, ticker: str, trade_amount: str):
        """
        takes a str ticker argument and returns a created order

        """
        try:
            bid_price = await self.get_bid_price(ticker=ticker)

            print(f"current trade amount for ticker: {ticker} is {trade_amount}")

            #create the order
            client_id = str(uuid.uuid4())
            self.client.limit_order_gtc_buy(
            client_order_id=client_id, product_id=ticker,base_size=str(trade_amount),limit_price=(str(bid_price)))


            print(f"the buy order for {ticker} was successful")
            await asyncio.sleep(1.50)


        except Exception as e:
            logging.error(f"an error occured in the create buy order function: {e}")
            logging.exception(msg=e, stack_info=True)

    async def collect_data(self, tickers: list):
        """
        collect candle data for the model to form a predicton before buying

        """
        try:
            for ticker in tickers:
                candles = await self.test_retrieve_candles(ticker)
                if candles.candles:
                    # Features
                    features = np.array([candles.candles[0].open, candles.candles[0].high, candles.candles[0].low])
                    self.features_list.append(features)

                    # Label (e.g., 1 if price increased, 0 otherwise)
                    if candles.candles[0].close > candles.candles[0].open:
                        self.labels_list.append(1)
                    else:
                        self.labels_list.append(0)
        except Exception as e:
            logging.exception(msg=e)
            logging.error(f"and error occured in the collect data function.")

    async def calculate_optimal_threshold(self, features_array, labels_array):
        """
        use sci kit learn to form an optimal threshold to check against the predictions
        buy the machine learning model

        """
        try:
            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(features_array, labels_array, test_size=0.2, random_state=42)

            # Fit the scaler to the training data
            self.scaler.fit(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            # Calculate optimal threshold
            probabilities = self.model.predict_proba(X_test_scaled)[:, 1]
            precision, recall, thresholds = precision_recall_curve(y_test, probabilities)
             # Calculate F1-score for each threshold
            f1_scores = 2 * (precision * recall) / (precision + recall)
            f1_scores = np.nan_to_num(f1_scores)  # Handle potential NaN values

            optimal_threshold = thresholds[np.argmax(f1_scores)]
            if optimal_threshold < 0 or optimal_threshold > 1:
                logging.warning(f"Optimal threshold {optimal_threshold} is outside the expected range [0, 1]")


            return optimal_threshold

        except Exception as e:
            logging.exception(msg=e)
            logging.error(f"an error occured in the calc optimal threshhold function")

    async def generate_buy_signals(self, tickers, optimal_threshold=.80):
        """
        iter through the tickers list and use the optimal threshold
        and the models predictions to generate buy signals
        """
        try:
            for ticker in tickers:

                candles = await self.test_retrieve_candles(ticker)
                if candles.candles:
                    features = np.array([[candles.candles[0].open, candles.candles[0].high, candles.candles[0].low]])
                    features_scaled = self.scaler.transform(features)
                    prediction = self.model.predict_proba(features_scaled)
                    print(f"Prediction for {ticker}: {prediction}")
                    if prediction.shape[1] > 1:  # Check if there are multiple classes
                        prediction = prediction[0][1] # 0 is up. 1 is down
                    else:
                        prediction = prediction[0][0]  # If not, use the single class probability
                    if prediction > optimal_threshold:  # Use the optimal threshold
                        print(f"Buy signal generated for {ticker} with prediction value: {prediction}")
                        # create buy order here
                        trade_amount = await self.trade_amount(ticker=ticker)
                        #here I can add my marker makers strategy
                        #or do I create a seperate analysis cycle for it
                        #or maybe even a seperate bot
                        # await self.market_maker(ticker=ticker)
                        await self.create_buy_order(ticker=ticker, trade_amount=trade_amount)
                    else:
                        print(f"Current prediction is too low at {prediction}")

        except Exception as e:
            logging.exception(msg=e)
            logging.error(f"an error occured in the generate buy signals function")


    async def buy_logic(self):
        """
        list the buy logic steps
        1. get the candles for the ticker
        2. pass the candles to the crypto predictor to generate a buy signal
        3.get the trade amount
        4.create the buy order
        5.check if the order went through
        """
        try:

            tickers = await self.get_top_gainers() # List of tickers to check
            await self.collect_data(tickers)

            features_array = np.array(self.features_list)
            labels_array = np.array(self.labels_list)
            optimal_threshold = await self.calculate_optimal_threshold(features_array, labels_array)
            print(f"Optimal threshold: {optimal_threshold}")

            await self.generate_buy_signals(tickers, optimal_threshold)
            self.features_list.clear()
            self.labels_list.clear()
            return

        except Exception as e:
            logging.exception(msg=e)
            logging.error(f"an error occured in the buy logic function")

    async def order_management_logic(self):
        """
        well I need to check all of the open orders and only return true if there are none

        """
        try:
            pass
        except Exception as e:
            logging.exception(msg=e)

    #todo implement new methods to check unrealized gain instead
    async def sell_logic(self):
        try:

            spots = await self.get_spot_positions()

            for asset in spots:
                check_pnl = await self.test_unrealized_gains(breakdown=spots, ticker=asset)

                #here I can create a list of profitable positions and then call the average ip
                trade_amount = asset['available_to_trade_crypto']

                d = Decimal(str(trade_amount))  # Convert to string first to preserve precision
                places = abs(d.as_tuple().exponent)
                profit_trade_amount = round(Decimal(trade_amount) * Decimal('.50'), ndigits=places)
                await self.take_profits(pnl=check_pnl, profit_threshold=self.profit_threshold, ticker=asset['asset'] +"-USD", trade_amount=profit_trade_amount)
                await self.stop_loss(pnl=check_pnl, stop_loss_threshold=self.stop_loss_threshold, ticker=asset['asset']+"-USD", trade_amount=trade_amount)

        except Exception as e:
            logging.error(f"an error occured in the sell login function: {e}")
            logging.exception(msg=e, stack_info=True)
            
    async def average_up(self, ticker):
        try:
            average_up_amount = await self.get_trading_balance()
            check_amount = Decimal(average_up_amount)
            if check_amount >= Decimal(1.25):


                #create sell order here
                #dont forget to add the -usd
                await self.create_buy_order(ticker=ticker, trade_amount=average_up_amount)
                print(f"averaging up on: {ticker} with this amount: ${average_up_amount}")
        except Exception as e:
            logging.exception(msg=e)

    async def take_profits(self, pnl, profit_threshold, ticker, trade_amount):
        try:
            #also need to check if the latest buy matches the current ticker

            
            if pnl > Decimal('.01'):
                
                print(f"Breakout detected current pnl: {pnl} on {ticker}.")
                
                #lets whammy the profitable positions and Ill handle the stop loss for now
                await self.average_up(ticker=ticker)
          
            if pnl >= self.profit_threshold:
                print(f"large gain detected, taking profits at: {pnl} for {ticker}")
                await self.create_sell_order(ticker=ticker, trade_amount=trade_amount)
            return
        except Exception as e:
            logging.exception(msg=e)

    async def stop_loss(self, pnl, stop_loss_threshold, ticker, trade_amount):
        try:
            #check for open orders before selling to keep unrealized gains accurate


            if pnl <= stop_loss_threshold:
                print("stop loss threshold exceeded, creating sell order")
                print(f"current pnl: {pnl} on {ticker}. Stop loss threshold: {stop_loss_threshold}, trade_amount: {trade_amount}")
                await self.create_sell_order(ticker=ticker, trade_amount=trade_amount)
            #this is where I can add my cut losses flip to gainers
            return
        except Exception as e:
            logging.exception(msg=e)


    
    async def get_portfolio_id(self) -> str:
        """
        return a string of the portfolio id
        """
        try:
            portfolios = self.client.get_portfolios()
            test = portfolios.portfolios[0].uuid
            return test
        except Exception as e:
            logging.exception(msg=e, stack_info=True)

    async def get_portfolio_breakdown(self):
        """
        return a breakdown of the portfolio
        can be used for a variety of different functions
        """
        try:
            id = await self.get_portfolio_id()

            test = self.client.get_portfolio_breakdown(portfolio_uuid=id)
            return test.breakdown
        except Exception as e:
            logging.exception(msg=e, stack_info=True)

    async def get_portfolio_balances(self) -> dict:
        """
        returns a dict of current portfolio balances
        """
        try:
            id = await self.get_portfolio_id()

            test = self.client.get_portfolio_breakdown(portfolio_uuid=id)
            return test.breakdown
        except Exception as e:
            logging.exception(msg=e, stack_info=True)


    async def get_spot_positions(self) -> list:

        """
        returns a list of all currently held spot positions

        """
        try:

            breakdown = await self.get_portfolio_breakdown()
            positions = breakdown.spot_positions
            return positions
        except Exception as e:
            logging.exception(msg=e, stack_info=True)

    async def test_unrealized_gains(self, breakdown, ticker: str) -> str:
        """
    takes breakdown of spot positions and ticker string to return
    a string of the current unrealized gain or loss for that ticker

    """
        try:

            #asset = await self.get_asset_by_ticker(breakdown=breakdown, ticker=ticker)
            if ticker:

                return ticker['unrealized_pnl']
        except Exception as e:
            logging.exception(msg=e)

    async def trade_amount(self, ticker:str,):
        """
        args takes a ticker as creates a trading amount based on the amount
        you want to spend per trade represented in the positiion size

        """
        try:
            #current_balance = await self.check_account_balance()
            #dont forget to pack , unpack, and repack
            #balance = Decimal(current_balance)
            balance = await self.get_trading_balance()
            position_size_check = balance - Decimal('5.00')
            if position_size_check >= Decimal('1.25'):
                position_size = position_size_check
                print(f"trading amount function trading balance: {position_size}")

                current_asset_price = await self.get_price(ticker)
                price = Decimal(current_asset_price)

                

                trade_amount = position_size / price
                d = Decimal(str(trade_amount))  # Convert to string first to preserve precision
                places = abs(d.as_tuple().exponent)

                trade_amount = round(trade_amount, ndigits=2)

                print(f"trade amount function amount is: {trade_amount}")

                return trade_amount

        except Exception as e:
            logging.exception(msg=e)


    async def test_retrieve_candles(self, ticker):
        try:
            candles = await self.get_candles(ticker=ticker)
            return candles
        except Exception as e:
            logging.exception(msg=e)

    async def get_trading_balance(self):
        """
        add the current wallet amount with the open orders hold amount
        to determine the amount of cash avail to trade
        """
        try:
            hold_on_open_orders = await self.open_orders_hold_amount()
            if hold_on_open_orders:
                hold = Decimal(hold_on_open_orders)
                print(f"the current hold amount for open orders is: {hold}")
                current_balance = await self.check_account_balance()
                balance = Decimal(current_balance) + hold
                print(f"current balance is at: {balance}")
                print(f"the current amount avail to trade is: {balance}")
                return balance
        except Exception as e:
            logging.exception(msg=e)

    async def cycle(self):
        """
        use asyncio.gather to call the buy logic and the sell logic concurrently


        """
        try:
            balance = await self.get_trading_balance()

            if balance > Decimal(5.00):
                print(f"beginning buy logic phase with ${balance}")
                await self.buy_logic()

            open_orders = await self.fetch_open_orders()

            if not open_orders:
                await asyncio.sleep(30.0)
                print(f"beginning sell cycle")

                #await self.sell_logic()


        except Exception as e:
            logging.exception(msg=e)
            logging.error(f"an error occured in the cycle function")


async def main():

    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    client = CryptoLinkClient(api_key, api_secret)
    while True:
        await client.cycle()





if __name__=='__main__':
    asyncio.run(main())
