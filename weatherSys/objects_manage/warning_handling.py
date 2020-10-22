from weatherSys import db_handling as db
import pandas as pd
import time


def event_count(username, useradmin):
    warning_type = {1: '高温预警', 2: '路面状况预警', 3: '能见度预警', 4: '降雨预警', 5: '大风预警'}
    data = db.event_count(username, useradmin)
    print('warning', data)
    # warning_data = {1:[],2:[],3:[],4:[],5:[]}
    warning_data = {}
    count = {1:0,2:0,3:0,4:0,5:0}
    total = 0
    if data:
        for x in data:
            if x[0] not in warning_data:
                warning_data[x[0]] = {1:[],2:[],3:[],4:[],5:[]}
            warning_data[x[0]][x[4]].append(x[1])

        for x in warning_data:
            for y in warning_data[x]:
                if y == 2:
                    print(warning_data[x][y])

                box = []
                for index, z in enumerate(warning_data[x][y]):
                    if len(warning_data[x][y]) > 1:
                        if index > 0 and z - warning_data[x][y][index - 1] > 10800:
                            box.append(z - warning_data[x][y][index - 1])
                    else:
                        box = warning_data[x][y]
                num = len(box)

                count[y] += num
                total += num
    print(count)
    transfer_count = {}
    for x in count:
        transfer_count[warning_type[x]] = count[x]

    result = {'count':transfer_count, 'total':total}
    return result

def get_warning(username, useradmin):

    warning = db.get_warning(username, useradmin, 1008000000)

    warning_type = {1: '高温预警', 2: '路面状况预警', 3: '能见度预警', 4: '降雨预警', 5: '大风预警'}
    warning_lev = {1: '红', 2: '橙', 3: '黄', 4: '蓝'}
    result = []
    for x in warning:
        result.append({'date': time.strftime("%m-%d %H:%M:%S", time.localtime(x[7])), 'name': x[1], 'warning':warning_type[x[10]]})


    return  result


