[![Generic badge](https://img.shields.io/badge/license-Unlicense-green.svg)](https://shields.io/)

# DCA-Crypto

<div align="center">
	<br>
	<br>
	<img src="res/icon.png" width="200" height="200">
	<h1>DCA-Crypto</h1>
	<p>
    <b>Simple DCA script for cryptocurrency using the ccxt API.</b>
	</p>
	<br>
	<br>
	<br>
</div>

This simple script will invest, every day, a given quantity of money on the 
different currencies listed in a .json. These currencies 
can be weighted, and the investment put on each of them depends
on the performances of the assets during the day (i.e. the ones that perform the
best will have a smaller investment). 
The script is highly flexible to your needs, and will output daily 
records of your investment as a .csv file.

## Usage

### Your currencies

You have to modify the `currencies.json` file depending on
the objectives of your investment.
Each asset should be in the following format:

```json
"Asset name": {
    "symbol": "ASSETSYMBOL",
    "weight": X
},
```

Where:
- `X` is a number in [0, 1], s.t. the sum of the weights
  in the file is equal to 1.
- `"ASSETSYMBOL"` is the symbol that identifies the currency.


### The script

To perfom your daily investment, you have to execute the following
command once (and keep your computer on):

```bash
python dca.py $EXCHANGE $YOUR_API_KEY $YOUR_API_SECRET $DAILY_INVESTMENT $FIAT $FEES $HH
```

- `$EXCHANGE` defines the exchange that you want to use
  (the list of the available exchanges is available on 
  [ccxt](https://github.com/ccxt/ccxt)).
- `$YOUR_API_KEY` and `$YOUR_API_SECRET` are obtained on
  the exchange that you defined before, and can be obtained
  in its paremeters. 
- `$DAILY_INVESTMENT` defines your daily investment quantity.
- `$FIAT` defines the currency used to buy the assets defined
  in `currencies.json`. 
- `$FEES` corresponds to the amount deducted by the exchange
  on every transaction that you made (if you don't know how many
  they deduct, just put 0).
- `$HH` defines the hour at which the script will perform the
  investments.

Example for crypto.com/exchange, with 4% fees, using 20 USDT/day, 
and buying every day at 12:00:

```bash
python dca.py cryptocom XXXX ZZZZ 20 USDT 0.04 12
```

## Attributions

<div>
	Icon made by 
	<a href="https://www.flaticon.com/authors/flat-icons" title="Flat Icons">Monkik - Flat Icons</a> 
	from 
	<a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
	.
</div>
