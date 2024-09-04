import requests
import json
import hashlib
import hmac
import time
from config import *


def get_my_trade():
    order_url = '/api/v3/myTrades'
    # Generate a timestamp in milliseconds
    timestamp = int(time.time() * 1000)

    # Create the query string
    query_string = f'symbol={symbol}&timestamp={timestamp}'

    # Generate the signature
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Set the request payload
    payload = {
        'symbol': symbol,
        'timestamp': timestamp,
        'signature': signature
    }

    # Send the GET request to retrieve the order
    response = requests.get(base_url + order_url, headers=headers, params=payload)

    # Print the response
    print(" my trade "+str(response.json()))
