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

async def test_trade_amount():
    test = await client.trade_amount(ticker='AST-USD')
    decimal_places = abs(test.as_tuple().exponent)
    print(test)
    return decimal_places

async def test_refactor():
    #position size
    position_size = Decimal(1.00)
    
    current_asset_price = await client.get_price('DEGEN-USD')
    price = Decimal(current_asset_price)
    trade_amount = position_size / price
    decimal_places= abs(trade_amount.as_tuple().exponent)
    if decimal_places:
        trade_amount = round(decimal_places, ndigits=2)
        
        return trade_amount
    else:
        return trade_amount
    
    

async def main():
    
    
    test = await test_refactor()
    print(f"the trading amount for ticker is {test}")
if __name__=='__main__':
    asyncio.run(main())
    
    