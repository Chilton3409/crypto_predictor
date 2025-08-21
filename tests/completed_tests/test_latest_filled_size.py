#!/usr/bin/env python3
#New file created
import AsyncCryptoV1
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from decimal import Decimal
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

client = AsyncCryptoV1.CryptoLinkClient(api_key, api_secret)
target = Decimal(10.00)

async def test_last_filled_size():
    latest_buy = await client.get_fills(ticker='ABT-USD')
    if latest_buy.side == 'BUY':
        latest_buy_size = latest_buy.size
        latest_price = latest_buy.price
        amount = Decimal(latest_buy_size) * Decimal(latest_price)
        amount = round(amount, ndigits=2)
        return amount


async def main():
    
    test = await test_last_filled_size()
    
    print(test)
if __name__=='__main__':
    asyncio.run(main())
    
    