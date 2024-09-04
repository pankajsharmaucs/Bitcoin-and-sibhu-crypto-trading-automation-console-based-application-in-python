
import os
from datetime import datetime


def logger(log_data):
    now = str(datetime.now())
    log_string=now + " " + str(log_data)
    print(log_string)

    c = datetime.now()
    current_date = c.strftime('%Y-%m-%d')

    log_folder = 'logs/'+current_date
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_filename = 'btc.log'

    with open(os.path.join(log_folder, log_filename), 'a') as log_file:
        log_file.write(log_string + '\n')


def logger_current(log_data):
    now = str(datetime.now())
    log_string=now + " " + str(log_data)
    print(log_string)

    c = datetime.now()
    current_date = c.strftime('%Y-%m-%d')

    log_folder = 'logs/'+current_date
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_filename = 'current.log'

    with open(os.path.join(log_folder, log_filename), 'a') as log_file:
        log_file.write(log_string + '\n')
