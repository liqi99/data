import os


fs = os.listdir('./')

ad = [f for f in fs if '.' not in f]
af = [f for f in fs if '.' in f]
print(ad)
print(af)

for d in ad:
    #print(d)
    tmp_fs = os.listdir('./'+d)
    #print(tmp_fs)

    for tmp_f in tmp_fs:
        if '-' in tmp_f:
            #print('{0}/{1}'.format(d,tmp_f))
            #aok = input('请输入同不同意(y/n):')
            aok = 'y'
            if aok == 'y':
                res_f = tmp_f.split('-')[1]
                #print('{0}/{1} -- {0}/{2}'.format(d,tmp_f,res_f))
                if res_f in tmp_fs: 
                    print(res_f)
                    time.sleep(60)
                print('mv ./{0}/{1} to ./{0}/{2}'.format(d,tmp_f,res_f))
                os.system('mv ./{0}/{1} ./{0}/{2}'.format(d,tmp_f,res_f))    
            if aok == 'n':
                print(tmp_f, '没有被换名字')
    #print('\n')
