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
"""
list the buy logic steps

get a list of all spot positions
filtered by asset name: ticker
check the ticker pnl
eval stop loss or take profit



"""
async def test_sell_logic():
    
    spots = await client.get_spot_positions()
    for asset in spots:
        check_pnl = await client.test_unrealized_gains(breakdown=spots, ticker=asset)
        print(f"{asset['asset']} is at {check_pnl} :")
        await client.stop_loss(pnl=check_pnl, stop_loss_threshold=client.stop_loss_threshold, ticker=asset['asset']+ "-USD")
    return
    
    
async def test_retrieve_portfolio(spots):
    spots = spots
    for asset in spots:
        assets = asset['asset']
        return assets
    

    
    

async def main():
    
    
    test = await client.sell_logic()
    print(test)
    
    """

    for asset in spots:
        check_pnl = await client.test_unrealized_gains(breakdown=spots, ticker=asset)
        print(f"{asset['asset']} is at {check_pnl} :")

   """
    
if __name__=='__main__':
    asyncio.run(main())
    
    
