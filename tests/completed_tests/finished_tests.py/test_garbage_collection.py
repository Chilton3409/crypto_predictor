#!/usr/bin/env python3
#New file created
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

client.top_performers = ['sd-usd', 'eth-usd']
client.ticker_list = ['btc-usd', 'eth-usd', 'sd-usd']
client.garbage_collection('btc-usd')
#print(client.garbage)

    
first_key = list(client.average_prices.keys())[0]
first_value = client.average_prices[first_key]
