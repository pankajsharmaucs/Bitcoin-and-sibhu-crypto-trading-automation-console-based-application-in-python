import requests
import json
import hashlib
import hmac
import time
from config import *


def balance():
    order_url = '/api/v3/account'
    # Generate a timestamp in milliseconds
    timestamp = int(time.time() * 1000)

    # Create the query string
    query_string = f'timestamp={timestamp}'

    # Generate the signature
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Set the request payload
    payload = {
        'timestamp': timestamp,
        'signature': signature
    }

    # Send the GET request to retrieve the order
    response = requests.get(base_url + order_url, headers=headers, params=payload)

    # Parse the response JSON
    response_json = json.loads(response.content)

    # Find the USDT balance in the response
    usdt_balance = None
    for asset in response_json['balances']:
        if asset['asset'] == 'USDT':
            usdt_balance = asset['free']
            break

    return usdt_balance

    # if usdt_balance is None:
    #     print('Could not find USDT balance in account.')
    # else:
    #     print(f'USDT balance: {usdt_balance}')


