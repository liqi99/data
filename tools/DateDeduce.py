import datetime
import time
import pandas as pd


def nDaysLater(aday, n):
    #today_time_array = time.localtime()
    #today = time.strftime('%Y-%m-%d', today_time_array)
    aday = datetime.datetime.strptime(aday, '%Y-%m-%d')
    #aday = aday.strftime('%Y-%m-%d')
    #n = 1-n
    offset = datetime.timedelta(days=n)
    nDaysL = (aday + offset).strftime('%Y-%m-%d')
    return nDaysL

def LastMon(amon=None):
    ''' amon='XXXX-XX'格式'''
    if amon is not None: return amon
    else:
        today = datetime.date.today()
        first = today.replace(day=1)
        #print(today, first)
        last_month = first - datetime.timedelta(days=1)
        amon = last_month.strftime("%Y-%m")
    return str(amon)

def getNDaysDF(start, n):
    days = list()
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    for i in range(n):
        offset = datetime.timedelta(days=i)
        re_date = (start + offset).strftime('%Y-%m-%d')
        days.append(re_date)
    #days.reverse()
    df = pd.DataFrame(days, columns=['ds'])
    return df

def getNMonIterator(start, n):
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    #print(type(start))
    month = start.month
    year = start.year

    for i in range(n):
        year = int(year)
        month = int(month)

        if month == 1:
            year = year-1
            month = 12
        else:
            month = month-1
        if len(str(month)) == 1:
            month = '0'+str(month)
        ym = str(year)+'-'+str(month)
        yield ym
    #pass

def getInterval(left, right):
    res = [left]
    tmp=left
    while(tmp<right):
        tmp = datetime.datetime.strptime(tmp, '%Y-%m-%d')
        offset = datetime.timedelta(days=1)
        tmp = (tmp + offset).strftime('%Y-%m-%d')
        res.append(tmp)
    return res

def getDaysDis(str_r,str_l):
    ds1 = datetime.datetime.strptime(str_r, '%Y-%m-%d')
    ds2 = datetime.datetime.strptime(str_l, '%Y-%m-%d')
    return (ds1-ds2).days

#print(getDaysDis('2020-09-01','2020-09-01'))
