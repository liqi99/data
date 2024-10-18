import os
import pandas as pd

import sys
import time
from Polish import refreshCode,refreshA,isToTopDown
from StockDay import *
import datetime


#pd.set_option('display.max_columns',None)

def readINHist(aday,selection = None):
    ayear = aday[:4]
    adf = pd.read_csv('./hist_dump/oneday/{}/stock_price_{}.csv'.format(ayear,aday),sep=',',index_col=0)
    adf = adf[adf['交易日期'] == aday]

    adf['股票代码'] = adf['股票代码'].apply(lambda x: refreshCode(x))
    adf['涨跌幅'] = adf['涨跌幅%'].apply(lambda x: refreshA(x))

    del adf['涨跌幅%']

    adf['最低价'] = adf['最低价'].apply(lambda x: refreshA(x))
    adf['最高价'] = adf['最高价'].apply(lambda x: refreshA(x))
    adf['收盘价'] = adf['收盘价'].apply(lambda x: refreshA(x))
    adf['开盘价'] = adf['开盘价'].apply(lambda x: refreshA(x))
    adf['成交量'] = adf['成交量'].apply(lambda x: refreshA(x))

    adf = adf[~adf['最高价'].isna()]
    adf = adf[~adf['收盘价'].isna()]

    if selection is not None:
        if type(selection) in [int,float]:
            adf = adf[adf['涨跌幅']>=selection]
        if type(selection) == str and selection == 'toTop':
            adf = adf[adf['涨跌幅']>=0]
            adf = adf[adf.apply(lambda row: isToTopDown(row['涨跌额'],row['收盘价'],row['股票代码'],row['股票名称'])[0],axis=1)]
        elif type(selection) == str and selection == 'wasToTop':
            #adf = adf[adf['涨跌幅']>=0]
            adf = adf[adf.apply(lambda row: isToTopDown(row['涨跌额'],row['最高价'],row['股票代码'],row['股票名称'],row['收盘价'])[0],axis=1)]
    #print(adf.columns)
    #print(aday)
    #print(adf[:10])
    adf = adf[['股票代码','股票名称','交易日期','开盘价','收盘价','最高价','最低价','成交量','成交额','振幅','涨跌额','涨跌幅']]

    return adf

def readINNew(aday,selection = None):
    try:
        adf = pd.read_csv('./dump/{}/stock_data_{}_3.csv'.format(aday[:4],aday),sep=',')
    except Exception:
        adf = pd.read_csv('./dump/{}/stock_data_{}_2.csv'.format(aday[:4],aday),sep=',')
    names = ['股票代码', '股票名称', '最新价', '涨跌幅',  '成交量（手）', '最高', '最低', '今开', '振幅', '涨跌额', '成交额']
    adf = adf[names]
    #adf['股票代码'] = adf['股票代码'].astype(str)
    adf['股票代码'] = adf['股票代码'].apply(lambda x: refreshCode(x))
    adf['涨跌幅'] = adf['涨跌幅'].apply(lambda x: refreshA(x))

    adf['交易日期'] = aday
    adf = adf.rename(columns={'成交量（手）':'成交量',
                              '今开':'开盘价',
                              '最新价':'收盘价',
                              '最高':'最高价',
                              '最低':'最低价'})
    adf = adf[['股票代码','股票名称','交易日期','开盘价','收盘价','最高价','最低价','成交量','成交额','振幅','涨跌额','涨跌幅']]

    adf['最低价'] = adf['最低价'].apply(lambda x: refreshA(x))
    adf['最高价'] = adf['最高价'].apply(lambda x: refreshA(x))
    adf['收盘价'] = adf['收盘价'].apply(lambda x: refreshA(x))
    adf['开盘价'] = adf['开盘价'].apply(lambda x: refreshA(x))
    adf['成交量'] = adf['成交量'].apply(lambda x: refreshA(x))

    #这里把退市股排除了，导致计算涨跌幅分布的时候==0的数据和一般的交易软件对不上
    adf = adf[~adf['最高价'].isna()]
    adf = adf[~adf['收盘价'].isna()]

    if selection is not None:
        if type(selection) in [int,float]:
            adf = adf[adf['涨跌幅']>=selection]
        elif type(selection) == str and selection == 'toTop':
            adf = adf[adf['涨跌幅']>=0]
            adf = adf[adf.apply(lambda row: isToTopDown(row['涨跌额'],row['收盘价'],row['股票代码'],row['股票名称'])[0],axis=1)]
        elif type(selection) == str and selection == 'wasToTop':
            #adf = adf[adf['涨跌幅']>=0]
            adf = adf[adf.apply(lambda row: isToTopDown(row['涨跌额'],row['最高价'],row['股票代码'],row['股票名称'],row['收盘价'])[0],axis=1)]
    #print(adf.columns)
    #print(adf[:5])

    return adf

def defAmpLevel(updownNum,lastNum,code,name,high,low,udAmp):
    toTop,toLow = False,False
    toTop,toLow = isToTopDown(updownNum,lastNum,code,name)
    #if code == '001336': print(toTop,toLow)
    if toTop is True and lastNum==high: return 'ZT'
    elif toLow is True and lastNum==low: return '-DT'
    elif udAmp is not None:
        udAmp = round(udAmp,2)
        if udAmp>7: return '>7'
        elif udAmp>5: return '>5'
        elif udAmp>2: return '>2'
        elif udAmp>0: return '>0'
        elif udAmp == 0: return '=0'
        elif udAmp <-7: return '<-7'
        elif udAmp <-5: return '<-5'
        elif udAmp <-2: return '<-2'
        elif udAmp <0: return '<0'
        else: 
            print('涨跌幅',upAmp)
            time.sleep(10)
            return None
    
def readOne(aday,selection=None):
    #if aday in ['2023-06-14','2023-06-05','2023-05-25','2023-08-11','2023-09-21','2023-10-24','2023-10-25','2023-11-02'] or aday < '2023-05-19' or (aday>='2023-11-20' and aday<='2023-11-28'):
    try:
        adf = readINNew(aday,selection)
    except Exception:
        adf = readINHist(aday,selection)
        #adf = None
        #print('没有--{}--这天的数据'.format(aday))
    adf = adf[adf['交易日期']==aday]
    #adf = adf[adf['股票名称'].apply(lambda x: 'st' not in x.lower())]
    return adf

def readOneCsv(afile):
    afile = open(afile,'r')
    lines = afile.readlines()
    s_names = []
    s_codes = []
    for line in lines:
        line = line.strip()
        if line.startswith('#') or line == '': continue
        if ',' in line:
            s_code,s_name=line.split(',')[:2]
        elif '\t' in line:
            s_code,s_name=line.split('\t')
        else:
            info=line.split(' ')
            s_name,s_code = [it for it in info if it!='']
            #print(afile)
            #time.sleep(60)
        s_codes.append(s_code)
        s_names.append(s_name)
    afile.close()
    #print(s_names)
    return s_codes,s_names

