#https://www.jianshu.com/p/997576830608
import requests
import xlwt
import time
import json


# 第一步：抓取中彩网数据
def requests_data(index):
  cookies = {
        'Hm_lvt_12e4883fd1649d006e3ae22a39f97330': '1606980',
        '_ga': 'GA1.2.1535259899.1606980613',
        'PHPSESSID': 'ko9acne5fc09ag34tauema9dk5',
        'Hm_lvt_692bd5f9c07d3ebd0063062fb0d7622f': '1606980',
        'Hm_lpvt_692bd5f9c07d3ebd0063062fb0d7622f': '1606980',
        '_gid': 'GA1.2.702530936.16077449',
        'Hm_lpvt_12e4883fd1649d006e3ae22a39f97330': '1607745',
    }

  headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Referer': 'https://www.zhcw.com/kjxx/3d/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

  params = (
        ('callback', 'jQuery1122035713028555611515_1607745050216'),
        ('transactionType', '10001001'),
        ('lotteryId', '2'),
        ('issueCount', '210'),
        ('startIssue', ''),
        ('endIssue', ''),
        ('startDate', ''),
        ('endDate', ''),
        ('type', '0'),
        ('pageNum', index),
        ('pageSize', '30'),
        ('tt', '0.7235300526774737'),
        ('_', '1607745050225'),
    )
    # 获取服务器返回数据 
  response = requests.get('https://jc.zhcw.com/port/client_json.php', headers=headers, params=params, cookies=cookies).content.decode('utf-8')
  response = response.split('jQuery1122035713028555611515_1607745050216')[-1][1:-1]
  # print(response)
  #time.sleep(60)
  return response
   

# 第二步： 处理数据 并 存储
def save_data(tony_dict,res):
    for item in tony_dict:
        #sheet.write(j, 0, item['issue'])
        #sheet.write(j, 1, item['openTime'])
        #sheet.write(j, 2, item['frontWinningNum'])
        #sheet.write(j, 3, item['saleMoney'])
        #wd=item['winnerDetails']
        #print(item['issue'],item['frontWinningNum'],item['saleMoney'],item['openTime'])
        n1,n2,n3 = item['frontWinningNum'].split(' ')
        #if n1 == n2 and n1 ==n3: 
        #    print('豹子')
        nums = item['frontWinningNum'].split(' ')
        nums = [int(it.strip()) for it in nums]
        total = sum(nums)
        print(item['issue'],item['frontWinningNum'],round(int(item['saleMoney'])/1E8,2),item['openTime'],total)
        res.write('\t'.join([item['issue'],item['frontWinningNum'],item['saleMoney'],item['openTime']])+'\n')
        #if item['openTime'] == '2016-12-15': exit()
        #print('\n')
        


if __name__ == '__main__':
  res = open('res_log.csv','w')
  for index in range(1, 20):
    tony_dict=requests_data(index)
    tony_dict = json.loads(tony_dict)
    #print(type(tony_dict))
    #print(tony_dict.keys())
    if tony_dict is None or len(tony_dict['data']) ==0: continue
    save_data(tony_dict['data'],res)
    #time.sleep(60)

  res.close()

