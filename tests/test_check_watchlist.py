#!/usr/bin/env python3
#New file created
import AsyncCryptoV1
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from decimal import Decimal
import logging

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

client = AsyncCryptoV1.CryptoLinkClient(api_key, api_secret)
target = Decimal(10.00)

async def test_get_portfolios_id():
    portfolios = client.client.get_portfolios()
    test = portfolios.portfolios[0].uuid
    return test

async def test_portfolio_breakdown():
    id = await test_get_portfolios_id()
    
    test = client.client.get_portfolio_breakdown(portfolio_uuid=id)
    return test.breakdown

async def test_get_portfolio_balances():
    """
    return a list of portfolio balances
    
    """
    try:
        
        breakdown = await test_portfolio_breakdown()
        #balances = breakdown.portfolio_balances
        return breakdown
    except Exception as e:
        logging.exception(msg=e, stack_info=True)

async def test_get_total_usd_balance() -> str:
    """
    return the total balance of cash
    
    """
    breakdown = await test_portfolio_breakdown()
    usd = breakdown.portfolio_balances['total_balance']['currency']
    value = breakdown.portfolio_balances['total_balance']['value']
    value = str(value)
    
    return value
    

async def test_get_spot_positions():
    """
    returns a list of all currently held spot positions
    
    """
    breakdown = await test_portfolio_breakdown()
    positions = breakdown.spot_positions
    return positions
async def test_get_average_price():
    """
    returns a list of average prices for all held spot positions
    """
    breakdown = await test_get_spot_positions()
    assets = breakdown[0]['average_entry_price']
    #assets = [position.account_uuid for position in breakdown]
    return assets

async def get_unrealized_profit_loss():
    """
    returns a list of unrealized profit and loss for myn portfolio
    
    """
    breakdown = await test_get_spot_positions()
    unrealized_pnl = breakdown[0]['unrealized_pnl']
    return unrealized_pnl
    
    
    

async def get_cost_basis():
    """
    retrieves the cost basis for all the tickers in my portfolio
    """
    breakdown = await test_get_spot_positions()
    cost_basis = breakdown[0]['cost_basis']['value']
    return cost_basis
    
    

async def main():
    
    test = await test_get_portfolio_balances()
    print(test)
if __name__=='__main__':
    asyncio.run(main())
    