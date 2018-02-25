import requests, json, math, time, hashlib

class Coinbene:
  def __init__(self, apiid=None, secret=None, debug=False):
    self.apiid = apiid
    self.secret = secret
    self.publicURI = 'http://api.coinbene.com/v1/market'
    self.privateURI = 'http://api.coinbene.com/v1/trade'
    self.publicMethods = ['ticker', 'orderbook', 'trades']
    self.privateMethods = ['balance', 'order/place', 'order/info', 'order/cancel', 'order/open-orders']
    self.debug = debug


  def createRequest(self, method, params):
    if method.lower() in self.publicMethods:
      url = f'{self.publicURI}/{method}?'
      for param in params:
        url += f'{param}={params[param]}&'
      url = url[:-1]
      if self.debug: print('\ncreateRequest().url =>', url)
      r = json.loads(requests.get(url).text)
      return r
    elif method.lower() in self.privateMethods and self.apiid != None and self.secret != None:
      url = f'{self.privateURI}/{method}?'
      for param in params:
        url += f'{param}={params[param]}&'
      url = url[:-1]
      if self.debug: print('\ncreateRequest().url =>', url)
      r = json.loads(requests.post(url).text)
      return r
    elif self.apiid == None or self.secret == None:
      return print('Error: Cannot use private methods without apiid and secret')
    else:
      return print(f'Error: Invalid Method ({method})')

  def getTimestamp(self):
    t = math.floor(time.time()*1000)
    if self.debug: print('\ngetTimestamp() =>', t)
    return t

  def generateSignature(self, params):
    sign = ''
    params['secret'] = self.secret
    sortedKeys = sorted(params)
    for key in sortedKeys:
      sign += f'{key}={params[key]}&'
    sign = sign.upper()[:-1].encode('utf-8')
    if self.debug: print('\ngenerateSignature() =>', sign)
    return hashlib.md5(sign).hexdigest()

  def getTicker(self, symbol):
    params = {
      'symbol': symbol.upper()
    }
    data = self.createRequest('ticker', params)
    return data

  def getAsk(self, symbol):
    return float(self.getTicker(symbol)['ticker'][0]['ask'])

  def getBid(self, symbol):
    return float(self.getTicker(symbol)['ticker'][0]['bid'])

  def getAskBid(self, symbol):
    ticker = self.getTicker(symbol)['ticker'][0]
    return [float(ticker['ask']), float(ticker['bid'])]

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

  def getBalances(self):
    params = {
      'account': 'exchange',
      'apiid': self.apiid,
      'timestamp': self.getTimestamp(),
    }
    params['sign'] = self.generateSignature(params)

    if self.debug: print('\ngetBalance().params =>', params)
    data = self.createRequest('balance', params)
    return data['balance']

  def getBalance(self, coin):
    balances = self.getBalances()
    return [i for i in balances if i['asset'] == coin.upper()][0]
  
  def getAvailableBalance(self, coin):
    return float(self.getBalance(coin)['available'])

  def placeOrder(self, price, quantity, symbol, type):
    params = {
      'apiid': self.apiid,
      'price': price,
      'quantity': quantity,
      'symbol': symbol,
      'type': type,
      'timestamp': self.getTimestamp()
    }
    params['sign'] = self.generateSignature(params)

    if self.debug: print('\nplaceOrder().params =>', params)
    data = self.createRequest('order/place', params)
    return data

  def limitBuy(self, price, quantity, symbol):
    data = self.placeOrder(price, quantity, symbol, 'buy-limit')
    return data

  def limitSell(self, price, quantity, symbol):
    data = self.placeOrder(price, quantity, symbol, 'sell-limit')
    return data

  