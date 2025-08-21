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
    position_size = Decimal(5.00)
    
    current_asset_price = await client.get_price('COOKIE-USD')
    if current_asset_price:
        
        if "." in current_asset_price:
            decimal_places = len(current_asset_price.split('.')[1])
            if decimal_places >= 4:
                asset_price = Decimal(current_asset_price)
                price = Decimal(current_asset_price)
                trade_amount = position_size / price
                trade_amount = round(trade_amount, 1)
                print(f"Number of decimal places: {decimal_places} and the current price is {asset_price}. Current trade amount is: {trade_amount} Rounding trade amount to 1 digit.")
            else:
                asset_price = Decimal(current_asset_price)
                price = Decimal(current_asset_price)
                trade_amount = position_size / price
                trade_amount = round(trade_amount, 2)
                print(f"Number of decimal places: {decimal_places} and the current price is {asset_price}. Current trade amount is: {trade_amount} Rounding trade amount to 2 digits.")
        else:
            trade_amount = round(trade_amount, 2)
            print(f"No decimal places found in the price. Rounding trade amount to 2 digits.")

            return trade_amount

        

async def main():
    
    
    test = await client.trade_amount(ticker='HOPR-USD')
    
if __name__=='__main__':
    asyncio.run(main())
    
    