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











def device_remote_control(request):
    if request.method == 'POST':
        d = json_transfer(request.body)
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

    data = str(data)[1:]
    if re.sub("'", '', str(data)):
        data = eval(re.sub("'", '', str(data)))

        data = chinese_transfer(data)
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


