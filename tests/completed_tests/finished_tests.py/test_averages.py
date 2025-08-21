#!/usr/bin/env python3
#New file created
import CryptoLink
from dotenv import load_dotenv
load_dotenv()
import os


api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

client = CryptoLink.CryptoLinkClient(api_key, api_secret)

client.average_prices = {
'btc-usd': [3.99, 5.02, 9.00],
'eth-usd': [4.00, 2.00, 29.00]
}


prices = client.average_prices.get('btc-usd')
for p in prices:
    total = p + p
    count = len(prices)
    average = total/count
    
print(average)

    
    