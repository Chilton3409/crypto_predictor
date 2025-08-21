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


async def take_profit_trade_amount(asset):
    
        avail_trade = asset['available_to_trade_crypto']
        profit_trade = Decimal(avail_trade) * Decimal(.50)
        return profit_trade

async def test():
    await client.cycle()


async def main():
    await test()
        
        
    #print(buy_orders)
if __name__=='__main__':
    asyncio.run(main())
    
    