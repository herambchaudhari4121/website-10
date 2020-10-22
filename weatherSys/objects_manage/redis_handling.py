from redis import StrictRedis
from weatherSys import db_handling as db
# from channels.layers import get_channel_layer
# channel_layer = get_channel_layer()
from asgiref.sync import async_to_sync


class redis_manage:
    def __init__(self):
        self.redis_0 = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True, password = 'hzg61270388*!')
        self.redis_1 = StrictRedis(host='localhost', port=6379, db=1, decode_responses=True, password = 'hzg61270388*!')
        self.redis_3 = StrictRedis(host='localhost', port=6379, db=3, decode_responses=True, password='hzg61270388*!')
        self.redis_4 = StrictRedis(host='localhost', port=6379, db=4, decode_responses=True, password = 'hzg61270388*!')
        print('start redis')
        # self.redis_0.flushall()
        # self.redis_1.flushall()
        # self.redis_4.flushall()
        get_column = db.get_column()
        show_dic = db.show_dict()
        num_letter = db.num_letter()
        self.redis_1.hmset("get_column",{x[0]:x[1] for x in get_column})
        self.redis_1.hmset("show_dict", {x[0]: x[1] for x in show_dic})
        self.redis_1.hmset("num_letter", {x[0]: x[1] for x in num_letter})
        data = db.read_paramater('')
        extend_data = {}
        for x in data:
            if x[1] in extend_data:
                extend_data[x[1]][x[2]] = x[3]
            else:
                extend_data[x[1]] = {x[2]:x[3]}
        print(extend_data)

        # self.redis_4.flushall()
        for x in extend_data:
            self.add_paramater(x, extend_data[x])
        read_equip_name()
        equip_find_user()
        read_status()



    def download_count(self, username):
        self.redis_1.incr(username)
        if int(self.redis_1.get(username)) == 1:
            self.redis_1.expire(username, 3600)
            return self.redis_1.get(username)
        else:
            return self.redis_1.get(username)


    def add_paramater(self, eid, extend_data):
        try:
            for x in extend_data:
                data = {x:','.join(extend_data[x]) for x in extend_data}
            self.redis_4.hmset(eid, data)
            return True
        except:
            return False


def read_equip_name():
    try:
        redis_0 = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True, password='hzg61270388*!')
        data = db.equip_name_redis()
        data_box = {}
        print(1)

        for x in data:
            if x[0] not in data_box:
                data_box[x[0]] = {'0101':'', '0102':''}
            data_box[x[0]][x[1]]+=x[2] + ':' + x[3]
            data_box[x[0]][x[1]] += ','
        print(2)
        for x in data_box:
            for y in data_box[x]:
                data_box[x][y] = data_box[x][y][:-1]
        print(3)
        print(data_box)
        for x in data_box:
            redis_0.hmset(x, data_box[x])
        return True
    except Exception as e:
        print(e)
        return False


def equip_find_user():
    try:
        redis_1 = StrictRedis(host='localhost', port=6379, db=1, decode_responses=True, password='hzg61270388*!')
        data = db.equip_name_redis()
        weather = {}
        soil = {}
        for x in data:
            if x[1] == '0101':
                if x[2] not in weather:
                    weather[x[2]] = ''
                weather[x[2]] += x[0] + ','
            else:
                if x[2] not in soil:
                    soil[x[2]] = ''
                soil[x[2]] += x[0] + ','
        for x in weather:
            weather[x] = weather[x][:-1]
        for x in soil:
            soil[x] = soil[x][:-1]
        print('weathery', weather)
        redis_1.hmset('weather_user', weather)
        redis_1.hmset('soil_user', soil)
        return True
    except Exception as e:
        print(e)
        return False

def read_status():
    try:
        redis_3 = StrictRedis(host='localhost', port=6379, db=3, decode_responses=True, password='hzg61270388*!')
        redis_3.flushdb()
        data = db.read_status()
        box = {}
        for x in data:
            box[x[0]] = {"station_name":x[1], "longitude":float(x[3]),"latitude":float(x[4]), "address": x[7], "status":x[11], "status_time": x[12]}
        print(box)
        for x in box:

            redis_3.hset(name = x, mapping = box[x])
        return True
    except Exception as e:
        print(e)
        return False


# class warning_status_monitor:
#     def __init__(self):
#         self.redis_1 = StrictRedis(host='localhost', port=6379, db=1, decode_responses=True, password='hzg61270388*!')
#
#
#         return
#
#     async def monitor_status(self):
#         pubsub = self.redis_1.pubsub()
#         pubsub.psubscribe("__keyevent@1__:hset station_status")
#         for data in pubsub.listen():
#             if data:
#                 data = self.redis_1.hgetall('station_status')
#                 data
#                 async_to_sync(channel_layer.group_send)({"type": "test_message", "data": data})

