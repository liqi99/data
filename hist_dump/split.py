import pandas as pd
import os

adf = pd.read_csv('data_for_all_A_stock_2024-04-17.csv')
print(adf)


for day in adf['交易日期'].unique():
    print(day)
    if day<='2023-11-01': continue
    tmp = adf[adf['交易日期']==day]
    year = day.split('-')[0]
    if os.path.exists('./'+year) is False:
        #print(year)
        os.mkdir('./'+year)
    tmp = tmp.sort_values(by=['涨跌幅%'],ascending=False).reset_index(drop=True)
    tmp.to_csv('./'+year+'/stock_price_{}.csv'.format(day))
