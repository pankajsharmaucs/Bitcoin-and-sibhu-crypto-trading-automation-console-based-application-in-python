from config import *
import json
from datetime import datetime
from datetime import date

# sell_order(price)
# all_orders()
# orderId = '11130238'
# get_by_id(orderId)
# buy_new(price)
# open_orders()
# get_my_trade()


def read_json():
    f = open('files/' + BTC_JSON + '.json')
    data = json.load(f)
    f.close()
    return data


def update_json(data):
    with open('files/' + BTC_JSON + '.json', 'w') as f:
        json.dump(data, f)


def validate_quota(COIN):
    f = open('files/' + QUOTA_FILE + '.json')
    qdata = json.load(f)
    f.close()

    # get current date
    now = datetime.now()
    # format date into year-month-day format
    current_date = now.strftime('%Y-%m-%d')

    total = ''
    used = ''
    trade_date = '2023-04-01'
    trade_date = datetime.strptime(trade_date, '%Y-%m-%d').date()

    if COIN == COIN1:
        total = qdata[0]['total']
        used = qdata[0]['used']
        trade_date = qdata[0]['trade_date']
    if COIN == COIN2:
        total = qdata[1]['total']
        used = qdata[1]['used']
        trade_date = qdata[1]['trade_date']

    if trade_date < current_date:
        trade_date = current_date
        if COIN == COIN1:
            qdata[0]['trade_date'] = current_date
            qdata[0]['used'] = 0
        elif COIN == COIN2:
            qdata[1]['trade_date'] = current_date
            qdata[1]['used'] = 0
        with open('files/' + QUOTA_FILE + '.json', 'w') as f:
            json.dump(qdata, f)

    remain = total - used
    if remain < BTC_PER_TRADE_QUOTA:
        QUOTA_LIMIT = False
    else:
        QUOTA_LIMIT = True
    return qdata


def update_qdata(qdata):
    with open('files/' + QUOTA_FILE + '.json', 'w') as f:
        json.dump(qdata, f)
