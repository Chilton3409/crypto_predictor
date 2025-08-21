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
import uuid
client = RESTClient(api_key, api_secret)





def futures_summary():
    """
    returns the futures summary from the api as a dict
    
    """
    try:
        futures = client.get_futures_balance_summary()
        return futures
    
    
    except Exception as e:
        print(f"an uknown error occured {e}")
        return
    
def get_futures_position(ticker: str):
    
    """
    args provide a ticker to look`up the futures contract
    get futures positon info from the client as a dict
    
    """
    try:
        futures_postion = client.get_futures_position()
        if futures_postion is not None:
            
            return futures_postion
        else:
            message = "you dont have any open futures contracts"
            return message
    except Exception as e:
        print(f"an error occured in the get futures position function")
    return
    
def get_perps_portfolio_balances():
    """
    look up perp portfolio balances
    """
    try:
        perps = client.get_perps_portfolio_balances()
        return perps
    
    except Exception as e:
        print(f"error occured in perp balance breakdown")
        return
    

        
        