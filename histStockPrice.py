#首先导入需要用到的库
import requests
import pandas as pd
import json
import os,sys


#从网站获取指定股票的历史数据
def get_stock_data(stock_code,last_day,limit):
    #判断股票是上证沪指，还是深指或创业板
    if stock_code.startswith('6'): #代表是沪指上市公司
        v_HAList = 'ty-1-' + stock_code + '-%u6C64%u59C6%u732B'
        v_secid = '1.' + stock_code
    else :
        v_HAList = 'ty-0-' + stock_code + '-%u6C64%u59C6%u732B'
        v_secid = '0.' + stock_code
    cookies = {
    'qgqp_b_id': '79a11878738d85a3214f7e1622e357c0',
    'st_si': '26019701284765',
    'HAList': v_HAList,
    'st_asi': 'delete',
    'st_pvi': '37297162141235',
    'st_sp': '2023-02-14%2016%3A13%3A24',
    'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
    'st_sn': '13',
    'st_psi': '20230302173734493-111000300841-1579303040',
     }

    headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    #'Cookie': 'qgqp_b_id=79a11878738d85a3214f7e1622e357c0; st_si=26019701284765; HAList=ty-0-300498-%u6C64%u59C6%u732B; st_asi=delete; st_pvi=37297162141235; st_sp=2023-02-14%2016%3A13%3A24; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=13; st_psi=20230302173734493-111000300841-1579303040',
    'Referer': 'http://quote.eastmoney.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    params = {
    'cb': 'jQuery35108531420469859112_1677749719883',
    'secid': v_secid,
    'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
    'fields1': 'f1,f2,f3,f4,f5,f6',
    'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
    'klt': '101',
    'fqt': '1',
    #'end': '20221231',
    #'lmt': '242',
    'end': last_day,
    'lmt': limit,
    '_': '1677749719941',
    }

    response = requests.get(
    'http://17.push2his.eastmoney.com/api/qt/stock/kline/get',
    params = params,
    cookies = cookies,
    headers = headers,
    verify = False,
    )
    return response

#股票历史数据存放到DataFrame
def store_data_to_pandas(response):
    #剔除无用字符串，可以通过print(response.text)来直观的查看response的内容
    rep_text=response.text.replace('jQuery35108531420469859112_1677749719883(','').replace(');','')
    #生成dict
    json_data=json.loads(rep_text)
    #提取股票数据
    stock_data=json_data['data']['klines']
    #创建DataFrame存储股票数据
    pd_data=pd.DataFrame(columns=['股票代码','股票名称','交易日期','开盘价','收盘价','最高价','最低价','成交量','成交额','振幅','涨跌幅%','涨跌额'])
    #解析股票数据分别对应到Dataframe各列
    for i in range(len(stock_data)):
        pd_data.loc[i]=[json_data['data']['code'],json_data['data']['name'],stock_data[i].split(',')[0],stock_data[i].split(',')[1],stock_data[i].split(',')[2],stock_data[i].split(',')[3],stock_data[i].split(',')[4],stock_data[i].split(',')[5],stock_data[i].split(',')[6], stock_data[i].split(',')[7],stock_data[i].split(',')[8],stock_data[i].split(',')[9]]
    return pd_data


#批量获取股票历史数据
def dump_history_data():
    #final_data=pd.DataFrame(columns=['股票代码','股票名称','交易日期','开盘价','收盘价','最高价','最低价','成交量','成交额','振幅','涨跌幅%','涨跌额'])
    last_day = '2024-04-17'
    limit = 180

    file_name = './hist_dump/data_for_all_A_stock_{}.csv'.format(last_day)
    if os.path.exists(file_name):
        os.system('rm {}'.format(file_name))
        print('remove {}'.format(file_name))
    
    adf = pd.read_csv('./dump/2024/stock_data_2024-04-18.csv',sep=',')
    codes = adf['股票代码'].tolist()
    print('一共{}个股票'.format(len(codes)))
   
    last_day = last_day.replace('-','')
    limit = str(limit)
    j = 0
    for code in codes:
        j+=1
        if j%10==0: 
            print(j)

        code = str(code)
        if len(code)<6: 
            code = (6-len(code))*'0'+code

        try:
            tmp_value = store_data_to_pandas(get_stock_data(code,last_day,limit))
            if j == 1:
                tmp_value.to_csv(file_name,sep=',')
            else:
                tmp_value.to_csv(file_name,sep=',',mode='a',header=False)
        except Exception:
            continue
            print('Exception', code, j)
        #else:
        #    final_data=pd.concat([final_data,tmp_value])
    
    #final_data.to_csv('./hist_dump/oneweek_data_for_all_A_stock_20230518.csv',sep=',')
 

if __name__ == '__main__':   
    dump_history_data()    


