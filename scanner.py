import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import time
import talib

class Scanner:

    def fetch():
        exchange = ccxt.binance()

        symbols = ['BTC/USDT', 'ETH/BTC', 'EOS/BTC', 'ONT/BTC', 'BCC/BTC', 'XRP/BTC', 'NANO/BTC', 'NEO/BTC', 'ICX/BTC', 'VET/BTC',
                   'ETC/BTC', 'XLM/BTC', 'LTC/BTC', 'XVG/BTC', 'TRX/BTC', 'XMR/BTC', 'IOTA/BTC', 'ADA/BTC', 'DASH/BTC', 'WAN/BTC',
                   'SC/BTC', 'ZRX/BTC', 'KEY/BTC', 'ZIL/BTC', 'WTC/BTC', 'BCN/BTC', 'NPXS/BTC', 'TUSD/BTC', 'IOST/BTC',
                   'QKC/BTC', 'MFT/BTC', 'NULS/BTC', 'DOCK/BTC', 'AION/BTC', 'QTUM/BTC', 'NAS/BTC', 'HOT/BTC', 'ENG/BTC', 'XEM/BTC',
                   'DENT/BTC', 'INS/BTC', 'ZEC/BTC', 'CVC/BTC', 'ELF/BTC', 'BTG/BTC', 'GTO/BTC', 'OMG/BTC', 'ADX/BTC', 'BQX/BTC', 'NCASH/BTC',
                   'ARN/BTC', 'THETA/BTC', 'CHAT/BTC', 'LOOM/BTC', 'GVT/BTC', 'STRAT/BTC', 'STORM/BTC', 'REP/BTC', 'VIB/BTC', 'NEBL/BTC', 'CMT/BTC',
                   'LSK/BTC', 'BAT/BTC', 'OST/BTC', 'AE/BTC', 'MDA/BTC', 'BLZ/BTC', 'IOTX/BTC', 'SALT/BTC', 'GAS/BTC', 'MCO/BTC', 'POE/BTC',
                   'NXT/BTC', 'PPT/BTC', 'YOYO/BTC', 'SUB/BTC', 'BCPT/BTC', 'MTL/BTC', 'LUN/BTC', 'LINK/BTC', 'GNT/BTC', 'MANA/BTC', 'SKY/BTC',
                   'KMD/BTC', 'ENJ/BTC', 'BRD/BTC', 'POA/BTC', 'LEND/BTC', 'BTS/BTC', 'XZC/BTC', 'POWR/BTC', 'POLY/BTC', 'ZEN/BTC', 'FUN/BTC', 'TNB/BTC',
                   'DGD/BTC', 'DLT/BTC', 'STEEM/BTC', 'SNM/BTC', 'WPR/BTC', 'RCN/BTC', 'FUEL/BTC', 'SNT/BTC', 'WPR/BTC', 'RCN/BTC', 'FUEL/BTC',
                   'SNT/BTC', 'PHX/BTC', 'WAVES/BTC', 'RDN/BTC', 'LRC/BTC', 'WINGS/BTC', 'QSP/BTC', 'REQ/BTC', 'HSR/BTC', 'QLC/BTC', 'PIVX/BTC', 'AMB/BTC',
                   'CLOAK/BTC', 'APPC/BTC', 'VIBE/BTC', 'TRIG/BTC', 'NAV/BTC', 'CDT/BTC', 'BNT/BTC', 'STORJ/BTC', 'WABI/BTC', 'DATA/BTC', 'KNC/BTC'
                   'GRS/BTC', 'ARK/BTC', 'SYS/BTC', 'SNGLS/BTC', 'AST/BTC', 'CND/BTC', 'EDO/BTC', 'GXS/BTC', 'DNT/BTC', 'TNT/BTC', 'AGI/BTC', 'RLC/BTC',
                   'BCD/BTC', 'OAX/BTC', 'ARDR/BTC', 'MOD/BTC', 'EVX/BTC', 'VIA/BTC', 'ICN/BTC', 'MTH/BTC']

        for symbol in symbols:
            ohlcv = exchange.fetch_ohlcv(symbol, '1h')
            df = pd.DataFrame(ohlcv, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
            df['date'] = pd.to_datetime(df['date'], unit='ms')

            market = exchange.fetch_tickers(symbol)
            price = market[symbol]['bid']

            rsi = talib.RSI(df['close'])

            upper, middle, lower = talib.BBANDS(df.close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
            lowerClose = (df.close.iloc[-1] - lower.iloc[-1]) / lower.iloc[-1] * 100
            upperClose = (df.close.iloc[-1] - upper.iloc[-1]) / upper.iloc[-1] * 100

            macd, macdsignal, macdhist = talib.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)

            vol = (df.volume.iloc[-1] - df.volume.iloc[-2]) / df.volume.iloc[-2] * 100

            if rsi.iloc[-1] <= 30:
                print('RSI UNDER 30')
                print(symbol)
                print('Price: ', price)
                print('RSI: ', rsi[-1])
                print('   ')
                print('   ')

            if df.close.iloc[-1] <= lower.iloc[-1] or lowerClose <= 0.1:
                print('LOWER BB')
                print(symbol)
                print('Price: ', price)
                print('Candle close: ', df.close.iloc[-1])
                print('Lower BB: ', lower.iloc[-1])
                print('   ')
                print('   ')

            if macd.iloc[-1] >= macdsignal.iloc[-1] and macd.iloc[-2] <= macdsignal.iloc[-2]:
                print('MACD CROSS')
                print(symbol)
                print('Price: ', price)
                print('   ')
                print('   ')

            if vol >= .05:
                print('VOLUME INCREASE')
                print(symbol)
                print('Price: ', price)
                print(vol, "%")


            else:
                print(symbol)
                print('Price: ', price)
                print('   ')

            # time.sleep(exchange.rateLimit / 1000)
            time.sleep(10)
    fetch()