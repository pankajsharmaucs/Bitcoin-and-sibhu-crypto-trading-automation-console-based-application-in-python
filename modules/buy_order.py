import requests
import json
import hashlib
import hmac
import time
from config import *
from modules.helper import *


def buy_new(price):
    order_url = '/api/v3/order'

    # Generate a timestamp in milliseconds
    timestamp = int(time.time() * 1000)

    quantity = BTC_PER_TRADE_QUOTA / price

    # Order parameters
    side = 'BUY'
    type = 'LIMIT'
    time_in_force = 'GTC'
    # quantity = '0.01'
    quantity = round(quantity, 3)

    # Create the query string
    query_string = f'symbol={symbol}&side={side}&type={type}&timeInForce={time_in_force}&quantity={quantity}&price={price}&timestamp={timestamp}'

    # Generate the signature
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Set the request payload
    payload = {
        'symbol': symbol,
        'side': side,
        'type': type,
        'timeInForce': time_in_force,
        'quantity': quantity,
        'price': price,
        'timestamp': timestamp,
        'signature': signature
    }

    # Send the POST request to create the order
    response = requests.post(base_url + order_url, headers=headers, params=payload)

    #  response in log
    logger("Buy Order response  :: " + str(response.json()))

    logger_current("Buy Order response  :: " + str(response.json()))

    response_json = json.loads(response.content)
    data = {
        "orderId": response_json['orderId'],
        "status": response_json['status'],
        "origQty": response_json['origQty'],
    }

    return data
