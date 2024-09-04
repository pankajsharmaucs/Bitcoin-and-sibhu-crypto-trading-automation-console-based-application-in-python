import requests
import json
import hashlib
import hmac
import time
from config import *


def get_by_id(orderId):

    # Binance API endpoint URLs
    order_url = '/api/v3/order'

    # Generate a timestamp in milliseconds
    timestamp = int(time.time() * 1000)

    # Create the query string
    query_string = f'symbol={symbol}&orderId={orderId}&timestamp={timestamp}'

    # Generate the signature
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Set the request headers
    headers = {
        'X-MBX-APIKEY': api_key
    }

    # Set the request payload
    payload = {
        'symbol': symbol,
        'orderId': orderId,
        'timestamp': timestamp,
        'signature': signature
    }

    # Send the GET request to retrieve the order
    response = requests.get(base_url + order_url, headers=headers, params=payload)

    # logger("Buy Order response  :: " + response.json())

    response_json = json.loads(response.content)
    data = {
        "orderId": response_json['orderId'],
        "status": response_json['status'],
    }

    return data
