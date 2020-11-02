from redis import StrictRedis
import math
redis_0 = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True, password='hzg61270388*!')
redis_3 = StrictRedis(host='localhost', port=6379, db=3, decode_responses=True, password='hzg61270388*!')
from . import current_data as cd
current_data = cd.current_data()
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()

def hypotenuse(angle, long):
    radian = 2 * math.pi/360*angle
    side_1 = math.sin(radian) * long
    side_2 = math.cos(radian) * long

    return side_1, side_2






def data_processing(eid, data):
    try:
        wind_direction = data['wd_iwd']
        wind_speed = data['ws_iws1']
        longitude = redis_3.hget(eid,'longitude')
        latitude = redis_3.hget(eid,'latitude')
        if latitude == None:
            return False
        direction_tag = [89, 179, 269, 359]
        special_direction = [90, 180, 270]
        angle = 0
        if wind_direction in special_direction:
            if wind_direction == 90:
                side_length = [wind_speed,0]
            if wind_direction == 180:
                side_length = [0,wind_speed]
            if wind_direction == 270:
                side_length = [-wind_speed, 0]
        else:
            side_length = hypotenuse(wind_direction, wind_speed)


        records = [float(longitude),float(latitude),float(side_length[0]),float(side_length[1]),float(wind_speed)]
        return records
    except:
        return False

def create_data(username):
    records = []
    if username == 'admin':
        for x in current_data.data_box:
            data = data_processing(x, current_data.data_box[x])
            if data:
                records.append(data)
                add_data = [data[0] + 3, data[1] + 3, data[2], data[3], data[4]]
                minus_data = [data[0] - 3, data[1] - 3, data[2], data[3], data[4]]
                records.append(add_data)
                records.append(minus_data)
        data = {"data": records, "data_type": "wind_data"}
        print(data)
        return data
    else:
        eid_list = [y.split(":")[0] for y in redis_0.hget(username, '0101').split(',')]
        records = []
        if eid_list[0]:
            for y in eid_list:
                data = data_processing(y, current_data.data_box[y])
                if data:
                    records.append(data)

                    add_data = [data[0] + 3, data[1] + 3, data[2], data[3], data[4]]
                    minus_data = [data[0] - 3, data[1] - 3, data[2], data[3], data[4]]
                    records.append(add_data)
                    records.append(minus_data)

        data = {"data": records, "data_type": "wind_data"}
        return data



def wind_send():
    user_list = redis_0.keys('*')
    for x in user_list:
        data = create_data(x)
        async_to_sync(channel_layer.group_send)(x, {"type": "test_message", "data": data})
    data = create_data('admin')
    print(data)
    async_to_sync(channel_layer.group_send)('admin', {"type": "test_message", "data": data})
    #     eid_list = [x.split(":")[0] for x in redis_0.hget(x,'0101').split(',')]
    #     records = []
    #     if eid_list[0]:
    #         for y in eid_list:
    #             data = data_processing(y, current_data.data_box[y])
    #             if data:
    #                 records.append(data)
    #     print(records)
    #     data = {"data": records, "data_type": "wind_data"}
    #     async_to_sync(channel_layer.group_send)(x, {"type": "test_message", "data": data})
    # records = []
    # for x in current_data.data_box:
    #     data = data_processing(x,current_data.data_box[x])
    #     if data:
    #         records.append(data)
    # data = {"data":records,"data_type":"wind_data"}
    # async_to_sync(channel_layer.group_send)("admin", {"type": "test_message", "data": data})

