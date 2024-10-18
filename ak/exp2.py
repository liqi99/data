date_mapping_1 = {
    "03-31": "季度报告：",
    "06-30": "半年度报告：",
    "09-30": "季度报告：",
    "12-31": "年度报告："
}
date_mapping_2 = {
    "03-31": "Q1",
    "06-30": "H1",
    "09-30": "前三季度",
    "12-31": "年"
}
  
  
def get_summary():
    period = period_entry.get()
    code_list = code_list_entry.get().split(',')
    try:
        results = []  # 输出结果
  
        title = date_mapping_1.get(period[5:], "未知")  # 摘要标题
        if title == "未知":
            messagebox.showerror("报告期错误")
            return  # 结束函数的运行
        quarter = date_mapping_2.get(period[5:], "未知")  # 季度描述
  
        # 获取去年同期的报告期字符串
        year = period[:4]  # 获取前四个字符
        int_year = int(year) - 1  # 将前四个字符转换为数字并减去1
        last_year = str(int_year).zfill(4)  # 将得到的数字转换为字符串，补齐至四位
        yoy_period = period.replace(year, last_year, 1)  # 替换字符串的前四个字符，得到去年同期的报告期
  
        period_desc = f"{title}公司{year}{quarter}"
  
        # 对每个输入的code取数据
        for code in code_list:
            # 检查code能否匹配公司
            try:
                company = ak.stock_individual_info_em(symbol=code)
                name = company.iloc[5][1]
            except KeyError:
                results.append(f"[code]：无法匹配\n")
                continue
            # 从同花顺获取关键财务指标
            try:
                data = ak.stock_financial_abstract_ths(symbol=code, indicator="按报告期")
                data = data.set_index(data.columns[0])
            except KeyError:
                results.append(f"[code]：{name}获取财报数据失败\n")
                continue
            # 判断是否存在数据
            try:
                revenue = remove_unit(data.loc[period, "营业总收入"])
                revenue_change = str2percentage(data.loc[period, "营业总收入同比增长率"])
                profit = remove_unit(data.loc[period, "净利润"])
                profit_change = str2percentage(data.loc[period, "净利润同比增长率"])
                # 获取去年归母净利润数据
                pre_profit = remove_unit(data.loc[yoy_period, "净利润"])
            except KeyError:
                results.append(f"[code]：{name}报告未更新\n")
                continue
  
            # 调用函数获取财报摘要，并保存在输出列表中
            summary = generate_summary(name, period_desc, revenue, revenue_change, profit, profit_change, pre_profit)
            results.append(f"{summary}\n")
        result_text.config(state='normal')  # 将输出区域状态更改为可编辑
        result_text.delete('1.0', tk.END)  # 清空区域
        result_text.insert(tk.END, "\n".join(results))  # 将输出列表中的内容以换行符分隔，添加到输出区域中
        result_text.config(state='disabled')  # 将输出区域状态更改为不可编辑
    except Exception as e:
        messagebox.showerror("Error", f"获取摘要时出错：{str(e)}")
  
  
# 创建主窗口
root = tk.Tk()
root.title("日报-财务报告摘要akshare")
  
# 添加标签和输入框
period_label = tk.Label(root, text="请输入报告期（如2023-06-30）")
period_label.pack()
  
period_entry = tk.Entry(root)
period_entry.pack()
  
code_list_label = tk.Label(root, text="请输入公司code（多个则以英文逗号分隔）")
code_list_label.pack()
  
code_list_entry = tk.Entry(root, width=100)
code_list_entry.pack()
  
# 添加按钮
run_button = tk.Button(root, text="运行", command=get_summary)
run_button.pack()
  
# 添加结果显示区域
result_text = tk.Text(root, height=30, width=120, state='disabled')
result_text.pack()
  
# 启动 GUI 循环
root.mainloop()
