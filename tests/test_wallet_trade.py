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

async def test_sell_trade_amount(ticker: str) -> str:
    
    test = await client.get_spot_positions()
    asset = await client.get_asset_by_ticker(test, ticker='HOME')
    #available_to_trade_crypto
    amount_to_trade = asset['available_to_trade_crypto']
    
    return amount_to_trade
    
    

    


async def main():
    test = await client.sell_trade_amount(ticker='HOPR')
    
if __name__=='__main__':
    asyncio.run(main())
    
    
