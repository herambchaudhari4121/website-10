from weatherSys import db_handling as db
from weatherSys import time_handling as th
import time
import re
"""
小程序历史数据，获取eid下的所有数据，要素可为空，空为小程序要素字典要素，不分页
结构：
"records": [
        {
            "eid": "HZG070C3007002",
            "name": "abcdefg",
            "addr_value": null,
            "details": [
                {
                    "obs_date": 1589040000,
                    "f_code": {
                        "at_at1": "-999.9",
                        "at_maxat1": "-999.9"
                    },
                    "q_code": [
                        "at_at1",
                        "at_maxat1"
                    ]
                },
"""


def data_show_room(eid_list, column, period, page, size):
    records = []
    result = db.feature_his(eid_list, column, period, page, size)
    feature = result[0]  # 取得数据
    page_number = False
    if page:
        total_numbers = int(result[1])
        page_number = total_numbers // int(size) + 1
    #  feature: f.eid, f.obs_time, e.name, f.obs_date, e.addr_value
    if not feature:
        return False
    if column == None:  # 如果不选要素，要素为小程序要素字典的要素
        column = [i[0] for i in db.get_column_name('wsys_feature_his')]
        column = column[5:]
    quality = db.quality_his(eid_list, period)  # 质量码
    for x in feature:
        try:
            key = str(x[0]) + str(x[1])  # 建立和质量码匹配的key
        except:
            next  # 处理如果left join 出现有eid 没有obs_time的状况， 不添加这个key
        column_values = x[4:]  # 不要features中f.eid, f.obs_time, e.name, f.obs_date, e.addr_value， 取后面具体要素数据
        f_code = {}
        if not column_values:  # 处理数据库中有该条但是没要素数据的状况
            column_values = ('')
        for index, z in enumerate(column):
            f_code[z] = column_values[index]  # column_values数据顺序和column里的title一一对应，改为dict
        q_code = []
        if key in quality:  # 找到feature条对应的质量码条
            for y in column:
                if y in quality[key]:  # 如果质量码中出现要素的title，基于质量码进行相应的操作
                    if quality[key][y] == "2":  # 页面只判读质量码是否为2
                        q_code.append(y)
                    if quality[key][y] == "8":
                        f_code[y] == '////'
                    if quality[key][y] == 'N':
                        f_code[y] == '---'
            # 建立具体数据条
        values = {
            "obs_date": x[1],
            "date": x[3],
            "f_code": f_code,
            "q_code": q_code}

        records.append(values)
    return records, page_number


"""
要素实时数据
结构：
"records": [
        {
            "eid": "HZG070B1005002",
            "st_name": "equip10",
            "addr_value": "34",
            "obs_time": 1571327880,
            "f_code": {
                所有要素数据
                "wetslipcoef": 0.82
            },
            "q_code": []
        },
"""


def feature_now(eid_list):
    result = db.feature_now(eid_list)  # 取得实时数据
    # feature: f.eid, e.station_name, f.obs_time, f.feature_info, q.quality_info
    records = []
    if result:
        for x in result:
            q_code = []
            f_code = x[3]
            if x[4] != None:  # 如果有质量码，相对应修改

                for y in x[4]:
                    if x[4][y] == 2:
                        q_code.append(y)
                    if x[4][y] == 8:
                        f_code[y] == "////"
                    if x[4][y] == "N":
                        f_code[y] == "---"
            # 组成每一条数据
            values = {
                "eid": x[0],
                "st_name": x[1],
                "obs_time": x[2],
                "f_code": f_code,
                "q_code": q_code}

            records.append(values)
    return records


"""
网页要素数据
结构：
"records": [
        {
            "eid": "HZG070C3007002",
            "name": "abcdefg",
            "addr_value": null,
            "obs_date": 1589040000,
            "at_at1": "-999.9",
            "at_maxat1": "-999.9",
            "q_code": [
                "at_at1",
                "at_maxat1"
            ]
        },
"""


# def feature_his(eid_list, column, period, page):
#     records = []
#     size = "12"
#     result = db.feature_his(eid_list, column, period, page, size)
#     feature = result[0]
#     #  feature: f.eid, f.obs_time, e.name, f.obs_date, e.addr_value
#     page = result[1]  # list,每个台站有多少条feature
#     total_numbers = 0
#     # 总共有多少条feature
#     for x in page:
#         total_numbers += x[0]
#     obs_time = []
#     if not feature:
#         return False, 0
#     else:
#         for x in feature:
#             obs_time.append(x[1])
#     p = [str(sorted(obs_time)[0]), str(sorted(obs_time)[-1])]
#     quality = db.quality_his(eid_list, p)
#     # 后面和data_show_room基本相同
#
#     for x in feature:
#         key = x[0] + str(x[1])
#         column_values = x[5:]
#         f_code = {}
#         values = {
#             "eid": x[0],
#             "name": x[2],
#             "obs_date": x[1],
#             "address": x[4]}
#         for index, z in enumerate(column):
#             values[z] = column_values[index]
#         q_code = []
#         if key in quality:
#             # q_values = []
#             # q_column = []
#             for y in column:
#                 if y in quality[key]:
#                     if quality[key][y] == "2":
#                         q_code.append(y)
#                     if quality[key][y] == "8":
#                         f_code[y] == '////'
#                     if quality[key][y] == 'N':
#                         f_code[y] == '---'
#         values['q_code'] = q_code
#
#         records.append(values)
#     return records, total_numbers

def initial_data(page, size, username, useradmin):
    records = []
    result = db.initial_data(page, size, username, useradmin)
    data = result[0]
    #  feature: f.eid, f.obs_time, e.name, f.obs_date, e.addr_value

    total_numbers = result[1]
    column = ['at_at1', 'ah_rh1', 'ws_iws1', 'wd_iwd', 'rs_rst', 'rs_ct10', 'rw_trs', 'rw_wft', 'rw_ift', 'rw_sft', 'av_avg1mhv']
    transfer = {'11': '干燥', '12': '潮湿', '13': '积水', '14': '雪', '15': '冰', '16': '霜', '17': '有融雪剂', '00': '状况未知',
                '99': '其他'}

    if not data:
        return False, 0
    for x in data:
        features = x[5: 5 + 11]
        # quality = x[5 + 11: 5 + 11 * 2]
        values = {
            "eid": x[0],
            "name": x[2],
            "obs_date": x[1],
            "address": x[4]}
        q_code = []
        for index, z in enumerate(column):
            # if quality[index] == '2':
            #     q_code.append(z)
            # elif quality[index] == "8":
            #     values[z] = '////'
            # elif quality[index] == 'N':
            #     values[z] = '---'
            # else:
            if z == 'rw_trs':
                if features[index]:
                    if features[index][:2] in transfer:
                        values[z] = transfer[features[index][:2]]
                    else:
                        values[z] = features[index]
                else:
                    values[z] = features[index]
            else:
                values[z] = features[index]
        values['q_code'] = q_code
        records.append(values)
    return records, total_numbers


def river_data(eid_list, column):
    period = [str(int(time.time()-3600)), str(int(time.time()))]
    result = db.feature_his(eid_list, column, period, '', '')[0]
    data = []
    reverse_column = db.get_reverse_column()
    for index, y in enumerate(column):
        for x in result:

            name = ''
            for z in reverse_column:
                if z['key'] == y:
                    name = z['value']
            data.append([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x[1])), float(x[5+index]), name])
    return data


def line_data(eid_list, column, period):
    soil_column = ['soil_volume', 'gravimetric_water', 'soil_moisture', 'aswc', 'soil_frequency',
                   'soil_voltage', 'nor_frequency']
    result = db.feature_his(eid_list, column, period, '', '')[0]
    data = []

    # if column[0] not in soil_column:
    #     for index, x in enumerate(column):
    #         box = {x:[[],[]]}
    #         for y in result:
    #             box[x][0].append(time.strftime("%Y-%m-%d %H:%M", time.localtime(y[1])))
    #             try:
    #                 box[x][1].append(float(y[5+index]))
    #             except:
    #                 box[x][1].append(y[5 + index])
    #
    #         data.append(box)

    if column[0] not in soil_column:
        for index, x in enumerate(column):
            i = len(result) - 1
            box = {x: [[], []]}
            while i > -1:
                box[x][0].append(time.strftime("%m-%d %H:%M", time.localtime(result[i][1])))
                try:
                    box[x][1].append(float(result[i][5 + index]))
                except:
                    box[x][1].append(result[i][5 + index])
                i -= 1
            data.append(box)
    else:
        i = len(result) - 1

        if i != -1:

            data = [{x: [[], []]} for x in range(1,len(result[i][5])+1)]
        while i > -1:

            try:
                for index, x in enumerate(result[i][5]):
                    data[index][index+1][0].append(time.strftime("%m-%d %H:%M", time.localtime(result[i][1])))
                    data[index][index+1][1].append(float(x))

            except:
                for index, x in enumerate(result[i][5]):
                    data[index][index+1][0].append(time.strftime("%m-%d %H:%M", time.localtime(result[i][1])))
                    data[index][index+1][1].append(None)
            i -= 1



    return data



def traffic_line(eid_list, column, period):

    result = db.traffic_line(eid_list, column, period, '', '')


    if result:
        records = {'time':[],'data':[]}
        for x in result:
            records['time'].append(time.strftime("%m-%d %H:%M", time.localtime(x[0])))
            records['data'].append(x[1])

        return records
    else:
        return False





def feature_his(eid_list, column, period, page, size):
    records = []
    result = db.feature_his(eid_list, column, period, page, size)
    data = result[0]
    #  feature: f.eid, f.obs_time, e.name, f.obs_date, e.addr_value

    total_numbers = result[1]
    soil_column = ['soil_volume', 'gravimetric_water', 'soil_moisture', 'aswc', 'soil_frequency', 'soil_voltage', 'nor_frequency']

    if not data:
        return False, 0
    for x in data:
        features = x[5: 5 + len(column)]
        quality = x[5 + len(column): 5 + len(column) * 2]
        values = {
            "eid": x[0],
            "name": x[2],
            "obs_date": x[1],
            "address": x[4]}
        q_code = []
        for index, z in enumerate(column):

            if quality[index] == '2':
                q_code.append(z)
            elif quality[index] == "8":
                values[z] = '////'
            elif quality[index] == 'N':
                values[z] = '---'
            else:
                if z in soil_column:
                    data = ''
                    if features[index]:
                        for index, x in enumerate(features[index]):
                            data += '第' + str(index+1) + '层：' + x + ';\r\n '
                            values[z] = data
                    else:
                        values[z] = features[index]
                else:
                    values[z] = features[index]
        values['q_code'] = q_code
        records.append(values)

    return records, total_numbers


def rain_fall_data(eid):
    data = db.rain_fall_data(eid)
    records = {"time" : [], "rain" : [], "road" : []}
    count = 0
    for x in data:
        records['time'].append(time.strftime("%H:%M", time.localtime(x[0])))
        records["rain"].append(x[1])
        if re.search('13',x[2]):
            count += 1
        records['road'].append(count)
    return records



