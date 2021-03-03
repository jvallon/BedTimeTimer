# import sched, time
# s = sched.scheduler(time.time, time.sleep)

# def print_time(a='default'):
#     print("print_time", time.time(), a)

# print(time.time())
# s.enter(7,1,print_time,argument=('first',))
# s.enter(6,1,print_time,argument=('second',))
# s.enter(5,1,print_time,argument=('third',))
# s.run()

from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# from apscheduler.triggers.interval import IntervalTrigger
# from apscheduler.triggers.combining import AndTrigger
from datetime import date, datetime, timedelta
import time

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('cron', hour=22)
def red():
    print("red")

def yellow():
    print("yellow")

@scheduler.scheduled_job('cron', hour=5)
def green():
    print("green")

# scheduler.add_job(red,'cron', CronTrigger(datetime=datetime.now() + timedelta(seconds=10)))
# scheduler.add_job(red,'cron', CronTrigger(datetime=datetime.now() + timedelta(seconds=20)))
scheduler.add_job(red)
scheduler.add_job(yellow,'date', run_date=datetime.now() + timedelta(seconds=5))
scheduler.start()
while(True):
    x = 1