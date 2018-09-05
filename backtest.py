import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import time
import talib


class BackTester:

    def backTest():

        symbols = ['VET/BTC', 'ETH/BTC', 'ICX/BTC']

        exchange = ccxt.binance()

        pos = 0
        neg = 0
        totalPercent = 0
        percents = []


        for symbol in symbols:
            time.sleep(5)
            # symbol = 'BTC/USDT'

            timeframe = '5m'
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
            df = pd.DataFrame(ohlcv, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
            df['date'] = pd.to_datetime(df['date'], unit='ms')

            market = exchange.fetch_tickers(symbol)
            price = market[symbol]['bid']

            upper, middle, lower = talib.BBANDS(df.close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

            macd, macdsignal, macdhist = talib.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)

            i = 0
            intrade = 0
            prices = []
            total = 0
            totalp = 0



            for date in df['date']:
                # print(i)

                # print(intrade)

                #
                # if df.close.iloc[i-1] == lower.iloc[i-1] or lowerClose <= 0.05 and intrade == 0 and macd.iloc[i-1] >= \
                #         macdsignal.iloc[-1]:
                lowerClose = (df.low.iloc[i] - lower.iloc[i]) / lower.iloc[i] * 100
                upperClose = (df.low.iloc[i] - upper.iloc[i]) / upper.iloc[i] * 100

                if (df.low.iloc[i] <= lower.iloc[i] or lowerClose <= 0.1) and intrade == 0:

                    # buyPrice = df.close[i]
                    # buyPrice = (df.open[i] + df.close[i]) / 2

                    # print(i)
                    buyPrice = df.close[i]
                    if i > len(df):
                        i = len(df)


                    prices.append(buyPrice)


                    # print('Bought at', buyPrice)
                    intrade += 1



                # if df.close.iloc[i-1] == middle.iloc[i-1] or upperClose <= 0.05 and intrade == 1 and macd.iloc[i-1] <= \
                #         macdsignal.iloc[i-1]:
                elif (df.close.iloc[i] > upper.iloc[i] or abs(upperClose) <= 0.05) and intrade == 1:
                    sellPrice = df.close[i]
                    # sellPrice = df.open[i + 1]

                    if i > len(df):
                        i = len(df)

                    prices.append(sellPrice)
                    p = (prices[1] - prices[0])/prices[0] * 100
                    totalp += p

                    diff = prices[1] - prices[0]
                    total += diff


                    # print('Sold at', sellPrice)
                    # print('Difference', diff)


                    del prices[0]
                    del prices[0]

                    intrade -= 1

                i += 1


            if total < 0:
                neg += 1
            if total > 0:
                pos += 1

            percentage = (total / price) * 100
            # percentage = (total / ) * 100
            percents.append(percentage)
            totalPercent += percentage
            total = total * 7200
            index = percents.index(max(percents))
            print(symbol)
            print('Total: ', total)
            print('Percentage: ', totalp, '%')
            print('  ')
            print('Coins Positive: ', pos)
            print('Coins Negative: ', neg)
            # print('total p', totalp)


        print('  ')
        print('Total Coins Positive: ', pos)
        print('Total Coins Negative: ', neg)
        print('Average Percentage: ', totalPercent / len(symbols))
        print('Highest Percentage: ', max(percents))
        print('Symbol: ', symbols[index])


    backTest()