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

async def get_spots():
    spots = await client.get_spot_positions()
    return spots
async def test():
    pass

async def get_average_entry(asset):
    try:
        
        return asset['average_entry_price']['value']
    
    except Exception as e:
        logging.exception(msg=e)


async def main():
    test = await get_spots
    for asset in test:
       
        print(f"the average entry price for {asset['asset']}")
        entry = await get_average_entry(asset=asset)
        print(entry)
        
    #print(buy_orders)
if __name__=='__main__':
    asyncio.run(main())
    
    