from datetime import datetime,timedelta



def getToday():
    today_str = datetime.now().strftime('%Y%m%d')
    return today_str

def getNday(N):
    nday = datetime.now()+timedelta(N)
    nday = nday.strftime('%Y%m%d')
    return nday
