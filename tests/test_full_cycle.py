#!/usr/bin/env python3
import asyncio
import AsyncCryptoV1
from dotenv import load_dotenv
import os
from decimal import Decimal
import logging
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import precision_recall_curve

from sklearn.model_selection import train_test_split
from dotenv import load_dotenv  
load_dotenv()
load_dotenv()
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
client = AsyncCryptoV1.CryptoLinkClient(api_key, api_secret)

target = Decimal(10.00)
async def test_cycle():
    await asyncio.gather(client.buy_logic(), client.sell_logic())

async def main():
    while True:
        
        await test_cycle()
    

asyncio.run(main())

