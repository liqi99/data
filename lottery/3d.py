import random
import os
import sys
import math
import numpy as np


times = 0

for i in range(0,10):
    for m in range(0,10):
        for n in range(0,10):
            #if i+m+n <12 and i+m+n>5 and len(list(set([i,n,m])))<=2 and i%2==1 and i==3:# and i%2==0 and m%2==1 and n%2==1: 
            if i in [1,5] and i+m+n in [13,14]:
                res = [i,m,n]
                if len(list(set(res)))==3:
                    times +=1
                    print([i,m,n])

print(times)


random.randint(0,33)
