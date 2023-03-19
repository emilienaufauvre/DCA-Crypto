import ccxt
import datetime 
import os
import pandas as pd 
import schedule
import sys
import time
import numpy as np

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


def fetch_info(symbol):
    print("Fetching informations\t%s" % symbol)
    return EXCHANGE.fetch_ticker("%s/%s" % (symbol, FIAT))


def place_purchase(symbol, amount):
    print("Purchasing\t\t%f %s" % (amount, symbol))
    EXCHANGE.create_market_buy_order("%s/%s" % (symbol, FIAT), amount)


def job():
    """
    Compute the purchases to be made, and place them on
    the market.
    """
    date = datetime.datetime.now()
    print("----------------------------------------------\n%s\n" % str(date))

    df = pd.read_json(PATH_INPUT).transpose()
    check_weights(df)

    info = [fetch_info(s) for s in df[COL_SYMB]]

    df[COL_PRIC] = [float(i["info"][0]["a"]) for i in info]
    df[COL_VAR1] = [float(i["info"][0]["c"]) for i in info]
    df[COL_VAR2] = df[COL_WEIG]#df[COL_VAR1] * df[COL_WEIG] - 100 
    df[COL_PUR1] = df[COL_VAR2] / sum(df[COL_VAR2]) * TOTAL_PURCHASE
    df[COL_PUR2] = np.maximum(df[COL_PUR1], (df[COL_MINI] * df[COL_PRIC]))
    df[COL_AMO1] = df[COL_PUR2] / df[COL_PRIC]
    df[COL_AMO2] = df[COL_AMO1] * (1 - FEES) 

    df.index.name = COL_NAME 
    df.drop(COL_VAR2, axis=1, inplace=True)

    for i, r in df.iterrows():
        try:
            # Buy the currency using the computed values.
            place_purchase(r[COL_SYMB], r[COL_AMO1])
        except Exception as e:
            print(e)
            # No assets bought.
            df.loc[i, [COL_PUR2]] = 0
            df.loc[i, [COL_AMO1]] = 0
            df.loc[i, [COL_AMO2]] = 0

    df.to_csv("%s/%s.csv" % (PATH_OUTPUT, date.strftime(FORMAT_OUTPUT)))
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
    # Connect to the exchange.
    EXCHANGE = getattr(ccxt, sys.argv[1])({
        "apiKey": sys.argv[2],
        "secret": sys.argv[3],
        })

    create_output_dir()

    job()
    schedule.every().day.at(sys.argv[7] + ":00").do(job)
    wait()

