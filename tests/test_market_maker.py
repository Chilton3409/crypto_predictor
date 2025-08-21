#!/usr/bin/env python3
#New file created
import AsyncCryptoV1
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from decimal import Decimal
import logging
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

client = AsyncCryptoV1.CryptoLinkClient(api_key, api_secret)

async def get_most_active():
        """

        returns a list of the most active by 24 hour volume change
        

        """
        print("collecting data on top 25 gainers")
     
        test = await client.get_coin_info()
        
        sorted_test = sorted(test, key=lambda x: (float(x.volume_percentage_change_24h) if x.volume_percentage_change_24h else 0,
                                               float(x.price_percentage_change_24h) if x.price_percentage_change_24h else 0),
                        reverse=True)
        top_gainers_last_day = sorted_test[:25]  # Get the top 25
        top_gainers_tickers = [gainer.product_id for gainer in top_gainers_last_day]

        #self.ticker_list.extend(top_gainers_tickers)


        return top_gainers_tickers
    
async def market_maker_check(ticker, position_size):
    try:
        bid_price = await client.get_bid_price(ticker)
        ask_price = await client.get_ask_price(ticker)
        spread = Decimal('0.03')
        min_spread = Decimal('0.01')
        
        
        bid_price = Decimal(bid_price) * (1 - spread)
        ask_price = Decimal(ask_price) * (1 - spread)          
        spread_value = ask_price - bid_price
        if spread_value >= min_spread:
            #mayve add a while loop to get it to focus on obe
            
            print(f"Ptofitable market maker detected {ticker}. Current bid: {bid_price}: current ask: {ask_price}")
            #check to make sure spread hits the minimum
            trade_amount = position_size / bid_price
            trade_amount = round(trade_amount, ndigits=2)
            #await client.create_buy_order(ticker=ticker, trade_amount=trade_amount)
            
            sell_trade_amount = position_size / ask_price
            sell_trade_amount = round(sell_trade_amount, ndigits=2)
            print(f"current buy amount is: {trade_amount}. Current sell amount is: {sell_trade_amount}")
            
            #here we place a buy order and a cell order
            #create a sell order
            #await client.create_sell_order(ticker=ticker, trade_amount=sell_trade_amount)
            return True
        else:
            print(f"the spread for {ticker} is to low. Spread: {spread}. bid price: {bid_price}. Ask price: {ask_price}")

    except Exception as e:
        logging.exception(msg=e)
        
       
async def market_makers(tickers:list):
    try:
        position_size = Decimal('1.25')
        for ticker in tickers:
            bid_price = await client.get_bid_price(ticker)
            ask_price = await client.get_ask_price(ticker)
            spread = Decimal('0.03')
            min_spread = Decimal('0.01')
            
            
            bid_price = Decimal(bid_price) * (1 - spread)
            ask_price = Decimal(ask_price) * (1 - spread)          
            spread_value = ask_price - bid_price
            if spread_value >= min_spread:
                #mayve add a while loop to get it to focus on obe
                
                print(f"Ptofitable market maker detected {ticker}. Current bid: {bid_price}: current ask: {ask_price}")
                #check to make sure spread hits the minimum
                trade_amount = position_size / bid_price
                trade_amount = round(trade_amount, ndigits=2)
                #await client.create_buy_order(ticker=ticker, trade_amount=trade_amount)
                
                sell_trade_amount = position_size / ask_price
                sell_trade_amount = round(sell_trade_amount, ndigits=2)
                print(f"current buy amount is: {trade_amount}. Current sell amount is: {sell_trade_amount}")
                
                #here we place a buy order and a cell order
                #create a sell order
                #await client.create_sell_order(ticker=ticker, trade_amount=sell_trade_amount)
                return True
            else:
                print(f"the spread for {ticker} is to low. Spread: {spread}. bid price: {bid_price}. Ask price: {ask_price}")
                
                
    except Exception as e:
        logging.exception(msg=e)
        
async def main():
    
        top_gainers = await client.get_top_gainers()
        most_active = await get_most_active()
        print(f"here are the most_active tickers: {most_active}")
        #await market_makers(tickers=most_active)
        
        #await market_makers(tickers=top_gainers)
        print(f"here are the top gainers: {top_gainers}")
        print("cycle complete")
    
    #print(buy_orders)
if __name__=='__main__':
    asyncio.run(main())
    
    