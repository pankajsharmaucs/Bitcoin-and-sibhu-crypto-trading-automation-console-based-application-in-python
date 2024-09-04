import requests
import json
import hashlib
import hmac
import time
from config import *


def all_orders():
    order_url = '/api/v3/allOrders'

    # Generate a timestamp in milliseconds
    timestamp = int(time.time() * 1000)

    # Create the query string
    query_string = f'symbol={symbol}&timestamp={timestamp}'

    # Generate the signature
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Set the request headers
    headers = {
        'X-MBX-APIKEY': api_key
    }

    # Set the request payload
    payload = {
        'symbol': symbol,
        'timestamp': timestamp,
        'signature': signature
    }

    # Send the GET request to retrieve the order
    response = requests.get(base_url + order_url, headers=headers, params=payload)

    # Print the response
    print(response.json())


