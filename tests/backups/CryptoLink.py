#!/usr/bin/env python3
#New file created
from multiprocessing import Pool, Manager
import os
import sys

from dotenv import load_dotenv

from decimal import Decimal


from coinbase.rest import RESTClient
from decimal import Decimal
import uuid
load_dotenv()
import time
import datetime


class CryptoLinkClient():
    def __init__(self, api_key, api_secret):
        #first get the client

        self.client = RESTClient(api_key=api_key, api_secret=api_secret)

        self.ticker_list = []
        self.garbage = []
        self.top_performers = []
        self.average_prices = getattr(self, 'average_prices', {})
        self.gain_or_loss = {}
        self.profit_threshold = Decimal(1.25)
        self.stop_loss_threshold = Decimal(-1.50)
    def get_all_coin_info(self):
        try:

            products = self.client.get_products(get_tradability_status=True,)
            test = products.products
            test = [product for product in test if product.quote_name =="US Dollar"]
            return test
        except Exception as e:
            print(f"Error occured in get all coin info: {e}")

    def find_top_five_gainers(self):
        print("collecting data on top 15 gainers")
        try:
            test = self.get_all_coin_info()
            sorted_test = sorted(test, key=lambda x: (float(x.price_percentage_change_24h) if x.price_percentage_change_24h else 0,
                                               float(x.volume_percentage_change_24h) if x.volume_percentage_change_24h else 0),
                        reverse=True)

            top_gainers_last_day = sorted_test[:15]  # Get the top 5 gainers
            top_gainers_tickers = [gainer.product_id for gainer in top_gainers_last_day]
            time.sleep(1.00)
            self.ticker_list.extend(top_gainers_tickers)
            self.top_performers.extend(top_gainers_tickers)

            return top_gainers_tickers
        except Exception as e:
            print(f"error occurred in the find top 5 gainers: {e}")

    def get_price(self, ticker):
        asset = self.client.get_product(ticker)
        price = asset.price
        return price

    def get_info(self, ticker):
        info = self.client.get_products(product_ids=[ticker])
        #this will get info on a single coin
        return info

    #get the order book with bid/ask price for a single ticker.
    def get_order_book(self, ticker):
        #get the order book for a single ticker
        order_book = self.client.get_product_book(ticker)
        #bid_price = order_book.pricebook.bids[0].price
        #ask_price = order_book.pricebook.asks[0].price
        return order_book

    def get_bid_price(self, ticker):
        #get the bid price for a single ticker.
        order_book = self.get_order_book(ticker=ticker)
        bid_price = order_book.pricebook.bids[0].price
        return bid_price

    def get_ask_price(self, ticker):
        order_book = self.get_order_book(ticker=ticker)
        ask_price = order_book.pricebook.asks[0].price
        return ask_price

    #get the candle data for a single ticker
    def get_candles(self, ticker):
        try:
            
    #dont forget to set the unix date, time, and granularity for the charts
            start_time = datetime.datetime.now()-datetime.timedelta(seconds=60)
            start_time_unix = int(datetime.datetime.timestamp(start_time))
            end_time = datetime.datetime.now()
            end_time_unix = int(datetime.datetime.timestamp(end_time))
            candles = self.client.get_candles(ticker, start=start_time_unix,end=end_time_unix,granularity="1")
        
        except Exception as e:
            print(f"error from the get candles logic: {e}")

        return candles
    #get the latest order fills
    def get_fills(self, ticker):
        fills = self.client.get_fills(product_ids=ticker)
        if fills.fills:
            fills = fills.fills[0]
            return fills #return the latest ordrer
        else:
            return [] #haven't ordered this ticker before.

    #get the latest transaction summary
    def get_summary(self):
        summary = self.client.get_transaction_summary()
        return summary

    def check_account_balance(self):
        try:
            summary = self.client.get_futures_balance_summary()
            total_usd_balance= summary.balance_summary['total_usd_balance']['value']
            total_usd_balance = Decimal(total_usd_balance)
            total = str(total_usd_balance)

            print(total)
        except Exception as e:
            print(f"error from check account balance: {e}")
        return total

    def create_sell_order(self, ticker):
        
        ask_price = self.get_ask_price(ticker=ticker)

        #get the trading amount
        trade_amount = self.trade_amount(ticker=ticker)
        client_id = str(uuid.uuid4())
        try:

            self.client.limit_order_gtc_sell(
                client_order_id=client_id, product_id=ticker, base_size=str(trade_amount),limit_price=str(ask_price))

            #check if the order went through
            time.sleep(5.00)
            print("sell order for {ticker} executed succesfully")
            if ticker in self.average_prices:
                order_price = self.average_prices[ticker].pop(0)
               
                print(f"Removed {order_price} to average_prices[{ticker}]")

        except Exception as e:
            print(f"Error from the sell order: {e}")

        return

    def create_buy_order(self, ticker):
    
    #need to also get the bid price, lets try that at the bottom
        bid_price = self.get_bid_price(ticker=ticker)
        #get the trade amount.
        trade_amount = self.trade_amount(ticker=ticker)
        client_id = str(uuid.uuid4())
        try:
            self.client.limit_order_gtc_buy(
        client_order_id=client_id, product_id=ticker,base_size=str(trade_amount),limit_price=(str(bid_price)))

            #check the order status
            time.sleep(5.00)
                #add the price to the list
            print(f"Buy order for {ticker} executed successfully")
            if ticker not in self.average_prices:
                self.average_prices[ticker] = []
                order_price = Decimal(bid_price)
                self.average_prices[ticker].append(order_price)
                print(f"Added {order_price} to average_prices[{ticker}]")
            else:
                self.average_prices[ticker].append(order_price)
        except Exception as e:
            print(f"error from the create buy order: {e}")

        return

    def get_latest_order(self, ticker):
        latest_order= self.get_fills(ticker=ticker)
        if latest_order is not None:

            return latest_order

    def get_latest_buy(self, ticker):
        latest_order = self.get_latest_order(ticker=ticker)
        if latest_order:
            if latest_order.side == "BUY":
                latest_buy = latest_order.price
                return latest_buy
            else:
                return None

    def get_order_status(self, client_id):
        try:
            recent = self.client.get_order(order_id=client_id)
            return recent.order.status
        except Exception as e:
            print(f"error getting order status {e}")
            return None

    def get_latest_sale(self, ticker):
        latest_order = self.get_latest_order(ticker=ticker)
        if latest_order.side == "SELL":
            latest_sale = latest_order.price
            return latest_sale
        else:
            return None

    def calculate_average(self, ticker):
        #beware division by zero
        #go through the list of average price by using tickr as key
        try:
            if ticker not in self.average_prices:
                self.average_prices[ticker] = [None]
            #here is the problem
            coin_prices = self.average_prices.get(ticker)
            print(f"Coin prices for {ticker}: {coin_prices}")  # <--- Add 
            if not coin_prices or None in coin_prices:
                print(f"No purchases yet for {ticker}")
                return Decimal(0)
            
                
            average = Decimal(sum(coin_prices)) / Decimal(len(coin_prices))
            return average
        except Exception as e:
            print(f"Error calculating average for {ticker}: {e}")
            return None
        except Exception as e:
            print(f"error from calculate average: {e}")

    def calculate_gain_loss(self, ticker):
        try:
        #need the asset price
            current_price = self.get_price(ticker)
            time.sleep(1.00)
            #get the average price
            average_price = self.calculate_average(ticker)
            
            #need the last purchase price
            if average_price != 0:
                    average_price = Decimal(average_price)
            #current gain or loss is asset price - latest_buy price
                    
                    current_gain_or_loss = Decimal(current_price) - Decimal(average_price)

                #turn it into a percent
                    current_gain_loss_percent = current_gain_or_loss / Decimal(average_price) * 100
                    current_gain_or_loss = round(current_gain_loss_percent, ndigits=4)
                    
                    if current_gain_or_loss >= self.profit_threshold:
                        print(f"taking profits on ticker {ticker} at {current_gain_or_loss}")
                        self.create_sell_order(ticker=ticker)
                    if current_gain_or_loss <= self.stop_loss_threshold:
                        print(f"stopping loss on {ticker} at {current_gain_or_loss}")
                        self.create_sell_order(ticker=ticker)

                    print(f"current gain or loss on {ticker} is %{current_gain_or_loss}")
                    time.sleep(5.00)
                    
            elif average_price == 0:
                return None

        except Exception as e:
            print(f'error occured in calculate gain or loss: {e}')

    
    def trade_amount(self, ticker):
        try:
            
            position_size = Decimal(2.00)
            current_asset_price = self.get_price(ticker=ticker)
            trade_amount = position_size / Decimal(current_asset_price)
            trade_amount = round(trade_amount, ndigits=2)
        except Exception as e:
            print(f"error from the trade amount: {e}")

        return trade_amount

    def buy_logic(self, ticker):
        try:
            #check account balance 
            #if greater than $1.00 proceed
            current_balance = self.check_account_balance()
            balance = Decimal(current_balance)
            if balance >= Decimal(1.00):
                
            
                print("in the buy logic phase")
                #get the candle data for a single ticker
                candles = self.get_candles(ticker=ticker)

                # Calculate the short and long moving averages
                short_window = 2
                long_window = 4
                buy_threshold = Decimal(.04)
                short_ma = sum(Decimal(candle.low) for candle in candles.candles[-short_window:]) / Decimal(short_window)

                long_ma = sum(Decimal(candle.high) for candle in candles.candles[-long_window:]) / Decimal(long_window)
                long_ma = round(long_ma, ndigits=8)

                var = long_ma * Decimal(1.0) + buy_threshold
                var = round(var, ndigits=8  )
                #assess whether or not to buy the ticker
                if short_ma > var:
                    #add create sale function here, passing in the ticker as a parameter,
                    print(f"buy signal generated on {ticker}")
                    self.create_buy_order(ticker=ticker)
                    time.sleep(5.00)
        except Exception as e:
            print(f"error from buy logic: {e}")


    def garbage_collection(self, ticker):
        try:
            
            print("Garbage collection phase")

            if ticker in self.average_prices:
                print(f'the ticker {ticker} is in garbage collection phase 1')

                if ticker not in self.ticker_list:
                    self.garbage.append(ticker)
                    print(f"appended {ticker} to the garbage.")

        except Exception as e:
            print(f"error from the garbage collection: {e}")
            
            return

    def sell_garbage(self, ticker):
        print("Selling garbage phase")
        if ticker in self.garbage:
            print(f"current garbage list is {self.garbage}")

            try:

                #now we can safely take out the garbage
                self.create_sell_order(ticker=ticker)
                print(f"we should be selling {ticker} for harvesting")
            except Exception as e:
                print(f'error selling {ticker} error {e}')
            return