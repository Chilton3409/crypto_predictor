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

async def open_orders_hold_amount():
    try:
        balances = client.client.get_futures_balance_summary()
        if balances.balance_summary.total_open_orders_hold_amount.value:
            
            return balances.balance_summary.total_open_orders_hold_amount.value
    
    except Exception as e:
        logging.exception(msg=e)
        
async def main():
    
    test = await open_orders_hold_amount()
    print(test)
    #print(buy_orders)
if __name__=='__main__':
    asyncio.run(main())
    
    