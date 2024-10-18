import json
import time
import os
import requests
from datetime import datetime
import random


def save_date(data,Q_No):
    with open(file_name, "a+", encoding='utf-8') as f:
        for s_data in data:
            code = s_data['SECURITY_CODE']
            name = s_data['SECURITY_NAME_ABBR']
            income = s_data['TOTAL_OPERATE_INCOME'] #营业收入（万）
            income_y_inc_rate = s_data['YSTZ'] #营业收入同比增长率
            income_m_inc_rate = s_data['YSHZ'] #营业收入环比增长率
            profit = s_data['PARENT_NETPROFIT'] #净利润
            profit_y_rate = s_data['SJLTZ'] #净利润同比增长率
            profit_m_rate = s_data['SJLHZ'] #净利润环比增长率
            roe = s_data['WEIGHTAVG_ROE'] #净资产收益率
            bps = s_data['BPS'] #每股净资产
            eps = s_data['BASIC_EPS'] #每股收益
            industry = s_data['PUBLISHNAME'] #行业
            rep_date = s_data['UPDATE_DATE']
            atype = s_data['SECURITY_TYPE']
            row = "{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(code,name, income, income_y_inc_rate, income_m_inc_rate, 
                            profit, profit_y_rate, profit_m_rate, eps,bps,roe, industry,rep_date,atype)
            f.write(row)
            f.write('\n')
          
def create_file():
   if os.path.exists(file_name):
       os.system('rm {}'.format(file_name))
       print('remove {}'.format(file_name))
   with open(file_name, 'a+', encoding='utf-8') as f:
       f.write("股票代码,股票名称,营业收入,营业收入同比,营业收入环比,净利润,净利润同比,净利润环比,每股收益,每股净资产,净资产收益率,所属行业,报告时间,AB股\n")


def main(url):
    for i in range(1, 200):
        print("抓取网页%s" % str(i))
        json_url = url.format(i)
        #print(json_url)
        res = requests.get(json_url)
        res = res.text
        #print(res)
        result = res.split("jQuery1123035942327538932894_1688889790270")[1][1:-2]#split("(")[1].split(");")[0]
        #print(result)
        result_json = json.loads(result)
        #except Exception:
        #    print(result)
        if result_json['result'] is None: break
        stock_data = result_json['result']['data']

        if len(stock_data)>0:
            save_date(stock_data,Q_No)

        if len(stock_data)<50:
            break
        #print(stock_data[0])

if __name__ == '__main__':
    Q_No = '2023-06-30'
    global file_name
    file_name = "/Users/liqi/stockData/dump/QR_{}.csv".format(Q_No)

    create_file()

    json_url = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123035942327538932894_1688889790270&sortColumns=UPDATE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=50&pageNumber={}&reportName=RPT_LICO_FN_CPD&columns=ALL&filter=(REPORTDATE%3D%27"+Q_No+"%27)"
    main(json_url) #ALL

