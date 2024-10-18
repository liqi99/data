"""
===========================
@Time : 2023/7/26 20:13
@File : stock_day
@Software: PyCharm
@Platform: Win10
@Author : DataShare
===========================
"""
import akshare as ak
import pandas as pd
import datetime
import sys


def stock_to_excel(stock_code, stock_name):
    if stock_code[0] == '6':
        market = 'sh'
    elif stock_code[0] == '0':
        market = 'sz'

    df1 = ak.stock_zh_a_spot_em()
    df2 = df1[df1['代码'] == stock_code]

    dt = str(datetime.date.today())   #当日
    df3 = ak.stock_individual_fund_flow(stock=stock_code, market=market) #在15:00之后获取
    df4 = df3[df3['日期'] == dt]

    result = {
        "日期": dt,
        "股票代码": stock_code,
        "股票名称": stock_name,
        "前一日收盘价": df2['昨收'].to_list()[0],
        "开盘": df2['今开'].to_list()[0],
        "收盘": df2['最新价'].to_list()[0],
        "最高": df2['最高'].to_list()[0],
        "最低": df2['最低'].to_list()[0],
        "成交量": df2['成交量'].to_list()[0],
        "成交额": df2['成交额'].to_list()[0],
        "振幅": df2['振幅'].to_list()[0],
        "涨跌幅": df2['涨跌幅'].to_list()[0],
        "涨跌额": df2['涨跌额'].to_list()[0],
        "换手率": df2['换手率'].to_list()[0],
        "量比": df2['量比'].to_list()[0],
        "市盈率-动态": df2['市盈率-动态'].to_list()[0],
        "市净率": df2['市净率'].to_list()[0],
        "60日涨跌幅": df2['60日涨跌幅'].to_list()[0],
        "主力净流入-净额": df4['主力净流入-净额'].to_list()[0],
        "主力净流入-净占比": df4['主力净流入-净占比'].to_list()[0],
        "超大单净流入-净额": df4['超大单净流入-净额'].to_list()[0],
        "超大单净流入-净占比": df4['超大单净流入-净占比'].to_list()[0],
        "大单净流入-净额": df4['大单净流入-净额'].to_list()[0],
        "大单净流入-净占比": df4['大单净流入-净占比'].to_list()[0],
        "中单净流入-净额": df4['中单净流入-净额'].to_list()[0],
        "中单净流入-净占比": df4['中单净流入-净占比'].to_list()[0],
        "小单净流入-净额": df4['小单净流入-净额'].to_list()[0],
        "小单净流入-净占比": df4['小单净流入-净占比'].to_list()[0]
    }

    return result


if __name__ == '__main__':
    stocks_code = {'000651': '格力电器',
                   '002241': '歌尔股份',
                   '002739': '万达电影',
                   '600956': '新天绿能',
                   '600031': '三一重工',
                   '600703': '三安光电',
                   '002027': '分众传媒',
                   '600030': '中信证券',
                   '002939': '长城证券',
                   }   #小编买过的股票
    
    dt = str(datetime.date.today())
    results=[]
    for stock_code, stock_name in stocks_code.items():
        print(f'{stock_name}:{stock_code}')
        try:
            results.append(stock_to_excel(stock_code, stock_name))
        except Exception as e:
            print("运行中出错",e)
            sys.exit(-1)
    
    pd.DataFrame.from_dict(results).to_excel(f'./data/{dt}.xlsx', index=False)


