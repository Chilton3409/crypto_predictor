#!/usr/bin/env python3
#New file created
import CryptoLink
from dotenv import load_dotenv
load_dotenv()
import os
from decimal import Decimal

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

client = CryptoLink.CryptoLinkClient(api_key, api_secret)

def check_wallets():
    wallets = client.client.get_accounts(limit=None)
    
    return wallets



def print_wallets():
    x = check_wallets()
    wallet_info = []
    for wallet in x.accounts:
        currency_name = wallet.currency
        wallet_creation_date = wallet.created_at
        wallet_balance = wallet.available_balance['value']
        
        
        
        if Decimal(wallet_balance) > 0:
            wallet_info.append(currency_name + '-USD')
            wallet_info.append(wallet_creation_date)
            wallet_info.append(wallet_balance)
        
    return wallet_info
    
x = print_wallets()
for wallet in x:
    print(wallet)
    

    
