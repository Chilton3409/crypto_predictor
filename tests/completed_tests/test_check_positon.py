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
wallet_info = []
def check_wallets():
    wallets = client.client.get_accounts(limit=None)
    
    return wallets

def get_wallet_balance():
    wallets = check_wallets()
    for wallet in wallets.accounts:
        return wallet.available_balance
    
    
def get_currency_name():
    wallets = check_wallets()
    for wallet in wallets.accounts:
        return wallet.currency
    

def get_creation_date():
    wallets = check_wallets()
    for wallet in wallets.accounts:
        return wallet.created_at
    