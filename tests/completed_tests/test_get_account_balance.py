#!/usr/bin/env python3
#New file created
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

def check_account_balance():
    
    summary = client.get_futures_balance_summary()


    total_usd_balance= summary.balance_summary['total_usd_balance']['value']
    total_usd_balance = Decimal(total_usd_balance)
    
    total = str(total_usd_balance)
    print(total)
    return total

current_balance = check_account_balance()
balance = Decimal(current_balance)
if balance > 1:
    print(f"current balance is greater than 1 at {current_balance}")
else:
    print('account balance is not greaterr than 1')

