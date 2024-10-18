import os
import pandas as pd

import sys
import time
from Polish import refreshCode,refreshA
from StockDay import *
import datetime
from ReadIn import readOne


#pd.set_option('display.max_columns',None)

#ds  dayofweek 日期类型         说明
#ay = getYear(2023)

def reportDate(x):
    cy = by[by.ds>=x]
    cy = cy[(cy.dayofweek<6) & (cy['日期类型']<2)] 
    aday = cy['ds'].tolist()[0]
    #if aday !=x:
    #    print(x,aday)
    return aday

def readAllReport():
    pred_file   = '../dump/QPredR_{}.csv'.format(Q_No)
    report_file = '../dump/QR_{}.csv'.format(Q_No)    
    quick_file  = '../dump/QQuickR_{}.csv'.format(Q_No)
    pred_df   = pd.read_csv(pred_file,sep=',',header=0)
    pred_df['type'] = '业绩预告'
    report_df = pd.read_csv(report_file,sep=',',header=0)
    report_df['type'] = '业绩报告'
    quick_df  = pd.read_csv(quick_file,sep=',',header=0)
    quick_df['type'] = '业绩快报'
    pred_df   = pred_df[['股票代码','股票名称','报告时间','AB股','type']]
    report_df = report_df[['股票代码','股票名称','报告时间','AB股','type']]
    quick_df  = quick_df[['股票代码','股票名称','报告时间','AB股','type']]

    all_df = pd.concat([pred_df,report_df,quick_df])
    all_df = all_df[all_df['AB股']=='A股']
    #all_df.drop(['AB股'],inplace=True,axis=1)
    all_df = all_df.rename(columns={'报告时间':'报告日期'})
    all_df['报告日期'] = all_df['报告日期'].apply(lambda x: x[:10])
    all_df = all_df.sort_values(by=['报告日期']).reset_index(drop=True)
    all_df['股票代码'] = all_df['股票代码'].astype(str)
    all_df['股票代码'] = all_df['股票代码'].apply(lambda x: refreshCode(x))
    return all_df


def showYeJi(interval):

    obj_df = readAllReport()
    print(obj_df[:10])
    obj_df = obj_df[obj_df['报告日期']<='2023-05-15']
    obj_df = obj_df.sort_values(by=['股票代码','报告日期']).reset_index(drop=True)
 
    tmp_res = list()
    bu_days = dict()
    for ind in obj_df.index.tolist():
        s_date = obj_df.at[ind,'报告日期']
        #print('here',s_date)
        s_date = reportDate(s_date)
        bu_days_one = list()
        if s_date not in bu_days:
            bu_days_one = GetNWorkDays(s_date,0-interval)[:2]
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
    print(all_bu_df[:10])
    all_bu_df = pd.merge(left=all_bu_df,right=tmp_code_date,left_on=['股票代码','交易日期'],right_on=['s_code','s_date'])
    all_bu_df.drop(['s_code','s_date'],inplace=True,axis=1)
     
    #obj_df = obj_df.rename(columns={'报告日期':'交易日期'})
    #obj_df = pd.concat([all_bu_df,obj_df])
    obj_df = all_bu_df
    obj_df = obj_df.drop_duplicates()
    
    obj_df = obj_df[['股票代码','股票名称','交易日期','开盘价','收盘价','涨跌幅']]
    obj_df = obj_df.sort_values(by=['股票代码','交易日期','涨跌幅']).reset_index(drop=True)

    print(obj_df)
    print(obj_df.shape)
    print(len(list(obj_df['股票代码'].unique())))
    

if __name__ == '__main__':
    global Q_No
    Q_No = '2024-06-30'
    global by
    by = getYear(int(Q_No[:4]))
    by['日期类型'] = by['日期类型'].astype(int)

    #showYeJi(interval=1)

    adf = readOne('2023-07-31')
    obj_df = readAllReport()
    obj_df = obj_df[(obj_df['AB股'] =='A股') & (obj_df['报告日期']>'2023-07-28')][['股票代码','报告日期']]
    obj_df =obj_df.drop_duplicates()
    obj_df = pd.merge(obj_df,adf,how='left',left_on=['股票代码'],right_on=['股票代码'])
    obj_df = obj_df.sort_values(by=['涨跌幅'],ascending=False).reset_index(drop=True)
    print(obj_df)
    print(obj_df.columns)
    #by = by[by['']]




