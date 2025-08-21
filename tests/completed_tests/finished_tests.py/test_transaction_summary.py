#!/usr/bin/env python3
#New file created

from coinbase.rest import RESTClient
import os
from dotenv import load_dotenv
load_dotenv()
from decimal import Decimal

import json
import CryptoLinkv2
import uuid



# Replace with your API credentials
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
client = RESTClient(api_key, api_secret)

test_id = "00ac2d60-1b3f-47b0-95cd-c1ace39d679f"


def transaction_summary():
    """
    get the latest trade summary 
    """
    try:
        transactions = client.get_transaction_summary()
        return transactions
    except Exception as e:
        return e
    
x = transaction_summary()
print(x)