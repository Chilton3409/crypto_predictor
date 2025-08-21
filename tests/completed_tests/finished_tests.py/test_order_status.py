#!/usr/bin/env python3
#New file created

from coinbase.rest import RESTClient
import os
from dotenv import load_dotenv
load_dotenv()
from decimal import Decimal

import json
import CryptoLink
import uuid



# Replace with your API credentials
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
client = RESTClient(api_key, api_secret)

test_id = "00ac2d60-1b3f-47b0-95cd-c1ace39d679f"


def get_order_status(client_id: str):
    
        """
        args: takes a client order uuid and returns the order status.
        
        
        """
        try:
            recent = client.get_order(order_id=client_id)
            return recent.order.status
        except Exception as e:
            print(f"error getting order status {e}")
            return None

status=get_order_status(test_id)


if status:
    print(f"status is currently {status}")