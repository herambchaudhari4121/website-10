#coding=utf-8
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from . import db_handling as db
from .objects_manage import user_handling as uh
from .objects_manage import equipment_handling as eh
from .objects_manage import service_handling as sh
from .objects_manage import remote_handling as rh
from .objects_manage import warning_handling as wh
from django.http import JsonResponse, HttpResponse
from .objects_manage import feature_handling as fh
from .objects_manage import data_storage_handling as dh
import re
import time
from urllib import parse
import json
from redis import StrictRedis
from django.views.decorators.csrf import csrf_exempt
from dwebsocket.decorators import accept_websocket, require_websocket
from random import random
import token_module

# from . import websocket_handling as wh
import threading
import asyncio
from .objects_manage import live_data_handling as lh
redis_0 = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True, password = 'hzg61270388*!')
redis_1 = StrictRedis(host='localhost', port=6379, db=1, decode_responses=True, password = 'hzg61270388*!')






# current_data = lh.current_data()
class current_data:
    def __init__(self):
        self.data_box = {}
        transfer = {'11':'干燥', '12':'潮湿','13':'积水','14':'雪','15':'冰', '16':'霜', '17':'有融雪剂','00':'状况未知','99':'其他'}
        for x in db.current_data():
            if x[1]:
                x[1]['obs_time'] = x[2]
                if 'rw_trs' in x[1]:
                    if x[1]['rw_trs']:

                        if x[1]['rw_trs'][:2] in transfer:
                            x[1]['rw_trs'] = transfer[x[1]['rw_trs'][:2]]
                    else:
                        x[1]['rw_trs'] = '--'
                else:
                    x[1]['rw_trs'] = '--'
                self.data_box[x[0]] = x[1]

            else:
                self.data_box[x[0]] = {'obs_time':x[2]}

    def new_data(self, eid, data):
        transfer = {'11': '干燥', '12': '潮湿', '13': '积水', '14': '雪', '15': '冰', '16': '霜', '17': '有融雪剂', '00': '状况未知',
                    '99': '其他'}
        if 'rw_trs' in data:
            if data['rw_trs']:
                if str(data['rw_trs'])[:2] in transfer:
                    data['rw_trs'] = transfer[str(data['rw_trs'])[:2]]
            else:
                data['rw_trs'] = '--'
        else:
            data['rw_trs'] = '--'


        self.data_box[eid] = data
# websocket_client = wh.client()
# user_portal = wh.user_portal_handling()
# current_data = current_data()
# print('user:',user_portal.portal)


# 历史数据查询

def index(request):  # 单台站全要素12条数据：0.6s, 单要素:0.45s
    if request.method == "POST":
        d = json_transfer(request.body)  # 从body得到的byte数据转为dict
        tree = None
        page_number = 0
        if d:
            # 如果字典转换成功，调用fh来查找数据
            # 返回查找结果
            page = str(d['page'])
            size = str(d['size'])
            eid = [d['eid']]
            period = [str(d['start_time']), str(d['end_time'])]
            if 'feature_filter' in d:
                feature_filter = d['feature_filter']
            else:
                feature_filter = None
            result = fh.data_show_room(eid, feature_filter, period, page, size)
            tree = result[0]
            page_number = result[1]

        if tree:
            code = 1
            msg = "成功"
        else:
            code = 0
            msg = "失败"
            # return JsonResponse({'records': None, 'code': code, 'msg': msg})
        if page_number:
            return JsonResponse({'records': tree, 'code': code, 'msg': msg, 'page_number': page_number}, json_dumps_params={'ensure_ascii':False})
        else:
            return JsonResponse({'records': tree, 'code': code, 'msg': msg}, json_dumps_params={'ensure_ascii':False})


# 显示所有设备信息
def show_equip(request):  # 全台站：0.04s
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    eid_list = []
    if request.method == 'POST':
        d = json_transfer(request.body)
        print(d)
        eid_list = d['eid_list']
    records = eh.show_equip(eid_list)
    code = 1
    msg = {0: '数据获取失败！', 1: '数据获取成功！'}
    if not records:
        code = 0
    return JsonResponse({'records': records, 'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def equip_name(request):    # 0.03s
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'POST':
        useradmin = token_module.authenticate(username, token)
        username = request.headers['username']
        d = json_transfer(request.body)
        print(d)
        e_code = d['e_code']
        records = []
        if username == 'admin':
            records = eh.equip_name()
            code = 1

        else:
            data = redis_0.hgetall(username)[e_code]
            if data:
                data = data.split(',')
                for x in data:
                    records.append({"key":x.split(':')[0], "value": x.split(':')[1]})
                code = 1
            else:
                code = 0

        msg = {0: '数据获取失败/无数据', 1: '数据获取成功！'}
        if not records:
            code = 0
        return JsonResponse({'records': records, 'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


# 所有要素信息字典对照
def features(request):  # 0.1
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == "POST":
        result = redis_1.hgetall('get_column')
        records = [{'key':x, 'value':result[x]} for x in result]
        code = 1
        msg = {0: '数据获取失败！', 1: '数据获取成功！'}
        if not records:
            code = 0
        return JsonResponse({'records': records, 'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def reverse_features(request):  # 0.1
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == "POST":
        result = redis_1.hgetall('get_column')
        soil_column = ['soil_volume', 'gravimetric_water', 'soil_moisture', 'aswc', 'soil_frequency', 'soil_voltage',
         'nor_frequency']
        records = {'weather':[],'soil':[]}
        print(records)
        for x in result:
            if result[x] in soil_column:
                records['soil'].append({'key': result[x], 'value': x})
            else:
                records['weather'].append({'key': result[x], 'value': x})



        # records = [{'key': result[x], 'value': x} for x in result]
        code = 1
        msg = {0: '数据获取失败！', 1: '数据获取成功！'}
        if not records:
            code = 0
        return JsonResponse({'records': records, 'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


# 小程序需求要素字典对照
def features_filter(request):   # 0.1s
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == "POST":
        # user_id = request.session.get('user_id')
        records = db.features_filter()  # 正则
        code = 1
        msg = {0: '数据获取失败！', 1: '数据获取成功！'}
        if not records:
            code = 0
        return JsonResponse({'records': records, 'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


# 实时数据
def feature_now(request):  # 全部数据： 0.2s

    if request.method == "POST":
        d = json_transfer(request.body)  # 从body得到的byte数据转为dict
        if d:
            eid_list = d['eid']
        records = fh.feature_now(eid_list)
        code = 1
        msg = {0: '数据获取失败！', 1: '数据获取成功！'}
        if not records:
            records = None
            code = 0
        return JsonResponse({'records': records, 'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def initial_data(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'POST':
        d = json_transfer(request.body)  # 从body得到的byte数据转为dict
        # print(d)
        records = None
        numbers = 0
        username = request.headers['username']
        useradmin = token_module.authenticate(username, token)
        if d:
            try:
                page = str(d['page'])
                size = d['size']
                result = fh.initial_data(page, size, username, useradmin)
                records = result[0]
                numbers = result[1]
            except Exception as e:
                print(e)
                records = None


        code = 1
        msg = {0: '数据获取失败！', 1: '数据获取成功！'}
        if not records:
            code = 0
        # print(websocket_client.pool)
        # print('records', records, time.localtime(time.time()))
        return JsonResponse({'records': records, 'code': code, 'msg': msg[code], 'numbers': numbers, 'type': 1},
                            json_dumps_params={'ensure_ascii': False})


def get_status(request):
    if request.method == 'POST':
        try:
            token = request.headers['Token']
            username = request.headers['username']
            if not token_module.authenticate(username, token):
                return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        except:
            return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})

    username = request.headers['username']
    useradmin = token_module.authenticate(username, token)
    return JsonResponse({'records':eh.get_status(username, useradmin)}, json_dumps_params={'ensure_ascii':False})



def get_success_rate(request):
    if request.method == 'POST':
        try:
            token = request.headers['Token']
            username = request.headers['username']
            if not token_module.authenticate(username, token):
                return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        except:
            return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})

        username = request.headers['username']
        useradmin = token_module.authenticate(username, token)
        success_rate = eh.get_success_rate(username, useradmin)

        return JsonResponse(success_rate, json_dumps_params={'ensure_ascii':False})



def generate_file(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == "POST":
        redis_counts = StrictRedis(host='localhost', port=6379, db=1, decode_responses=True)
        d = json_transfer(request.body)
        code = 1
        msg = {0: '文件生成失败！', 1: '文件生成成功！'}
        counts = '1'
        if d:
            try:
                username = request.headers['username']
                useradmin = token_module.authenticate(username, token)
                eid_list = d['eid']
                file_type = d['file_type']
                period = [str(int(int(d['start_time']) / 1000)), str(int(int(d['end_time']) / 1000 + 86400))]
                # print(period)
                # period = ['1596297600','1596470400']
                column = d['feature_filter']
                # counts = redis_manage.download_count(username)
                redis_counts.incr(username)
                if int(redis_counts.get(username)) == 1:
                    redis_counts.expire(username, 3600)
                counts = redis_counts.get(username)
                if counts:
                    code = 1
                else:
                    code = 0
                # if dh.generate_file(username, useradmin, period, eid_list, column, file_type):
                #     code = 1
                #     redis_manage.download_count(username)
                #
                # else:
                #     code = 0

            except Exception as e:
                code = 0
                print(e)

        return JsonResponse({'code': code, 'msg': msg[code], 'counts': counts}, json_dumps_params={'ensure_ascii':False})


def features_his(request):  # 单要素： 0.12s, 全要素0.16s
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == "POST":
        # print(request.body)
        d = json_transfer(request.body)  # 从body得到的byte数据转为dict
        print(d)
        # print(d)
        records = None
        numbers = 0
        if d:
            # 如果字典转换成功，调用fh来查找数据
            # 返回查找结果
            try:
                eid_list = d['eid']
                page = str(d['page'])
                period = [str(int(int(d['start_time']) / 1000)), str(int(int(d['end_time']) / 1000 + 86400))]
                # print(period)
                # period = ['1596297600','1596470400']
                feature_filter = d['feature_filter']
                size = d['size']
                if not size:
                    size = '15'
                result = fh.feature_his(eid_list, feature_filter, period, page, size)
                # print(result,'result')
                records = result[0]
                numbers = result[1]
            except Exception as e:
                print(e)
                records = None
        code = 1
        msg = {0: '数据获取失败！', 1: '数据获取成功！'}
        if not records:
            code = 0
        print(records)


        # print(websocket_client.pool)
        # print('records', records, time.localtime(time.time()))
        return JsonResponse({'records': records, 'code': code, 'msg': msg[code], 'numbers': numbers, 'type':2}, json_dumps_params={'ensure_ascii':False})






# 用户添加页面
def add_user(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
        else:
            if token_module.authenticate(username, token) !=2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})

    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'POST':
        d = json_transfer(request.body)

        useradmin = token_module.authenticate(username, token)
        username = d['username']
        password = d['password']
        service_code = d['service_code']  # 可为空
        role = str(d['is_admin'])
        if role == "0":
            role = False
        code = uh.add(username, password, service_code, role)
        msg = {0: "用户添加失败！", 1: "用户添加成功！", 2: "用户名已存在！", 3: "业务号不存在！"}
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})




def all_service(request):   # 0.08
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        username = request.headers['username']
        useradmin = token_module.authenticate(username, token)

        service_code = d['code']
        service = sh.all_service(service_code, username, useradmin)
        print(service)

        test = {1:2}
        return JsonResponse({'service': service}, json_dumps_params={'ensure_ascii':False})


def user_list(request): # 0.04
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})

    username = request.headers['username']
    useradmin = token_module.authenticate(username, token)
    return JsonResponse({'user': uh.user_list(username, useradmin)}, json_dumps_params={'ensure_ascii':False})


def modify_user(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)

        code = uh.modify_user(d['id'], d['user_name'], d['service_code'], d['password'], d['status'])
        msg = {0: "修改失败!", 1: "修改成功！", 2: "用户名已存在！"}
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def delete_user(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        code = uh.delete_user(d['id'], d['service_code'])
        msg = {0: '删除失败！', 1: '删除成功！'}
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def add_equipments(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        print(d)
        code = eh.add_equipments(d)
        msg = {0: '失败！', 1: '成功！', 2: '设备station_id重复',
               3: '设备名重复', 4: '设备addr_value重复', 5: '辅助设备station_id重复',
               6: '辅助设备名重复', 7: '辅助设备eid重复'
               }
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})





def unconnected_equip(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    records = eh.unconnected_equip()
    code = 1
    msg = {0: '没有无归属设备！', 1: '数据获取成功！'}
    if not records:
        code = 0
    return JsonResponse({'records': records, 'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def add_service(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        code = d['code']
        name = d['name']
        location_code = d['location_code']
        parent_code = d['parent_code']
        create_time = str(int(time.time()))
        code = sh.add_service(code, name, location_code, create_time, parent_code)
        msg = {0: '上级项目号非法或不存在！', 1: '添加成功！', 2: '项目添加失败！', 3: '项目号已存在！', 4: '项目名已存在！'}
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def location_tree(request):     # 0.01s
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    records = sh.get_location_tree()
    code = 1
    msg = {0: '数据获取失败！', 1: '数据获取成功！'}
    if not records:
        code = 0
    return JsonResponse({'children': records, 'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def modify_service(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        code = sh.modify_service(d['code'], d['name'], d['parent_code'], d['status'], d['location_code'])
        msg = {0: '上级项目号非法或不存在！', 1: '修改成功！', 2: '项目修改失败！', 3: '项目号已存在！', 4: '项目名已存在！'}
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def delete_service(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        service_code = d['code']
        code = sh.delete_service(service_code)
        msg = {0: '删除失败！', 1: '删除成功！', 2: '项目号不存在！', 3: '删除子项目失败！', 4: '解除关联账户失败!', 5: '解除关联设备失败!'}
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def equip_type(request):    # 0.04 不准确，数据增多时间未知
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        e_code = ''
        e_code_dict = {'2': '0101', '3': '0102', '4': '03%'}
        if str(d['e_code']):
            e_code = e_code_dict[str(d['e_code'])]
        records = eh.equip_type(e_code)
        code = 1
        msg = {0: '数据获取失败！', 1: '数据获取成功！'}
        if not records:
            code = 0
        return JsonResponse({'records': records, 'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def unconnected_assist_equip(request):  # 0.14
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    return JsonResponse({'records': eh.unconnected_assist_equip()}, json_dumps_params={'ensure_ascii':False})


def delete_equipments(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        eid = str(d['eid'])
        code = eh.delete_equipments(eid)
        msg = {0: '失败', 1: '成功'}
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def equip_all_info(request):    # 0.11
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    e_code_dict = {}
    if request.method == 'POST':
        d = json_transfer(request.body)
        print(d)
        username = request.headers['username']
        useradmin = token_module.authenticate(username, token)
        e_code_dict = {'2': '0101', '3': '0102', '4': '03%', '': ''}
        # print(websocket_client.pool)
        records = eh.equip_all_info(e_code_dict[d['e_code']], username, useradmin)

    return JsonResponse({'records': records}, json_dumps_params={'ensure_ascii':False})


def show_dict(request):     # 0.003
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})

    result = redis_1.hgetall('show_dict')
    records = [{'key': x, 'value': result[x]} for x in result]
    return JsonResponse({'records': records}, json_dumps_params={'ensure_ascii':False})


def manage_equipments(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        code = eh.manage_equipments(d)
        msg = {0: '失败！', 1: '成功！', 2: '设备station_id重复', 3: '设备名重复'}
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def manage_parameter(request):      # 0.1S
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        print(d)
        code = eh.manage_parameter(d)
        msg = {0: '失败！', 1: '成功！'}
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def objects_under_service(request):     # 0.14
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'POST':
        d = json_transfer(request.body)

        records = sh.objects_under_service(d['service_code'])
        code = 1
        msg = {0: '失败！', 1: '成功！'}
        if not records:
            code = 0
        return JsonResponse({'records': records, 'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})


def manage_connection(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        print(d)

        code = sh.manage_connection(d)
        msg = {1: '成功！', 2: '用户关系删除失败！', 3: '设备关系删除失败！', 4: '用户关系添加失败！', 5: '设备关系添加失败！'}
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})



def show_requests(request):
    if request.method == 'POST':
        d = json_transfer(request.body)
        code = 1
        msg = "成功"
        data = {}

        return JsonResponse({'code': code, 'msg': msg, 'data': data})



def set_weather_id(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        result = rh.set_weather_id(d['eid'], d['station_id'], d['key'])
        if random() > 0.5:
            return JsonResponse({'code': 1, 'result': '成功！'})
        else:
            return JsonResponse({'code': 0, 'result': '失败！'})


def get_weather_id(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        records = rh.get_weather_id(d['eid_list'], d['key'])
        # records = {d['eid']:'A0001'}

        return JsonResponse({'code': 1, 'result': '成功！'})



def get_time(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        identity = d['identity']
        if identity == '1':
            result = rh.get_weather_time(d['eid_list'], d['key'])
        else:
            result = rh.get_soil_time(d['eid_list'], d['key'])
    # code = int(json_transfer(result)['code'])
    code = 1
    msg = {0: '失败！', 1: '成功！'}
    print(result)
    return JsonResponse({'code': code, 'msg': msg[code]})

def set_time(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        identity = d['identity']
        if identity == '1':
            result = rh.set_weather_time(d['eid_list'], d['key'])
        else:
            result = rh.set_soil_time(d['eid_list'], d['key'])
    code = 1
    msg = {0: '失败！', 1: '成功！'}
    return JsonResponse({'code': code, 'msg': msg[code]})


def soil_live_collection(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        result = rh.set_soil_time(d['eid_list'], d['key'])
    code = 1
    msg = {0: '失败！', 1: '成功！'}
    return JsonResponse({'code': code, 'msg': msg[code]})



def re_write_data(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':

        d = json_transfer(request.body)
        identity = d['identity']
        if identity == '1':
            result = rh.weather_re_write(d['eid_list'], [int(d['start_time'])/1000, int(d['end_time'])/1000], d['key'])
        else:
            result = rh.soil_re_write(d['eid_list'], int(d['start_time'])/1000, int(d['end_time'])/1000, d['key'])
        # code = int(json_transfer(result)['code'])
        msg = {0: '失败！', 1: '成功！'}
        code = 1

        return JsonResponse({'code': code, 'msg': msg[code]})




def modify_db_station_id(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']

        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
        else:
            if token_module.authenticate(username, token) != 2:
                return JsonResponse({'code': -2, 'msg': '账号无权限'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        eid = d['eid']
        station_id = d['station_id']
        msg = {0:'失败！', 1:'成功！'}
        code = eh.modify_db_station_id(eid, station_id)

        return  JsonResponse({'code': code, 'msg': msg[code]})





# 登录页面
def login(request):
    if request.method == 'POST':
        print(request.body)
        print(request.headers)
        d = json_transfer(request.body)
        username = d['username']
        password = d['password']
        direction = d['nextPage']
        account = db.wsys_user_pwd(username, password)
        # account = ["123","123",'123',False]
        # msg = {0: "用户名/密码错误！", 1: "登录成功！"}
        token = ''
        code = 0
        if account:  # 如果有账户
            # if account[3]:  # account -> (username, password, id, is_admin). 如果是管理员账户
            #     token = token_module.get_token(username, 7776000)
            #     code = 2
            # else:
            #     token = token_module.get_token(username, 7776000)
            #     code = 3
            code = 1
            if account[5] == 1:
                if direction == 'console':
                    result = False
                else:
                    result = True
                    token = token_module.get_token(username, 7776000)
            else:

                result = True
                token = token_module.get_token(username, 7776000)
        else:
            result = False
        return JsonResponse({'result': result, 'token':token, 'code': code}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'OPTIONS':
        return HttpResponse('1')


def map_point(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    useradmin = token_module.authenticate(username, token)
    username = request.headers['username']
    data = eh.map_point(username, useradmin)
    print(data)
    return JsonResponse({'records':data})


def get_warning(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'POST':

        useradmin = token_module.authenticate(username, token)
        warning = wh.get_warning(username, useradmin)
        events = wh.event_count(username, useradmin)

        records = {'records':warning, 'count':events['count'], 'total': events['total']}
        return JsonResponse({'records': records})


def rain_fall_data(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        eid = d['eid']
        records = fh.rain_fall_data(eid)
    return JsonResponse({'records': records})




def river_data(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'POST':
        d = json_transfer(request.body)
        eid = d['eid']
        eid_list = [eid]
        column = d['column']
        result = fh.river_data(eid_list, column)
    return JsonResponse({'records':result})



def line_data(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'POST':
        print(request.body)
        d = json_transfer(request.body)
        print(d)

        eid = d['eid']
        eid_list = [eid]
        column = d['column']

        if 'start_time' in d:
            start_time = d['start_time']
            end_time = d['end_time']
            period = [start_time[:-3], end_time[:-3]]
        else:
            period = [str(int(time.time() - 3600)), str(int(time.time()))]
        result = fh.line_data(eid_list, column, period)
    return JsonResponse({'records':result})



def traffic_line(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii':False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii':False})
    if request.method == 'POST':
        print(request.body)
        d = json_transfer(request.body)

        eid = d['eid']
        eid_list = eid
        column = d['column']

        if 'start_time' in d:
            start_time = d['start_time']
            end_time = d['end_time']
            period = [start_time[:-3], end_time[:-3]]
        else:
            period = [str(int(time.time() - 3600)), str(int(time.time()))]
        result = fh.traffic_line(eid_list, column, period)
    return JsonResponse({'records':result})





def token_test(request):
    if request.method == 'POST':
        d = json_transfer(request.body)

        code = 1
        msg = {0: '未登录', 1: '成功'}
        try:
            token = request.headers['token']
            username = request.headers['username']
            if not token_module.authenticate(username, token):
                code = 0
        except:
            code = 0
        finally:
            return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})




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


# @accept_websocket
# def send_socket(req):
#     print(req)
#     if req.is_websocket():
#         msg = ['1','2','3','4','5','6','7']
#         count = 0
#         while True:
#
#             for x in msg:
#                 req.websocket.send(x.encode('utf-8'))
#                 time.sleep(3)
#                 count += 1
#             if count >= 7:
#                 break
#         print('收到websocket请求')


# @accept_websocket
# def send_socket(req):
#     print(req)
#     if req.is_websocket():
#         msg = ['1','2','3','4','5','6','7']
#         count = 0
#         print(req.websocket)
#         key = websocket_client.new_websocket(req)
#         print(key)
#         while True:
#
#             for x in msg:
#                 websocket_client.push_socket(key, x)
#                 # req.websocket.send(x.encode('utf-8'))
#                 time.sleep(3)
#                 count += 1
#             if count >= 7:
#                 websocket_client.close_websocket(key)
#                 break
#         print('收到websocket请求')


# def socket_thread(key):
#     # print('socket_s')
#     # if req.is_websocket():
#     #     t = threading.Thread(target=send_socket, args=(req))
#         try:
#
#
#             # print('socket')
#             # print('socket_start')
#             # key = websocket_client.new_websocket(req)
#             # # print(websocket_client.pool)
#             # websocket_client.push_socket(key, 'key' + str(key))
#             # user_portal.remove_connection(key)
#             # print('e', websocket_client.pool)
#             # print('user:', user_portal.portal)
#             # print('thread_start')
#
#
#             if websocket_client.pool[key].wait() == None:
#
#                 print('thread_stop')
#
#             # for message in websocket_client.pool[key]:
#             #     if not message:
#             #         print('thread_stop')
#             #         break
#
#             # if websocket_client.pool[key].wait() == None:
#             #     user_portal.remove_connection(key)
#             #     print(user_portal)
#             #     websocket_client.close_websocket(key)
#             #     print(websocket_client.pool)
#             #     print('close')
#             #     print(key)
#         finally:
#
#             user_portal.remove_connection(key)
#             websocket_client.close_websocket(key)
#
#
#
#
# @accept_websocket
# def send_socket(req):
#     print('socket_s')
#     if req.is_websocket():
#         print('socket_s')
#         if req.is_websocket():
#
#
#             print('socket')
#             print('socket_start')
#             key = websocket_client.new_websocket(req)
#             # print(websocket_client.pool)
#             websocket_client.push_socket(key, 'key' + str(key))
#             user_portal.remove_connection(key)
#             print('e', websocket_client.pool)
#             print('user:', user_portal.portal)
#
#             t = threading.Thread(target=socket_thread, args=((key,)))
#             t.start()
#     #     try:
#     #         lock = threading.RLock()
#     #         print('socket')
#     #         print('socket_start')
#     #         key = websocket_client.new_websocket(req)
#     #         # print(websocket_client.pool)
#     #         websocket_client.push_socket(key, 'key'+str(key))
#     #         user_portal.remove_connection(key)
#     #         print('e',websocket_client.pool)
#     #         print('user:' , user_portal.portal)
#     #
#     #         for message in req.websocket:
#     #             if not message:
#     #                 break
#     #
#     #         # if websocket_client.pool[key].wait() == None:
#     #         #     user_portal.remove_connection(key)
#     #         #     print(user_portal)
#     #         #     websocket_client.close_websocket(key)
#     #         #     print(websocket_client.pool)
#     #         #     print('close')
#     #         #     print(key)
#     #     finally:
#     #
#     #         user_portal.remove_connection(key)
#     #         websocket_client.close_websocket(key)
#     #         lock.release()
#     # else:
#     #     print('now_socket')
#
#
#
#
#
# def socket_close(request):
#     if request.method == 'POST':
#         print('close',websocket_client.pool)
#         d = json_transfer(request.body)
#         # print(d['key'])
#         key = int(d['key'])
#         user_portal.remove_connection(key)
#         websocket_client.close_websocket(key)
#         # print(d)
#         return HttpResponse('成功！')
#
#
#
# def select_equipment(request):
#     if request.method == 'POST':
#         print('s', websocket_client.pool)
#         d = json_transfer(request.body)
#         key = int(d['key'])
#         user_portal.remove_connection(key)
#         print('user:' , user_portal.portal)
#         print(websocket_client.pool)
#         if d['eid']:
#             user_portal.select_equip(key, d['eid'])
#             data = str(current_data.data_box[d['eid']])
#             data = data.replace("'", '"')
#             json_data = json.dumps(data, ensure_ascii=False)
#             # print(json_data)
#             print(websocket_client.pool)
#             print(json_data)
#             websocket_client.push_socket(key, json_data)
#         code = 1
#         msg = {0:'失败！', 1:'成功！'}
#         return JsonResponse({'code': code, 'msg': msg[code]})
#
#


def live_data_distribution(request):
    if request.method == 'POST':
        data = str(request.body)[1:]
        print(data)
        if re.sub("'", '', str(data)):
            d = eval(re.sub("'", '', str(data)))
        eid = d['eid']
        data = d['data']
        for x in data:
            data[x] = data[x]
        print(data)
        current_data.new_data(eid, data, data)
        data = str(current_data.data_box[eid])
        data = data.replace("'", '"')
        json_data = json.dumps(data, ensure_ascii=False)
        print(json_data)
        # if eid in user_portal.portal:
        #     key = user_portal.portal[eid]
        #     for x in key:
        #         websocket_client.push_socket(x, json_data)
        code = 1
        msg = {0: '失败！', 1: '成功！'}
        return JsonResponse({'code': code, 'msg': msg[code]})
#
#
#
#
# # def time_out_test(request):
# #     while True:
# #         code = 1
# #     return JsonResponse({'code': 0, 'msg': '成功！'})
#
#
# def socket_test(request):
#     return render(request,'socket_test.html')
#
#
# def get_message(request):
#     if request.method == 'POST':
#         d = json_transfer(request.body)
#         key = int(d['uid'])
#         value = d['value']
#         websocket_client.push_socket(key, value)
#
#     return JsonResponse({'code': 0, 'msg':'成功！'})
#
#
#
#
#
# def ws_test(request):
#     d = json_transfer(request.body)
#     key = int(d['key'])
#     value = d['value']
#     websocket_client.push_socket(key, value)
#     return JsonResponse({'code': 0})





# def close_socket(request):
#     d = json_transfer(request.body)
#     key = int(d['key'])
#     websocket_client.close_websocket(key)
#     return JsonResponse({'code': 0})


# @require_websocket
# def stability_test(req):
#     if req.is_websocket():
#         key = websocket_client.new_websocket(req)
#         print(websocket_client.pool)
#         while True:
#             websocket_client.push_socket(key, str(key)*1024)
#             time.sleep(3)


def wb_test(request):

    return render(request,'socket_test.html')