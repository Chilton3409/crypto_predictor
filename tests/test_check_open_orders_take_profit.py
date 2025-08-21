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

async def test_get_open_orders(ticker):
    try:
        orders = client.client.list_orders(product_ids=ticker, order_status='OPEN')
        if orders.orders[0].side == 'SELL':
            open_sell_orders = orders.orders[0].side == 'SELL'
            return open_sell_orders
            
       
    except Exception as e:
        logging.exception(msg=e)

async def main():
    
    sell_orders = await client.get_open_sell_orders(ticker='KERNEL-USDC')
    buy_orders = await client.get_open_buy_orders(ticker='KERNEL-USDC')
    print(sell_orders)
    print(buy_orders)
if __name__=='__main__':
    asyncio.run(main())
    
    