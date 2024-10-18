import os
from WeekDayEnd import *
from DateDeduce import *
import datetime
import numpy as np


def parseHol(ayear):
    res = list()
    local_path = os.getcwd()
    with open('{}/data/vocation_{}.txt'.format(local_path,ayear), 'r') as f:
        for l in f.readlines():
            #print(l)
            l = l.strip().split('\t')
            if len(l) == 0: continue

            if l[2] != '无':
                its = l[2].split(',')
                for it in its:
                    ae = [it, 0, l[0]+'调休']
                    res.append(ae)

            hols = l[1].split(',')
            if len(hols) == 1: hols = [hols[0]]*2
            for hol in getInterval(hols[0],hols[1]): 
                ae = [hol, 2, l[0]]
                res.append(ae)
    return res

def judgeType(x,y):
    if x =='*' and y in [1,2,3,4,5]: return 0
    elif x =='*' and y in [6,7]: return 1
    elif x != '*': return x

def getYear(ayear):
    start = '{}-01-01'.format(ayear)
    n = 366

    dsdf = getNDaysDF(start,n)

    #print(dsdf)

    dsdf['dayofweek'] = dsdf['ds'].apply(lambda x: whichDay(x)[0]+1)
    #dsdf['星期几'] = dsdf['DS'].apply(lambda x: whichDay(x)[1])

    #dsdf= dsdf.rename(columns={'DS':'ds'})
    res = parseHol(ayear)
    res = np.array(res)

    #print('hhhh',len(res))
    #print('hhhh',res)

    holi = pd.DataFrame(res,columns= ['ds','日期类型','说明'])
    #print('hhhhh',len(holi))
    #print('hhhhh',holi)


    dsdf = pd.merge(dsdf,holi,how='outer',left_on=['ds'],right_on=['ds'])
    dsdf.fillna('*',inplace=True)
    dsdf['日期类型'] = dsdf.apply(lambda row: judgeType(row['日期类型'],row['dayofweek']), axis=1)
    dsdf['dayofweek'] = dsdf['ds'].apply(lambda x: whichDay(x)[0]+1)
    dsdf.sort_values(by=['ds'],inplace=True)
    dsdf.reset_index(drop=True,inplace=True)
    dsdf = dsdf[dsdf.ds<='{}-12-31'.format(ayear)]
    return dsdf

#这个函数产生你所希望看到的两个年之间所有day的星期几, 假期类型的dataframe
#侧重于排除在getYear()函数中导致的两个相邻年重复的日期的假期类型不一致的情况
#比如, 在getYear(2018)返回的df中2018-12-29日是星期六, 但是在
#getYear(2019)中返回2018-12-29日这天却是放元旦假期的调休, 调休, 调休
def getAllYears(yleft,yright):
    yleft = int(yleft)
    yright = int(yright)
    df = None
    while(yleft<=yright):
        #print(getYear(yleft))
        tmp = getYear(yleft)
        if df is None: df =tmp
        else: df = pd.concat([df,tmp])
        yleft +=1
        
    df.reset_index(drop=True,inplace=True)
    groupd = df.groupby(['ds'], as_index=False).count()
    #print(groupd)
    obj_ds = groupd[groupd['说明']>1]['ds'].tolist()
    df = df.drop(df[(df.ds.isin(obj_ds)) & (df['说明']=='*')].index)
    df.reset_index(drop=True,inplace=True)
    return df

def getRepairedYear(ayear):
    #如果现实不是2020年，你应该把这里使用localtime去获取当前年，然后把下面2行的2020年替换成当前年
    thisyear = datetime.datetime.now().year
    print(thisyear)
    print(type(thisyear))
    #time.sleep(60000)
    if ayear>=thisyear: 
        ayear = thisyear
        df = getAllYears(thisyear-1,thisyear)
    else: 
        df = getAllYears(ayear-1,ayear+1)
    df = df[df.ds.apply(lambda x: int(x.split('-')[0]) == ayear)]
    df.reset_index(drop=True,inplace=True)
    return df

#print(getRepairedYear(2021))
    

