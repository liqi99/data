import json
import time
import os
import requests
from datetime import datetime
import random


def save_date(data,Q_No):
#{"SECURITY_CODE":"600596",
#"SECURITY_NAME_ABBR":"新安股份",
#"TRADE_MARKET":"上交所主板",
#"TRADE_MARKET_CODE":"069001001001",
#"SECURITY_TYPE":"A股",
#"SECURITY_TYPE_CODE":"058001001",
#"UPDATE_DATE":"2023-04-15 00:00:00",
#"REPORT_DATE":"2022-12-31 00:00:00",
#"BASIC_EPS":2.5796,
#"TOTAL_OPERATE_INCOME":21827830100,
#"TOTAL_OPERATE_INCOME_SQ":18976663600,
#"PARENT_NETPROFIT":2955587500,
#"PARENT_NETPROFIT_SQ":2654485500,
#"PARENT_BVPS":10.08,
#"WEIGHTAVG_ROE":29.04,
#"YSTZ":15.024593153456,
#"JLRTBZCL":11.343139753448,
#"DJDYSHZ":-22.702000025774,
#"DJDJLHZ":-83.4489426684,
#"PUBLISHNAME":"农药兽药",
#"ORG_CODE":"10002654",
#"NOTICE_DATE":"2023-04-15 00:00:00",
#"QDATE":"2022Q4",
#"DATATYPE":"2022年 年报",
#"MARKET":"0101",
#"ISNEW":"1",
#"EITIME":"2023-04-14 17:14:14",
#"SECUCODE":"600596.SH"
#}

    with open(file_name, "a+", encoding='utf-8') as f:
        for s_data in data:
            code = s_data['SECURITY_CODE']
            name = s_data['SECURITY_NAME_ABBR']

            income = s_data['TOTAL_OPERATE_INCOME'] #营业收入（万）
            income_y_inc_rate = s_data['YSTZ'] #营业收入同比增长率
            income_m_inc_rate = s_data['DJDYSHZ'] #营业收入环比增长率
            income_last_y = s_data['TOTAL_OPERATE_INCOME_SQ'] #去年营业收入

            profit = s_data['PARENT_NETPROFIT'] #净利润
            profit_last_y = s_data['PARENT_NETPROFIT_SQ'] #去年净利润
            profit_y_rate = s_data['JLRTBZCL'] #净利润同比增长率
            profit_m_rate = s_data['DJDJLHZ'] #净利润环比增长率

            roe = s_data['WEIGHTAVG_ROE'] #净资产收益率
            bps = s_data['PARENT_BVPS'] #每股净资产
            eps = s_data['BASIC_EPS'] #每股收益
            industry = s_data['PUBLISHNAME'] #行业
            rep_date = s_data['UPDATE_DATE']
            atype = s_data['SECURITY_TYPE']
            row = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(code,name, income, income_y_inc_rate, income_m_inc_rate, income_last_y,
                            profit, profit_y_rate, profit_m_rate, profit_last_y, roe, bps, eps, industry, rep_date, atype)
            f.write(row)
            f.write('\n')
          
def create_file(Q_No):
   if os.path.exists(file_name):
       os.system('rm {}'.format(file_name))
       print('remove {}'.format(file_name))
   with open(file_name, 'a+', encoding='utf-8') as f:
       f.write("股票代码,股票名称,营业收入,营业收入同比,营业收入环比,去年营业收入,净利润,净利润同比,净利润环比,去年净利润,净资产收益率,每股净资产,每股收益,所属行业,报告时间,AB股\n")


def main(url):
    for i in range(1, 200):
        print("抓取网页%s" % str(i))
        json_url = url.format(i)
        #print(json_url)
        res = requests.get(json_url)
        res = res.text
        #print(res)
        result = res.split("jQuery1123041164226693770234_1688887510584")[1][1:-2]#split("(")[1].split(");")[0]
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
    file_name = "/Users/liqi/stockData/dump/QQuickR_{}.csv".format(Q_No)

    create_file(Q_No)

    json_url = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123041164226693770234_1688887510584&sortColumns=UPDATE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=50&pageNumber={}&reportName=RPT_FCI_PERFORMANCEE&columns=ALL&filter=(SECURITY_TYPE_CODE+in+(%22058001001%22%2C%22058001008%22))(TRADE_MARKET_CODE!%3D%22069001017%22)(REPORT_DATE%3D%27"+Q_No+"%27)"
    main(json_url) #京市


