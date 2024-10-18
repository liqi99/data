import os
import pandas as pd

import sys
import time
from Polish import refreshCode,refreshA,isToTopDown
from StockDay import *
import datetime
from ReadIn import readOne


#pd.set_option('display.max_columns',None)


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
            print(afile)
            #time.sleep(60)
        s_codes.append(s_code)
        s_names.append(s_name)

    print(s_names)
    return s_codes,s_names

def lookV(aday,interval,ticai='AI-CPO'):
    s_codes,s_names = readOneCsv('./ticai/{}.csv'.format(ticai))
    names = dict(zip(s_codes,s_names))
    print('\n', s_names)
    days = GetNWorkDays(aday,interval)

    res_df = pd.DataFrame()
    #names = dict()
    #names = dict(zip(res_df['股票代码'],res_df['股票名称']))
    for day in days:
        adf = readOne(day)
        as_ad = adf[adf['股票代码'].isin(s_codes)]
        if res_df.empty: 
            res_df = as_ad
            #names = dict(zip(res_df['股票代码'],res_df['股票名称']))
        else: res_df = pd.concat([res_df,as_ad])

    res_df = res_df.sort_values(by=['股票代码','交易日期']).reset_index(drop=True)

    if len(days)>6:
        acode = None
        indexes = res_df.index.tolist()
        start_code= None
        for ind in indexes:
            bcode = res_df.at[ind,'股票代码']
            if bcode != start_code:
                #print(bcode)
                bench = 1
                start_code = bcode
            new_val = (res_df.at[ind,'涨跌幅']/100+1)*bench
            new_val = round(new_val,4)
            res_df.at[ind,'涨跌幅_2'] = new_val
            bench = new_val
        res_df = res_df[['股票代码','股票名称','交易日期','涨跌幅','涨跌幅_2']]
        print(res_df) 
        return res_df

    res_df = res_df[['股票代码','涨跌幅','交易日期']]
    res_df = pd.pivot_table(res_df, index=['股票代码'], values=['涨跌幅'], columns=['交易日期'], fill_value=0)
    #res_df.reset_index(inplace=True)
    res_df.columns = res_df.columns.droplevel(0)
    res_df.reset_index(inplace=True)
    #print(res_df['股票代码'])
    #res_df['股票名称'] = res_df['股票代码'].apply(lambda x: names[x])
    #print(res_df.index.tolist())

    amp = []
    #for code in res_df['股票代码'].tolist():
    for code in s_codes:
        if code not in res_df['股票代码'].tolist(): 
            print(code,names[code],'\n停牌？\n')
            continue
            #time.sleep(60)
            #exit()
        val_l = [code]
        n_val = 1
        vals = res_df[res_df['股票代码']==code].values[0].tolist()[1:]
        for val in vals:
            n_val = n_val*(1+val/100)
            n_val = round(n_val,4)
            val_l.append(n_val)
        #print(val_l)
        amp.append(val_l)
    bdf = pd.DataFrame(amp,columns= res_df.columns)
    #res_df = pd.concat([res_df,bdf])
    bdf['股票名称'] = bdf['股票代码'].apply(lambda x: names[x])
    bdf = bdf.sort_values(by=[days[-1]])
    print(bdf)
    res_df['股票名称'] = res_df['股票代码'].apply(lambda x: names[x])
    print(res_df)
    #res_df = res_df.sort_values(by=['股票代码']).reset_index(drop=True)
    return res_df


def showToHigh(aday,bday,interval):
    days = GetIntervalDays(aday,bday)

    all_df = pd.DataFrame()
    for day in days:
        adf = readOne(day)
        if all_df.empty: 
            all_df = adf
        else:
            all_df = pd.concat([all_df,adf])
  
    obj_df = all_df[all_df['涨跌幅']>=7]
    
    obj_df = obj_df.sort_values(by=['股票代码','交易日期']).reset_index(drop=True)

    tmp_res = list()
    bu_days = dict()
    for ind in obj_df.index.tolist():
        s_date = obj_df.at[ind,'交易日期']
        print('here',s_date)
        bu_days_one = list()
        if s_date not in bu_days:
            bu_days_one = GetNWorkDays(s_date,interval+1)[:interval]
            bu_days[s_date] = bu_days_one
        else:
            bu_days_one = bu_days[s_date]
        s_code = obj_df.at[ind,'股票代码']
        for day in bu_days_one:
            tmp_res.append([s_code,day])
    tmp_code_date = pd.DataFrame(tmp_res,columns=['s_code','s_date'])
    tmp_code_date = tmp_code_date.drop_duplicates()
    
    all_bu_days = tmp_code_date['s_date'].unique()
    all_bu_days = list(all_bu_days)
                
    all_bu_df = pd.DataFrame()
    for day in all_bu_days:
        tmp_df = readOne(day)
        if all_bu_df.empty:
            all_bu_df = tmp_df
        else:
            all_bu_df = pd.concat([all_bu_df,tmp_df])
    all_bu_df = pd.merge(left=all_bu_df,right=tmp_code_date,left_on=['股票代码','交易日期'],right_on=['s_code','s_date'])
    all_bu_df.drop(['s_code','s_date'],inplace=True,axis=1)
     
    obj_df = pd.concat([all_bu_df,obj_df])
    obj_df = obj_df.drop_duplicates()
    
    obj_df = obj_df.sort_values(by=['股票代码','交易日期']).reset_index(drop=True)

    print(obj_df)
    print(obj_df.shape)
    print(len(list(obj_df['股票代码'].unique())))
    

if __name__ == '__main__':
    ad = datetime.datetime.today().strftime('%Y-%m-%d')
    #ad = '2023-07-07'
    ad = GetLatestWorkDay()
    bd = GetNWorkDays(ad,5)
    showToHigh(ad,bd,5)
    

