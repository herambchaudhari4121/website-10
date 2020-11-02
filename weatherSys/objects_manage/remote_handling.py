import requests
import json
from weatherSys import time_handling as th
import time
from random import random
import binascii
import re

address = 'http://172.18.2.160:5000/control'

def get_weather_time(eid_list, key):
    data = {'commands':{x: "DATETIME\r\n"}for x in eid_list}
    data['uid'] = key
    data['identity'] = '1'
    return requests.post(address, data=json.dumps(data), verify=False).content


def get_soil_time(eid_list, key):
    return requests.post(address, data=json.dumps({'eid_list': eid_list,\
           "commands": soil_command_generator(b'\x03', b'\x82',b'', eid_list), "uid": str(key), 'identity':'2'}), verify=False).content


def set_weather_time(eid_list, key):
    data = {'commands': {x: 'DATETIME ' + th.timestamp_to_string(time.time()) + '\r' + '\n'} for x in eid_list}
    data['uid'] = key
    data['identity'] = '1'


    return requests.post(address, data=json.dumps(data), verify=False).content


def set_soil_time(eid_list, key):
    return requests.post(address, data=json.dumps({'eid_list': eid_list,\
            "commands": soil_command_generator(b'\x0a', b'\x81',bytes(int(y) for y in time.strftime("%Y,%m,%d,%H,%M,%S",\
             time.localtime(int(time.time())))[2:].split(',')), eid_list), "uid": str(key), 'identity':'2'}), verify=False).content


def soil_live_collection(eid_list, key):
    return requests.post(address, data=json.dumps({'eid_list': eid_list, "commands":\
        soil_command_generator(b'\x03', b'\x83',b'', eid_list), "uid": str(key), 'identity':'2'}), verify=False).content



def set_weather_id(eid, station_id, key):
    return requests.post(address, data=json.dumps({'commands': {eid: 'ID ' + \
           station_id + '\r\n'}, 'uid': key, 'identity':'1'}), verify=False).content

def get_weather_id(eid_list, key):
    data = {'commands': {x: "ID\r\n"} for x in eid_list}
    data['uid'] = key
    data['identity'] = '1'
    return requests.post(address, data = json.dumps(data), verify=False).content


def weather_re_write(eid_list,time_list, key):
    data = {'commands': {x: "DMTD " + time.strftime("%Y-%m-%d %H:%M", time.localtime(int(time_list[0]))) + ' ' +\
         time.strftime("%Y-%m-%d %H:%M", time.localtime(int(time_list[1]))) + '\r\n'} for x in eid_list}
    data['uid'] = key
    data['identity'] = '1'
    return requests.post(address, data=json.dumps(data), verify=False).content


def soil_re_write(eid_list, start_time, end_time, key):
    return requests.post(address, data=json.dumps({"commands": soil_command_generator(b'\x0d',b'\x94',\
           bytes(int(x) for x in time.strftime("%Y,%m,%d,%H,%M",time.localtime(int(start_time)))[2:].split(',') + time.strftime("%Y,%m,%d,%H,%M",\
           time.localtime(int(end_time)))[2:].split(',')), eid_list), "uid":str(key), 'identity':'2'}),verify=False).content

def soil_command_generator(length, command_index, middle, eid_list):
    commands_dic = {}
    for eid in eid_list:

        commands = b'\xaa' + length + command_index + int(eid.split('HZG04DZN2')[1]).to_bytes(length=2, byteorder='little', signed=False) + middle
        commands += int(sum(x for x in commands[2:])).to_bytes(length=2, byteorder='little', signed=False) + b'\xdd'
        print(commands)
        commands_dic[eid] = binascii.b2a_hex(commands).decode()

    return commands_dic

