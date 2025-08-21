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

async def test_get_portfolios_id():
    portfolios = client.client.get_portfolios()
    test = portfolios.portfolios[0].uuid
    return test

async def test_portfolio_breakdown():
    id = await test_get_portfolios_id()
    
    test = client.client.get_portfolio_breakdown(portfolio_uuid=id)
    return test.breakdown

async def test_get_asset_names():
    """
    returns a list of tickers of all currently held assets
    """
    breakdown = await test_get_spot_positions()
   
    asset_names = [position['asset'] for position in breakdown]
    #assets = [position.account_uuid for position in breakdown]
    return asset_names

async def test_unrealized_gains(breakdown, ticker: str) -> str:
    """
    takes breakdown of spot positions and ticker string to return
    a string of the current unrealized gain or loss for that ticker
    
    """
    try:
        
        asset = await client.get_asset_by_ticker(breakdown=breakdown, ticker=ticker)
        return asset['unrealized_pnl']
    except Exception as e:
        logging.exception(msg=e)
        


    

async def test_get_spot_positions() -> list:
    """
    returns a list of all currently held spot positions
    
    """
    try:
        
        breakdown = await test_portfolio_breakdown()
        positions = breakdown.spot_positions
        return positions
    except Exception as e:
        logging.exception(msg=e, stack_info=True)
        
async def main():
    
    breakdown = await client.get_spot_positions()
    
    pnl = await client.test_unrealized_gains(breakdown=breakdown, ticker='COMP')
    print(pnl)
    
    
    
    """
    if asset:
        print(asset)
    else:
        print(f"No asset found for ticker {ticker}")

    #test = await test_get_average_price()
    #test = await client.test_get_spot_positions()
"""
    #print(test)
if __name__=='__main__':
    asyncio.run(main())
    
    