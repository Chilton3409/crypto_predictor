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

async def test_sell_trade_amount():
    spots = await client.get_spot_positions()
    for asset in spots:
        trade_amount = await client.sell_trade_amount(breakdown=spots, ticker=asset)
        print(f"the current trade amount before cutting in half: {trade_amount}")
        reduce = Decimal(trade_amount) * Decimal(.50)
        reduce = str(reduce)
        print(f"the trade amount split in haf is: {reduce} for {asset['asset']}")
    
async def main():
    test = await client.sell_logic()
    print(test)  
    
    
    
if __name__=='__main__':
    asyncio.run(main())
    
    