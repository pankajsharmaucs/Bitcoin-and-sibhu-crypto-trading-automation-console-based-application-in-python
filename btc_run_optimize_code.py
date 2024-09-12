import time
from config import *
from modules.get_bal import balance
from modules.btc import get_current_price
from modules.sell_order import sell_order
from modules.buy_order import buy_new
from modules.get_all_order import all_orders
from modules.get_by_order_id import get_by_id
from modules.get_open_orders import open_orders
from modules.get_my_trades import get_my_trade
from modules.helper import read_json, update_json, validate_quota, update_qdata
from function import logger

def update_order_status(order, status_key, new_status, additional_data=None):
    """Update the order status and optionally add additional data."""
    update_data = {status_key: new_status}
    if additional_data:
        update_data.update(additional_data)
    order.update(update_data)

def process_buy_order(order, balance, quota_data):
    """Process a buy order."""
    buy_price = order['buy_price']
    if not QUOTA_LIMIT:
        logger("Daily quota has exhausted.")
        return
    if float(balance) < float(BTC_PER_TRADE_QUOTA):
        logger("Account balance is low.")
        return
    logger(f"Going to Buy order {order['buy_orderId']} :: {buy_price}")
    buy_response = buy_new(buy_price)
    qty = round(BTC_PER_TRADE_QUOTA / buy_price, 3)
    logger(f"{COIN1}, Buying price: {buy_price}, Quantity: {qty}, Order Buy success :: OrderId: {buy_response['orderId']} Status: {buy_response['status']}")
    update_order_status(order, 'buy_status', 1, {
        'buy_orderId': str(buy_response['orderId']),
        'buy_qty': str(buy_response['origQty'])
    })
    
    # Update daily quota
    total, used = quota_data['total'], quota_data['used']
    quota_data['used'] = used + 500
    update_qdata(quota_data)
    remain = total - quota_data['used']
    logger(f"Daily Quota updated:: remaining quota is {remain}")

def process_sell_order(order):
    """Process a sell order."""
    qty = order['buy_qty']
    sell_price = order['sell_price']
    logger(f"Going to Sell order {order['sell_orderId']} :: {sell_price}")
    sell_response = sell_order(sell_price, qty)
    logger(f"{COIN1}, Selling price: {sell_price}, Quantity: {qty}, Order Sell success :: OrderId: {sell_response['orderId']} Status: {sell_response['status']}")
    update_order_status(order, 'sell_status', 1, {
        'sell_orderId': str(sell_response['orderId'])
    })

def handle_order_status(order, order_type, status_key, order_id_key):
    """Handle the status of buy or sell orders."""
    order_id = order[order_id_key]
    if order_id:
        status_response = get_by_id(order_id)
        status = status_response['status']
        if status == "FILLED":
            logger(f"{order_type.capitalize()} order successfully. Set to 2 for order id: {order_id}")
            update_order_status(order, status_key, 2)
        elif status == "CANCELED":
            logger(f"{order_type.capitalize()} order reset to 0 for order id: {order_id}")
            update_order_status(order, status_key, 0, {
                order_id_key: '',
                'buy_qty' if order_type == 'buy' else 'sell_qty': ''
            })
        else:
            logger(f"{order_type.capitalize()} status for order id: {order_id} is in progress. Current status is {status}")

def init():
    """Initialize and execute trading operations."""
    try:
        bal = str(balance())
        logger(f"Account Balance USDT:: {bal}")
        price = get_current_price()
        logger(f"Current {symbol} Price :: {price}")

        quota_data = validate_quota(COIN1)
        json_data = read_json()

        for order in json_data:
            if order['buy_status'] == 0:
                process_buy_order(order, bal, quota_data)
                time.sleep(1)

            if order['buy_status'] == 1:
                handle_order_status(order, 'buy', 'buy_status', 'buy_orderId')
                time.sleep(1)

            if order['sell_status'] == 0 and order['buy_status'] == 2:
                process_sell_order(order)
                time.sleep(1)

            if order['sell_status'] == 1:
                handle_order_status(order, 'sell', 'sell_status', 'sell_orderId')
                time.sleep(1)

        update_json(json_data)
        logger(f"Remaining Balance USDT:: {balance()}")

    except ValueError:
        logger("Something went wrong in execution, please check")

def mainloop():
    """Main loop to execute trading operations multiple times."""
    try:
        for _ in range(exe_count):
            logger("Executing buying and selling process...")
            init()
            time.sleep(6)
    except ValueError:
        logger("Execution Terminated...")

if __name__ == "__main__":
    mainloop()
    input("Press any key to exit...")
