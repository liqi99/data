import os,sys
from Holiday import *
import pandas as pd
import datetime

#pd.set_option('display.max_rows',None)


def GetNWorkDays(aday='',interval=5, ayear=2023):
    ayear = int(aday[:4])
    ay = getYear(ayear)
    #print(ay)
    del ay['说明']
    #print(ay)
    #print(len(ay))
    ay['日期类型'] = ay['日期类型'].astype(int)
    
    #print(ay)
    
    ay = ay[(ay.dayofweek<6) & (ay['日期类型']<2)]
    #print(ay)

    ay = ay.sort_values(by=['ds']).reset_index(drop=True)
    #print(ay)
    #print(aday)
    aindex = ay[ay.ds<=aday].index.tolist()[-1]
    #print(ay)
    #print(aindex)
    aindex = int(aindex)

    tmp_year = ayear
    while(aindex-interval+1<0):
        last_year = tmp_year -1
        tmp_year = last_year
        last_y = getYear(last_year)
        del last_y['说明']
        last_y['日期类型'] = last_y['日期类型'].astype(int)
        last_y = last_y[(last_y.dayofweek<6) & (last_y['日期类型']<2)]

        ay = pd.concat([last_y,ay])        
        ay = ay.sort_values(by=['ds']).reset_index(drop=True)
        aindex = ay[ay.ds<=aday].index.tolist()[-1]
        aindex = int(aindex)

    left,right = sorted([aindex+1,aindex-interval+1])
    left = max([left,0])
    obj_days = ay[left:right].ds.tolist()

    if interval <0: 
        obj_days = [aday]+obj_days
     
    print(obj_days)

    return obj_days


def GetIntervalDays(aday,bday,step=50):
    bday, aday = sorted([aday,bday])
    days = list()
    N = 1
    while True:
       days = GetNWorkDays(aday,step*N)
       if days[0]<=bday:
           break
       else:
           N+=1
    days = [day for day in days if day>=bday]
    print(days)
    return days


def GetLatestWorkDay():
    ad = datetime.datetime.today().strftime('%Y-%m-%d')
    #ad = '2023-07-06'
    anow = datetime.datetime.now()
    if (anow.hour<15 or anow.weekday()>=5) and os.path.exists("./dump/2023/stock_data_{}.csv".format(ad)) is False:
        days = GetNWorkDays(ad,7)
        days = [day for day in days if day<ad]
        ad = days[-1]
    return ad

#GetNWorkDays('2023-01-07',-2,2023)
#days = GetIntervalDays('2021-01-01','2021-12-31'); print(len(days))
