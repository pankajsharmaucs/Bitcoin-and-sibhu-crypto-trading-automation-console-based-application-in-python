import requests


def get_current_price():
    url1 = "https://testnet.binance.vision/api/v3/ticker/price?symbol=BTCUSDT"
    res = requests.get(url1)
    data = res.json()
    price = float(data['price'])
    return price
