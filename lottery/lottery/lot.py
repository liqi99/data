import os,sys
import pandas as pd

def readin():
    adf = pd.read_csv('numbers.txt',sep=',',index_col=0)
    print(adf)
    return adf


res = readin()
resall = list()

i=6
while(i):
    res1 = res.iloc[0-i,:].tolist()
    i -=1
    print(res1)
    resall.extend(res1)

resall = sorted(resall)

from collections import Counter
resall = Counter(resall)

print(resall)
resall = list(resall.keys())
print(resall)
print(len(resall))
