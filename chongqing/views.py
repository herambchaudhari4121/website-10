from django.shortcuts import render
import token_module
from django.http import JsonResponse, HttpResponse
# Create your views here.
from .objects_manage import equipment_handling as eh
import re
from urllib import parse

def soil_map(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'records':eh.soil_map(username)})



def soil_data_receive(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'records':eh.soil_data_receive(username)})


def report_rate(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'records': eh.report_rate(json_transfer(request.body)['station_id'], username, json_transfer(request.body)['time'])})


def get_report(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'records': eh.get_report(json_transfer(request.body)['station_id'],json_transfer(request.body)['time'])})


def district_station(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'records': eh.district_station(username)})

def chongqing_features(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})

    start =  str(int(json_transfer(request.body)['start']))
    end =  str(int(json_transfer(request.body)['end']))
    district = json_transfer(request.body)['district']
    station_id = json_transfer(request.body)['station_id']
    return JsonResponse({'records': eh.chongqing_features(username, start, end, district, station_id)})


def chongqing_statistic(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    start =  str(int(json_transfer(request.body)['start']))
    end =  str(int(json_transfer(request.body)['end']))
    district = json_transfer(request.body)['district']
    station_id = json_transfer(request.body)['station_id']


    return JsonResponse({'records': eh.chongqing_statistic(username, start, end, district, station_id)})


def chongqing_line(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    start =  str(int(json_transfer(request.body)['start']))
    end =  str(int(json_transfer(request.body)['end']))
    station_id = json_transfer(request.body)['station_id']
    return JsonResponse({'records': eh.chongqing_line(username, start, end, station_id)})

def vertical_statistic(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    day_1 = json_transfer(request.body)['day_1']
    day_2 = json_transfer(request.body)['day_2']
    district = json_transfer(request.body)['district']
    station_id = json_transfer(request.body)['station_id']
    return JsonResponse({'records': eh.vertical_statistic(username, day_1, day_2, district, station_id)})

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


def kriging(request):
    try:
        token = request.headers['Token']
        username = request.headers['username']
        if not token_module.authenticate(username, token):
            return JsonResponse({'code': -1, 'msg': '登录过期'}, json_dumps_params={'ensure_ascii': False})
    except:
        return JsonResponse({'code': -1, 'msg': '缺少token/username'}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        d = json_transfer(request.body)

        timestamp = str(int(d['time']) - int(d['time'])%3600)

    return JsonResponse({'records': eh.kriging(username,timestamp)})



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
        code = eh.manage_parameter(d)
        msg = {0: '失败！', 1: '成功！'}
        return JsonResponse({'code': code, 'msg': msg[code]}, json_dumps_params={'ensure_ascii':False})
