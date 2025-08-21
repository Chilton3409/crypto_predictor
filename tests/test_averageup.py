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
target = Decimal(10.00)

async def test_latest_buy():
    latest_buy = await client.get_fills(ticker='MDT-USD')
    if latest_buy.side == 'BUY':
        
        return latest_buy.price
    
async def test_fetch_orders_by_ticker(ticker):
    try:
        orders = client.client.list_orders(order_status='OPEN', product_ids=ticker)
        if orders:
            
            return orders
        else:
            return None
    
    except Exception as e:
        logging.exception(msg=e)
async def test_fetch_orders():
    try:
        orders = client.client.list_orders(order_status='OPEN')
        return orders
    
    except Exception as e:
        pass
    
async def test_profit_cycle():
    try:
        pass
    
    except Exception as e:
        logging.exception(msg=e)
async def average_up(ticker):
    try:
        average_up_amount = await client.check_account_balance()
        print(average_up_amount)
        #create sell order here
        #dont forget to add the -usd
        await client.create_buy_order(ticker=ticker, trade_amount=average_up_amount)
        print(f"average up completed successully")
    except Exception as e:
        logging.exception(msg=e)
        
async def test_average_up(spots,):
    
    
    try:
        
    
        for asset in spots:
            
            check_pnl = await client.test_unrealized_gains(breakdown=spots, ticker=asset)
            
            if check_pnl < Decimal(-.01):
                print(f"{asset['asset']} is at: {check_pnl}")
        
            if check_pnl >= Decimal(.06):
                pass
                #call the average up function here
                
                
    except Exception as e:
        logging.exception(msg=e)

async def main():
    await client.sell_logic()
    
    
        
    #print(buy_orders)
if __name__=='__main__':
    asyncio.run(main())
    
    