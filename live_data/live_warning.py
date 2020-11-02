from . import layers_manage
from redis import StrictRedis
from weatherSys import db_handling as db
from asgiref.sync import async_to_sync
import time
import logging
import asyncio

class status_warning_monitor:
    def __init__(self):
        logging.info('run warning')
        self.redis_3 = StrictRedis(host='localhost', port=6379, db=3, decode_responses=True, password='hzg61270388*!')
        self.redis_0 = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True, password='hzg61270388*!')
        self.redis_2 = StrictRedis(host='localhost', port=6379, db=2, decode_responses=True, password='hzg61270388*!')
        loop_1 = asyncio.get_event_loop()
        loop_2 = asyncio.get_event_loop()
        asyncio.loop_1.run_until_complete(self.monitor_status())
        asyncio.loop_2.run_until_complete(self.monitor_warning())



    async def monitor_status(self):
        pubsub = self.redis_3.pubsub()
        pubsub.psubscribe("__keyevent@3__:hset")
        for data in pubsub.listen():
            if data:
                await self.map_point()

    async def monitor_warning(self):
        pubsub = self.redis_2.pubsub()
        pubsub.psubscribe("__keyevent@1__:*")
        for data in pubsub.listen():
            if data:
                await self.map_point()



    async def map_point(self):
        status = self.redis_3.keys('*')
        user = self.redis_0.keys('*')
        warning = self.redis_2.keys('*')
        map_point = []
        warning_type = {1: '高温预警', 2: '路面状况预警', 3: '能见度预警', 4: '降雨预警', 5: '大风预警'}
        warning_lev = {1: '红', 2: '橙', 3: '黄', 4: '蓝'}
        warning_type_en = {1: 'temperature', 2: 'road', 3: 'fog', 4: 'rianfall', 5: 'speed', None: 'normal'}
        warning_lev_en = {1: 'red', 2: 'orange', 3: 'yellow', 4: 'blue', None: 'green'}
        for x in status:
            status_data = self.redis_3.hgetall(x)
            lat_lon = [float(status_data['latitude']), float(status_data['longitude'])]
            status_data.pop('latitude')
            status_data.pop('longitude')
            status_data['lat_lon'] = lat_lon
            status_data['eid'] = x
            status_data['warning_level'] = 'green'
            status_data['warning_type'] = 'normal'
            status_data['description'] = ''
            status_data['obs_time'] = int(time.time())
            map_point.append(status_data)

        for x in warning:
            eid = x.split('_')[0]
            for y in map_point:
                if eid == y['eid']:
                    warning_data = self.redis_2.hgetall(x)
                    description = '位于' + y['address'] + '的路面于北京时间,' + time.strftime("%Y-%m-%d %H:%M:%S",\
                                  time.localtime(int(x.split('_')[1]))) + ' 报告' + warning_lev[int(warning_data['warning_lvl'])]\
                                  + '色级别' + warning_type[int(x.split('_')[2])] + '，报警状况为： ' + \
                                  warning_type[int(x.split('_')[2])][:-2] + " " + warning_data['warning_value']
                    y['warning_level'] = warning_lev_en[int(warning_data['warning_lvl'])]
                    y['warning_type'] = warning_type_en[int(x.split('_')[2])]
                    y['obs_time'] = int(x.split('_')[1])
                    y['description'] = description

        for x in user:
            equip = self.redis_0.hgetall(x)
            send_box = []
            user_equip = []
            for y in equip:

                user_equip += [y.split(':')[0] for y in equip[y].split(',')]

            for y in map_point:
                if y['eid'] in user_equip:
                    send_box.append(y)
            data = {'map_point':send_box}


            await layers_manage.status_warning_monitor(x, data)
        await layers_manage.status_warning_monitor('admin', map_point)
        return True

            # map_point[eid].update(self.redis_4.hgetall(x))
        # for x in user:
            # equip_holder = self.redis_0.hgetall(x)
            # equip = []
            # for x in equip_holder:
            #     equip += [x.split(':')[0] for x in equip_holder[x].split(',')]
            # send_holder = {}
            # for x in data:
            #     if x in equip:
            #         send_holder[x] = data[x]
            # layers_manage.send_status(x, send_holder)


    # async def monitor_warning(self):
    #     pubsub = self.redis_2.pubsub()
    #     pubsub.psubscribe("__keyevent@2__: *")
    #     for data in pubsub.listen():
    #         operator = data['channel'].split(':')[1]
    #         if operator == 'hset':


# def map_point(username, useradmin):
#     # result = equipments.map_point(username, useradmin)
#     data = []
#     warning_type = {1: '高温预警', 2: '路面状况预警', 3: '能见度预警', 4: '降雨预警', 5: '大风预警'}
#     warning_lev = {1: '红', 2: '橙', 3: '黄', 4: '蓝'}
#     warning_type_en = {1: 'temperature', 2: 'road', 3: 'fog', 4: 'rianfall', 5: 'speed', None: 'normal'}
#     warning_lev_en = {1: 'red', 2: 'orange', 3: 'yellow', 4: 'blue', None: 'green'}
#
#     for x in result:
#         description = ''
#         if x[7]:
#             description = '位于' + x[2] + '的路面于北京时间,' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x[7])) + ' 报告' + \
#                           warning_lev[int(x[8])] + '色级别' + warning_type[int(x[10])] + '，报警状况为： ' + warning_type[int(x[10])][:-2] + " " + \
#                           x[9]
#
#         data.append({
#             "eid":x[0],
#             "station_name":x[1],
#             "address":x[2],
#             "lat_lon":[float(x[3]),float(x[4])],
#             "warning":description,
#             "obs_time":x[7],
#             "status":x[5],
#             "status_time":x[6],
#             "warning_level": warning_lev_en[x[8]],
#             "warning_type": warning_type_en[x[10]]
#
#         })
#
#     return data



