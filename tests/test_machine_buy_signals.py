#!/usr/bin/env python3
#New file created

import asyncio 
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

tickers = client.get_top_gainers()

async def test_generate_buy_signals():
    pass


    
    

    


async def main():
    test = await client.sell_trade_amount(ticker='HOPR')
    
if __name__=='__main__':
    asyncio.run(main())
    
    
