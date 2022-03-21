import ccxt
import datetime 
import os
import pandas as pd 
import schedule
import sys
import time

from _global import *


def check_argv():
    if len(sys.argv) != 8:
        print("Error: format is - python dca.py $EXCHANGE $YOUR_API_KEY " 
              "$YOUR_API_SECRET $DAILY_INVESTMENT $FIAT $FEES $HH")
        exit()


def check_weights(df):
    if int(sum(df["weight"]) * 100) != 100:
        print("Error: the sum of the weights is not 1 (%f for %d tokens)." % 
                (sum(df["weight"]), len(df)))
        exit()


def create_output_dir():
    if not os.path.exists(PATH_OUTPUT):
        os.makedirs(PATH_OUTPUT)


def fetch_variation(symbol):
    print("Fetching variation\t%s" % symbol)
    return EXCHANGE.fetch_ticker("%s/%s" % (symbol, FIAT))["percentage"]


def fetch_price(symbol):
    print("Fetching price\t\t%s" % symbol)
    return EXCHANGE.fetch_ticker("%s/%s" % (symbol, FIAT))["bid"]


def place_purchase(symbol, amount):
    print("Purchasing\t\t%f %s" % (amount, symbol))
    EXCHANGE.create_market_buy_order("%s/%s" % (symbol, FIAT), amount)


def job():
    """
    Compute the purchase to be made, and place them on
    the market.
    """
    date = datetime.datetime.now()
    print("----------------------------------------------\n%s\n" % str(date))

    df = pd.read_json(PATH_INPUT).transpose()

    check_weights(df)

    df[COL_PRIC] = [fetch_price(symbol) for symbol in df[COL_SYMB]]
    df[COL_VAR1] = [fetch_variation(symbol) for symbol in df[COL_SYMB]]
    df[COL_VAR2] = df[COL_WEIG] * (df[COL_VAR1] + 100) 
    df[COL_PUR1] = df[COL_VAR2] / sum(df[COL_VAR2]) * TOTAL_PURCHASE
    df[COL_PUR2] = df[COL_PUR1].apply(lambda p: max(p, MIN_PURCHASE))
    df[COL_AMO1] = df[COL_PUR2] / df[COL_PRIC]
    df[COL_AMO2] = df[COL_AMO1] * (1 - FEES) 

    df.index.name = COL_NAME 
    df.drop(COL_VAR2, axis=1, inplace=True)
    df.to_csv("%s/%s.csv" % (PATH_OUTPUT, date.strftime(FORMAT_OUTPUT)))
    df.apply(lambda r: place_purchase(r["symbol"], r["amount NATIVE"]), axis=1)

    print(df.to_markdown())


def wait():
    """
    Infinite loop that waits for job to be executed.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    check_argv()

    # Total of the purchase to be made, in FIAT,
    # including the FEES.
    TOTAL_PURCHASE = float(sys.argv[4]) 
    FIAT = sys.argv[5]
    FEES = float(sys.argv[6])
    # Often, minimum purchase on a platform is 1ct / FEES
    # (depending on the number of decimal allowed).
    MIN_PURCHASE = 0.01 / FEES
    # Connect to the exchange.
    EXCHANGE = getattr(ccxt, sys.argv[1])({
        "apiKey": sys.argv[2],
        "secret": sys.argv[3],
        })

    create_output_dir()

    schedule.every().day.at(sys.argv[7] + ":00").do(job)
    wait()

