import os
import pandas as pd
import numpy as np

import sys
import time
from Polish import refreshCode,refreshA,isToTopDown,amount
from StockDay import *
import datetime
from ReadIn import readOne,defAmpLevel

from longTouAndShouBan import *
from ciXin import *
from st import *


#pd.set_option('display.max_columns',None)



#看一天的成交量，包含北交所的
#就是看一天的情绪量化指标用的
def lookOneDayAmount(aday):
    adf = readOne(aday)
    adf['成交额'] =adf['成交额'].apply(lambda x: 0 if x == '-' else float(x))
    #print(adf.head())
    #print(adf.tail())

    #adf = adf[adf['交易日期']==aday]

    bj_adf = adf[adf['股票代码'].apply(lambda x: x.startswith('8') or x.startswith('4'))]
    sh_adf = adf[adf['股票代码'].apply(lambda x: x.startswith('6'))]
    sz_adf = adf[adf['股票代码'].apply(lambda x: x.startswith('0') or x.startswith('3'))]

    amount = sum(adf['成交额'])/1E8
    amount = round(amount,4)
    #print('{}A股成交量: {}'.format(aday,amount))

    bj_amount = sum(bj_adf['成交额'])/1E8
    bj_amount = round(bj_amount,4)
    #print('{}北交所成交量: {}'.format(aday,bj_amount))

    sh_amount = sum(sh_adf['成交额'])/1E8
    sh_amount = round(sh_amount,4)
    #print('{}上交所成交量: {}'.format(aday,sh_amount))

    sz_amount = sum(sz_adf['成交额'])/1E8
    sz_amount = round(sz_amount,4)
    #print('{}深交所成交量: {}'.format(aday,sz_amount))

    return amount, sh_amount, sz_amount, bj_amount

def lookIntervalAmount(aday,bday):
    days = GetIntervalDays(aday,bday)
    for day in days:
        aday_amount,sh_amount,sz_amount,bj_amount = lookOneDayAmount(day)
        aday_amount = int(aday_amount)
        sh_amount = int(sh_amount)
        sz_amount = int(sz_amount)
        bj_amount = round(bj_amount,1)
        print(day, sh_amount+sz_amount, sh_amount, sz_amount, bj_amount)

#看一个板块内的股票整体涨跌情况
#这是为了切换用的，当龙头出现高位震荡或者一天就开始杀跌，那么看低位板块用的
def lookOneDomain(aday,ticai='AI-CPO',bday=None,interval=None):
    s_codes,s_names = readOneCsv('./ticai/{}.csv'.format(ticai))

    print(s_names)
    adf = readOne(aday)
    as_ad = adf[adf['股票代码'].isin(s_codes)]
    print(as_ad)

def showToHigh(ad,selection='toTop'):
    adf = readOne(ad,selection)
    adf = adf[adf['涨跌幅'].apply(lambda x: x>6)]
    print(adf)
    print(adf.shape)
    return adf

def showIntervalHigh(aday,bday,selection):
    days = GetIntervalDays(aday,bday)
    codes = []
    for ad in days:
        print(ad)
        adf = showToHigh(ad,selection)
        acodes = adf['股票代码'].tolist()
        codes+=acodes
    print(len(codes))
    print(len(set(codes)))

def getUpDownLevel(aday):
    adf = readOne(aday)
    #print(adf.head(50))
    #print(adf.tail(10))
  
    adf['level'] = adf.apply(lambda row: defAmpLevel(row['涨跌额'],row['收盘价'],row['股票代码'],row['股票名称'],row['最高价'],row['最低价'],row['涨跌幅']),axis=1)
    #print(adf[adf['level']=='toLow'])
    bdf = adf.groupby(['level']).count()['股票代码']
    #adf.columns = adf.columns.droplevel(0)
    #print('\n')
    print(aday)
    print(bdf)
    #print(adf[['股票代码','涨跌幅','level']])
    return adf

def ShowAmountOrder(aday):
    adf = readOne(aday)
    adf['成交额'] = adf['成交额'].astype(dtype=np.float64)
    adf = adf.sort_values(by=['成交额'],ascending=False).reset_index(drop=True)
    adf['成交额'] = adf['成交额'].apply(lambda x: amount(x))
    print(adf[:25])

def longtou():
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
    print('\n') 
    zhaBan(ad,lb_codes+sb_codes)
    print('\n')
    print('今天星期{}'.format(anow.weekday()+1))


if __name__ == '__main__':
    ad = sys.argv
    if len(ad) ==2 and sys.argv[1]!='':
        ad = sys.argv[1]
        if len(ad)==8:
            ad = ad[:4]+'-'+ad[4:6]+'-'+ad[6:]
    elif len(ad)==1 or True:
        ad = GetLatestWorkDay()

    ShowAmountOrder(ad)

    adf = showToHigh(ad); 
    #print(adf)
    #exit()

    #days = GetIntervalDays('2022-07-22','2023-07-21')
    #res_code = {}
    #for day in days:
    #    print(day)
    #    adf = showToHigh(day,'toTop')
    #    for code in adf['股票代码'].tolist():
    #        if code not in res_code: 
    #            res_code[code] =1
    #        else: res_code[code]+=1
    #
    #adf = readOne(day)
    #names = dict(zip(adf['股票代码'],adf['股票名称']))
    #res_code = sorted(res_code.items(), key=lambda x: x[1], reverse=True)
    #res_code = [list(it) for it in res_code]    
    #level_d={}
    #for i in range(len(res_code)):
    #    if res_code[i][0] in names:
    #        res_code[i][0] = names[res_code[i][0]]
    #    else:
    #        print(res_code[i])
    #    if res_code[i][1] not in level_d: level_d[res_code[i][1]] = 1
    #    else: level_d[res_code[i][1]] +=1
    #print(res_code)
    #print(len(res_code))
    #print(adf.shape[0])
    #print(len(res_code)/adf.shape[0])
    #print(level_d)
    #exit()

    #lookOneDomain(ad, '801760传媒/文化休闲-影视')

    aday_amount,sh_amount,sz_amount,bj_amount = lookOneDayAmount(ad)
    #print('\n')
    print(ad, round(sh_amount+sz_amount,1), round(sh_amount,1),round(sz_amount,1),round(bj_amount,1),round(aday_amount,1)); #exit()

    if len(sys.argv) ==3:
        aday = sys.argv[1]
        bday = sys.argv[2]
        aday,bday = sorted([aday,bday])
        lookIntervalAmount(aday,bday)

    #exit()
    adf = getUpDownLevel(ad); #exit()


    #print(adf[(adf['level']=='ZT')&(adf['涨跌幅'].apply(lambda x: x>11))])
    #print(adf[(adf['level']=='ZT')&(adf['涨跌幅'].apply(lambda x: x>6 and x<11))])
    #print(adf[(adf['level']=='ZT')&(adf['涨跌幅'].apply(lambda x: x<6))])
    #print(adf[(adf['level']=='-DT')&(adf['涨跌幅'].apply(lambda x: x<-6))])

    #for ad in GetIntervalDays('2023-03-20','2023-04-10'):
    #    getUpDownLevel(ad)
        #adf = showToHigh(ad,'toTop')
        #print(adf)

    #longtou()


