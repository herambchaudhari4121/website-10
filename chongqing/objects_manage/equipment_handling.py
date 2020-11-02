from chongqing import db_handling as db
import time
equipments = db.equipments()
from urllib import parse


def soil_map(username):
    data = db.soil_map(username, str(int(time.time()) - int(time.time()) % 3600))
    if data:
        point = []
        for x in data:
            point.append({"station_name": x[1],
                          "station_id": x[9],
                          "status": x[10],
                          "status_time": x[11],
                          "district":x[12],
                          "battery":x[13],
                          "obs_time": x[15],
                          "lat_lon": [x[3], x[4]],
                          "soil_volume": x[16],
                          "soil_moisture": x[17]
                          })
        return point
    else:
        return False


def soil_data_receive(username):
    data = db.soil_data_receive(username, str(int(time.time()) - int(time.time()) % 3600))

    if data:
        count_box = {'district': [], 'success': [], 'failure': [], 'total': []}
        for x in data:
            count_box['district'].append(x[2])
            count_box['success'].append(x[0])
            count_box['failure'].append(x[1] - x[0])
            count_box['total'].append(x[1])
            # count_box[x[2]] = {'total_num':x[1],'success':x[0]}
        return count_box
    else:
        return False


def report_rate(station_id, username, obs_time):
    now_time = int(time.time())
    # obs_time = now_time - now_time % 86400 + time.timezone
    obs_time = obs_time
    data = db.report_rate(station_id,username, str(obs_time))
    if data:
        total_num = (now_time-int(obs_time))//3600
        rate_box = []
        for x in data:
            rate_box.append({"station_name":x[3],
                             "station_id":x[11],
                             "obs_time":obs_time,
                             "lat_lon":[x[5],x[6]],
                             "report_rate":int(x[0]/total_num*100)})
        return rate_box
    else:
        return False

def get_report(station_id,obs_time):
    now_time = int(time.time())
    obs_time = obs_time
    # obs_time = now_time - now_time % 86400 + time.timezone
    time_box = [x*3600 + int(obs_time) for x in range(24) if x*3600 + int(obs_time) <= now_time]
    report_box = [0]*len(time_box)
    data = db.get_report(station_id, str(obs_time))
    for x in data:
        if x[0] in time_box:
            report_box[time_box.index(x[0])] = 1

    report_box += [-1]*(24-len(time_box))

    return report_box


def district_station(username):
    data = db.district_station(username)
    if data:
        district_box = {}
        for x in data:
            if x[0] not in district_box:
                district_box[x[0]] = {x[1]: [{'station_id':x[3],'station_name':x[4]}]}
            else:
                district_box[x[0]][x[1]].append({'station_id':x[3],'station_name':x[4]})

        return district_box
    else:
        return False



def chongqing_features(username, start, end, district, station_id):
    data = db.chongqing_features(username, start, end, district, station_id)
    if data:
        point = []
        for x in data:
            if x[16]:
                point.append({"station_name": x[1],
                              "station_id": x[9],
                              "status": x[10],
                              "status_time": x[11],
                              "district":x[12],
                              "battery":x[13],
                              "obs_time": x[15],
                              "lat_lon": [x[3], x[4]],
                              "soil_volume": x[16],
                              "soil_moisture": x[17]
                              })
            else:
                point.append({"station_name": x[1],
                              "station_id": x[9],
                              "status": x[10],
                              "status_time": x[11],
                              "district":x[12],
                              "battery":x[13],
                              "obs_time": x[15],
                              "lat_lon": [x[3], x[4]],
                              "soil_volume": [0,0],
                              "soil_moisture": [0,0]
                              })
        return point
    else:
        return False


def chongqing_statistic(username, start, end, district, station_id):
    data = db.chongqing_features(username, start, end, district, station_id)
    if data:
        data_box = {}
        for x in data:
            if x[9] not in data:
                if x[16]:
                    data_box[x[9]] = {'district': x[12],
                                      'station_name': x[1],
                                      'district': x[12],
                                      'obs_time':int(start),
                                      'address':x[7],
                                      'soil_volume_20': [float(x[16][0])],
                                      'soil_volume_40': [float(x[16][1])],
                                      "soil_moisture_20": [float(x[17][0])],
                                      "soil_moisture_40": [float(x[17][1])]
                                      }
                else:
                    data_box[x[9]] = {'district': x[12],
                                      'station_name': x[1],
                                      'district': x[12],
                                      'obs_time': int(start),
                                      'address': x[7],
                                      'soil_volume_20': [],
                                      'soil_volume_40': [],
                                      "soil_moisture_20": [],
                                      "soil_moisture_40": []
                                      }
            else:
                if x[16]:
                    data_box[x[9]]['soil_volume_20'].append(float(x[16][0]))
                    data_box[x[9]]['soil_volume_40'].append(float(x[16][1]))
                    data_box[x[9]]['soil_moisture_20'].append(float(x[17][0]))
                    data_box[x[9]]['soil_moisture_40'].append(float(x[17][1]))

        point = []

        for x in data_box:
            if len(data_box[x]["soil_volume_20"]) > 0:
                point.append({"station_id": x,
                              "station_name": data_box[x]["station_name"],
                              'district': data_box[x]['district'],
                              'obs_time': data_box[x]['obs_time'],
                              'address': data_box[x]['address'],
                              "soil_volume_20_avg": sum(data_box[x]["soil_volume_20"]) / len(data_box[x]["soil_volume_20"]),
                              "soil_volume_40_avg": sum(data_box[x]["soil_volume_40"]) / len(data_box[x]["soil_volume_40"]),
                              "soil_moisture_20_avg": sum(data_box[x]["soil_moisture_20"]) / len(
                                  data_box[x]["soil_moisture_20"]),
                              "soil_moisture_40_avg": sum(data_box[x]["soil_moisture_40"]) / len(
                                  data_box[x]["soil_moisture_40"]),
                              "soil_volume_20_min": min(data_box[x]["soil_volume_20"]),
                              "soil_volume_40_min": min(data_box[x]["soil_volume_40"]),
                              "soil_moisture_20_min": min(data_box[x]["soil_moisture_20"]),
                              "soil_moisture_40_min": min(data_box[x]["soil_moisture_40"]),
                              "soil_volume_20_max": max(data_box[x]["soil_volume_20"]),
                              "soil_volume_40_max": max(data_box[x]["soil_volume_40"]),
                              "soil_moisture_20_max": max(data_box[x]["soil_moisture_20"]),
                              "soil_moisture_40_max": max(data_box[x]["soil_moisture_40"])}
                             )
            else:
                point.append({"station_id": x,
                              "station_name": data_box[x]["station_name"],
                              'district': data_box[x]['district'],
                              'obs_time': data_box[x]['obs_time'],
                              'address': data_box[x]['address'],
                              "soil_volume_20_avg": 0,
                              "soil_volume_40_avg": 0,
                              "soil_moisture_20_avg": 0,
                              "soil_moisture_40_avg": 0,
                              "soil_volume_20_min": 0,
                              "soil_volume_40_min": 0,
                              "soil_moisture_20_min": 0,
                              "soil_moisture_40_min": 0,
                              "soil_volume_20_max": 0,
                              "soil_volume_40_max": 0,
                              "soil_moisture_20_max": 0,
                              "soil_moisture_40_max": 0}
                             )
        return point
    else:
        return False

def chongqing_line(username, start, end, station_id):
    data = db.chongqing_features(username, start, end, '', station_id)
    if data:
        line_box = {'date':[],'data':[[],[],[],[]]}
        for x in data:
            if x[16]:
                line_box['date'].append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x[15])))
                line_box['data'][0].append(x[16][0])
                line_box['data'][1].append(x[16][1])
                line_box['data'][2].append(x[17][0])
                line_box['data'][3].append(x[17][1])
        return line_box
    else:
        return False

def vertical_statistic(username, day_1, day_2, district, station_id):

    data_1 = db.chongqing_features(username, day_1[0], day_1[1], district, station_id)
    data_2 = db.chongqing_features(username, day_2[0], day_2[1], district, station_id)
    data_box = {}
    for x in data_1:
        if x[9] not in data_1:
            if x[16]:

                data_box[x[9]] = {'district': x[12],
                                  'station_name': x[1],
                                  'district': x[12],
                                  'address': x[7],
                                  'soil_volume_20_start': [float(x[16][0])],
                                  'soil_volume_40_start': [float(x[16][1])],
                                  'soil_volume_20_end':[],
                                  'soil_volume_40_end':[]
                                  }
            else:
                data_box[x[9]] = {'district': x[12],
                                  'station_name': x[1],
                                  'district': x[12],
                                  'address': x[7],
                                  'soil_volume_20_start': [0],
                                  'soil_volume_40_start': [0],
                                  'soil_volume_20_end': [],
                                  'soil_volume_40_end': []
                                  }
        else:
            data_box[x[9]]['soil_volume_20_start'].append(float(x[16][0]))
            data_box[x[9]]['soil_volume_40_start'].append(float(x[16][1]))


    point = []

    for x in data_2:

        if x[16]:
            data_box[x[9]]['soil_volume_20_end'].append(float(x[16][0]))
        else:
            data_box[x[9]]['soil_volume_20_end'].append(0)
        if x[16]:
            data_box[x[9]]['soil_volume_40_end'].append(float(x[16][1]))
        else:
            data_box[x[9]]['soil_volume_40_end'].append(0)


    print(data_box)
    for x in data_box:
        point.append({"station_id": x,
                      "station_name": data_box[x]["station_name"],
                      'district': data_box[x]['district'],
                      'address': data_box[x]['address'],
                      "soil_volume_start_20_avg": sum(data_box[x]["soil_volume_20_start"]) / len(data_box[x]["soil_volume_20_start"]),
                      "soil_volume_start_40_avg": sum(data_box[x]["soil_volume_40_start"]) / len(data_box[x]["soil_volume_40_start"]),
                      "soil_volume_start_20_min": min(data_box[x]["soil_volume_20_start"]),
                      "soil_volume_start_40_min": min(data_box[x]["soil_volume_40_start"]),
                      "soil_volume_start_20_max": max(data_box[x]["soil_volume_20_start"]),
                      "soil_volume_start_40_max": max(data_box[x]["soil_volume_40_start"]),
                      "soil_volume_end_20_avg": sum(data_box[x]["soil_volume_20_end"]) / len(
                          data_box[x]["soil_volume_20_end"]),
                      "soil_volume_end_40_avg": sum(data_box[x]["soil_volume_40_end"]) / len(
                          data_box[x]["soil_volume_40_end"]),
                      "soil_volume_end_20_min": min(data_box[x]["soil_volume_20_end"]),
                      "soil_volume_end_40_min": min(data_box[x]["soil_volume_40_end"]),
                      "soil_volume_end_20_max": max(data_box[x]["soil_volume_20_end"]),
                      "soil_volume_end_40_max": max(data_box[x]["soil_volume_40_end"])}

                     )
    return point


def equip_all_info(e_code, username, useradmin):
    eid_list = []
    if e_code:
        equip = db.column_name('wsys_equipment_info', equipments.equip_type(e_code))
    else:
        equip = db.column_name('wsys_equipment_info', equipments.show_equip(eid_list, username, useradmin))

    equip_location = db.equip_location(username)

    extra = equipments.show_extr(eid_list)
    sub = equipments.show_sub_device(eid_list)

    for x in equip:
        x['sub_device'] = []
        x['extend_data'] = {}
    print(extra)
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
                if x[2] != '0208' and x[2] != '0209' and x[2]:   # 除了0208,0209这两个对应整设备的
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
    for x in equip:
        for y in equip_location:
            if x['eid'] == y[0]:
                x['district'] = y[1]
    return equip


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
    equipments.delete_status(eid)
    result = equipments.db_confirm()
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


    if result:
        equipments.db_close()
    else:
        equipments.db_close()
    return 1


def kriging(username,timestamp):

    data = db.kriging(username, timestamp)
    if data:
        kriging_box = {'20cm':{'features':[]},'40cm':{'features':[]}}
        fid = 0
        for x in data:
            kriging_box['20cm']['features'].append({'attributes':{
                'FID':fid,
                'id': fid+1,
                'name':x[2],
                'x': x[3],
                'y':x[4],
                'z':x[0][0]
            },
            'geometry':{
                'x':x[3],
                'y':x[4]
            }})
            kriging_box['40cm']['features'].append({'attributes':{
                'FID':fid,
                'id': fid+1,
                'name':x[2],
                'x': x[3],
                'y':x[4],
                'z':x[0][1]
            },
            'geometry':{
                'x':x[3],
                'y':x[4]
            }})
            fid += 1

        return kriging_box
    else:
        return False