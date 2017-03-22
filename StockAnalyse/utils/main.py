import requests
from services import hardenstock
from db import dbsource
from apscheduler.schedulers.background import BlockingScheduler


# 用于测试各个测试案列
if __name__ == "__main__":

    sched = BlockingScheduler()
    # sched.add_job(job_function,'interval', seconds=5)

    sched.add_job(lambda:dbsource.save_harden_stocks(),'cron', day_of_week='mon-fri', hour=23, minute=50)
    sched.add_job(lambda:hardenstock.cal_harden_hook(),'cron', day_of_week='mon-fri', hour=16, minute=10)

    sched.start()

    # port_info = {}
    # r = requests.get("http://47.88.13.37.144:5555/api/pre_harden",data=port_info)
    # print(r.text)


