from weatherSys.objects_manage import redis_handling as redis_h

# from live_data import views
#
# status_warning_monitor = views.status_warning_monitor()

redis_manage = redis_h.redis_manage()
# from live_data import wind_data as wd
# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime
# import time


# def tick():
#     print('Tick! The time is: %s' % datetime.now())
#
#
#
# scheduler = BackgroundScheduler()
# # 每隔5秒执行一次
# scheduler.add_job(wd.wind_send, 'interval', seconds=3600)
# # 该部分调度是一个独立的线程
# scheduler.start()