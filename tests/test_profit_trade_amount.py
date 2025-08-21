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

async def test_sell_trade_amount():
    spots = await client.get_spot_positions()
    for asset in spots:
        trade_amount = await client.sell_trade_amount(breakdown=spots, ticker=asset)
        print(f"the current trade amount before cutting in half: {trade_amount}")
        profit_trade = await test_profit_trade_amount(trade_amount=trade_amount)
        print(profit_trade)
    
async def test_profit_trade_amount(trade_amount: str) -> str:
    """
    take the base trade amount and slice it in half if taking profits
    pack unpack and repack
    """
    try:
        
        profit_trade = Decimal(trade_amount) * Decimal(.50)
        profit_trade = str(profit_trade)
        return profit_trade
    except Exception as e:
        logging.exception(msg=e)
        
    pass


async def main():
    test = await test_sell_trade_amount()
    print(test)  
    
    
    
if __name__=='__main__':
    asyncio.run(main())
    
    