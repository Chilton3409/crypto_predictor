#!/usr/bin/env python3
#New file created
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

products = client.get_products()
print(products.products[0].quote_name)
