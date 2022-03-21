# DCA-Crypto

This simple script will invest a given quantity of money on the 
different currencies listed in a .json, everyday. These currencies 
can be weighted, and the investment put on each of them everyday depends
on the performances of the assets (i.e. the ones that perform the
best will have a smaller investment). 

## Usage

You have to modify the `currencies.json` file depending on
the objectives of your investment.

```bash
python dca.py $EXCHANGE $YOUR_API_KEY $YOUR_API_SECRET $DAILY_INVESTMENT $FIAT $FEES $HH
```

- `$YOUR_API_KEY` and `$YOUR_API_SECRET` are obtained 
  on the exchange that you want to use (i.e. `$EXCHANGE`). 
- The list of the available exchanges is available on [ccxt](https://github.com/ccxt/ccxt)
- The script will buy the currencies in `currencies.json` 
  using the `$FIAT` currency.
- The amount invested in `$FIAT` is equals to `$DAILY_INVESTMENT`.
- `$FEES` corresponds to the amount deducted by the exchange
  on every transaction that you made (if you don't know how many
  they deduct, just put 0).
- Everyday, this amount is invested at the hour defined
  with `$HH` (24h system).

Example for crypto.com/exchange, with 4% fees, using 20 USDT/day, 
and buying at 12:00:

```bash
python dca.py cryptocom XXXX ZZZZ 20 USDT 0.04 12
```
