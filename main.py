import time
from config import *
from modules.get_bal import balance
from modules.btc import *
from modules.sell_order import sell_order
from modules.buy_order import buy_new
from modules.get_all_order import all_orders
from modules.get_by_order_id import get_by_id
from modules.get_open_orders import open_orders
from modules.get_my_trades import get_my_trade
from modules.helper import *
from function import *


def init():
    # ===========Get current balance
    bal = str(balance())
    logger("Account Balance USDT:: " + bal)

    # ===========Get current price
    price = get_current_price()
    logger("Current " + symbol + " Price :: " + str(price))

    # ===========Validate==Daily==quota
    qdata = validate_quota(COIN1)

    # =====Fetch==buying and selling amount==
    jsonData = read_json()

    # execute buying and selling
    try:
        for i in jsonData:
            buy_orderId = i['buy_orderId']
            buy_price = i['buy_price']
            buy_status = i['buy_status']
            sell_orderId = i['sell_orderId']
            sell_price = i['sell_price']
            sell_status = i['sell_status']

            if not QUOTA_LIMIT:
                logger("Daily quota has exhausted.")
            elif float(bal) < float(BTC_PER_TRADE_QUOTA):
                logger("Account bal is low.")
            elif buy_status == 0:
                logger(" Going to Buy order " + str(buy_orderId) + " :: " + str(buy_price))
                isBuyResponse = buy_new(buy_price)
                logger(" "+str(COIN1)+",Buying price:"+str(buy_price)+",Quantity:"+str(BTC_PER_TRADE_QUOTA/buy_price)+", Order Buy  success :: OrderId:" + str(isBuyResponse['orderId']) + " Status:" + str(
                    isBuyResponse['status']))
                # ======Update==order buying data====
                newData = {"buy_status": 1, "buy_orderId": str(isBuyResponse['orderId']),
                           "buy_qty": str(isBuyResponse['origQty'])}
                i.update(newData)

                # =====Update Daily quota limit===
                total = qdata[0]['total']
                used = qdata[0]['used']
                qdata[0]['used'] = used + 500
                update_qdata(qdata)
                used = qdata[0]['used']
                remain = total - used
                print(qdata)
                logger("Daily Quota updated:: remaining quota is " + str(remain))

                time.sleep(1)

            if buy_status == 1:
                orderStatus = get_by_id(buy_orderId)
                if orderStatus['status'] == "FILLED":
                    newData = {"buy_status": 2}
                    i.update(newData)
                    logger("buying order successfully. Set to 2 for order id: " + str(buy_orderId))
                    time.sleep(1)
                elif orderStatus['status'] == "CANCELED":
                    newData = {"buy_status": 0, "buy_orderId": '', "buy_qty": ''}
                    i.update(newData)
                    logger("buying order reset to 0 for order id: " + str(buy_orderId))
                    time.sleep(1)
                else:
                    logger(
                        "buying status for order id: " + str(buy_orderId) + " is in progress. Current status is " + str(
                            orderStatus['status']))
                    time.sleep(1)

            if sell_status == 0 and buy_status == 2:
                qty = i['buy_qty']
                logger("Going to Sell order " + str(sell_orderId) + " :: " + str(sell_price))
                isSoldResponse = sell_order(sell_price, qty)
                order_id = isSoldResponse['orderId']
                status = isSoldResponse['status']
                logger(" "+str(COIN1)+",Selling price:"+str(sell_price)+",Quantity:"+str(qty)+"Order Sell success :: "
                                                                                              "OrderId: " + str(
                    order_id) + " Status: " + status)
                newData = {"sell_status": 1, "sell_orderId": str(isSoldResponse['orderId'])}
                i.update(newData)
                time.sleep(1)

            if sell_status == 1:
                orderStatus = get_by_id(sell_orderId)
                if orderStatus['status'] == "FILLED":
                    newData = {"buy_status": 0, "buy_orderId": '', "buy_qty": '', "sell_orderId": '', "sell_status": 0}
                    i.update(newData)
                    logger("Sell is completed for order id: " + str(sell_orderId) + ". Reset buy and sell status to 0")
                    time.sleep(1)
                elif orderStatus['status'] == "CANCELED":
                    newData = {"sell_status": 0}
                    i.update(newData)
                    logger(
                        "Sell order has been canceled for order id: " + str(sell_orderId) + ". Reset  sell status to 0")
                    time.sleep(1)
                else:
                    logger("Selling status for order id: " + str(
                        sell_orderId) + " is in progress. Current status is " + str(orderStatus['status']))
                    time.sleep(1)

            else:
                logger("Process Done...")
                time.sleep(1)

        update_json(jsonData)
        logger("Remaining  Balance USDT:: " + str(balance()))
        print("")
    except ValueError:
        logger("Something went wrong in execution, please check")


def mainloop():
    try:
        c = 0
        while c <= exe_count:
            logger("Executing buying and selling process...")
            init()
            time.sleep(6)
            c += 1
            if c == exe_count:
                break
    except ValueError:
        logger("Execution Terminated...")


if __name__ == "__main__":
    # mainloop()
    init()
    input("Press any key to exit...")
