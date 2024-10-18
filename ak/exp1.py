def generate_summary(name, period_desc, revenue, revenue_change, profit, profit_change, pre_profit):
    if revenue_change > 0:
        revenue_desc = f"同比上升{revenue_change:.2f}%"
    elif revenue_change < 0:
        revenue_desc = f"同比下降{abs(revenue_change):.2f}%"
    else:
        revenue_desc = "同比持平"
  
    if profit >= 0 and pre_profit >= 0:
        if profit > pre_profit:
            profit_decs = f"同比上升{profit_change:.2f}%"
        elif profit < pre_profit:
            profit_decs = f"同比下降{abs(profit_change):.2f}%"
        else:
            profit_decs = "同比持平"
    elif profit > 0 > pre_profit:
        profit_decs = "扭亏为盈"
    elif profit < 0 < pre_profit:
        profit_decs = "转盈为亏"
    else:  # 连年亏损
        if abs(profit) > abs(pre_profit):
            profit_decs = "亏损扩大"
        elif abs(profit) < abs(pre_profit):
            profit_decs = "亏损减少"
        else:
            profit_decs = "同比持平"
    # 转化为亿元、万元的单位
    revenue = get_unit(revenue)
    profit = get_unit(profit)
  
    summary = f"【{name}】{period_desc}实现营业总收入{revenue}，{revenue_desc}；" \
              f"归母净利润{profit}，{profit_decs}。"
    return summary
