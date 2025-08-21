#!/usr/bin/env python3
#New file created
import AsyncCryptoV1 
import asyncio 
import os
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
client = AsyncCryptoV1.CryptoLinkClient(api_key, api_secret)

async def test():
    
    data = client.client.get_portfolios()
    test = client.get_portfolio_breakdown()


async def main():
    
    test = await test()
    
    print(test)
if __name__=='__main__':
    asyncio.run(main())
    
    
