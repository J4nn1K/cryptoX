from requests import Request, Session
import json
import os

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
        prices.append(data['data'][i]['quote']['EUR']['price'])
        change30d.append(data['data'][i]['quote']['EUR']['percent_change_30d'])
    
    return symbols, prices, change30d

def generate_pairs(symbols):
    pairs = []
    for i in range(len(symbols)):
        pairs.append(symbols[i]+'EUR')
    return pairs

def cryptoX():
    X = 12     # Amount of Cryptocurrencies to fetch

    fng_raw = request_fng()
    fng_value, fng_classification= process_fng(fng_raw)
    
    cmc_raw = request_cmc(X)
    symbols, prices, change = process_cmc(X, cmc_raw)
    
    # ---- Output ---- 

    print('\n{:5s}|{:9s}|{:13s}'.format('',' Price[€]',' %[30d]'))
    print('-----|---------|---------')
    
    for i in range(X):
        print('{:5s}|{:9.2f}|{:7.2f}'.format(symbols[i], prices[i], change[i]))
    
    print('\nCurrent Fear & Greed Index: {}, {:s}\n'.format(fng_value, fng_classification))

    # ---- Tests ----

    # print(generate_pairs(symbols))

cryptoX() 

