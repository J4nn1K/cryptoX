from requests import Request, Session
from binance.client import Client
from binance.enums import *
import os

def check_api_keys():
    return 'CMC_API_KEY' in os.environ and 'BINANCE_API_KEY' in os.environ and 'BINANCE_SECRET_KEY' in os.environ

def get_prices(pairs):
    API_KEY = os.environ['BINANCE_API_KEY']
    API_SECRET = os.environ['BINANCE_SECRET_KEY']
    client = Client(API_KEY, API_SECRET)
    
    prices = []
    
    for pair in pairs:
        avg_price = client.get_avg_price(symbol=pair)
        prices.append(float(avg_price['price']))

    return prices

def calculate_quantity(fiat, percentages, prices):
    fiat_per_coin = []
    quantity = []
    for i in range(len(percentages)):
        fiat_per_coin.append(percentages[i]/100 * fiat)
    for i in range(len(fiat_per_coin)):
        quantity.append(fiat_per_coin[i] / prices[i])

    return fiat_per_coin, quantity
    
def place_order(pair, quantity):
    API_KEY = os.environ['BINANCE_API_KEY']
    API_SECRET = os.environ['BINANCE_SECRET_KEY']
    client = Client(API_KEY, API_SECRET)

    order = client.order_market_buy(
        symbol=pair,
        quantity=quantity)

    return order

def cryptoX():
    
    #### PARAMETERS ####
    
    pairs = ['BTCEUR', 'ETHEUR', 'BNBEUR', 'XRPEUR']
    percentages = [50, 30, 10, 10]
    fiat = 100

    #### CALCULATIONS ####
    
    prices = get_prices(pairs)
    investment, quantities = calculate_quantity(fiat, percentages, prices)

    print('\n    | Price    | %  | €     | Quantity   ')
    print('----|----------|----|-------|------------')
    for i in range(len(pairs)):
        print('{:3s} | {:8.2f} | {:2.0f} | {:4.2f} | {:9.8f}'.format(
            pairs[i][:3], prices[i], percentages[i], investment[i], quantities[i]
        ))
    
    #### Order ####
    
    q = input('\nDo you want to place market orders with {:.2f}€? (y/n) '.format(fiat))

    if q == 'y':
        for i in range(len(pairs)):
            place_order(pairs[i], quantities[i])

    else:
        pass

if check_api_keys() == True:
    cryptoX()
else:
    print('API keys not found')
