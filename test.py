# import time
#
# n=input(" Please type your name : ")
#
# print("welcome to Binance Api Automation "+n)
#
# exit_now = input("Do you like to exit now (Y)es (N)o  ? ")
#
# if exit_now.lower() == 'n':
#     print("Bye Bye")
#     time.sleep(2)
# else:
#     time.sleep(100)

from config import *

from modules.btc import *

print(get_current_price())