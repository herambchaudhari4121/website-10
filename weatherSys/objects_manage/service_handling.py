from weatherSys import db_handling as db
from django.shortcuts import render
from treelib import Tree, Node
from . import result_to_dic
import time
import json
from . import redis_handling as redis_h

service = db.service()
# user = db.user()
# equipments = db.equipments()


def add_service(code, name, location_code, create_time, parent_code):
    if db.service_code_exists(code):
        service.db_close()
        return 3
    if db.service_name_exists(name):
        service.db_close()
        return 4
    if parent_code:
        if not db.service_code_exists(parent_code):
            service.db_close()
            return 0
    result = service.add_service(code, name, location_code, create_time, parent_code)
    if service.db_confirm():
        service.db_close()
    else:
        service.db_close()
    return result


def get_service_tree():
    s = service.service()

    column = ['code', 'name', 'location_code', 'create_time', 'parent_code', 'parent_name','address']
    result = result_to_dic.to_dic(s, column)
    tree = Tree()
    tree.create_node('root', 'root')


    for x in result:
        if not x['parent_code']:
            tree.create_node(str(x['code']), str(x['code']), parent='root', data=x['name'])
        else:
            tree.create_node(str(x['code']), str(x['code']), parent=x['parent_code'], data=x['name'])

    def transfer(code):
        if not tree.children(code):
            struct = {
                'id': code,
                'label': tree.nodes[code].data,
            }
            return struct
        struct = {
            'id': code,
            'label': tree.nodes[code].data,
            'children': []
        }
        for node in tree.children(code):
            struct['children'].append(transfer(node.tag))

        return struct

    result = []
    for x in tree.children('root'):
        result.append(transfer(x.identifier))
    service.db_close()
    return result



def all_service(code, username, useradmin):
    if code:
        s = db.service_not_children(code)
    else:
        s = db.all_service(username, useradmin)
    return [dict(row) for row in s]



def get_location_tree():
    with open('weatherSys/cold_data/location.json', 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
    return json_data['children']


def modify_service(code, name, parent_code, status, location_code):
    if not db.service_code_exists(code):
        service.db_close()
        return 3
    if db.service_name_exists(name):
        service.db_close()
        return 4
    if parent_code:
        if not db.service_code_exists(parent_code):

            service.db_close()
            return 0
    result = service.modify_service(code, name, parent_code, status, location_code)
    if result == 1:
        if service.db_confirm():
            service.db_close()
        else:
            service.db_close()
    service.db_close()
    return result


def delete_service(code):
    if not db.service_code_exists(code):
        service.db_close()
        return 2
    if not service.delete_handling("wsys_service", "code", [code]):
        service.db_close()
        return 0
    if not service.delete_children_service(code):
        service.db_close()
        return 3
    account_id = [i[0] for i in service.service_find_user(code)]
    if account_id:
        if not service.delete_handling("wsys_service_user", "id", account_id):
            service.db_close()
            return 4
    equip_id = [i[0] for i in service.service_find_equipment(code)]

    if equip_id:
        if not service.delete_handling("wsys_service_equipment", "eid", equip_id):
            service.db_close()
            return 5
    if service.db_confirm():
        service.db_close()
    else:
        service.db_close()
    return 1



def objects_under_service(service_code):
    # service_equip = equip_under_service(service_code)
    # service_user = user_under_service(service_code)
    # unconnected_e = unconnected_equip()
    # unconnected_u = unconnected_user()
    column = ['eid', 'station_name']
    service_equip = result_to_dic.to_dic(service.service_find_equipment(service_code), column)
    column = ['user_id', 'user_name']
    service_user = result_to_dic.to_dic(service.service_find_user(service_code), column)
    column = ['eid', 'station_name']
    unconnected_e = result_to_dic.to_dic(service.unconnected_equip(), column)
    column = ['user_id', 'user_name']
    unconnected_u = result_to_dic.to_dic(service.unconnected_user(), column)

    for x in unconnected_u:
        x['selected'] = False
    for x in unconnected_e:
        x['selected'] = False
    for x in service_equip:
        unconnected_e.append({'eid': x['eid'], 'station_name': x['station_name'], 'selected': True})
    for x in service_user:
        for y in unconnected_u:
            if x['user_id'] == y['user_id']:
                y['selected'] = True
        # unconnected_u.append({'user_id': x['user_id'], 'user_name': x['user_name'], 'selected': True})

    records = {'un_connected_user': unconnected_u, 'un_connected_equip': unconnected_e}
    service.db_close()

    return records


def manage_connection(data):

    service.delete_connection(data['service_code'])


    if data['user_id']:
        if not service.add_user_service([[x, data['service_code']] for x in data['user_id']]):
            service.db_close()
            return 4


    if data['eid']:
        if not service.add_equipment_service([[x, data['service_code']] for x in data['eid']]):
            service.db_close()

    # equipments.db_confirm()
    # user.db_confirm()


    if service.db_confirm():
        service.db_close()
    else:
        service.db_close()
    redis_h.read_equip_name()
    redis_h.equip_find_user()
    return 1
