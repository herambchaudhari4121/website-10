from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
from asgiref.sync import async_to_sync
from redis import StrictRedis
import time
import logging



def send_live_data(eid, data):
    async_to_sync(channel_layer.group_send)(eid, {"type": "test_message", "data": data})


async def status_warning_monitor(username, data):
    await channel_layer.group_send(username, {"type": "status_warning_monitor", "data": data})


