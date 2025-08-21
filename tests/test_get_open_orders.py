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
    
async def test_fetch_orders():
    try:
        orders = client.client.list_orders(order_status='OPEN')
        return orders
    
    except Exception as e:
        pass

async def test_get_open_orders():
    try:
        orders = client.client.list_orders(order_status='OPEN')
        if orders:
            return orders.orders
        
    except Exception as e:
        logging.exception(msg=e)

async def main():
    
    orders = await test_get_open_orders()
    for order in orders:
        print(order.status)
        if not order.status == "FILLED":
            print("passed")
    #print(buy_orders)
if __name__=='__main__':
    asyncio.run(main())
    
    