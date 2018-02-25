import requests, json

class Coinbene:
  def __init__(self, apiid=None, secret=None):
    self.apiid = apiid
    self.secret = secret
    self.publicURI = 'http://api.coinbene.com/v1/market'
    self.privateURI = 'http://api.coinbene.com/v1/trade'
    self.publicMethods = ['ticker', 'orderbook', 'trades']
    self.privateMethods = ['balance', 'order/place', 'order/info', 'order/cancel', 'order/open-orders']

  def createRequest(self, method, params):
    if method.lower() in self.publicMethods:
      url = f'{self.publicURI}/{method}?'
      for param in params:
        url += f'{param}={params[param]}&'
      url = url[:-1]
      r = json.loads(requests.get(url).text)
      return r
    elif method.lower() in self.privateMethods and self.apiid != None and self.secret != None:
      r = json.loads(requests.post(url).text)
      return r
    elif self.apiid == None or self.secret == None:
      return print('Error: Cannot use private methods without apiid and secret')
    else:
      return print(f'Error: Invalid Method ({method})')

  def getTicker(self, symbol):
    params = {
      'symbol': symbol.upper()
    }
    data = self.createRequest('ticker', params)
    return data

  def getOrderbook(self, symbol, depth=200):
    if depth < 1 or depth > 500:
      return print('Error: Depth must be in the range 1 to 500')
    params = {
      'symbol': symbol.upper(),
      'depth': depth
    }
    data = self.createRequest('orderbook', params)
    return data

  def getTrades(self, symbol, size=300):
    if size < 1 or size > 2000:
      return print('Error: Depth must be in the range 1 to 2000')
    params = {
      'symbol': symbol.upper(),
      'size': size
    }
    data = self.createRequest('trades', params)
    return data