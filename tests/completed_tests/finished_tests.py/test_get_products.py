#!/usr/bin/env python3
#New file created
from coinbase.rest import RESTClient
import os
from dotenv import load_dotenv
load_dotenv()
from decimal import Decimal

import json
import CryptoLink

# Replace with your API credentials
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

client = RESTClient(api_key, api_secret)


def get_products():
        products = client.get_products(get_tradability_status=True,)
        test = products.products
        test = [product for product in test if product.quote_name =="US Dollar"]
        sorted_test = sorted(test, key=lambda x: (float(x.price_percentage_change_24h) if x.price_percentage_change_24h else 0, 
                                               float(x.volume_percentage_change_24h) if x.volume_percentage_change_24h else 0), 
                        reverse=True)
        top_gainers_last_day = sorted_test[:15]  # Get the top 5 gainers
        top_gainers_tickers = [gainer.product_id for gainer in top_gainers_last_day]
        return top_gainers_tickers
    
z = get_products()
print(z)