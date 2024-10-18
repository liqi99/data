import os


def readTxt(afile):
    f = open(afile,'r').readlines()
    msg = ''.join(f)
    return msg
    
