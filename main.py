import datetime as dt
import json

import requests

debug = False


# get history
def get_history(url, symbol, interval, start, end):
    par = {'symbol': symbol, 'interval': interval, 'startTime': start, 'endTime': end}
    data = json.loads(requests.get(url, params=par).text)
    return data


# get max price
def get_max_price(data):
    max_price = 0
    for i in data:
        if float(i[2]) > max_price:
            max_price = float(i[2])
    return max_price


# get current price
def get_current_price(url, symbol):
    par = {'symbol': symbol}
    data = json.loads(requests.get(url, params=par).text)
    return data['price']


# calculate profit
def calc_profit(max_price, current_price):
    return (float(current_price) - float(max_price)) / float(max_price) * 100


def main():
    url_history = 'https://api.binance.com/api/v3/klines'  # url for history
    url_current = 'https://api.binance.com/api/v3/ticker/price'  # url for current price
    symbol = 'XRPUSDT'  # symbol
    interval = '1m'  # interval for history

    # loop for getting data
    while (True):
        start = str(int(dt.datetime.now().timestamp() * 1000) - 60 * 60 * 1000)  # 1 hour ago
        end = str(int(dt.datetime.now().timestamp() * 1000))  # current time
        max_price = get_max_price(get_history(url_history, symbol, interval, start, end))
        current_price = get_current_price(url_current, symbol)
        profit = calc_profit(max_price, current_price)
        if debug:
            print(f'Max price: {max_price}, Current price: {current_price}, Profit: {profit}%')
        if abs(profit) > 1:
            print(f'The price has changed by more than 1 percent! \nMax price: {max_price}, '
                  f'Current price: {current_price}, Profit: {profit}%')


if __name__ == '__main__':
    main()
