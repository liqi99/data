import os
import pandas as pd

import sys
import time
from Polish import refreshCode,refreshA
from StockDay import *
import datetime
from ReadIn import readOne,readOneCsv


#pd.set_option('display.max_columns',None)


def lookV(aday,interval,ticai=['AI-CPO']):
    if type(ticai) == str: 
        ticai = [ticai]
    all_codes,all_names = [],[]
    for tc in ticai:
        s_codes,s_names = readOneCsv('./ticai/{}.csv'.format(tc))
        names = dict(zip(s_codes,s_names))
        all_codes+=s_codes
        all_names+=s_names
    print('\n', all_names)

    if type(interval) == str:
        days = GetIntervalDays(aday,interval)
    elif type(interval) == int:
        days = GetNWorkDays(aday,interval)

    res_df = pd.DataFrame()
    #names = dict()
    #names = dict(zip(res_df['股票代码'],res_df['股票名称']))
    for day in days:
        adf = readOne(day)
        as_ad = adf[adf['股票代码'].isin(all_codes)]
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


if __name__ == '__main__':
    ad = GetLatestWorkDay()
   
    #res_df = lookV(ad,'2023-07-24','801790非银金融/券商'); print(res_df[res_df['交易日期']==ad].sort_values(by=['涨跌幅_2'])); exit()
    res_df = lookV(ad,'2024-05-20',['801180房地产/物业服务']); exit()
    print(res_df[res_df['交易日期']==ad].sort_values(by=['涨跌幅_2'])); exit()
    #lookV(ad,5,'801730电力设备/胶膜')      
    #lookV(ad,5,'801080电子/光刻胶')       #7-23日本,业绩
    #lookV(ad,5,'801080电子/石英晶体')       #7-23日本,业绩
    lookV('2023-06-30','2023-01-30', ['AI-CPO','AI-模型','AI-芯片']); exit()
    lookV('2023-05-01',15,'801730电力设备/储能');exit() 
    lookV(ad,10,'/801050有色金属/稀土永磁');exit()
    lookV(ad,5,'801080电子/PCB')
    lookV(ad,5,'801080电子/存储')
    lookV(ad,5,'801080电子/LED')
    #lookV(ad,10,'801730电力设备/逆变器')  
    #lookV(ad,10,'801730电力设备/光伏设备')  
    exit()
    lookV(ad,5,'AI-CPO')
    exit()
    lookV(ad,10,'波段')
    exit()
    lookV(ad,10,'801740军工/船舶'); 
    lookV(ad,10,'801740军工/船舶'); 
    lookV(ad,6,'801880汽车/汽车-汽车整车')
    exit()

    lookV(ad,10,'801120饮食消费/白酒')   
    lookV(ad,10,'801790非银金融/保险')  
    lookV(ad,10,'801730电力设备/新能源-风电') 
    lookV(ad,10,'801730电力设备/储能')   
    lookV(ad,10,'801730电力设备/逆变器')  
    #exit()
    lookV(ad,6,'801760传媒/传媒-出版')
    lookV(ad,6,'801760传媒/文化休闲-影视') #暑期档电影票房
    lookV(ad,6,'801760传媒/休闲娱乐-游戏')
    lookV(ad,6,'801760传媒/传媒-在线阅读')
    lookV(ad,6,'801760传媒/传媒-官媒')
    #exit()
    lookV(ad,6,'AI-CPO')
    lookV(ad,6,'AI-服务器')
    lookV(ad,6,'AI-液冷')
    lookV(ad,6,'AI-芯片')
    lookV(ad,6,'AI-模型')
    lookV(ad,6,'801080电子/半导体-光刻机零部件') #6-29荷兰制裁
    lookV(ad,6,'801080电子/半导体-光刻胶')       #7-23日本,业绩
    exit()
    #lookV(ad,6,'AI-医疗')
    #lookV(ad,6,'801210社会服务/文化科技-教育')
    #lookV(ad,6,'801750计算机/计算机-教育信息')   
    #lookV(ad,6,'801210社会服务/体育')

    lookV(ad,6,'0001工业母机')
    lookV(ad,6,'0003人形机器人')
    lookV(ad,6,'801210社会服务/休闲旅游-景点与服务')
    lookV(ad,6,'801210社会服务/休闲旅游-酒店餐饮')
    lookV(ad,6,'801880汽车/汽车-汽车整车')
    #lookV(ad,6,'801880汽车/汽车零部件')
    lookV(ad,6,'801160公共事业/公共事业-火电')
    #lookV(ad,6,'801160公共事业/燃气') 

    lookV(ad,6,'0005集流体')
    lookV(ad,6,'0006代糖')

    #lookV(ad,6,'801730电力设备/锂电池产业链')
    #lookV(ad,6,'801730电力设备/锂电池')
    #lookV(ad,6,'801730电力设备/光伏组件')
    #lookV(ad,6,'801730电力设备/光伏原材料') #硅料
    #lookV(ad,6,'801730电力设备/光伏配件') #线盒，逆变器，银浆
    #lookV(ad,6,'801730电力设备/新能源-风电') #线盒，逆变器，银浆

    #lookV(ad,6,'水泥') #2019年下半年大涨原因分析
    #lookV(ad,6,'煤炭') #2021年下半年-2022年上半年大涨原因分析
    #lookV(ad,6,'钢铁') #2021？年大涨原因分析
    #lookV(ad,6,'银行')
    #lookV(ad,6,'石油采掘')

