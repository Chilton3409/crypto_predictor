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
ticker='AST-USD'

async def test_get_latest_order():
    
    lastest_order = await client.get_fills(ticker=ticker)
    return lastest_order

async def test_get_retail_id():
    order = await test_get_latest_order()
    retail_id = order.retail_portfolio_id
    return retail_id
    

async def test_get_user_id():
    order = await test_get_latest_order()
    user_id = order.user_id
    return user_id

async def test_get_retail_account():
    id = await test_get_retail_id()
    account = client.client.get_account()
    return account

async def test_get_accounts():
    
    id = await test_get_retail_id()
    accounts = client.client.get_accounts(retail_portfolio_id=id)
    
    return accounts

async def main():
    
    test = await test_get_accounts()
    
    print(test)
if __name__=='__main__':
    asyncio.run(main())
    
    