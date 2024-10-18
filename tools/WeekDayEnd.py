import time
import datetime


def weekD(astr):
    aday = datetime.datetime.strptime(astr, '%Y-%m-%d')
    dayw = aday.weekday()
    if dayw not in [5,6]: return 0
    elif dayw in [5,6]: return 1

def whichDay(astr):
    aday = datetime.datetime.strptime(astr, '%Y-%m-%d')
    dayw = aday.weekday()

    dayD = {
            0:'星期一',
            1:'星期二',
            2:'星期三',
            3:'星期四',
            4:'星期五',
            5:'星期六',
            6:'星期日',
           }

    return dayw, dayD[dayw]
