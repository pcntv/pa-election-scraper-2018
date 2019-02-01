import schedule
import time
import time
import os

def job1():
    os.system('get_congress_percentages')
    print ("congress working", time.ctime())

def job2():
    os.system('gov')
    print ("working", time.ctime())

def job3():
    os.system('senate')
    print ("working", time.ctime())

def job4():
    os.system('congress')
    print ("working", time.ctime())

def job5():
    os.system('crawl')
    print ("working", time.ctime())

def job6():
    os.system('pahouse')
    print ("working", time.ctime())


schedule.every(10).seconds.do(job1)
schedule.every(10).seconds.do(job2)
schedule.every(10).seconds.do(job3)
schedule.every(10).seconds.do(job4)
schedule.every(10).seconds.do(job5)
schedule.every(10).seconds.do(job6)


while True:
    schedule.run_pending()
    time.sleep(1)


