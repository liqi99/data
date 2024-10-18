import os
import time
import pandas as pd

atype = ['zuliu','zusan','baozi']

hezhi = [10,17]

i_jo=None;
j_jo=None;
m_jo=None;

i_jo=1;
j_jo=1;
m_jo=0;

baiwei_kuadu = [0,10] 
shiwei_kuadu = [0,10]
gewei_kuadu = [10,100]

adf = pd.read_csv('res_log.csv',sep='\t',names=['no','res','money','date'])
adf = adf.sort_values(by=['date']).reset_index(drop=True)
print(adf)

adict = {}

for i in range(0,10):
    pos = 'baiwei_{}'.format(i)
    adict[pos]=0
    pos = 'shiwei_{}'.format(i)
    adict[pos]=0
    pos = 'gewei_{}'.format(i)
    adict[pos]=0
#print(adict)

for i in adf.index:
    res = adf.res[i].split(' ')
    #print(res); break
    for i in range(0,10):
        if res[0] == str(i): adict['baiwei_{}'.format(i)] =0
        else: adict['baiwei_{}'.format(i)] -=1    
        if res[1] == str(i): adict['shiwei_{}'.format(i)] =0
        else: adict['shiwei_{}'.format(i)] -=1    
        if res[2] == str(i): adict['gewei_{}'.format(i)] =0
        else: adict['gewei_{}'.format(i)] -=1    

adict = dict(sorted(adict.items(),key=lambda x: x[0]))
for key,val in adict.items():
    adict[key] = abs(int(val))
print(adict)
#exit()

res = {}
res_zusan = {}
res_baozi = {}

for i in range(0,10):
    if i_jo is not None and i%2!=i_jo:continue
    pos = 'baiwei_{}'.format(i)
    if adict[pos]>=baiwei_kuadu[1] or adict[pos]<baiwei_kuadu[0]: continue
    for j in range(0,10):
        pos = 'shiwei_{}'.format(j)
        if adict[pos]>=shiwei_kuadu[1] or adict[pos]<shiwei_kuadu[0]: continue
        if j_jo is not None and j%2!=j_jo:continue
        for m in range(0,10):
            pos = 'gewei_{}'.format(m)
            if adict[pos]>=gewei_kuadu[1] or adict[pos]<gewei_kuadu[0]: 
                #print(i,adict[pos],gewei_kuadu[0],gewei_kuadu[1]);
                continue
            #print(i,adict[pos],gewei_kuadu[0],gewei_kuadu[1]);
            if m_jo is not None and m%2!=m_jo:continue

            tot = i+j+m

            if tot>=hezhi[0] and tot<=hezhi[1]: pass
            else: continue

            if i==j and j==m: 
                if atype[0] !='baozi':continue
                res_baozi[tot] = [[i,j,m]]; continue
            elif i==j or i==m or j==m:
                if atype[0] !='zusan':continue
                if tot in res_zusan: res_zusan[tot].append([i,j,m])
                else: res_zusan[tot] = [[i,j,m]]
                continue
            elif i!=j and i!=m and j!=m:    
                if atype[0] !='zuliu':continue
                if tot in res: res[tot].append([i,j,m])
                else: res[tot] = [[i,j,m]]
    
#print(len(res))
#print(len(res_zusan))
#print(len(res_baozi))

all_item = 0
for key,val in res.items():
    all_item +=len(val)
    print(key)
    print('  ', val)
for key,val in res_zusan.items():
    all_item +=len(val)
    print(key)
    print('  ', val)
for key,val in res_baozi.items():
    all_item +=len(val)
    print(key)
    print('  ', val)
print(all_item)
