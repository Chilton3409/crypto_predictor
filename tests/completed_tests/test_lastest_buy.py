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

async def test_latest_buy():
    latest_buy = await client.get_fills(ticker='AST-USD')
    if latest_buy.side == 'BUY':
        
        return latest_buy.price



async def main():
    
    test = await test_latest_buy()
    
    print(test)
if __name__=='__main__':
    asyncio.run(main())
    
    