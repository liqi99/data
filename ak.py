import akshare as ak




ainfo = ak.stock_individual_info_em(symbol="000651")

print(ainfo)



#ak.stock_zh_a_hist(symbol="000651", 
#                   period="daily", 
#                   start_date="20230701", 
#                   end_date='20230725', 
#                   adjust=""   #不复权
#                  )

#资金流向
#ak.stock_individual_fund_flow(stock="000651", market="sz")


#买入卖出5档
#ak.stock_bid_ask_em(symbol="000651")
