import ccxt
import datetime 
import pandas as pd 
import schedule
import sys
import time


def check_api_keys():
    if len(sys.argv) != 3:
        print("Error: you should pass API key and secret.") 
        exit()


def check_weights(df):
    if int(sum(df["weight"]) * 100) != 100:
        print("Error: the sum of the weights is not 1 (%f for %d tokens)." % 
                (sum(df["weight"]), len(df)))
        exit()


def fetch_variation(symbol):
    print("Fetching variation\t%s" % symbol)
    return cryptocom.fetch_ticker("%s/%s" % (symbol, FIAT))["percentage"]


def fetch_price(symbol):
    print("Fetching price\t\t%s" % symbol)
    return cryptocom.fetch_ticker("%s/%s" % (symbol, FIAT))["bid"]


def place_purchase(symbol, amount):
    print("Purchasing\t\t%f %s" % (amount, symbol))
    cryptocom.create_market_buy_order("%s/%s" % (symbol, FIAT), amount)


def job():
    """
    Compute the purchase to be made, and place them on
    the market.
    """
    date = datetime.datetime.now()
    print("----------------------------------------------\n%s\n" % str(date))

    df = pd.read_json(PATH).transpose()
    check_weights(df)

    df["price    FIAT"] = [fetch_price(symbol) for symbol in df["symbol"]]
    df["variation   %"] = [fetch_variation(symbol) for symbol in df["symbol"]]
    df["variation bis"] = df["variation   %"] * df["weight"] + CENTER 
    df["purchase FIAT"] = df["variation bis"] / df["variation bis"].sum() * TOTAL_PURCHASE
    df["purchase real"] = df["purchase FIAT"].apply(lambda p: max(p, MIN_PURCHASE))
    df["amount NATIVE"] = df["purchase real"] / df["price    FIAT"]
    df["amount real  "] = df["amount NATIVE"] * (1 - FEES) 

    df.to_csv("%s.csv" % date.strftime("dca_%d_%m_%Y__%H_%M_%S"))
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
    # Total of the purchase to be made, in FIAT,
    # including the FEES.
    TOTAL_PURCHASE = 12.5 
    FIAT = "USDT"
    FEES = 0.04
    # Often, minimum purchase on the platform is 1ct / FEES
    # (depending on the number of decimal allowed).
    MIN_PURCHASE = 0.01 / FEES
    # The currencies to buy, and their weight.
    PATH = "currencies.json"
    # To center the final weight.
    CENTER = -100

    check_api_keys()
    cryptocom = ccxt.cryptocom({
        "apiKey": sys.argv[1],
        "secret": sys.argv[2],
        })
    job()
    schedule.every().day.at("12:00").do(job)
    wait()

