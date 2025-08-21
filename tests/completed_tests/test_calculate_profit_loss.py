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
async def test_profit_loss():
    
    profit_loss = await client.calculate_gain_or_loss(ticker='AST-USD')
    return profit_loss

async def test_vary_price():
    current_price = await client.get_price(ticker="AST-USD")
    current_price = Decimal(current_price)
    latest_buy_price = await client.get_latest_buy(ticker='AST-USD')
    latest_buy_price = Decimal(latest_buy_price)
    check_gains = current_price - latest_buy_price
    percent = check_gains / latest_buy_price * 100
    rounded = round(percent, ndigits=3)
    if rounded >= target:
        print(f"Target reached \n Current position: {rounded}, target={target}")
    return rounded  



async def main():
    
    test = await test_vary_price()
    
    print(test)
if __name__=='__main__':
    asyncio.run(main())
    
    