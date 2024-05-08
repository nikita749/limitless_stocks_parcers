import json
import os

from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from configuration import *


def open_browser(url):
  options = Options()
  options.add_experimental_option("detach", True)

  browser = webdriver.Chrome(options=options)
  browser.get(url)

  return browser

def save_to_file(is_file, data):
  if (is_file):
    with open(os.path.join(os.getcwd(), "outputs", is_file), "w", encoding="UTF-8") as file_writer:
      json.dump(data, file_writer, indent=4)


class Binance:
  def __init__(self, url_api):
    self.url_api = url_api


  def BinanceParse(self, is_file=False):
    result = json.loads(urlopen(self.url_api).read())

    accepted_prefix = "USDT"
    output_data = {}
    for el in result:
      if (accepted_prefix in el["symbol"]):
        formated_currency = el["symbol"].replace(accepted_prefix, "").lower()

        if (formated_currency in accepted_cryptoCurrencies):
          output_data[formated_currency] = float(el["price"])

    save_to_file(is_file, output_data)

    return output_data


class HTX:
  def __init__(self, browser, fetch_script):
    self.browser = browser
    self.fetch_script = fetch_script


  def HTXParse(self, is_file=False):
    result = self.browser.execute_script(self.fetch_script)

    output_data = {}
    for i in result["data"][0]["singleList"]:
      formated_currency = i["baseCurrency"]
      if (formated_currency in accepted_cryptoCurrencies):
        output_data[formated_currency] = float(i['price'])

    save_to_file(is_file, output_data)

    return output_data


class ByBit:
  def __init__(self, browser, fetch_script):
    self.browser = browser
    self.fetch_script = fetch_script


  def ByBitParce(self, is_file=False):
    result = self.browser.execute_script(self.fetch_script)

    accepted_prefixe = "USDT"
    output_data = {}
    for key, value in result["result"].items():
      if (accepted_prefixe in key):
        formated_currency = key.replace(accepted_prefixe, "").lower()

        if (formated_currency in accepted_cryptoCurrencies):
          output_data[formated_currency] = float(value[-1]['c'])

    save_to_file(is_file, output_data)

    return output_data

class KuCoin:
  def __init__(self, browser, fetch_script):
    self.browser = browser
    self.fetch_script = fetch_script

  def KuCoinParse(self, is_file=False):
    result = self.browser.execute_script(self.fetch_script)

    output_data = {}

    for key, value in result["data"].items():
      formated_currency = key.lower()

      if (formated_currency in accepted_cryptoCurrencies):
        output_data[formated_currency] = float(value)

    save_to_file(is_file, output_data)

    return output_data

class OKX:
  def __init__(self, browser, fetch_script):
    self.browser = browser
    self.fetch_script = fetch_script

  def OkxParse(self, is_file=False):
    result = self.browser.execute_script(self.fetch_script)

    output_data = {}

    for i in result["data"]['list']:
      formated_currency = i['project'].lower()

      if (formated_currency in accepted_cryptoCurrencies):
        output_data[formated_currency] = float(i['last'])

    save_to_file(is_file, output_data)

    return output_data