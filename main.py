import threading

from Stocks import *


binance = Binance("https://api.binance.com/api/v3/ticker/price")
bybit = ByBit(open_browser("https://www.bybit.com/ru-RU/"), open("fetch_scripts/bybit_fetch.txt", "r").read())
htx = HTX(open_browser("https://www.htx.com/ru-ru/markets/"), open("fetch_scripts/htx_fetch.txt", "r").read())
kucoin = KuCoin(open_browser("https://www.kucoin.com/ru/markets"), open("fetch_scripts/kucoin_fetch.txt", "r").read())
okx = OKX(open_browser("https://www.okx.com/ru/markets/prices"), open("fetch_scripts/okx_fetch.txt", "r").read())


def binance_thread():
  binance_data = binance.BinanceParse(is_file="binance_output.json")

def bybit_thread():
  bybit_data = bybit.ByBitParce(is_file="bybit_output.json")

def htx_thread():
  htx_data = htx.HTXParse(is_file="htx_output.json")

def kucoin_thread():
  kucoin_data = kucoin.KuCoinParse(is_file="kucoin_output.json")

def okx_thread():
  okx_data = okx.OkxParse(is_file="okx_output.json")


threading.Thread(target=binance_thread).start()
threading.Thread(target=bybit_thread).start()
threading.Thread(target=htx_thread).start()
threading.Thread(target=kucoin_thread).start()
threading.Thread(target=okx_thread).start()
