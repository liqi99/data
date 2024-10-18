import random


#dlt
res = []
while(len(res)<6):
    num = random.randint(1,35)
    if num not in res:
        res.append(num)

res = sorted(res)
#print(res)

suffixes = []
while(len(suffixes)<2):
    num = random.randint(1,12)
    if num not in suffixes:
        suffixes.append(num)

suffixes = sorted(suffixes)
print(res, suffixes)


#ssq
res = []
while(len(res)<6):
    num = random.randint(1,33)
    if num not in res:
        res.append(num)

res = sorted(res)
#print(res)

suffixes = []
num = random.randint(1,16)
suffixes.append(num)

suffixes = sorted(suffixes)
print(res, suffixes)
