from requests import Request, Session
from binance.client import Client
from binance.enums import *
from math import log10
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

def get_balance(asset):
    API_KEY = os.environ['BINANCE_API_KEY']
    API_SECRET = os.environ['BINANCE_SECRET_KEY']
    client = Client(API_KEY, API_SECRET)

    balance = client.get_asset_balance(asset=asset)
    return float(balance['free'])

def calculate_quantity(fiat, percentages, prices, decimal_places):
    fiat_per_coin = []
    quantity = []
    for i in range(len(percentages)):
        fiat_per_coin.append(percentages[i] / 100 * fiat)
    for i in range(len(fiat_per_coin)):
        quantity.append(round(fiat_per_coin[i] / prices[i], decimal_places[i]))

    return fiat_per_coin, quantity
    
def place_order(pair, quantity):
    API_KEY = os.environ['BINANCE_API_KEY']
    API_SECRET = os.environ['BINANCE_SECRET_KEY']
    client = Client(API_KEY, API_SECRET)

    order = client.order_market_buy(
        symbol=pair,
        quantity=quantity)

    return order

def get_decimal_places(pairs):
    API_KEY = os.environ['BINANCE_API_KEY']
    API_SECRET = os.environ['BINANCE_SECRET_KEY']
    client = Client(API_KEY, API_SECRET)
    
    decimal_places=[]
    
    for pair in pairs:
        info = client.get_symbol_info(pair)
        minQty = float(info['filters'][2]['minQty'])
        stepSize = float(info['filters'][2]['stepSize'])
        decimal_places.append(int(-log10(stepSize)))
    
    return decimal_places

def get_minQty(pairs):
    API_KEY = os.environ['BINANCE_API_KEY']
    API_SECRET = os.environ['BINANCE_SECRET_KEY']
    client = Client(API_KEY, API_SECRET)

    minQties = []
    for pair in pairs:
        info = client.get_symbol_info(pair)
        minQty = float(info['filters'][2]['minQty'])
        minQties.append(minQty)
        print(info)

    return minQties

def cryptoX():
    
    #### PARAMETERS ####
    
    pairs = ['BTCEUR', 'ETHEUR', 'BNBEUR', 'XRPEUR']
    percentages = [50, 30, 10, 10] # vielleicht noch was mit der Marktkapitalisierung der einzelnen Coins berechnen
    fiat = 100

    # Problem: 'minNotional': '10.00000000' -- Order für 10€ geht nicht durch - müsste evtl minimal erhöht werden

    #### CALCULATIONS ####
    
    prices = get_prices(pairs)
    decimal_places = get_decimal_places(pairs)
    investment, quantities = calculate_quantity(fiat, percentages, prices, decimal_places)
    fiat_available = get_balance('EUR')

    print('\n    | Price    | %  | €     | Quantity   ')
    print('----|----------|----|-------|------------')
    for i in range(len(pairs)):
        print('{:3s} | {:8.2f} | {:2.0f} | {:5.2f} | {:9.8f} '.format(
            pairs[i][:3], prices[i], percentages[i], investment[i], quantities[i]
        ))
    print('\nAvailable: {:.2f}€'.format(fiat_available))
    print(get_minQty(pairs))
    #### ORDER ####
    
    q = input('\nDo you want to place market orders with {:.2f}€? (y/n) '.format(fiat))

    if q == 'y':
        for i in range(len(pairs)):
           print(place_order(pairs[i], quantities[i]))
            # Soll noch in Datei exportiert werden
    else:
        pass

if check_api_keys() == True:
    cryptoX()
else:
    print('API keys not found')
