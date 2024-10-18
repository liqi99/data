import os
import pandas as pd

import sys
import time
from StockDay import *
import datetime
from ReadIn import readOne


def showST(aday):
    adf = readOne(aday)
    print(adf['股票名称'])
    adf = adf[adf['股票名称'].apply(lambda x: 'st' in x.lower())]
    print(adf)
    print(adf.shape)


if __name__ == '__main__':

    ad = GetLatestWorkDay()

    print(ad)
    showST(ad)
