import os
import pandas as pd

import sys
import time
from StockDay import *
import datetime
from ReadIn import readOne

from DrawCandle import *
#pd.set_option('display.max_columns',None)


def zuoQuShi(aday,interval=5):
    if aday == '':
        aday = datetime.datetime.today().strftime('%Y-%m-%d')

    dfs = list()
    print('看这天的数据',aday)
    days = GetNWorkDays(aday,interval)
    cdf = pd.DataFrame()
    for day in days:
        print('日期: ',day)
        adf = None
        adf = readOne(day)

        if cdf.empty:
            cdf = adf
            #print(day,cdf)
        else:
            cdf = pd.concat([cdf,adf])
            #print(day,cdf)

    cdf = cdf.sort_values(by=['股票代码','交易日期']).reset_index(drop=True)
    del cdf['成交额']
    del cdf['成交量']

    res_df = pd.DataFrame()
    res_list = []
    for g,subdf in cdf.groupby(['股票代码']):
        if aday not in subdf['交易日期'].tolist(): continue
        #if len(subdf) >1 and aday in subdf['交易日期'].tolist():
            #subdf = subdf[subdf['股票代码'].apply(lambda x: ( x.startswith('60') or x.startswith('00') ))]
            #code = subdf['股票代码'].tolist()[0]
            #if code.startswith('00') or code.startswith('60'): pass
            #else: continue
            #if res_df.empty: res_df = subdf
            #else: res_df = pd.concat([res_df,subdf])
        #print(subdf)
        try:
            max_val = subdf['最高价'].max()
            min_val = subdf['最高价'].min()
            curr_val = subdf[subdf['交易日期']==aday]['收盘价'].values[0]
            c = subdf[:1]['股票代码'].tolist()[0]
            n = subdf[:1]['股票名称'].tolist()[0]
            huitiao_val = round((curr_val-max_val)/max_val*100,1)
            up_val = round((curr_val-min_val)/min_val*100,1)
            #print(c,n,max_val,curr_val,min_val,huitiao_val,up_val) 
            res_list.append([c,n,max_val,curr_val,min_val,huitiao_val,up_val])
        except Exception:
            print(subdf)
            time.sleep(60)
            exit()
    res_df = pd.DataFrame(res_list,columns=['code','name','max_val','today_val','min_val','fall_down','go_up'])
    print(res_df.sort_values(by=['fall_down']).reset_index(drop=True)[:200])
    print(res_df.sort_values(by=['go_up'],ascending=False).reset_index(drop=True)[:200])
  

if __name__ == '__main__':
    ad = '2023-06-30'
    #ad = datetime.datetime.today().strftime('%Y-%m-%d')
    #lookOneDayAmount(ad)
    #lookOneDomain(ad, '801760传媒/文化休闲-影视')
    #zuoQuShi('2023-06-28',5)
    drawCandle(['300637'],'2024-05-20','2024-06-03')


