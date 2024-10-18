import json
import time
import os
import requests
from datetime import datetime
import random
import sys
import pandas as pd


#
#json_url = "http://48.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402508937289440778_1658838703304&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1658838703305"
#
#res = requests.get(json_url)
#
#result = res.text.split("jQuery112402508937289440778_1658838703304")[1].split("(")[1].split(");")[0]
#result_json = json.loads(result)
#result_json


class DumpInfo(object):
    def __init__(self):
        self.last_page = 500 if len(sys.argv)!=2 else int(sys.argv[1])+1
        self.date = datetime.today().strftime('%Y-%m-%d') 
        self.stage = self.getStage()
        self.file_name = self.createFile()
        #self.last_page = 500 if len(sys.argv)!=2 else int(sys.argv[1])+1

    def getStage(self):
       now = datetime.now()
       hour = now.hour
       minute = now.minute
       if len(str(hour))==1: hour= '0'+str(hour)
       if len(str(minute))==1: minute= '0'+str(minute)
       time = '{}-{}'.format(hour,minute)
       if time>='09-25' and time<'09-30' and len(sys.argv)!=2:
           self.stage = 1
       elif time >='11-30' and time<'12-55' and len(sys.argv)!=2:
           self.stage = 2
       elif time >='15-00' and len(sys.argv)!=2:
           self.stage = 3
       else: 
           self.stage = 'tmp'
           self.last_page = 5 if len(sys.argv)!=2 else int(sys.argv[1])+1
       print('INFO::stage_num={}'.format(self.stage))
       print('INFO::page_num={}'.format(self.last_page))
       return self.stage

    def createFile(self):
       file_name = "./dump/{}/stock_data_{}_{}.csv".format(self.date[:4],self.date,self.stage)
       print('INFO::file_name={}'.format(file_name))
       if os.path.exists(file_name):
           os.system('rm {}'.format(file_name))
           print('INFO::remove {}'.format(file_name))
       with open(file_name, 'a+', encoding='utf-8') as f:
           f.write("股票代码,股票名称,最新价,涨跌幅,涨跌额,成交量（手）,成交额,振幅,换手率,市盈率,量比,最高,最低,今开,昨收,市净率\n")
       return file_name

    def saveData(self,data,date):
       #file_name = "./dump/2024/stock_data_{}.csv".format(date[:4])
       with open(self.file_name, "a+", encoding='utf-8') as f:
           for i in data:
               Code = i["f12"]
               Name = i["f14"]
               Close = i['f2']
               ChangePercent = i["f3"]
               Change = i['f4']
               Volume = i['f5']
               Amount = i['f6']
               Amplitude = i['f7']
               TurnoverRate = i['f8']
               PERation = i['f9']
               VolumeRate = i['f10']
               Hign = i['f15']
               Low = i['f16']
               Open = i['f17']
               PreviousClose = i['f18']
               PB = i['f22']
               row = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
                   Code,Name,Close,ChangePercent,Change,Volume,Amount,Amplitude,
                   TurnoverRate,PERation,VolumeRate,Hign,Low,Open,PreviousClose,PB)
               f.write(row)
               f.write('\n')

    def dumpInfo(self):
        for i in range(1, self.last_page):
            print("INFO::抓取网页%s" % str(i))
            json_url = "http://48.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402508937289440778_1658838703304&pn=%s&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1658838703305" % str(i)
            res = requests.get(json_url)
            result = res.text.split("jQuery112402508937289440778_1658838703304")[1].split("(")[1].split(");")[0]
            result_json = json.loads(result)
            #print(result_json)
            if result_json['data'] is None: break
            stock_data = result_json['data']['diff']
            if len(stock_data)>0:
                self.saveData(stock_data,self.date)
            if len(stock_data)<20:
                break
        print('INFO::下载数据: {}'.format(self.date))
        #print("抓取网页%s" % str(i))


    def printInfo(self):
        #if len(sys.argv)!=2:
        #date = datetime.today().strftime('%Y-%m-%d')
        types = {'股票代码':'str'}
        adf = pd.read_csv(self.file_name,dtype=types)
        b1df = adf[adf['股票代码'].apply(lambda x: x.startswith('4') or x.startswith('8') or x.startswith('9'))].reset_index(drop=True)
        b2df = adf[adf['股票代码'].apply(lambda x: x.startswith('3'))].reset_index(drop=True)
        c1df = adf[adf['股票代码'].apply(lambda x: x.startswith('688'))].reset_index(drop=True)
        c2df = adf[adf['股票代码'].apply(lambda x: (x.startswith('6') or x.startswith('0')) and (x.startswith('688') is False))].reset_index(drop=True)
        pd.set_option('display.max_rows',None)
        #print(adf[['股票代码','股票名称','最新价','涨跌幅']][:10])
        print(b1df[['股票代码','股票名称','最新价','涨跌幅']][:20])
        print(b2df[['股票代码','股票名称','最新价','涨跌幅']][:20])
        #print(c1df[['股票代码','股票名称','最新价','涨跌幅']][:10])
        print(c2df[['股票代码','股票名称','最新价','涨跌幅']][:50])

    def run(self):
        self.dumpInfo()
        self.printInfo()


if __name__ == '__main__':
    #aday = datetime.today().strftime('%Y-%m-%d')
    #create_file(aday)
    exam = DumpInfo()
    exam.run()


