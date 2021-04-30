from requests import Request, Session
from binance.client import Client
from binance.enums import *
import json
import os

def check_api_keys():
    return 'CMC_API_KEY' in os.environ and 'BINANCE_API_KEY' in os.environ and 'BINANCE_SECRET_KEY' in os.environ

def request_fng():
    url = 'https://api.alternative.me/fng/'
    parameters = {
        'date_format': 'world'
    }
    headers = {
        'Accepts': 'application/json',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e

def process_fng(data):
    fng_value = int(data['data'][0]['value'])
    fng_classification = data['data'][0]['value_classification']
    return fng_value, fng_classification

def request_cmc(amount):
    API_KEY = os.environ['CMC_API_KEY']
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': str(amount),
        'convert': 'EUR'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e

def process_cmc(amount, data):
    symbols = []
    prices = []
    change30d = []

    for i in range(amount):
        symbols.append(data['data'][i]['symbol'])
        prices.append(float(data['data'][i]['quote']['EUR']['price']))
        change30d.append(
            float(data['data'][i]['quote']['EUR']['percent_change_30d']))

    return symbols, prices, change30d

def get_balance(assets):
    API_KEY = os.environ['BINANCE_API_KEY']
    API_SECRET = os.environ['BINANCE_SECRET_KEY']
    client = Client(API_KEY, API_SECRET)
    
    data = []
    balances = []
    
    for asset in assets:
        data.append(client.get_asset_balance(asset=asset))
    for i in range(len(assets)):
        balances.append(float(data[i]['free'])+float(data[i]['locked']))

    return balances

def calculate_value(balances, prices):
    values = []
    for i in range(len(balances)):
        values.append(balances[i] * prices[i])

    return values

def generate_pairs(symbols):
    pairs = []
    for i in range(len(symbols)):
        pairs.append(symbols[i]+'EUR')
    return pairs

def portfolio_percentage(X):
    fixed_percentages = [30, 20]    # Fixed percentages for BTC & ETH
    portfolio_percentages = fixed_percentages
    
    for i in range(X - len(fixed_percentages)):
        portfolio_percentages.append((100 - sum(fixed_percentages))/(X - len(fixed_percentages)))
    
    return portfolio_percentages

def calculate_quantity(fiat, percentages, prices):
    fiat_per_coin = []
    quantity = []
    for i in range(len(percentages)):
        fiat_per_coin.append(percentages[i]/100 * fiat)
    for i in range(len(fiat_per_coin)):
        quantity.append(fiat_per_coin[i] / prices[i])

    return fiat_per_coin, quantity
    
def create_order(pair, quantity):
    API_KEY = os.environ['BINANCE_API_KEY']
    API_SECRET = os.environ['BINANCE_SECRET_KEY']
    client = Client(API_KEY, API_SECRET)

    order = client.order_market_buy(
        symbol=pair,
        quantity=quantity)

    return order

# EXPORT ORDER TO FILE
# Import Symbole und Prozentwerte von datei dann nur das printen
# Only Track worth of Orders (not Binance Portfolio)
# Abfrage von Sparrate, die verteilt werden soll
 

def cryptoX():
    X = 8     # Amount of cryptocurrencies to work with

    fng_raw = request_fng()
    fng_value, fng_classification = process_fng(fng_raw)

    cmc_raw = request_cmc(X)
    symbols, prices, change = process_cmc(X, cmc_raw)

    balances = get_balance(symbols)
    values = calculate_value(balances, prices)
    
    balance_eur = get_balance(['EUR'])[0]
    portfolio_percentages = portfolio_percentage(X)
    fiat_per_coin, quantity = calculate_quantity(balance_eur, portfolio_percentages, prices)
    
    #### Output: Market & Account Data ####

    print('\n{:5s}| {:43s} | Investment Data (using {:6.2f}€)'.format('','Market & Account Data', balance_eur))
    print('{:5s}| {:8s} | {:6s} | {:12s} | {:8s} | {:6s} | {:8s} | {:12s}'.format('', 'Price[€]', '%[30d]', 'Balance', 'Value[€]', '[%]', '[€]', 'Quantity'))
    print('-----|----------|--------|--------------|----------|--------|----------|--------------')

    for i in range(X):
        print('{:4s} | {:8.2f} | {:6.2f} | {:12.8f} | {:8.2f} | {:6.2f} | {:8.2f} | {:12.8f}'.format(
            symbols[i], prices[i], change[i], balances[i], values[i], portfolio_percentages[i], fiat_per_coin[i], quantity[i])
            )

    print('\nCurrent Fear & Greed Index: {}, {:s}\n'.format(fng_value, fng_classification))

    #### Order ####
    
if check_api_keys() == True:
    cryptoX()
else:
    print('API keys not found')