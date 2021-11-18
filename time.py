import schedule
import time
import datetime
import random

from threading import Timer
from ro import ro

hour = random.randint(7,12)
minute = random.randint(0,59)

def doSth():
    ro()
    print(u'這個程式要開始瘋狂的運轉啦')

def main(h=hour,m=minute):
    print(h,m)
    while True:
        now = datetime.datetime.now()
        # print(now.hour, now.minute)
        if now.hour == h and now.minute == m:
            break
    
    doSth()

    # 每86400秒（1天），傳送1次
    t = Timer(86400, main)
    t.start()

# def job():
#     print("I'm working...")
#     ro()

# schedule.every(10).minutes.do(job) 
# schedule.every().hour.do(job)
# schedule.every().day.at('10:14').do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)   

# while True:  
#     schedule.run_pending()  
#     time.sleep(1)