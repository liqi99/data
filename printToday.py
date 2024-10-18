import os
import pandas as pd
import numpy as np
    
import sys
import time
from Polish import refreshCode,refreshA,isToTopDown,amount
from StockDay import *
import datetime
from ReadIn import readOne,defAmpLevel

from longTouAndShouBan import *
from ciXin import *
from st import *
    
pd.set_option('display.max_rows',None)
 

    
if __name__ == '__main__':
    ad = sys.argv
    if len(ad) ==2 and sys.argv[1]!='':
        ad = sys.argv[1]
        if len(ad)==8:
            ad = ad[:4]+'-'+ad[4:6]+'-'+ad[6:]
    elif len(ad)==1 or True:
        ad = GetLatestWorkDay()       
    adf = readOne(ad)
    print(adf[:50])
    print(adf[-20:])
