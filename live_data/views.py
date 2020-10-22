from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# channel_layer = get_channel_layer()

import time
from . import layers_manage
import logging
from . import current_data as cd
current_data = cd.current_data()
import re
import json
from urllib import parse
import token_module
from redis import StrictRedis


def list(request):
    # c.push(text_data= 'views')

    return render(request, 'socket_test.html', {})

# def wb_test(request):
#     eid = 'HZG1234'
#     print(channel_layer)
#     async_to_sync(channel_layer.group_send)(eid, {"type": "test_message","data":{"eid":"12345"}})
#     return HttpResponse(123)


def live_data_distribution(request):
    data = str(request.body)[1:]
    code = 1
    msg = {0: '失败！', 1: '成功！'}
    data = re.sub("null","None", str(data))
    if re.sub("'", '', str(data)):
        d = eval(re.sub("'", '', str(data)))
    eid = d['eid']
    data = d['data']
    for x in data:
        data[x] = data[x]
    current_data.new_data(eid, data)
    data = json.dumps(current_data.data_box[eid])
    # async_to_sync(channel_layer.group_send)(eid, {"type": "test_message", "data": data})
    layers_manage.send_live_data(eid, data)
    return JsonResponse({'code': code, 'msg': msg[code]})






# class status_warning_monitor:
#     def __init__(self):
#         print('runmonitor')
#         self.redis_3 = StrictRedis(host='localhost', port=6379, db=3, decode_responses=True, password='hzg61270388*!')
#         self.redis_0 = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True, password='hzg61270388*!')
#         self.redis_2 = StrictRedis(host='localhost', port=6379, db=2, decode_responses=True, password='hzg61270388*!')
#         self.monitor_status()
#         self.monitor_warning()
#         print('runmonitor')
#
#     def monitor_status(self):
#         print('run monitor status')
#         pubsub = self.redis_3.pubsub()
#         pubsub.psubscribe("__keyevent@3__:hset")
#         for data in pubsub.listen():
#             self.map_point()
#
#     def monitor_warning(self):
#         pubsub = self.redis_2.pubsub()
#         pubsub.psubscribe("__keyevent@1__:*")
#         for data in pubsub.listen():
#             self.map_point()
#
#
#
#     def map_point(self):
#         status = self.redis_3.keys('*')
#         user = self.redis_0.keys('*')
#         warning = self.redis_2.keys('*')
#         map_point = []
#         warning_type = {1: '高温预警', 2: '路面状况预警', 3: '能见度预警', 4: '降雨预警', 5: '大风预警'}
#         warning_lev = {1: '红', 2: '橙', 3: '黄', 4: '蓝'}
#         warning_type_en = {1: 'temperature', 2: 'road', 3: 'fog', 4: 'rianfall', 5: 'speed', None: 'normal'}
#         warning_lev_en = {1: 'red', 2: 'orange', 3: 'yellow', 4: 'blue', None: 'green'}
#         for x in status:
#             status_data = self.redis_3.hgetall(x)
#             lat_lon = [float(status_data['latitude']), float(status_data['longitude'])]
#             status_data.pop('latitude')
#             status_data.pop('longitude')
#             status_data['lat_lon'] = lat_lon
#             status_data['eid'] = x
#             status_data['warning_level'] = 'green'
#             status_data['warning_type'] = 'normal'
#             status_data['description'] = ''
#             status_data['obs_time'] = int(time.time())
#             map_point.append(status_data)
#
#         for x in warning:
#             eid = x.split('_')[0]
#             for y in map_point:
#                 if eid == y['eid']:
#                     warning_data = self.redis_2.hgetall(x)
#                     description = '位于' + y['address'] + '的路面于北京时间,' + time.strftime("%Y-%m-%d %H:%M:%S",\
#                                   time.localtime(int(x.split('_')[1]))) + ' 报告' + warning_lev[int(warning_data['warning_lvl'])]\
#                                   + '色级别' + warning_type[int(x.split('_')[2])] + '，报警状况为： ' + \
#                                   warning_type[int(x.split('_')[2])][:-2] + " " + warning_data['warning_value']
#                     y['warning_level'] = warning_lev_en[int(warning_data['warning_lvl'])]
#                     y['warning_type'] = warning_type_en[int(x.split('_')[2])]
#                     y['obs_time'] = int(x.split('_')[1])
#                     y['warning'] = description
#
#         for x in user:
#             equip = self.redis_0.hgetall(x)
#             send_box = []
#             user_equip = []
#             for x in equip:
#                 for y in equip[x]:
#                     user_equip += [x.split(':')[0] for x in equip[x][y].split(',')]
#
#             for x in map_point:
#                 if x['eid'] in user_equip:
#                     send_box.append(x)
#             data = {'map_point':send_box}
#
#             layers_manage.status_warning_monitor(x, data)
#         layers_manage.status_warning_monitor('admin', map_point)







def device_remote_control(request):
    if request.method == 'POST':
        d = json_transfer(request.body)
        print(d)
        code = 1
        msg = {0: '失败！', 1: '成功！'}
        return JsonResponse({'code': code, 'msg': msg[code]})

def get_live_data(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})

    if request.method == 'POST':
        current_data = cd.current_data()
        d = json_transfer(request.body)
        eid = d['eid']
        data = {}
        try:
            return JsonResponse(current_data.data_box[eid], json_dumps_params={'ensure_ascii': False})
        except:
            return JsonResponse({"result":None}, json_dumps_params={'ensure_ascii': False})

def json_transfer(data):
    # print(data)
    data = str(data)[1:]
    if re.sub("'", '', str(data)):
        data = eval(re.sub("'", '', str(data)))
        # print(data)
        data = chinese_transfer(data)
        # print(data)
        return data
    else:
        return False


def chinese_transfer(data):

    if isinstance(data, str):
        data = parse.unquote(data)
    elif isinstance(data, int):
        data = parse.unquote(str(data))
    else:
        if isinstance(data, dict):
            for x in data:
                data[x] = chinese_transfer(data[x])
        else:
            if isinstance(data, list):
                box = data.copy()
                data = []
                for x in box:
                    data.append(chinese_transfer(x))
    return data


