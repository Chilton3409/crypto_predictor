#!/usr/bin/env python3
#New file created
import AsyncCryptoV1
import os
import logging
from multiprocessing import Pool
import time
from decimal import Decimal
import asyncio

async def cycle(ticker, Crypto):
    #going to wrap 4 functions togeth so they can be called concurrently
    #calling them at the same time will be bad ass
    try:
        current_balance = await Crypto.check_account_balance()
        #dont forget to pack , unpack, and repack 
        balance = Decimal(current_balance)
        
        if balance > Decimal(2.00):
            print(f"Beginning buy logic, current balance is at: {balance}")
            await Crypto.buy_logic()
            
        #I think I want to call this after the cycle
        #spot_positions = await Crypto.get_spot_positions()
        #await Crypto.sell_logic(spot_positions=spot_positions, ticker=ticker)
        
    except Exception as e:
        logging.error(f"An error occurred while processing {ticker}: {e}")
        logging.exception(msg=e)
        
async def main():
    while True:
        try:
            api_key = os.environ.get("API_KEY")
            api_secret = os.environ.get("API_SECRET")

            if not api_key or not api_secret:
                logging.error("API key or secret is missing")
                return

            Crypto = AsyncCryptoV1.CryptoLinkClient(api_key=api_key, api_secret=api_secret)

            #first find the top 25 gainers
            await Crypto.get_top_gainers()
          
        
              # Execute trades concurrently using asyncio.gather
            await asyncio.gather(*[cycle(ticker, Crypto) for ticker in Crypto.ticker_list])
            
            print(f'current top performers are: {Crypto.ticker_list}')
            
            print("beginning sell logic phase")
            
            await Crypto.sell_logic()

            logging.info("Completed a cycle")

        except Exception as e:
            logging.error(f"An error occurred: {e}")
        await asyncio.sleep(15.00)

if __name__ == '__main__':
    asyncio.run(main())
    