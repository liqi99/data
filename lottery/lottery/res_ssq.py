ad = dict()
f = open('ssq_res.csv','r')
for l in f.readlines():
    l = l.replace('。','')
    l = l.strip().split(',')[:-1]

    print(l)
    for i in l:
        if '内蒙古' in i or '黑龙江' in i:
            name = i[:3]
            num = i[3:-1]
            i = i[:3]+'\t'+i[3:]
        else:
            name = i[:2]
            num = i[2:-1]
            i = i[:2]+'\t'+i[2:]
        if name not in ad:
            ad[name] = int(num)
        else:
            ad[name] = ad[name]+int(num)
        print(i)
ad = sorted(ad.items(),key=lambda x:x[1],reverse=True)
print(ad)
print(len(ad))
