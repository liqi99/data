import os


res = {}
for i in range(40,81):
    for j in range(40,81):
        for m in range(40,81):
            #print(i,j,m)
            tot = i+j+m
            if tot in res: res[tot].append([i,j,m])
            else: res[tot] = [[i,j,m]]
    
print(len(res))

all_item = 0
sub_item = 0
for key,val in res.items():
    #for it in val: 
    #    print(it)
    print(key,len(val))
    #print('\n')
    all_item+=len(val)
    if key>=200: sub_item+=len(val)
print(sub_item)
print(all_item)
print(41*41*41)
