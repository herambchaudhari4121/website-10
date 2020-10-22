from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import random
import logging
from asgiref.sync import async_to_sync
from . import current_data as cd
import json
from redis import StrictRedis
redis_10 = StrictRedis(host='localhost', port=6379, db=10, decode_responses=True, password='hzg61270388*!')
import time

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

        print('关闭连接')


    async def test_message(self, event):
        data = event['data']
        await self.send_json(data)

    async def remote_control(self, message):
        return



    async def receive_json(self, content, **kwargs):
        # if 'username' not in content:
        current_data = cd.current_data()
        eid = content['eid']
        last_eid = content['last_eid']
        # key = "asgi:group:"+eid
        # redis_10.zrem(key, self.channel_name)
        # await redis_10.delete(key)
        if last_eid:
            await self.channel_layer.group_discard(last_eid, self.channel_name)
        # self.disconnect(eid)

        await self.channel_layer.group_add(eid, self.channel_name)
        try:
            data = json.dumps(current_data.data_box[eid])
        except:
            data = json.dumps({"result":None})
        await self.channel_layer.group_send(eid, {"type": "test_message", "data": data})
        # else:
        #     username = content['username']
        #     await self.channel_layer.group_add(username, self.channel_name)


# class statusWarningMonitor(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         logging.info('warning_connect')
#         # await self.channel_layer.group_add(username, self.channel_name)
#
#     async def receive_json(self, content, **kwargs):
#         username = content['username']
#         await self.channel_layer.group_add(username, self.channel_name)
#
#     async def disconnect(self, code):
#         print('关闭连接')
#
#     async def status_warning_monitor(self, event):
#         data = event['data']
#         await self.send_json(data)


class RemoteControl(AsyncJsonWebsocketConsumer):
    async def connect(self):
        logging.info('back_connect')
        await self.accept()
        await self.channel_layer.group_add('back_end', self.channel_name)
        await self.channel_layer.group_send('back_end', {"type": "back_connect", "data": {"result":"connect_success"}})




    async def disconnect(self, code):
        print('关闭连接')

    async def receive_json(self, content, **kwargs):
        logging.info(content)
        await self.channel_layer.group_send('back_end', {"type": "back_connect", "data": {"result": "receive"}})


    async def back_connect(self, event):
        logging.info(event)
        data = event['data']
        logging.info(data)
        await self.send_json(data)