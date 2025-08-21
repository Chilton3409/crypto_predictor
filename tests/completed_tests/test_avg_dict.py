#!/usr/bin/env python3
#New file created
#!/usr/bin/env python3
#New file created
import CryptoLinkv2
from dotenv import load_dotenv
load_dotenv()
import os
from decimal import Decimal
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

client = CryptoLinkv2.CryptoLinkClient(api_key, api_secret)


#client.average_prices = {
#'btc-usd': [3.99, 5.02, 9.00],
#'eth-usd': [4.00, 2.00, 29.00]
#}

ticker = 'btc-usd'
client.average_prices = {}
client.average_prices[ticker] = []

client.average_prices[ticker].append(Decimal(4.06))
client.average_prices[ticker].append(Decimal(2.01))


#calculate the average prices
average_price = sum(client.average_prices[ticker]) / len(client.average_prices[ticker])
average_price = round(average_price, ndigits=2)
#client.average_prices['btc-usd'].remove(3.99)
#client.average_prices['btc-usd'].append(3.13567)
print(client.average_prices.get('btc-usd'))
print(average_price)