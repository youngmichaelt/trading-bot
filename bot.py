import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import time
import talib

class Bot:



    def bot():
        intrade = 0
        i = 0
        prices = []
        total = 0

        while i < 1:
            symbol = 'VET/BTC'

            exchange = ccxt.binance()

            timeframe = '1m'
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
            df = pd.DataFrame(ohlcv, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
            df['date'] = pd.to_datetime(df['date'], unit='ms')

            market = exchange.fetch_tickers(symbol)
            price = market[symbol]['bid']
            print('')
            print('Price: ', price)

            upper, middle, lower = talib.BBANDS(df.close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

            macd, macdsignal, macdhist = talib.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)

            lowerClose = (df.low.iloc[-1] - lower.iloc[-1]) / lower.iloc[-1] * 100
            upperClose = (df.low.iloc[-1] - upper.iloc[-1]) / upper.iloc[-1] * 100

            if (df.low.iloc[-1] <= lower.iloc[-1] or lowerClose <= 0.1) and intrade == 0:

                # buyPrice = df.close[i]
                # buyPrice = (df.open[i] + df.close[i]) / 2

                buyPrice = df.close.iloc[-1]
                prices.append(buyPrice)


                print('Bought at', buyPrice)
                intrade += 1




            elif (df.close.iloc[-1] > upper.iloc[-1] or abs(upperClose) <= 0.05) and intrade == 1:
                sellPrice = df.close.iloc[-1]

                prices.append(sellPrice)

                diff = prices[1] - prices[0]
                total += diff
                percentage = (total / price) * 100

                print('sold at: ', sellPrice)
                print('Difference', diff)
                print('Total: ', total)
                print('Percentage: ', percentage)


                del prices[0]
                del prices[0]

                intrade -= 1

            time.sleep(30)

    bot()