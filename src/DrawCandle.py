import os
import sys
import time

import pandas as pd
from StockDay import *
import datetime
from ReadIn import readOne
from Polish import *
from DrawCandle import *

#Draw Candle
#import matplotlib.pyplot as plt
#import mplfinance as mpf


def getIntervalStockPrice(code,daya,dayb):
    adf = pd.DataFrame()

    days = GetIntervalDays(daya,dayb)

    for day in days:
        tmp_adf = readOne(day)
        if adf.empty: adf = tmp_adf
        else: adf = pd.concat([adf,tmp_adf])

    print(adf[:10])
    adf = adf.rename(columns={ '成交量':'volume',
                            '开盘价':'open',
                            '收盘价':'close',
                            '最高价':'high',
                            '最低价':'low',
                            '交易日期':'date'})

    adf = adf[['股票代码','date','open','close','high','low','volume']]
    print(adf[:10])

    #for code in codes:
    #df = adf[adf['交易日期']>=daya & adf['交易日期']<=dayb]
    #print(code)
    df = adf[adf['股票代码'] == code]
    del df['股票代码']
    df["date"] = pd.to_datetime(df["date"])
   
    df = df.set_index(['date'],drop=True)
    #print(df)
    return df
        
#if __name__ == '__main__':
#    df = drawCandle('','','')
#    mpf.plot(df, type="candle", title="三六零", ylabel="市价", style="binance")
