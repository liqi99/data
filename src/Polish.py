import os,sys

import pandas as pd
import time
import datetime
from StockDay import GetNWorkDays
import numpy as np


pd.set_option('display.max_rows',None)
#pd.set_option('display.max_columns',None)


def refreshA(x):
    if x == '-':
        return np.nan
    else:
        return float(x)

def refreshCode(x):
    x = str(x)
    if len(x) !=6:
        x = (6-len(x))*'0'+x
        return x
    else: return x

def amount(x):
    x = float(x)
    if x>=1e8:
        x = x/1e8
        x = round(x,2)
        x = str(x)+'亿'
    elif x>1e7:
        x = x/1e7
        x = round(x,2)
        x = str(x)+'千万'
    elif x>1e6:
        x = x/1e7
        x = round(x,2)
        x = str(x)+'百万'
    elif x>1e4:
        x = x/1e4
        x = round(x,2)
        x = str(x)+'万'

    return x

def isToTopDown(x_amp,x_obj,code,name,x_now=None):
    #x_yest = str(x_yest)
    #if x_yest.strip() == '-' or x_yest.strip() == '': 
    #    return False,False
    # x_yest 涨跌额
    #print(x_yest,x_obj,code,name)
    x_amp  = float(x_amp)
    x_obj = float(x_obj)
    if x_now is not None:
        #print('debug',x_now)
        x_now = float(str(x_now))
        x_yest = x_now-x_amp
    else:
        x_yest = x_obj-x_amp

    rate_h,rate_l = 0,0
    if code.startswith('00') or code.startswith('60'): 
        if name.startswith('N') or name.startswith('C'): #上市首日，最高涨44%，最低跌-36%，第二天开始10%上下涨幅限制
            rate_h, rate_l = False,False
        else:
            if name.startswith('ST') or name.startswith('*ST'): 
                rate_h,rate_l = 0.05,-0.05
            else: 
                rate_h,rate_l = 0.1,-0.1
    elif code.startswith('30') or code.startswith('68'):
        if name.startswith('N') or name.startswith('C'):
            return False,False
        else:
            rate_h, rate_l = 0.2,-0.2
    elif code.startswith('8') or code.startswith('4'): 
        if name.startswith('N'):
            rate_h,rate_l = False,False
        else:
            rate_h,rate_l = 0.3,-0.3

    len_h = NRound(x_yest*rate_h)
    len_l = NRound(x_yest*rate_l)
    #len_h = np.round(x_yest*rate_h,2)
    #len_l = np.round(x_yest*rate_l,2)
    #print(len_h,len_l)
    toTop = x_yest+len_h
    toLow = x_yest+len_l

    #if code == '000100':
    #    print(rate_h,rate_l)
    #    print(toTop,toLow) 
    #    print(x_today,x_yest)
    #    exit()

    if abs(x_obj-toTop)<1e-3 or abs(x_obj-toTop-0.01)<1e-5: return True,False
    if abs(x_obj-toLow)<1e-3 or abs(x_obj-toLow+0.01)<1e-5: return False,True
    else: 
        return False,False

def NRound(an):
    amp = str(float(an))+'000'
     
    tmp_amp = '+'
    if '-' in amp: 
        tmp_amp = '-'
        amp = amp[1:]

    #print(amp)
    amp = amp.split('.')
    #print(amp)
    d_3 = int(amp[1][2])
    amp = amp[0]+'.'+amp[1][:2]
    amp = float(amp)
    #amp = round(amp,2)
    if d_3>=5:
        amp = amp+0.0100
    len_hl = amp
    if tmp_amp =='-': 
        len_hl = 0-len_hl
    return len_hl
