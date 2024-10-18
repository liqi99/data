import json
import time
import os
import requests
from datetime import datetime
import random


def save_date(data,Q_No):
    with open(file_name, "a+", encoding='utf-8') as f:

#{"SECURITY_CODE":"600779",
#"SECURITY_NAME_ABBR":"水井坊",
#"REPORT_TYPE":"2",
#"REPORT_YEAR":"2023",
#"FIRST_APPOINT_DATE":"2023-07-29 00:00:00",
#"FIRST_CHANGE_DATE":null,
#"SECOND_CHANGE_DATE":null,
#"THIRD_CHANGE_DATE":null,
#"ACTUAL_PUBLISH_DATE":null,
#"SECURITY_TYPE_CODE":"058001001",
#"SECURITY_TYPE":"A股",
#"TRADE_MARKET_CODE":"069001001001",
#"TRADE_MARKET":"上交所主板",
#"REPORT_DATE":"2023-06-30 00:00:00",
#"APPOINT_PUBLISH_DATE":"2023-07-29 00:00:00",
#"RESIDUAL_DAYS":14,
#"REPORT_TYPE_NAME":"2023年 半年报",
#"IS_PUBLISH":"0",
#"MARKET":"0101",
#"EITIME":"2023-06-21 16:12:28",
#"SECUCODE":"600779.SH"},

        for s_data in data:
            code = s_data['SECURITY_CODE']
            name = s_data['SECURITY_NAME_ABBR']
            appo_date = s_data['FIRST_APPOINT_DATE']
            first_date = s_data['FIRST_CHANGE_DATE']
            second_date = s_data['SECOND_CHANGE_DATE']
            third_date = s_data['THIRD_CHANGE_DATE']
            true_date = s_data['ACTUAL_PUBLISH_DATE']
            atype = s_data['SECURITY_TYPE']
            row = "{},{},{},{},{},{},{}".format(code,name, appo_date, first_date, second_date, third_date, true_date, atype)
            f.write(row)
            f.write('\n')
          
def create_file():
   if os.path.exists(file_name):
       os.system('rm {}'.format(file_name))
       print('remove {}'.format(file_name))
   with open(file_name, 'a+', encoding='utf-8') as f:
       f.write("股票代码,股票名称, 首次预约时间, 第一次修改时间, 第二次修改时间, 第三次修改时间, 真实披露时间, AB股\n")

def main(url):
    for i in range(1, 200):
        print("抓取网页%s" % str(i))
        json_url = url.format(i)
        #print(json_url)
        res = requests.get(json_url)
        res = res.text
        #print(res)
        result = res.split("jQuery112305991071102465495_1689423718913")[1][1:-2]#split("(")[1].split(");")[0]
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
    file_name = "/Users/liqi/stockData/dump/QRYY_{}.csv".format(Q_No)

    create_file()

    json_url = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112305991071102465495_1689423718913&sortColumns=FIRST_APPOINT_DATE%2CSECURITY_CODE&sortTypes=1%2C1&pageSize=50&pageNumber={}&reportName=RPT_PUBLIC_BS_APPOIN&columns=ALL&filter=(SECURITY_TYPE_CODE+in+(%22058001001%22%2C%22058001008%22))(TRADE_MARKET_CODE!%3D%22069001017%22)(REPORT_DATE%3D%27"+Q_No+"%27)"
    main(json_url) #ALL

