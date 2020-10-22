from django.test import TestCase

# Create your tests here.
import requests
import json
import time
import random
from weatherSys import db_handling as db
from treelib import Tree, Node

time_start=time.time()

# eid = ['HZGEXT0306', 'HZGEXT9527', 'HZGEXT45', 'HZGEXT789', 'HZGEXT987', 'HZGEXT456', 'HZGEXT321', 'HZG0723423002', 'HZG0765489002', 'HZGEXT65489', 'HZGEXT99999', 'HZGEXT963', 'HZGEXT258', 'HZGEXT53219545', 'HZGEXT484348761348', 'HZGEXT165464658', 'HZG070B1005002', 'HZGEXT4545548', 'HZGEXT464613484', 'HZGEXT46465483135', 'HZGEXT8551354', '104', 'HZG0774123002', 'HZGEXT88522', 'HZGEXT464', 'HZG07653945002', 'HZG04DN24648451', 'HZGEXT546465464', 'HZG07741852963002', 'HZGEXT963852741', 'HZG04DN247898563', 'HZG04DN215648454848', 'HZG04DN246548465465']



# for x in range(100):
#     requests.post('http://172.18.2.168:1234/', data = json.dumps({"eid":"HZG070B1011002", "size": "12", "page":"1","start_time":"1392816699","end_time":"1592816699","feature_filter":["at_maxat1"]}), verify=False)
#     print(x)


# for x in range(100):
#     print(x)
#     requests.post('http://172.18.2.168:1234/show_equip', data = json.dumps({'eid_list':x}), verify=False)

# for x in range(100):
#     print(x)
#     requests.post('http://172.18.2.168:1234/equip_name', verify=False)


# for x in range(100):
#     print(x)
#     requests.post('http://172.18.2.168:1234/features', verify=False)


# for x in range(100):
#     print(x)
#     requests.post('http://172.18.2.168:1234/features_filter', verify=False)

# for x in range(100):
#     print(requests.post('http://172.18.2.168:1234/feature_now', data = json.dumps({'eid':''}), verify=False).text)



# for x in range(100):
#
#     print(requests.post('http://172.18.2.168:1234/features_his', data = json.dumps({"eid":["HZG070B1011002"], "page":"1","start_time":1392816699000,"end_time":1592816699000,"feature_filter":["at_at1"]}), verify=False))


# for x in range(100):
#     print(x)
#     requests.post('http://172.18.2.168:1234/service_tree', verify=False)


# code = [('901',), ('526',), ('100000',), ('105',), ('103',), ('201',), ('952',), ('300',), ('107',), ('202',), ('400',), ('401',), ('639',), ('200',), ('104',), ('106',)]
#
#
# for x in code:
#     requests.post('http://172.18.2.168:1234/all_service', data = json.dumps({'code': x[0]}), verify=False)

# for x in range(100):
#     print(x)
#     requests.post('http://172.18.2.168:1234/user_list', verify=False)


# for x in range(100):
#     print(x)
#     requests.post('http://172.18.2.168:1234/location_tree', verify=False)


# for x in range(100):
#     print(x)
#     requests.post('http://172.18.2.168:1234/equip_type',data = json.dumps({'e_code': '3'}), verify=False)


# for x in range(100):
#     print(x)
#     requests.post('http://172.18.2.168:1234/unconnected_assist_equip', verify=False)


# for x in range(100):
#     print(x)
#     requests.post('http://172.18.2.168:1234/equip_all_info', data = json.dumps({'e_code': ''}), verify=False)


# for x in range(100):
#     print(x)
#     requests.post('http://172.18.2.168:1234/show_dict', verify=False)


# for x in code:
#     print(x)
#     requests.post('http://172.18.2.168:1234/objects_under_service',data = json.dumps({'service_code': x[0]}), verify=False)
#

# for x in range(100):
while True:
    # requests.post('http://172.18.2.168:1234/live_data_distribution', data = json.dumps({"eid": "HZG070A4007002", "data": {"obs_time": str(int(time.time())-random.randint(0,100000)),"at_at1":random.randint(0,100), "ah_rh1":random.randint(0,100), "rs_ct10":random.randint(0,100), "rs_rst": random.randint(0,100), "wd_iwd": random.randint(0,100), "ws_iws1":random.randint(0,100), "av_avg1mhv": random.randint(0,100), "pm25": random.randint(0,100), "mntrnfl": random.randint(0,100), "rw_wft": random.randint(0,100), "rw_ift": random.randint(0,100), "rw_sft": random.randint(0,100), "rw_trs":"121111", "wetslipcoef": random.randint(0,100)}}), verify=False)
    requests.post('http://172.18.2.168:1234/live_data_distribution', data=json.dumps({"eid": "HZG070A4007002", "data": {
        "obs_time": str(int(time.time()) - random.randint(0, 100000)), "at_at1": random.randint(0, 100),
        "ah_rh1": random.randint(0, 100), "rs_ct10": random.randint(0, 100), "rs_rst": random.randint(0, 100),
        "wd_iwd": random.randint(0, 100), "ws_iws1": random.randint(0, 100), "av_avg1mhv": random.randint(0, 100),
        "pm25": random.randint(0, 100), "mntrnfl": random.randint(0, 100), "rw_wft": random.randint(0, 100),
        "rw_ift": random.randint(0, 100), "rw_sft": random.randint(0, 100), "rw_trs": "121111",
        "wetslipcoef": random.randint(0, 100),"a":random.randint(0, 100),"b":random.randint(0, 100),"c":random.randint(0, 100),"d":random.randint(0, 100)}}), verify=False)

    time.sleep(1)
    # print(x)


time_end = time.time()
print('totally cost', (time_end-time_start)/100)