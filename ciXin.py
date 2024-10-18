import os
import pandas as pd

import sys
import time
from StockDay import *
import datetime
from ReadIn import readOne


def showXinGu(aday):
    tmp_names = ['股票代码','股票名称','涨跌幅','收盘价','最高价','交易日期']

    adf = readOne(aday)
    adf = adf[tmp_names]
    adf = adf[adf['股票名称'].apply(lambda x: 'N' == x[0] or 'C' == x[0])]
    if adf.empty:
        print('{} 没有新股发布'.format(aday))
    else:
        print(adf)
    return adf


def ciXin(aday):
    tmp_names = ['股票代码','股票名称','涨跌幅','最高价','交易日期']

    adf = readOne(aday)
    adf = adf[tmp_names]
    adf = adf[adf['股票名称'].apply(lambda x: 'N' == x[0] or 'C' == x[0])]
    return adf


def showCiXinNext(aday,bday):
    print(aday,bday)

    #判断涨停，先简单判断
    tmp_names = ['股票代码','股票名称','涨跌幅','最高价','交易日期']

    adf = readOne(aday)
    adf = adf[tmp_names]
    adf = adf[adf['股票名称'].apply(lambda x: 'N' == x[0])]
    if adf.empty: 
        print('{}没有新股发布'.format(aday))
        return adf
    
    bdf = readOne(bday)
    bdf = bdf[tmp_names]
    #print(bdf)
    xdf = bdf[bdf['股票名称'].apply(lambda x: 'C' == x[0])]
        
    cdf = pd.merge(left = adf, right = bdf,how = 'left', on=['股票代码'],suffixes=['_首日','_次日'])
    cdf = cdf.sort_values(by=['涨跌幅_次日']).reset_index(drop=True)

    names= [ '股票代码','股票名称_首日', '涨跌幅_首日',  '交易日期_首日',  '股票名称_次日', '涨跌幅_次日', '交易日期_次日']
    cdf = cdf[names]
    
    print(cdf) 
    print(cdf.shape)

    print(xdf)
    print(xdf.shape)
 
   
def IntervalCiXin(aday,bday):
    res_df = pd.DataFrame()
    if aday ==None or bday is None:
        days = GetNWorkDays(ad,14)
    else:
        days = GetIntervalDays(aday,bday)
    for day in days:
        adf = ciXin(day) #主板1天44%~-36%，北交所1天+-inf，300/688 5天+-inf
        if res_df.empty: res_df =adf
        else: res_df = pd.concat([res_df,adf])
    res_df = res_df.sort_values(by=['股票代码','交易日期']).reset_index(drop=True)
    #for g,subdf in res_df.groupby(['股票代码']):
    #    if subdf.shape[0]>=1 and subdf.shape[0]<5 and 'N' in subdf['股票名称'].values[0]:
    #        print(subdf)
    print(res_df[res_df['股票名称'].apply(lambda x: 'N' in x)].sort_values(by=['交易日期','涨跌幅']).reset_index(drop=True))
    print(res_df[res_df['股票名称'].apply(lambda x: 'C' in x)].sort_values(by=['股票代码','交易日期','涨跌幅']).reset_index(drop=True))
    print(res_df[res_df['股票代码'].apply(lambda x: str(x).startswith('3'))])
    print(res_df[res_df['股票代码'].apply(lambda x: str(x).startswith('0') or str(x).startswith('60'))])
    return res_df



if __name__ == '__main__':
    ad = GetLatestWorkDay()
    showXinGu(ad)
    #exit()
    #
    #if len(sys.argv)>3:
    #    aday,bday=sys.argv[2],sys.argv[3]
    #else: 
    #    aday,bday=ad,None
    #
    #IntervalCiXin(aday,bday)
