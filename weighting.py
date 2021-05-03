from requests import Request, Session
import json, os

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
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e

    symbols = []
    market_caps = []

    for i in range(amount):
        symbols.append(data['data'][i]['symbol'])
        market_caps.append(int(data['data'][i]['quote']['EUR']['market_cap']))

    return symbols, market_caps

X = 2

symbols, market_caps = request_cmc(X)
percentages = []

for cap in market_caps:
    percentages.append(100 * cap / sum(market_caps))

for i in range(X):
    print('{:4s}| {:13.0f}€ | {:5.2f}'.format(symbols[i], market_caps[i], percentages[i]))


# https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeQuotesLatest noch absolutes Market Cap % einführen