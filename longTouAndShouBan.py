import os
import pandas as pd

import sys
import time
from Polish import refreshCode,refreshA
from StockDay import *
import datetime
from ReadIn import readOne

#pd.set_option('display.max_columns',None)


#看涨停第二天收益
def showTopNext(aday):
    #判断涨停，先简单判断
    tmp_names = ['股票代码','股票名称','涨跌幅','最高价','交易日期','收盘价']

    adf = readOne(aday)
    adf = adf[tmp_names]

    bday = GetNWorkDays(aday,2)[0]

    bdf = readOne(bday,'toTop')
    bdf = bdf[tmp_names]

    cdf = pd.merge(left = bdf, right = adf,how = 'left', on=['股票代码'],suffixes=['_涨停日','_次日'])
    cdf = cdf.sort_values(by=['涨跌幅_涨停日']).reset_index(drop=True)

    names= [ '股票代码','股票名称_涨停日', '涨跌幅_涨停日',  '交易日期_涨停日',  '涨跌幅_次日', '交易日期_次日','收盘价_次日']
    cdf = cdf[names]
    cdf = cdf[cdf['涨跌幅_涨停日'].apply(lambda x: x>6)].sort_values(by=['涨跌幅_次日'],ascending=False).reset_index(drop=True)

    print(cdf)
    print(cdf.shape)
    print('昨日涨停溢价')


#某天的高收益股票
def lookShouBan(aday,codes=None):
    adf = readOne(aday,'toTop')
    adf = adf[adf['股票名称'].apply(lambda x: 'ST' not in x)]
    adf = adf.reset_index(drop=True) 

    print(adf)
    print(adf.shape)
    print('今日涨停的股票')
    return adf['股票代码'].tolist()
 

def zhaBan(aday,codes=None):
    adf = readOne(aday,'wasToTop')
    adf = adf.reset_index(drop=True)
    adf = adf[~adf['股票代码'].isin(codes)]
    adf = adf.reset_index(drop=True)
    print(adf)
    print(adf.shape)
    print('今日炸板的股票')


#查看龙头和趋势股
def lookLongTou(aday='',interval=7):
    if aday == '':
        aday = datetime.datetime.today().strftime('%Y-%m-%d')
        #raise Exception('lookLongTou() 必须指定是日期')
        print('看这天的数据',aday)

    if type(interval) == int:
        days = GetNWorkDays(aday,interval)
    elif type(interval) == str and len(interval) == 10:
        days = GetIntervalDays(aday,interval)

    cdf = pd.DataFrame()
    for day in days:
        #print('日期: ',day)
        adf = None
        adf = readOne(day,'toTop')

        if cdf.empty:
            cdf = adf
        else:
            cdf = pd.concat([cdf,adf])

    cdf = cdf.sort_values(by=['股票代码','交易日期']).reset_index(drop=True)
    del cdf['成交额']
    del cdf['成交量']

    res_df = pd.DataFrame()
    for g,subdf in cdf.groupby(['股票代码']):
        #if g=='000004': print(subdf)
        if len(subdf) >2:# and aday in subdf['交易日期'].tolist():
            #subdf = subdf[subdf['股票代码'].apply(lambda x: ( x.startswith('60') or x.startswith('00') ))]
            #code = subdf['股票代码'].tolist()[0]
            #if code.startswith('00') or code.startswith('60'): pass
            #else: continue
            if res_df.empty: res_df = subdf
            else: res_df = pd.concat([res_df,subdf])

    res2_df = pd.DataFrame()
    for g,subdf in res_df.groupby(['股票代码']):
        jy_days = subdf['交易日期'].tolist()
        if days[-1] in jy_days:
            if res2_df.empty: res2_df = subdf
            else: res2_df = pd.concat([res2_df,subdf])       

    res1_df = res_df[~res_df['股票代码'].isin(res2_df['股票代码'].unique().tolist())]

    codes = res2_df['股票代码'].tolist()
    codes = list(set(codes))

    #print(res_df)
    #print(res_df.shape)
    #print('近期连板的股票')

    #print(res1_df)
    #print(res1_df.shape)
    #print('近期连板但今天未板的股票')

    print(res2_df)
    print(res2_df.shape)
    print('今日非首板个数: {}'.format(len(codes)))

    return codes


def Find(aday='',interval=7):
    if aday == '':
        aday = datetime.datetime.today().strftime('%Y-%m-%d')
        #raise Exception('lookLongTou() 必须指定是日期')
        print('看这天的数据',aday)

    if type(interval) == int:
        days = GetNWorkDays(aday,interval)
    elif type(interval) == str and len(interval) == 10:
        days = GetIntervalDays(aday,interval)

    cdf = pd.DataFrame()
    for day in days:
        #print('日期: ',day)
        adf = None
        adf = readOne(day,'toTop')

        if cdf.empty:
            cdf = adf
        else:
            cdf = pd.concat([cdf,adf])

    cdf = cdf[cdf['股票代码'].apply(lambda x: x.startswith('3'))]

    for bday in days:
        #bday = datetime.datetime.today().strftime('%Y-%m-%d')
        bdf = readOne(bday)
        bdf = bdf[bdf['股票代码'].apply(lambda x: x.startswith('3'))]
        bdf = bdf[bdf['股票代码'].isin(cdf['股票代码'].unique())]
        cdf = pd.concat([cdf,bdf])
    cdf = cdf.drop_duplicates()
    for g,subdf in cdf.groupby(['股票代码']):
        print(subdf[['交易日期','股票代码','股票名称','涨跌幅']].sort_values(by=['交易日期']).reset_index(drop=True))
    #print(cdf.sort_values(by=['股票代码']).reset_index(drop=True))
    print('近期创业板有过涨停的标的')


if __name__=='__main__':
    if len(sys.argv)>1:
        ad = sys.argv[1]
    else:
        ad = GetLatestWorkDay()

    #涨停溢价
    showTopNext(ad)

    #龙头发现
    anow = datetime.datetime.now()
    if anow.weekday()<=1:
        howmany = 5+anow.weekday()+1
    else:
        howmany = 6

    #连板
    lb_codes = lookLongTou(ad,howmany)
    #首板
    sb_codes = lookShouBan(ad,lb_codes)
    zhaBan(ad,lb_codes+sb_codes)
    Find(ad)
    print('今天星期{}'.format(anow.weekday()+1))



