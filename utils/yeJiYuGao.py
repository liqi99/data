import json
import time
import os
import requests
from datetime import datetime
import random


def save_date(data):
# {
#"SECUCODE":"002518.SZ",
##"SECURITY_CODE":"002518",
##"SECURITY_NAME_ABBR":"科士达",
#"ORG_CODE":"10132727",
#"NOTICE_DATE":"2023-07-08 00:00:00",
#"REPORT_DATE":"2023-06-30 00:00:00",
#"PREDICT_FINANCE_CODE":"003",
##"PREDICT_FINANCE":"每股收益",
##"PREDICT_AMT_LOWER":0.77,
##"PREDICT_AMT_UPPER":0.94,
##"ADD_AMP_LOWER":null,
##"ADD_AMP_UPPER":null,
#"PREDICT_CONTENT":"预计2023年1-6月每股收益盈利:0.77元至0.94元。",
#"CHANGE_REASON_EXPLAIN":"报告期内,公司结合市场需求情况,加快产品迭代和新产品开发,持续加大海内外销售渠道拓展力度。公司凭借全球渠道业务优势,数据中心、新能源光伏及储能业务板块均呈现出快速增长态势,从而带动公司整体业绩增长。",
#"PREDICT_TYPE":"预增",
##"PREYEAR_SAME_PERIOD":0.37,
#"TRADE_MARKET":"深交所主板",
#"TRADE_MARKET_CODE":"069001002001",
##"SECURITY_TYPE":"A股",
#"SECURITY_TYPE_CODE":"058001001",
#"INCREASE_JZ":null,
#"FORECAST_JZ":0.855,
#"FORECAST_STATE":"increase",
#"IS_LATEST":"T",
##"PREDICT_RATIO_LOWER":-7.5,
##"PREDICT_RATIO_UPPER":35,
#"PREDICT_HBMEAN":0.1375}
    with open(file_name, "a+", encoding='utf-8') as f:
        for s_data in data:
            code = s_data['SECURITY_CODE']
            name = s_data['SECURITY_NAME_ABBR']
            rtype = s_data['PREDICT_FINANCE']
            pred_num_l = s_data['PREDICT_AMT_LOWER'] 
            pred_num_u = s_data['PREDICT_AMT_UPPER'] 
            add_amt_l = s_data['ADD_AMP_LOWER'] 
            add_amt_u = s_data['ADD_AMP_UPPER'] 
            add_Q_inc_l = s_data['PREDICT_RATIO_LOWER']
            add_Q_inc_u = s_data['PREDICT_RATIO_UPPER']
            last_year_num = s_data['PREYEAR_SAME_PERIOD']
            atype = s_data['SECURITY_TYPE']
            rep_date = s_data['NOTICE_DATE']
            row = "{},{},{},{},{},{},{},{},{},{},{},{}".format(code, name, rtype, pred_num_l, pred_num_u, 
                                                                  add_amt_l, add_amt_u, add_Q_inc_l, add_Q_inc_u, last_year_num, atype, rep_date)
            f.write(row)
            f.write('\n')
          
def create_file():
   if os.path.exists(file_name):
       os.system('rm {}'.format(file_name))
       print('remove {}'.format(file_name))
   with open(file_name, 'a+', encoding='utf-8') as f:
       f.write("股票代码,股票名称,预测指标,预测数值下,预测数值上,同比下,同比上,环比下,环比上,去年数值,AB股,报告时间\n")


def main(url):
    for i in range(1, 200):
        print("抓取网页%s" % str(i))
        json_url = url.format(i)
        #print(json_url)
        res = requests.get(json_url)
        res = res.text
        #print(res)
        result = res.split("jQuery1123038799530802233795_1688869678040")[1][1:-2]#split("(")[1].split(");")[0]
        #print(result)
        result_json = json.loads(result)
        #except Exception:
        #    print(result)
        if result_json['result'] is None: break
        stock_data = result_json['result']['data']

        if len(stock_data)>0:
            save_date(stock_data)

        if len(stock_data)<50:
            break
        #print(stock_data[0])

if __name__ == '__main__':
    Q_No = '2023-06-30'
    global file_name
    file_name = "/Users/liqi/stockData/dump/QPredR_{}.csv".format(Q_No)

    create_file()

    json_url = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123038799530802233795_1688869678040&sortColumns=NOTICE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=50&pageNumber={}&reportName=RPT_PUBLIC_OP_NEWPREDICT&columns=ALL&filter=(REPORT_DATE%3D%27"+Q_No+"%27)"
    main(json_url) #沪深


