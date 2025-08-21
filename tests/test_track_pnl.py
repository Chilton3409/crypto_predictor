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

async def test_bot_pnl(pnl):
    """
    track the bots profit and loss after each stop loss and take profit order"""
    try:
        
        if pnl:
            pnl = Decimal(pnl)
            client.bot_pnl += pnl
        
            return 
    except Exception as e:
        logging.exception(msg=e)
        
    
    
async def main():
    test = await client.sell_logic() 
    
    print(client.profit_and_loss)
    
if __name__=='__main__':
    asyncio.run(main())
    
    