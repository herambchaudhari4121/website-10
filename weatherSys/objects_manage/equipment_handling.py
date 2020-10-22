from weatherSys import db_handling as db
from weatherSys import input_validation as vl
from django.shortcuts import render
from weatherSys import time_handling as th

import time
from urllib import parse
equipments = db.equipments()
from redis import StrictRedis
redis_4 = StrictRedis(host='localhost', port=6379, db=4, decode_responses=True, password = 'hzg61270388*!')
redis_3 = StrictRedis(host='localhost', port=6379, db=3, decode_responses=True, password = 'hzg61270388*!')
redis_0 = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True, password = 'hzg61270388*!')
from . import redis_handling as redis_h

def add_equipments(data):
    basic_info = to_basic(data)

    exist = equipments.equip_exist(basic_info['eid'], basic_info['station_id'], basic_info['station_name'])
    redis_status = {'station_name':basic_info['station_name'], 'longitude':basic_info['longitude'],
                    'latitude': basic_info['latitude'], 'address': basic_info['address'], 'status':'0',
                    'status_time':basic_info['create_time']}
    if exist:
        equipments.db_close()
        return exist
    if not add_basic(basic_info):
        equipments.db_close()
        return 0
    new_sub_device = data['new_sub_device']     # 新建辅助设备信息
    sub_device = data['sub_device']     # 已有辅助设备关联
    eid = basic_info['eid']
    if sub_device['0301'] or sub_device['0302'] or sub_device['0303']:
        result = add_sub_device(basic_info, new_sub_device, sub_device)
        if not result:
            equipments.db_close()
            return 0
        else:
            if result != 1:
                equipments.db_close()
                return result
    extend_data = data['extend_data']

    if extend_data:
        if not add_extend(basic_info, extend_data):
            equipments.db_close()
            return 0

    if data['addr_value']:
        addr_value = {'010201':[data['addr_value']]}
        if not add_extend(basic_info, addr_value):
            equipments.db_close()
            return 0
    equipments.add_status(eid)
    result = equipments.db_confirm()

    if extend_data:
        data = {x: ','.join(extend_data[x]) for x in extend_data}
        redis_4.hmset(eid, data)
    redis_3.hset(name = eid, mapping = redis_status)

    if result:
        equipments.db_close()
    else:
        equipments.db_close()

    return 1


def to_basic(data):
    e_code = data['e_code']
    basic_info = data['basic_info'].copy()
    addr_value = data['addr_value']
    # eid = ''
    # if e_code == '0102':
    #     eid = 'HZG04DN2' + addr_value
    # else:
    #     if e_code == '0301' or e_code == '0302' or e_code == '0303':
    #         eid = 'HZGEXT' + basic_info['station_id']
    #     else:
    #         eid = 'HZG07' + basic_info['station_id'] + '002'
    # basic_info['eid'] = eid
    basic_info['e_code'] = e_code
    if basic_info['message_push']:
        basic_info['message_push'] = 'true'
    else:
        basic_info['message_push'] = 'false'
    if basic_info['address']:
        basic_info['address'] = parse.unquote(basic_info['address'])

    create_time = str(int(time.time()))
    basic_info['create_time'] = create_time

    return basic_info


def add_basic(basic_info):
    column = [i for i in basic_info.keys() if basic_info[i]]
    values = [[i for i in basic_info.values() if i]]
    # column = "("+
    #
    # (column)+")"
    # values = "('"+"','".join(values)+"')"
    result = equipments.add_basic_info(column, values)
    return result


def add_sub_device(basic_info, new_sub_device, sub_device):
    result = True

    for x in new_sub_device:
        if new_sub_device[x]:
            for y in new_sub_device[x]:
                data = {}
                data['basic_info'] = y.copy()
                data['e_code'] = x
                data['addr_value'] = ''
                sub_basic_info = to_basic(data)

                if equipments.equip_exist(sub_basic_info['eid'], sub_basic_info['station_id'], sub_basic_info['station_name']):
                    result = equipments.equip_exist(sub_basic_info['eid'], sub_basic_info['station_id'], sub_basic_info['station_name']) + 3
                    return result
                if not add_basic(sub_basic_info):
                    return 0
    sub_connection = []

    for x in sub_device:
        for y in sub_device[x]:
            value = [basic_info['eid'], x,"'{" + y + "}'"]
            sub_connection.append(value)

    result = equipments.add_extend(sub_connection)
    if not result:
        return 0
    return 1


def add_extend(basic_info, extend_data):
    extend_connection = [[basic_info['eid'], x, "'{" + ','.join(extend_data[x]) + "}'"] for x in extend_data]
    print(extend_connection)
    result = equipments.add_extend(extend_connection)
    if result:
        return True
    else:
        return False


def show_equip(eid_list):
    equip = db.column_name('wsys_equipment_info', equipments.show_equip(eid_list))
    equipments.db_close()
    return equip


def equip_type(e_code):
    equip = db.column_name('wsys_equipment_info', equipments.equip_type(e_code))
    equipments.db_close()
    return equip


def equip_name():
    equip = equipments.equip_name()

    result = [{"key": x[0], "value": x[1]} for x in equip]
    equipments.db_close()
    return result





def equip_all_info(e_code, username, useradmin):
    eid_list = []
    if e_code:
        equip = db.column_name('wsys_equipment_info', equipments.equip_type(e_code))
    else:
        equip = db.column_name('wsys_equipment_info', equipments.show_equip(eid_list, username, useradmin))

    extra = equipments.show_extr(eid_list)
    sub = equipments.show_sub_device(eid_list)

    for x in equip:
        x['sub_device'] = []
        x['extend_data'] = {}

    for x in sub:
        for y in equip:
            if x[0] == y['eid']:
                y['sub_device'].append({'id': x[1], 'station_name': x[2], 'station_type': x[3]})
    """
    土壤水分参数纵转横
    """
    for y in equip:
        level = []
        for x in extra:    # 每个设备对应辅助表内的信息
            if x[1] == y['eid']:    # 如果对上了
                if x[2] != '0208' and x[2] != '0209':   # 除了0208,0209这两个对应整设备的
                    # if x[3]:    # 如果数据不为空
                    if level:   # 如果变量已声明
                        for index, z in enumerate(level):   # level内对应index位置找extr内参数
                            if index >= len(x[3]):  # 如果位置对应不上，空值
                                z.append('')
                            else:
                                z.append(x[3][index])   # 否则加入值
                        y['extend_data']['column'].append(x[2])
                        y['extend_data']['id'].append(x[0])
                    else:
                        if x[3]:
                            level = [[x] for x in x[3]]     # 声明
                        else:
                            level = [[""]]
                        y['extend_data']['column'] = [x[2]]
                        y['extend_data']['id'] = [x[0]]
                    y['extend_data']['data'] = level
                else:
                    if x[3]:
                        single = x[3]
                    else:
                        single = [""]
                    single.append(x[0])
                    y['extend_data'][x[2]] = single
    equipments.db_close()
    return equip


def unconnected_equip():
    equip = db.column_name('wsys_equipment_info', equipments.unconnected_equip())
    equipments.db_close()
    return equip


def extra_code():
    soil = equipments.soil_code()
    assist = equipments.assist_device_code()
    equipments.db_close()
    return soil, assist


def unconnected_assist_equip():
    equip = equipments.unconnected_assist_equip()
    sub_device = db.get_dic('03')
    records = [{'value': x[5], 'label': x[1], 'children': []} for x in sub_device]
    for x in equip:
        for y in records:
            if x[2] == y['value']:
                y['children'].append({'value': x[0], 'label': x[1]})
                break
    equipments.db_close()
    return records

def delete_equipments(eid):
    if not equipments.delete_equipments(eid):
        equipments.db_close()
        return 0
    if not equipments.delete_equipment_service(eid):
        equipments.db_close()
        return 0
    equipments.delete_status(eid)
    result = equipments.db_confirm()
    redis_4.delete(eid)
    redis_3.delete(eid)
    if result:
        equipments.db_close()
    else:
        equipments.db_close()
    return 1


def manage_equipments(d):
    sub_device = d['sub_device']
    # extend = d['extend_data']
    station_name = d['station_name']
    station_id = d['station_id']
    basic = {x: d[x] for x in d if d[x] and x != "sub_device" and x != "extend_data"}
    eid = basic['eid']
    basic.pop('eid')
    if equipments.equip_exist('', station_id, station_name):
        equipments.db_close()
        return equipments.equip_exist('', station_id, station_name)
    result = equipments.update_basic(basic, eid)
    if not result:
        equipments.db_close()
        return 0
    if sub_device['id']:
        if not equipments.delete_extend(sub_device['id']):
            equipments.db_close()
            return 0
    if sub_device['new_sub_device']:
        sub_connection = [[eid, x[0], "'{"+ x[1] + "}'"] for x in sub_device['new_sub_device']]
        if not equipments.add_extend(sub_connection):
            equipments.db_close()
            return 0

    if equipments.db_confirm():
        redis_h.read_status()
        equipments.db_close()
    else:
        equipments.db_close()
    return 1


def manage_parameter(d):
    extend_data = d['extend_data']
    line_id = d['id']
    column = d['column']
    eid = d['eid']
    update_dict = {x: [] for x in line_id}
    redis_update_dict = {x:[] for x in column}
    if not extend_data:
        d['extend_data'].append(len(line_id)*[[]])
    for index, x in enumerate(line_id):
        for y in extend_data:
            if y[index]:
                update_dict[x].append(y[index])
    for index, x in enumerate(column):
        for y in extend_data:
            if y[index]:
                redis_update_dict[x].append(y[index])


    for x in d['single']:
        if x['value']:
            update_dict[x['id']] = [x['value']]
        else:
            update_dict[x['id']] = []
    for x in d['single']:
        if x['value']:
            redis_update_dict[x['column']] = [x['value']]
        else:
            redis_update_dict[x['column']] = []
    for x in redis_update_dict:
        redis_update_dict[x] = ','.join(redis_update_dict[x])

    if not equipments.update_extend(update_dict):
        equipments.db_close()
        return 0
    result = equipments.db_confirm()

    redis_4.hmset(eid, redis_update_dict)

    if result:
        equipments.db_close()
    else:
        equipments.db_close()
    return 1

def modify_db_station_id(eid, station_id):
    if not equipments.modify_db_station_id(eid,station_id):
        equipments.db_close()
        return 0
    result = equipments.db_confirm()
    if result:
        equipments.db_close()
    else:
        equipments.db_close()
    return 1

# def map_point(username, useradmin):
#     result = equipments.map_point(username, useradmin)
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
#         print(data)
#
#     return data




def map_point(username, useradmin):
    redis_3 = StrictRedis(host='localhost', port=6379, db=3, decode_responses=True, password='hzg61270388*!')
    redis_0 = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True, password='hzg61270388*!')
    redis_2 = StrictRedis(host='localhost', port=6379, db=2, decode_responses=True, password='hzg61270388*!')
    status = redis_3.keys('*')
    user = [username]
    warning = redis_2.keys('*')
    map_point = []
    warning_type = {1: '高温预警', 2: '路面状况预警', 3: '能见度预警', 4: '降雨预警', 5: '大风预警'}
    warning_lev = {1: '红', 2: '橙', 3: '黄', 4: '蓝'}
    warning_type_en = {1: 'temperature', 2: 'road', 3: 'fog', 4: 'rianfall', 5: 'speed', None: 'normal'}
    warning_lev_en = {1: 'red', 2: 'orange', 3: 'yellow', 4: 'blue', None: 'green'}
    for x in status:
        status_data = redis_3.hgetall(x)
        if 'longitude'  in status_data:

            lat_lon = [float(status_data['longitude']), float(status_data['latitude'])]
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
                warning_data = redis_2.hgetall(x)
                description = '位于' + y['address'] + '的路面, 于北京时间,' + time.strftime("%Y-%m-%d %H:%M:%S",\
                              time.localtime(int(x.split('_')[1]))) + ' 报告' + warning_lev[int(warning_data['warning_lvl'])]\
                              + '色级别' + warning_type[int(x.split('_')[2])] + '，报警状况为： ' + \
                              warning_type[int(x.split('_')[2])][:-2] + " " + warning_data['warning_value']

                y['warning_level'] = warning_lev_en[int(warning_data['warning_lvl'])]
                y['warning_type'] = warning_type_en[int(x.split('_')[2])]
                y['obs_time'] = int(x.split('_')[1])
                y['warning'] = description

    for x in user:
        equip = redis_0.hgetall(x)
        send_box = []
        user_equip = []

        for x in equip:

            user_equip += [x.split(':')[0] for x in equip[x].split(',')]

        for x in map_point:
            if x['eid'] in user_equip:
                send_box.append(x)
    print('send_box',send_box)
    print('map_point', map_point)

    if username == 'admin':
        return map_point
    else:
        return send_box
        # data = {'map_point':send_box}

    #     layers_manage.status_warning_monitor(x, data)
    # layers_manage.status_warning_monitor('admin', map_point)






def get_status(username, useradmin):
    status = equipments.get_status(username, useradmin)
    if not status:
        equipments.db_close()
        return 0
    transfer = {'11': '干燥', '12': '潮湿', '13': '积水', '14': '雪', '15': '冰', '16': '霜', '17': '有融雪剂', '00': '状况未知',
                '99': '其他','//':'//'}
    records = [{'station_id':x[0],
                'station_name':x[1],
                'status':x[2],
                'obs_time':x[3],
                'at_at1':x[4],
                'ah_rh1':x[5],
                'wd_iwd':x[6],
                'ws_iws1':x[7],
                'mntrnfl':x[8],
                'av_avg1mhv':x[9],
                'rs_rst':x[10],
                'rs_ct10':x[11],
                'rw_wft':x[12],
                'rw_ift':x[13],
                'rw_sft':x[14],
                'rw_trs':x[15],
                'wetslipcoef':x[16],
                'mainclctrvltgval':x[17],
                'eid':x[18]} for x in status]

    for x in records:
        if x['rw_trs']:
            x['rw_trs'] = transfer[x['rw_trs'][:2]]
        else:
            x['rw_trs'] = '//'
        if x['ah_rh1']:
            x['ah_rh1'] = str(x['ah_rh1']) + '%'
    equipments.db_close()
    return records


def get_success_rate(username, useradmin):
    eid_dic = redis_0.hgetall(username)
    eid_list = []
    if eid_dic:
        for x in eid_dic:
            eid_list += [y.split(':')[0] for y in eid_dic[x].split(',') if y]
    success_num = db.get_success_num(eid_list, useradmin)
    station_list = []
    rate_list = []
    print(success_num)
    if success_num:
        for x in success_num:
            # print('station_name',redis_3.hget(x[0],'station_name'))
            station_list.append(redis_3.hget(x[0],'station_name'))
            if x[1] >= 1440 :
                rate_list.append(100)
            else:
                rate_list.append(round(x[1]/1440*100,2))
    success_rate = {'station_list':station_list, 'rate_list':rate_list}
    return success_rate


