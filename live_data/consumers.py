from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import random
import logging
from asgiref.sync import async_to_sync
from . import current_data as cd
current_data = cd.current_data()
import json
from redis import StrictRedis
redis_10 = StrictRedis(host='localhost', port=6379, db=10, decode_responses=True, password='hzg61270388*!')
from . import wind_data as wd
import time
import token_module


@database_sync_to_async
def save_channel_name(key, channel_name, group_name):
    """
    :param key:
    :param channel_name:
    :param group_name:
    :return:
    """
    # 这里可以通过redis或数据库将对于的channel_name, group_name保存下来。
    pass


class ListDataConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # 这
        # key = self.scope['url_route']['kwargs']['peronId']  # 在websocket链接的时候获取到用户标识，可以从jwt信息中获取，可以在路由中获取某个参数作为标识
        print(self.scope)
        logging.info('connect')
        # key = eval(self.scope['query_string'])
        # print(key)
        uid = str(random.randint(0,100))

        # group_name = 'group_' + key
        # await save_channel_name(uid, self.channel_name)
        # # 当前频道添加进频道组

        # await self.channel_layer.group_add(eid, self.channel_name)

        await self.accept()
        # await self.send_json({"result":"connection successful"})
        # await self.channel_layer.group_send(eid, {"type": "test.message", "data": {"eid": "12345"}})
    async def disconnect(self, code):
        print(self.__dict__)
        if 'channel_name' in self.__dict__:
            if 'username' in self.__dict__:
                await self.channel_layer.group_discard(self.username,self.channel_name)
            if 'eid' in self.__dict__:
                await self.channel_layer.group_discard(self.eid, self.channel_name)
        print('关闭连接')


    async def test_message(self, event):
        data = event['data']
        await self.send_json(data)

    async def remote_control(self, message):
        return



    async def receive_json(self, content, **kwargs):
        # if 'username' not in content:

        if content['data_type'] == 'live_data':
            current_data = cd.current_data()
            self.eid = content['eid']
            last_eid = content['last_eid']
            if 'username' and 'token' in content:
                username = content['username']
                token = content['token']
                if not token_module.authenticate(username, token):
                    await self.channel_layer.group_send(self.eid, {"type": "test_message", "data": {"data":"token过期","data_type":"token"}})
                useradmin = token_module.authenticate(username, token)

                if last_eid:
                    await self.channel_layer.group_discard(last_eid, self.channel_name)
                # self.disconnect(eid)
                await self.channel_layer.group_add(self.eid, self.channel_name)
                # picture = 'sun.jpg'
                try:
                    # data = json.dumps(current_data.data_box[self.eid])
                    data = current_data.data_box[self.eid]
                    picture_name = cd.get_pic(data)
                except:
                    # data = json.dumps({"result":None})
                    data = {"result": None}
                    picture_name = ''
                await self.channel_layer.group_send(self.eid, {"type": "test_message", "data": {"data":data,"data_type":"live_data","picture":picture_name}})

            else:
                await self.channel_layer.group_send(self.eid, {"type": "test_message",
                                                          "data": {"data": "缺少username/token", "data_type": "token"}})


        if content['data_type'] == 'real_data':
            # self.channel_layer.group_send()
            await self.channel_layer.group_add('real_data', self.channel_name)
            eid = content['eid']
            data = content['data']
            for x in data:
                data[x] = data[x]
            current_data.new_data(eid, data)
            data = current_data.data_box[eid]
            picture_name = cd.get_pic(data)

            await self.channel_layer.group_send(eid,{"type": "test_message", "data": {"data": data, "data_type": "live_data","picture":picture_name}})


        if content['data_type'] == 'wind_data':
            current_data = cd.current_data()
            if 'username' and 'token' in content:
                self.username = content['username']
                token = content['token']
                if not token_module.authenticate(self.username, token):
                    await self.channel_layer.group_send(self.username, {"type": "test_message", "data": {"data":"token过期","data_type":"token"}})
                useradmin = token_module.authenticate(self.username, token)
                await self.channel_layer.group_add(self.username, self.channel_name)
                wind_data = wd.create_data(self.username)
                if wind_data["data"]:
                    await self.channel_layer.group_send(self.username, {"type": "test_message", "data": wind_data})
                else:
                    await self.channel_layer.group_send(self.username, {"type": "test_message", "data":{"result":None}})
            else:
                await self.channel_layer.group_send(self.eid, {"type": "test_message",
                                                          "data": {"data": "缺少username/token", "data_type": "token"}})





