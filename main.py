import threading

from Stocks import *
from configuration import *

import keyboard
from datetime import datetime

from time import sleep


binance = Binance("https://api.binance.com/api/v3/ticker/price")
bybit = ByBit(open_browser("https://www.bybit.com/ru-RU/"), open("fetch_scripts/bybit_fetch.txt", "r").read())
htx = HTX(open_browser("https://www.htx.com/ru-ru/markets/"), open("fetch_scripts/htx_fetch.txt", "r").read())
kucoin = KuCoin(open_browser("https://www.kucoin.com/ru/markets"), open("fetch_scripts/kucoin_fetch.txt", "r").read())
okx = OKX(open_browser("https://www.okx.com/ru/markets/prices"), open("fetch_scripts/okx_fetch.txt", "r").read())


print("%Browsers are Ready\n")

class Analyzer:
  def __init__(self):
    self.total_data = {}

    self.end_threader = 0


  def analyse(self):
    return_data = []

    for currency, market_data in self.total_data.items():
      if (len(market_data) > 1):
        prices, markets = list(market_data.values()), list(market_data.keys())
        min_price, max_price = min(prices), max(prices)

        if (min_price != max_price):
          return_data.append({"market_buy": markets[prices.index(min_price)], "market_sell": markets[prices.index(max_price)], "currency": currency, "price_buy": min_price, "price_sell": max_price})

    return return_data

  def total_data_filler(self, data, market):
    for currency, price in data.items():
      self.total_data[currency][market] = price

  def total_data_initialisation(self):
    for crypto_currency in accepted_cryptoCurrencies:
      self.total_data[crypto_currency] = {}

analyzer = Analyzer()
analyzer.total_data_initialisation()

def binance_thread():
  time_start = datetime.now()

  binance_data = binance.BinanceParse(is_file="binance_output.json" if (to_file) else False)
  analyzer.total_data_filler(binance_data, "binance")

  analyzer.end_threader += 1

  print(f"Binance - {(datetime.now() - time_start)}")

def bybit_thread():
  time_start = datetime.now()

  bybit_data = bybit.ByBitParce(is_file="bybit_output.json" if (to_file) else False)
  analyzer.total_data_filler(bybit_data, "bybit")

  analyzer.end_threader += 1

  print(f"ByBit - {(datetime.now() - time_start)}")

def htx_thread():
  time_start = datetime.now()

  htx_data = htx.HTXParse(is_file="htx_output.json" if (to_file) else False)
  analyzer.total_data_filler(htx_data, "htx")

  analyzer.end_threader += 1

  print(f"HTX - {(datetime.now() - time_start)}")

def kucoin_thread():
  time_start = datetime.now()

  kucoin_data = kucoin.KuCoinParse(is_file="kucoin_output.json" if (to_file) else False)
  analyzer.total_data_filler(kucoin_data, "kucoin")

  analyzer.end_threader += 1

  print(f"Kukoin - {(datetime.now() - time_start)}")

def okx_thread():
  time_start = datetime.now()

  okx_data = okx.OkxParse(is_file="okx_output.json" if (to_file) else False)
  analyzer.total_data_filler(okx_data, "okx")

  analyzer.end_threader += 1

  print(f"OKX - {(datetime.now() - time_start)}")



while True:
  if (keyboard.is_pressed("q")):
    print("Parsing\n\n")

    time_start = datetime.now()
    threading.Thread(target=binance_thread).start()
    threading.Thread(target=bybit_thread).start()
    threading.Thread(target=htx_thread).start()
    threading.Thread(target=kucoin_thread).start()
    threading.Thread(target=okx_thread).start()

    print(f"\n\nThreading Time - {datetime.now() - time_start}\n")

    while True:
      if (analyzer.end_threader == 5):
        save_to_file(is_file="total_data.json", data=analyzer.total_data)

        print("All Benefit Transactions:")
        for transaction in analyzer.analyse():
          print(transaction)

        analyzer.total_data_initialisation()
        analyzer.end_threader = 0

        break

    print(f"\nTotal Time - {datetime.now() - time_start}")
    sleep(5)