from weatherSys import db_handling as db
from django.shortcuts import render
import time
from . import result_to_dic

user = db.user()


def add(username, password, service_code, role):
    code = 1
    # 用户名已存在
    if db.user_name_exists(username):
        user.db_close()
        return 2
    # 项目号不存在
    if service_code:
        if not db.service_code_exists(service_code):
            user.db_close()
            return 3
    t = int(time.time())
    if not user.add_user(username, password, role, t):
        user.db_close()
        return 0
    if not role:
        if service_code:
            if not user.add_user_service([[user.username_find_id(username), service_code]]):
                user.db_close()
                return 0
    if user.db_confirm():
        user.db_close()
    else:
        user.db_close()
    return 1


# def user_list(username, useramdin):
#     u = user.user_list(username, useramdin)
#     column = ['id', 'user_name', 'service_name', 'service_code', 'create_time']
#     unique_user_id = []
#     unique_user = []
#     for index,x in enumerate(u):
#         if x[0] not in unique_user_id:
#             unique_user.append(x)
#             unique_user_id.append(x[0])
#     result = result_to_dic.to_dic(unique_user, column)
#     user.db_close()
#     return result


def user_list(username, useramdin):
    u = db.user_list(username, useramdin)
    data = [dict(row) for row in u]
    return data



def modify_user(user_id):


    if not user.modify_user(user_id):
        user.db_close()
        return 0
    if user.db_confirm():
        user.db_close()
    else:
        user.db_close()
    return 1


def delete_user(user_id, service_code):
    if not user.delete_user(user_id):
        user.db_close()
        return 0
    if service_code:
        if not user.delete_user_service([user_id]):
            user.db_close()
            return 0
    if user.db_confirm():
        user.db_close()
    else:
        user.db_close()
    return 1

