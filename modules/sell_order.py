import requests
import json
import hashlib
import hmac
import time
from config import *
from modules.helper import *


def sell_order(price, quantity):
    order_url = '/api/v3/order'

    # Generate a timestamp in milliseconds
    timestamp = int(time.time() * 1000)

    # Order parameters
    side = 'SELL'
    type = 'LIMIT'
    time_in_force = 'GTC'
    # quantity = round(quantity, 3)

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

    # Print the response
    response_json = json.loads(response.content)

    #  response in log
    logger("Sell Order response  :: " + str(response.json()))

    logger_current("Sell Order response  :: " + str(response.json()))

    data = {
        "orderId": response_json['orderId'],
        "status": response_json['status'],
    }

    # Serializing json
    # json_object = json.dumps(data)
    return data
