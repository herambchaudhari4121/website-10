import psycopg2
import re
from DBUtils.PooledDB import PooledDB
import json
import time
import psycopg2.extras

# pool = PooledDB(creator=psycopg2,  # 使用连接数据库的模块 psycopg2
#                 maxconnections=50,  # 连接池允许的最大连接数，0 和 None 表示不限制连接数
#                 mincached=5,  # 初始化时，链接池中至少创建的空闲的链接，0 表示不创建
#                 maxcached=20,  # 链接池中最多闲置的链接，0 和 None 不限制
#                 blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
#                 maxusage=None,  # 一个链接最多被重复使用的次数，None 表示无限制
#                 setsession=[],  # 开始会话前执行的命令列表
#                 host="192.168.0.43",
#                 port="5432",
#                 user="zygd",
#                 password="hzg61270388*!",
#                 database="WeatherSys")

# pool = PooledDB(creator=psycopg2,  # 使用连接数据库的模块 psycopg2
#                 maxconnections=50,  # 连接池允许的最大连接数，0 和 None 表示不限制连接数
#                 mincached=5,  # 初始化时，链接池中至少创建的空闲的链接，0 表示不创建
#                 maxcached=20,  # 链接池中最多闲置的链接，0 和 None 不限制
#                 blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
#                 maxusage=None,  # 一个链接最多被重复使用的次数，None 表示无限制
#                 setsession=[],  # 开始会话前执行的命令列表
#                 host="192.168.0.43",
#                 port="5432",
#                 user="zygd",
#                 password="hzg61270388*!",
#                 database="WeatherSys")


pool = PooledDB(creator=psycopg2,  # 使用连接数据库的模块 psycopg
                maxconnections=20,  # 连接池允许的最大连接数，0 和 None 表示不限制连接数
                mincached=5,  # 初始化时，链接池中至少创建的空闲的链接，0 表示不创建
                maxcached=20,  # 链接池中最多闲置的链接，0 和 None 不限制
                blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                maxusage=None,  # 一个链接最多被重复使用的次数，None 表示无限制
                setsession=[],  # 开始会话前执行的命令列表
                host="192.168.0.43",
                port="5432",
                user="zygd",
                password="hzg61270388*!",
                database="WeatherSys")




def wsys_user_pwd(username, pwd):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select * from wsys_user where user_name = '" + username + "' and  password ='" + pwd + "' ")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False



def code_transfer():
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select code, name from wsys_dict_code")
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False

class service:
    conn = pool.connection()
    cur = conn.cursor()

    def service(self,username, useradmin):
        try:


            if username == 'admin':
                self.cur.execute("with recursive tmp as ( select f.*, q.name as q_name, CONCAT_ws('/',c.name, b.name , a.name) as address\
                    from wsys_dict_range a join wsys_dict_range b on b.code = a.parent_code\
                    join wsys_dict_range c on c.code = b.parent_code join wsys_service f on f.location_code = a.code\
                    left join wsys_service q on f.parent_code = q.code where f.parent_code = '' or f.parent_code is null\
                    union all select a.* from (select f.*, q.name as q_name, CONCAT_ws('/',c.name, b.name , a.name) as address\
                    from wsys_dict_range a join wsys_dict_range b on b.code = a.parent_code\
                    join wsys_dict_range c on c.code = b.parent_code join wsys_service f on f.location_code = a.code\
                    left join wsys_service q on f.parent_code = q.code) a \
                    inner join tmp t on t.code=a.parent_code ) select * from tmp")
            else:
                self.cur.execute("with recursive tmp as ( select f.*, q.name as q_name, CONCAT_ws('/',c.name, b.name , a.name) as address\
                                from wsys_dict_range a join wsys_dict_range b on b.code = a.parent_code\
                                join wsys_dict_range c on c.code = b.parent_code join wsys_service f on f.location_code = a.code\
                                left join wsys_service q on f.parent_code = q.code where f.parent_code = '' or f.parent_code is null\
                                union all select a.* from (select f.*, q.name as q_name, CONCAT_ws('/',c.name, b.name , a.name) as address\
                                from wsys_dict_range a join wsys_dict_range b on b.code = a.parent_code\
                                join wsys_dict_range c on c.code = b.parent_code join wsys_service f on f.location_code = a.code\
                                left join wsys_service q on f.parent_code = q.code) a inner join tmp t on t.code=a.parent_code ) select tmp.* from tmp \
                				join wsys_service_user su on tmp.code = su.service_code join wsys_user u on su.user_id = u.id\
                				where u.user_name = '" + username + "'")

            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(e)
            return False


    def service_not_children(self, code):
        try:
            head = "select f.*, q.name as parent_name from wsys_service f left join wsys_service q\
                on f.parent_code = q.code  where f.code not in (with recursive tmp as ( select a.code\
                from wsys_service a where code="
            tail = " union all select a.code from wsys_service a \
                inner join tmp t on t.code=a.parent_code ) select * from tmp) order by f.code"

            query = head + "'" + code + "'" + tail
            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            return False

    def add_service(self, code, name, location_code, create_time, parent_code):
        try:
            table = "wsys_service"
            column = ["code", "name", "location_code", "create_time"]
            data = [[code, name, location_code, create_time]]

            if parent_code:
                column.append("parent_code")
                data[0].append(parent_code)

            query = insert_query(data, table, column)
            self.cur.execute(query)
            self.conn.commit()
            return 1
        except Exception as e:
            print(e)
            return 2


    def delete_handling(self, table, column, code_list):
        query = delete_query(table, column, code_list)
        try:
            self.cur.execute(query)
            return True
        except Exception as e:
            print(e)
            return False

    def delete_connection(self, code):
        try:
            self.cur.execute("delete from wsys_service_equipment where code = '" + code + "'")
            self.cur.execute("delete from wsys_service_user where service_code = '" + code + "'")
        except Exception as e:
            print(e)
            return False


    def delete_children_service(self, code):
        try:
            table = "wsys_service"
            update_data = {"parent_code": ""}
            w_column = "parent_code"
            w_value = code
            self.cur.execute(update_query(table, update_data, w_column, w_value))
            return True
        except Exception as e:
            print(e)
            return False

    def service_find_user(self, service_code):

        try:
            self.cur.execute("select s.user_id, u.user_name from wsys_user u join wsys_service_user s\
                on u.id = s.user_id where s.service_code =  '" + service_code + "'")

        except Exception as e:
            print(e)
            return False

        return self.cur.fetchall()


    def add_user_service(self, data):
        try:
            table = "wsys_service_user"
            column = ["user_id", "service_code"]
            # data = [[user_id, service_code]]

            self.cur.execute(insert_query(data, table, column))

        except Exception as e:
            print(e)
            return False
        return True

    # def update_user_service(self, user_id, service_code):
    #     try:
    #         self.cur.execute("update wsys_service_user set service_code = '" + service_code + "' \
    #                 where user_id = '" + user_id + "'")
    #     except Exception as e:
    #         print(e)
    #         return False
    #     return True

    def delete_user_service(self, code_list):
        table = 'wsys_service_user'
        column = 'user_id'
        try:
            self.cur.execute(delete_query(table, column, code_list))
        except Exception as e:
            print(e)
            return False
        return True

    def service_find_equipment(self, service_code):
        try:
            self.cur.execute("select e.eid, e.station_name\
                from wsys_service_equipment s join wsys_equipment_info e on s.eid = e.eid\
                 left join wsys_dict_code d on e.e_code = d.code where s.code = '" + service_code + "'")

        except Exception as e:
            print(e)
            return False

        return self.cur.fetchall()


    def add_equipment_service(self, data):
        # insert_query(data, table, column)
        try:
            column = ['eid', 'code']
            table = 'wsys_service_equipment'
            self.cur.execute(insert_query(data, table, column))
        except Exception as e:
            print(e)
            return False
        return True

    def delete_equipment_service(self, code_list):
        try:
            table = 'wsys_service_equipment'
            column = 'eid'
            self.cur.execute(delete_query(table, column, code_list))
        except Exception as e:
            print(e)
            return False
        return True

    def location_code_to_name(self, code_list):
        try:
            # self.cur.execute("select CONCAT_ws('/',c.name, b.name , a.name) as address\
            #     from wsys_dict_range a join wsys_dict_range b on b.code = a.parent_code\
            #     join wsys_dict_range c on c.code = b.parent_code where a.code = '" + code + "'")
            query = "select c.code, b.code, a.code, CONCAT_ws('/',c.name, b.name , a.name) as address\
                                            from wsys_dict_range a join wsys_dict_range b on b.code = a.parent_code\
                                            join wsys_dict_range c on c.code = b.parent_code where "
            if code_list:
                for x in code_list:
                    query += "a.code = '"
                    query += x
                    query += "' or "
                query = query[:-3]

                self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return self.cur.fetchall()

    def modify_service(self, code, name, parent_code, status, location_code):
        try:
            query = "update wsys_service set "
            if name:
                query += "name ='" + name + "',"
            if location_code:
                query += "location_code ='" + location_code + "',"
            if status:
                if not parent_code:
                    query += "parent_code = null,"
                else:

                    query += "parent_code = '" + parent_code + "',"

            query = query[:-1]
            query += " where code = '" + code + "'"
            self.cur.execute(query)
            return 1
        except Exception as e:
            print(e)
            return 2

    def unconnected_user(self):
        try:
            self.cur.execute("select id, user_name from wsys_user")
        except Exception as e:
            print(e)
            return False
        return self.cur.fetchall()

    def unconnected_equip(self):
        try:
            self.cur.execute("select eid, station_name from wsys_equipment_info where eid not in \
            (select e.eid from wsys_equipment_info e join wsys_service_equipment s on e.eid = s.eid) and e_code like '01%'")
        except Exception as e:
            print(e)
            return False
        return self.cur.fetchall()

    def db_confirm(self):
        self.conn.commit()
        return True

    def db_close(self):
        # self.conn.commit()
        self.cur.close()
        self.conn.close()
        self.conn = pool.connection()
        self.cur = self.conn.cursor()


def location():
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select * from wsys_dict_range")
        res = cur.fetchall()
        if len(res) == 0:
            return None
        else:
            return res
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return None



def service_find_equipment( service_code):

    conn = pool.connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("select e.eid, e.station_name\
        from wsys_service_equipment s join wsys_equipment_info e on s.eid = e.eid\
         left join wsys_dict_code d on e.e_code = d.code where s.code = '" + service_code + "'")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def service_not_children(code):
    conn = pool.connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    head = "select f.*, q.name as parent_name from wsys_service f left join wsys_service q\
        on f.parent_code = q.code  where f.code not in (with recursive tmp as ( select a.code\
        from wsys_service a where code="
    tail = " union all select a.code from wsys_service a inner join tmp t on t.code=a.parent_code ) select * from tmp) order by f.code"
    query = head + "'" + code + "'" + tail
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def all_service(username, useramdin):
    conn = pool.connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if useramdin == 2:
        cur.execute("with recursive tmp as ( select f.*,  CONCAT_ws('/',c.name, b.name , a.name) as address\
                from wsys_dict_range a join wsys_dict_range b on b.code = a.parent_code\
                join wsys_dict_range c on c.code = b.parent_code join wsys_service f on f.location_code = a.code\
                left join wsys_service q on f.parent_code = q.code where f.parent_code = '' or f.parent_code is null\
                union all select a.* from (select f.*,  CONCAT_ws('/',c.name, b.name , a.name) as address\
                from wsys_dict_range a join wsys_dict_range b on b.code = a.parent_code\
                join wsys_dict_range c on c.code = b.parent_code join wsys_service f on f.location_code = a.code\
                left join wsys_service q on f.parent_code = q.code) a \
                inner join tmp t on t.code=a.parent_code ) select * from tmp")
    else:
        cur.execute("with recursive tmp as ( select f.*, CONCAT_ws('/',c.name, b.name , a.name) as address\
                            from wsys_dict_range a join wsys_dict_range b on b.code = a.parent_code\
                            join wsys_dict_range c on c.code = b.parent_code join wsys_service f on f.location_code = a.code\
                            left join wsys_service q on f.parent_code = q.code where f.parent_code = '' or f.parent_code is null\
                            union all select a.* from (select f.*, CONCAT_ws('/',c.name, b.name , a.name) as address\
                            from wsys_dict_range a join wsys_dict_range b on b.code = a.parent_code\
                            join wsys_dict_range c on c.code = b.parent_code join wsys_service f on f.location_code = a.code\
                            left join wsys_service q on f.parent_code = q.code) a inner join tmp t on t.code=a.parent_code ) select tmp.* from tmp \
            				join wsys_service_user su on tmp.code = su.service_code join wsys_user u on su.user_id = u.id\
            				where u.user_name = '" + username + "'")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data




def service_tree(s_code):
    conn = pool.connection()
    cur = conn.cursor()

    service_code = s_code

    cur.execute("with recursive tmp as ( select a.id, a.code, a.name, a.parent_code, a.type \
                      from wsys_service a where code='" + service_code + "'  \
                      union all select a.id, a.code, a.name, a.parent_code, a.type from wsys_service a \
                         inner join tmp t on t.code=a.parent_code ) select * from tmp  ")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return column_name("wsys_service", data)


def user_find_service(user_id):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select service_code from wsys_service_user where user_id = '" + user_id + "'")
        service_code = cur.fetchone()[0]
        cur.close()
        conn.close()
        return service_code
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False


def read_paramater(eid):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        if eid:
            cur.execute("select * from wsys_equipment_extr where eid = '" + eid + "'")
        else:
            cur.execute("select * from wsys_equipment_extr")
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False



def user_name_exists(username):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select * from wsys_user where user_name = '" + str(username) + "'")
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False

def service_name_exists(name):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select * from wsys_service where name = '" + str(name) + "'")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False


def service_code_exists(service_code):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select * from wsys_service where code = '" + str(service_code) + "'")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False


def equip_find_user(eid):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select u.user_id from wsys_service_equipment e inner join wsys_service_user u on\
         u.service_code = e.code where e.eid = '" + eid + "'")
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False




class user:
    conn = pool.connection()
    cur = conn.cursor()

    def add_user(self, username, password, role, t):
        try:
            table = "wsys_user"
            column = ["user_name", "password", "role", "create_time"]
            data = [[username, password, role, t]]

            self.cur.execute(insert_query(data, table, column))

        except Exception as e:
            print(e)
            return False
        return True

    def username_find_id(self, username):
        try:
            self.cur.execute("select id from wsys_user where user_name = '" + str(username) + "'")
            user_id = self.cur.fetchone()[0]
        except Exception as e:
            print(e)
            return False
        return user_id

    def add_user_service(self, data):
        try:
            table = "wsys_service_user"
            column = ["user_id", "service_code"]
            # data = [[user_id, service_code]]

            self.cur.execute(insert_query(data, table, column))

        except Exception as e:
            print(e)
            return False
        return True

    def update_user_service(self, user_id, service_code):
        try:
            self.cur.execute("update wsys_service_user set service_code = '" + service_code + "' \
                    where user_id = '" + user_id + "'")
        except Exception as e:
            print(e)
            return False
        return True

    def delete_user_service(self, code_list):
        table = 'wsys_service_user'
        column = 'user_id'
        try:
            self.cur.execute(delete_query(table, column, code_list))
        except Exception as e:
            print(e)
            return False
        return True



    def modify_user(self, user_id):

        try:
            self.cur.execute("update wsys_user set password = '123456' where id = '" + user_id + "'")
        except Exception as e:
            print(e)
            return False
        return True


    def delete_user(self, user_id):
        try:
            user_query = "delete from wsys_user where id = '" + user_id + "'"
            self.cur.execute(user_query)
        except Exception as e:
            print(e)
            return 0
        return 1

    def db_confirm(self):
        self.conn.commit()
        return True

    def db_close(self):
        # self.conn.commit()
        self.cur.close()
        self.conn.close()
        self.conn = pool.connection()
        self.cur = self.conn.cursor()


# def equipments(service_code):
#     conn = psycopg2.connect(database="WeatherSys", user="zygd", password="zygd61270388", host="39.106.226.214",
#                             port="54321")
#     cur = conn.cursor()
#     tree = service_tree(service_code)
#     result = []
#     for x in tree:
#         if x[2] == service_code and x[3] == 'E':
#             result.append(x)
#     return result


class equipments:
    conn = pool.connection()
    cur = conn.cursor()
    def show_equip(self, eid_list, username, useradmin):
        try:
            if eid_list:
                query = 'select * from wsys_equipment_info where '
                for x in eid_list:
                    query += " eid = '" + x + "' or "
                query = query[:-4]
                self.cur.execute(query)
            else:
                if useradmin == 3:
                    self.cur.execute("select distinct e.* from wsys_equipment_info e \
                    join wsys_service_equipment se on e.eid = se.eid\
                    join wsys_service s on se.code = s.code\
                    join wsys_service_user su on s.code = su.service_code\
                    join wsys_user u on su.user_id = u.id\
                    where u.user_name = '" + username + "' order by e.station_id")
                else:
                    self.cur.execute("select * from wsys_equipment_info order by station_id")
            data = self.cur.fetchall()
            return data
        except Exception as e:
            print(e)
            return False

    def show_sub_device(self, eid_list):
        try:
            query = "select  e.eid, e.id, s.station_name, d.name from wsys_equipment_info i join wsys_equipment_extr e\
            on i.eid = e.eid join wsys_equipment_info s on e.p_value[1] = s.eid join wsys_dict_code d on\
             e.p_code = d.code where e.p_code like '03%'"
            if eid_list:
                query += " and ("
                for x in eid_list:
                    query += " e.eid = '" + x + "' or "
                query = query[:-4]
                query += ")"
            self.cur.execute(query)
            data = self.cur.fetchall()
            return data
        except Exception as e:
            print(e)
            return False

    def show_extra(self, eid):
        try:
            query = "select * from wsys_equipment_extr where eid = '" + eid + "'"
            self.cur.execute(query)
            data = self.cur.fetchall()
            return data
        except Exception as e:
            print(e)
            return False

    def unconnected_equip(self):

        try:
            self.cur.execute(
                "select * from wsys_equipment_info where eid not in (select code from wsys_service where type = 'E')")
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            return False

    def equip_name(self):
        try:

            self.cur.execute("select eid, station_name from wsys_equipment_info where e_code not like '03%'")


            # if e_code:
            #     self.cur.execute("select eid, station_name from wsys_equipment_info where e_code = '" + e_code + "'")
            # else:
            #     self.cur.execute("select eid, station_name from wsys_equipment_info")
            data = self.cur.fetchall()
            return data
        except Exception as e:
            print(e)
            return False






    def add_basic_info(self, column, data):
        try:
            table = "wsys_equipment_info"
            self.cur.execute(insert_query(data, table, column))
        except Exception as e:
            print(e)
            return 0
        return 1

    def add_extend(self, data):
        try:
            table = "wsys_equipment_extr"
            column = ["eid", "p_code", "p_value"]
            self.cur.execute(insert_query(data, table, column))
        except Exception as e:
            print(e)
            return 0
        return 1

    def update_extend(self, update_data, eid):

        try:
            for x in update_data:

                self.cur.execute("update wsys_equipment_extr set p_value = '{" + update_data[x] + "}' \
                where eid = '" + eid + "' and p_code = '" + x + "'")


        except Exception as e:
            print(e)
            return False
        return True

    def delete_extend(self, code_list):
        try:
            table = 'wsys_equipment_extr'
            column = 'id'
            query = delete_query(table, column, code_list)
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True



    def equip_exist(self, eid, station_id, station_name):
        try:
            select_query = "select eid from wsys_equipment_info where "
            if station_id:
                station_id_query = " station_id = '" + station_id + "'"
                self.cur.execute(select_query + station_id_query)
                if self.cur.fetchall():
                    return 2
            if station_name:
                station_name_query = " station_name = '" + station_name + "'"
                self.cur.execute(select_query + station_name_query)
                if self.cur.fetchall():
                    return 3
            if eid:
                eid_query = " eid = '" + eid + "'"
                self.cur.execute(select_query + eid_query)
                if self.cur.fetchall():
                    return 4
            return False
        except Exception as e:
            print(e)
            return False
        return

    def equip_type(self, e_code):
        try:
            if e_code:
                if e_code != "03%":
                    self.cur.execute("select * from wsys_equipment_info where e_code = '" + e_code + "' order by station_id")
                else:
                    self.cur.execute("select * from wsys_equipment_info where e_code like '" + e_code + "'order by station_id")
            else:
                self.cur.execute("select * from wsys_equipment_info")
        except Exception as e:
            print(e)
            return False
        return self.cur.fetchall()

    def unconnected_assist_equip(self):
        try:
            self.cur.execute("select * from wsys_equipment_info where e_code like '03%' and eid not in\
                (select p_value[1] from wsys_equipment_extr where p_code like '03%')")
        except Exception as e:
            print(e)
            return False
        return self.cur.fetchall()

    def delete_equipments(self, eid):
        table_info = 'wsys_equipment_info'
        table_extr = 'wsys_equipment_extr'
        column = 'eid'
        code_list = [eid]
        query_info = delete_query(table_info, column, code_list)

        query_extr = delete_query(table_extr, column, code_list)
        try:
            self.cur.execute(query_info)
            self.cur.execute(query_extr)
        except Exception as e:
            print(e)
            return False
        return True

    def update_basic(self, basic, eid):
        query = update_query('wsys_equipment_info', basic, 'eid', eid)
        try:
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def add_equipment_service(self, data):
        # insert_query(data, table, column)
        try:
            column = ['eid', 'code']
            table = 'wsys_service_equipment'
            self.cur.execute(insert_query(data, table, column))
        except Exception as e:
            print(e)
            return False
        return True

    def delete_equipment_service(self, code_list):
        try:
            table = 'wsys_service_equipment'
            column = 'eid'
            self.cur.execute(delete_query(table, column, code_list))
        except Exception as e:
            print(e)
            return False
        return True

    def get_parameter(self, id_list):
        try:
            query = "select id, p_value from wsys_equipment_extr where "
            for x in id_list:
                query += " id = " + str(x) + " or "
            query = query[:-3]
            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            return False

    def modify_db_station_id(self, eid, station_id):
        try:
            query = update_query('wsys_equipment_info', [station_id], 'eid', eid)
            self.cur.execute(query)
            return True
        except Exception as e:
            print(e)
            return False
        return






    def map_point(self, username, useradmin):
        if useradmin == 2:
            query = "select e.eid, e.station_name, e.address, e.longitude, e.latitude, st.status, st.opt_time, \
                t1.obs_time, t1.warning_lvl, t1.warning_value, t1.warning_type\
                from wsys_equipment_info e \
                left join wsys_equipment_status st on e.eid = st.eid\
                left join (select * from wsys_warning_info where (eid, obs_time) in \
                (select max(eid) as eid, max(obs_time) as obs_time from wsys_warning_info where obs_time >= "\
                + str(int(time.time()) - 10800000) + " group by eid)) as t1\
                on e.eid = t1.eid where e.e_code not like '03%' "
        else:
            query = "select e.eid, e.station_name, e.address, e.longitude, e.latitude, st.status, st.opt_time,\
                t1.obs_time, t1.warning_lvl, t1.warning_value, t1.warning_type\
                from wsys_equipment_info e left join wsys_equipment_status st on e.eid = st.eid\
                left join (select * from wsys_warning_info where (eid, obs_time) in \
                (select max(eid) as eid, max(obs_time) as obs_time from wsys_warning_info where obs_time >= "\
                + str(int(time.time()) - 10800000) + " group by eid)) as t1\
                on e.eid = t1.eid join wsys_service_equipment se on e.eid = se.eid\
                join wsys_service s on se.code = s.code\
                join wsys_service_user su on s.code = su.service_code\
                join wsys_user u on su.user_id = u.id\
                where u.user_name = '" + username + "' and e.e_code not like '03%'"

        try:
            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            return False

    def get_status(self, username, useradmin):
        try:

            if useradmin == 2:
                self.cur.execute("select e.station_id, e.station_name, st.status, f.obs_time, f.at_at1, f.ah_rh1, f.wd_iwd, f.ws_iws1,\
                    f.mntrnfl, f.av_avg1mhv, f.rs_rst, f.rs_ct10, f.rw_wft, f.rw_ift, f.rw_sft, f.rw_trs, f.wetslipcoef, sn.mainclctrvltgval, e.eid\
                    from wsys_equipment_info e \
                    join wsys_feature_now f on e.eid = f.eid\
                    join wsys_sensor_now sn on e.eid = sn.eid\
                    join wsys_equipment_status st on e.eid = st.eid\
                    where e.e_code = '0101'\
                    order by e.station_name")
            else:
                self.cur.execute("select e.station_id, e.station_name, st.status, f.obs_time, f.at_at1, f.ah_rh1, f.wd_iwd, f.ws_iws1,\
                    f.mntrnfl, f.av_avg1mhv, f.rs_rst, f.rs_ct10, f.rw_wft, f.rw_ift, f.rw_sft, f.rw_trs, f.wetslipcoef, sn.mainclctrvltgval, e.eid\
                    from wsys_equipment_info e \
                    join wsys_feature_now f on e.eid = f.eid\
                    join wsys_service_equipment se on e.eid = se.eid\
                    join wsys_service_user su on se.code = su.service_code\
                    join wsys_user u on su.user_id = u.id\
                    join wsys_sensor_now sn on e.eid = sn.eid\
                    join wsys_equipment_status st on e.eid = st.eid\
                    where u.user_name = '" + username + "' and e.e_code not like '03%'\
                    order by e.station_name")

        except Exception as e:
            print(e)
            return False
        data = self.cur.fetchall()
        return data


    def add_status(self, eid):
        try:
            self.cur.execute("insert into wsys_equipment_status (eid, status, opt_time) values ('" + eid + "',0,"\
                             + str(int(time.time())) + ")")
        except Exception as e:
            print(e)
            return False
        return True

    def delete_status(self, eid):
        try:
            self.cur.execute("delete from wsys_equipment_status where eid = '" + eid + "'")
        except Exception as e:
            print(e)
            return False
        return True

    def db_confirm(self):
        self.conn.commit()
        return True

    def db_close(self):
        # self.conn.commit()
        self.cur.close()
        self.conn.close()
        self.conn = pool.connection()
        self.cur = self.conn.cursor()



def user_list(username, useramdin):
    conn = pool.connection()
    cur = conn.cursor(cursor_factory= psycopg2.extras.RealDictCursor)

    if useramdin == 2:
        cur.execute("select u.id, u.user_name, s.name as service_name, w.service_code, u.create_time from wsys_user u\
         left join wsys_service_user w on u.id = w.user_id left join wsys_service s on w.service_code = s.code")
    else:
        cur.execute("select u.id, u.user_name, s.name as service_name, w.service_code, u.create_time from wsys_user u\
                         left join wsys_service_user w on u.id = w.user_id left join wsys_service s on w.service_code = s.code\
                         where u.user_name = '" + username + "'")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data





def delete_query(table, column, code_list):
    query = "delete from " + table + " where "
    # character = column_is_character(table)
    character = character_column(table)
    if column in character:
        for x in code_list:
            query += column + " = '" + x + "'"
            query += " or "
    else:
        for x in code_list:
            query += column + " = " + str(x)

            query += " or "

    query = query[:-3]
    return query


def insert_query(data, table, column):
    query = "insert into " + table + " (" + ','.join(column) + ") values "
    # character = column_is_character(table)
    character = character_column(table)
    for x in data:
        query += "("
        for index, y in enumerate(x):
            if column[index] in character:
                query += "'" + str(y) + "',"
            else:
                query += str(y) + ","
        query = query[:-1]
        query += "),"

    query = query[:-1]

    return query


def get_success_num(eid_list, useradmin):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        if useradmin == 2:

            cur.execute("select eid, count(obs_time) from wsys_feature_his where obs_time >= " + str(int(time.time()) - 86400) + " group by eid ")
            data = cur.fetchall()
        else:
            if eid_list:
                query = "select eid, count(obs_time) from wsys_feature_his where obs_time > " + str(int(time.time()) - 86400) + " where "
                for x in eid_list:
                    query += "eid = '" + x + "' or "
                query = query[:-4]
                query += " group by eid"
                cur.execute(query)
                data = cur.fetchall()

            else:
                return None
        cur.close()
        conn.close()

        return data

    except Exception as e:
        cur.close()
        conn.close()
        print(e)
        return False





def read_status():
    conn = pool.connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("select e.eid, e.station_name, e.longitude, e.latitude, e.address, s.status, s.opt_time as status_time \
        from wsys_equipment_info e left join wsys_equipment_status s on e.eid = s.eid where e.e_code like '01%'")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def equip_user():
    conn = pool.connection()
    cur = conn.cursor()
    cur.execute("select e.eid, u.user_name from wsys_equipment_info e \
        join wsys_service_equipment se on e.eid = se.eid\
        join wsys_service_user su on se.code = su.service_code\
        join wsys_user u on su.user_id = u.id where e.e_code like '01%'")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def get_warning( username, useradmin, period):
    conn = pool.connection()
    cur = conn.cursor()
    if useradmin == 2:
        query = "select e.eid, e.station_name, e.address, e.longitude, e.latitude, st.status, st.opt_time, \
            t1.obs_time, t1.warning_lvl, t1.warning_value, t1.warning_type\
            from wsys_equipment_info e \
            left join wsys_equipment_status st on e.eid = st.eid\
            right join (select * from wsys_warning_info where (eid, obs_time, warning_type) in \
            (select max(eid) as eid, max(obs_time) as obs_time, warning_type from wsys_warning_info where obs_time >= "\
            + str(int(time.time()) - period) + " group by eid, warning_type)) as t1\
            on e.eid = t1.eid where e.e_code not like '03%' "
    else:
        query = "select e.eid, e.station_name, e.address, e.longitude, e.latitude, st.status, st.opt_time,\
            t1.obs_time, t1.warning_lvl, t1.warning_value, t1.warning_type\
            from wsys_equipment_info e left join wsys_equipment_status st on e.eid = st.eid\
            right join (select * from wsys_warning_info where (eid, obs_time, warning_type) in \
            (select max(eid) as eid, max(obs_time) as obs_time, warning_type from wsys_warning_info where obs_time >= "\
            + str(int(time.time()) - period) + " group by eid, warning_type)) as t1\
            on e.eid = t1.eid join wsys_service_equipment se on e.eid = se.eid\
            join wsys_service s on se.code = s.code\
            join wsys_service_user su on s.code = su.service_code\
            join wsys_user u on su.user_id = u.id\
            where u.user_name = '" + username + "' and e.e_code not like '03%'"

    try:
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except Exception as e:
        cur.close()
        conn.close()
        print(e)
        return False



def update_query(table, update_data, w_column, w_value):

    query = "update " + table + " set "

    # character = column_is_character(table)
    character = character_column(table)
    for x in update_data:
        if x in character:
            query += str(x) + " = '" + str(update_data[x]) + "' , "
        else:
            query += str(x) + " = " + str(update_data[x]) + " , "

    query = query[:-2]
    query += " where "
    query += w_column + " = '" + str(w_value) + "'"

    return query


def character_column(table):
    with open('weatherSys/cold_data/character.json', 'r', encoding='utf8')as fp:
        json_data = json.load(fp)

    return json_data[table]






def initial_data(page, size, username, useradmin):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        if useradmin == 2:
            query = "select f.eid, f.obs_time, e.station_name, f.obs_date, e.address, f.at_at1, f.ah_rh1, f.ws_iws1, f.wd_iwd, \
            f.rs_rst, f.rs_ct10, f.rw_trs, f.rw_wft, f.rw_ift, f.rw_sft, f.av_avg1mhv \
            from wsys_equipment_info e  left join wsys_feature_now f on e.eid = f.eid \
            left join wsys_quality_now q on f.eid = q.eid and f.obs_time = q.obs_time \
            where e.e_code not like '03%' \
            order by e.station_name"
            query += " limit " + size + " offset " + str((int(page) - 1) * int(size))
            cur.execute(query)
            data = cur.fetchall()
            count_query = "select count(f.eid) from wsys_equipment_info e  left join wsys_feature_now f on e.eid = f.eid \
            left join wsys_quality_now q on f.eid = q.eid and f.obs_time = q.obs_time where e.e_code not like '03%'"
            cur.execute(count_query)
            total_numbers = cur.fetchall()

            return data, total_numbers[0][0]
        else:
            query = "select f.eid, f.obs_time, e.station_name, f.obs_date, e.address, f.at_at1, f.ah_rh1, f.ws_iws1, f.wd_iwd, \
                        f.rs_rst, f.rs_ct10, f.rw_trs, f.rw_wft, f.rw_ift, f.rw_sft, f.av_avg1mhv \
                        from wsys_equipment_info e  left join wsys_feature_now f on e.eid = f.eid \
                        left join wsys_quality_now q on f.eid = q.eid and f.obs_time = q.obs_time \
            join wsys_service_equipment se on e.eid = se.eid\
            join wsys_service s on se.code = s.code\
            join wsys_service_user su on s.code = su.service_code\
            join wsys_user u on su.user_id = u.id\
            where u.user_name = '" + username + "' and e.e_code not like '03%'\
            order by e.station_name"
            query += " limit " + size + " offset " + str((int(page) - 1) * int(size))
            cur.execute(query)
            data = cur.fetchall()
            count_query = "select count(f.eid) from wsys_equipment_info e  left join wsys_feature_now f on e.eid = f.eid \
                        left join wsys_quality_now q on f.eid = q.eid and f.obs_time = q.obs_time join wsys_service_equipment se on e.eid = se.eid\
            join wsys_service s on se.code = s.code\
            join wsys_service_user su on s.code = su.service_code\
            join wsys_user u on su.user_id = u.id\
            where e.e_code not like '03%'"
            cur.execute(count_query)
            total_numbers = cur.fetchall()

            return data, total_numbers[0][0]

    except Exception as e:
        conn.close()
        cur.close()
        print(e)
        return False







def feature_his(eid_list, column, period, page, size):
    conn = pool.connection()
    cur = conn.cursor()
    try:

        start = period[0]
        end = period[1]
        select_query = "select f.eid, f.obs_time, e.station_name, f.obs_date, e.address, "
        from_query = " from wsys_feature_his f left join wsys_equipment_info e on e.eid = f.eid \
        left join wsys_quality_his q on f.eid = q.eid and f.obs_time = q.obs_time "
        id_query = "where ("
        total_numbers = 0


        for x in eid_list:
            id_query += "f.eid = '"
            id_query += x
            id_query += "' or "
        id_query = id_query[:-3]
        id_query += ")"
        time_query = " and f.obs_time >=" + start + " and f.obs_time <=" + end

        if column == None:
            select_query = "select f.*"


        else:
            for x in column:
                select_query += "f." + x + " , "
            for x in column:
                select_query += "q." + x + " , "
            select_query = select_query[:-2]

        if page:
            limit_query = " limit " + size + " offset " + str((int(page) - 1) * int(size))
            count_query = "select count (*) "
            cur.execute(count_query + from_query + id_query + time_query)
            total_numbers = cur.fetchall()[0][0]

        else:
            limit_query = ""

        order_query = " order by f.obs_date desc, e.station_name "
        cur.execute(select_query + from_query + id_query + time_query + order_query + limit_query)

        feature = cur.fetchall()



        cur.close()
        conn.close()
        return feature, total_numbers


    except Exception as e:
        conn.close()
        cur.close()
        print(e)
        return False


def traffic_line(eid_list, column, period, page, size):
    conn = pool.connection()
    cur = conn.cursor()
    try:

        start = period[0]
        end = period[1]
        select_query = "select obs_time, "
        if "mainclctrvltgval" in column:
            from_query = " from wsys_sensor_his "
        else:
            from_query = " from wsys_feature_his"
        id_query = " where ("

        for x in eid_list:
            id_query += "eid = '"
            id_query += x
            id_query += "' or "
        id_query = id_query[:-3]
        id_query += ")"
        time_query = " and obs_time >=" + start + " and obs_time <=" + end + " and obs_time % 3600 = 0"

        if column == None:
            select_query = "select *"


        else:
            for x in column:
                select_query += x + " , "
            select_query = select_query[:-2]

        order_query = " order by obs_time"
        cur.execute(select_query + from_query + id_query + time_query + order_query)
        feature = cur.fetchall()

        cur.close()
        conn.close()
        return feature


    except Exception as e:
        conn.close()
        cur.close()
        print(e)
        return False




def event_count(username, useradmin):
    conn = pool.connection()
    cur = conn.cursor()
    if useradmin == 2:
        query = "select * from wsys_warning_info"
    else:
        query = "select w.* from wsys_warning_info w join wsys_service_equipment se on w.eid = se.eid\
                join wsys_service_user su on se.code = su.service_code join wsys_user u on su.user_id = u.id\
                where u.user_name = '" + username + "'"

    try:
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except Exception as e:
        cur.close()
        conn.close()
        print(e)
        return False



def rain_fall_data(eid):
    conn = pool.connection()
    cur = conn.cursor()
    query = "select obs_time, mntrnfl, rw_trs from wsys_feature_his where obs_time >= " + str(int(time.time()) - 3600) + \
        " and eid = '" + eid + "'"
    try:

        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False



def quality_his(eid_list, period):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        start = period[0]
        end = period[1]
        query = "select eid, obs_time, quality_info from wsys_quality_his where "
        id_query = "("
        for x in eid_list:
            id_query += "eid = '"
            id_query += x
            id_query += "' or "
        id_query = id_query[:-3]
        id_query += ")"
        time_query = " and obs_time >=" + start + " and obs_time <=" + end
        cur.execute(query + id_query + time_query)
        quality = {}

        result = cur.fetchall()

        for x in result:
            if x[2]:
                key = x[0] + str(x[1])
                quality[key] = x[2]
        cur.close()
        conn.close()
        return quality
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False


def current_data():
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select eid, feature_info, obs_time from wsys_feature_now where eid like 'HZG07%'")
        return cur.fetchall()
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False


def equip_name_redis():
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select distinct u.user_name, e.e_code, e.eid, e.station_name from wsys_equipment_info e \
            join wsys_service_equipment se on e.eid = se.eid \
            join wsys_service s on se.code = s.code \
            join wsys_service_user su on s.code = su.service_code \
            join wsys_user u on su.user_id = u.id")
        data = cur.fetchall()
        return data
    except Exception as e:
        print(e)
        return False




def get_column():
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "select name, ex_value from wsys_dict_code where code like '04020%'  and ex_value is not null")

        result = cur.fetchall()
        box = []
        for x in result:
            column = {"key": x[0], "value": x[1]}
            box.append(column)
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False


def get_reverse_column():
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "select ex_value, name from wsys_dict_code where code like '04020%'  and ex_value is not null")

        result = cur.fetchall()
        box = []
        for x in result:
            column = {"key": x[0], "value": x[1]}
            box.append(column)
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False


def features_filter():
    column = get_column()
    result = []

    for x in column:
        if not re.search(r'max|min|ews|trs|\d+mw|exw', x['key']):
            result.append(x)

    return result


def get_column_name(table):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "select column_name from information_schema.columns  where table_name= '" + table + "' order by ordinal_position")
        column = cur.fetchall()
        cur.close()
        conn.close()
        return column
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False


def column_is_character(table):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select column_name, data_type from information_schema.columns where table_name = '" + table + "'")
        column = cur.fetchall()
        result = {}
        for x in column:
            if x[1] == 'character varying':
                result[x[0]] = True
            else:
                result[x[0]] = False
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False


def column_name(table, data):
    # column = get_column_name(table)
    with open('weatherSys/cold_data/column.json', 'r', encoding='utf8')as fp:
        json_data = json.load(fp)

    column = json_data[table]
    if column:
        result = []
        for x in data:
            d = {}
            for index, y in enumerate(x):
                d[column[index]] = y
            result.append(d)

        return result


def feature_now(eid_list):
    conn = pool.connection()
    cur = conn.cursor()

    try:
        where_query = ""
        if eid_list:
            where_query = " where "
            for x in eid_list:
                where_query += "f.eid = '"
                where_query += x
                where_query += "' or "

            where_query = where_query[:-3]

        select_query = "select f.eid, e.station_name, f.obs_time, f.feature_info, q.quality_info from wsys_feature_now f left join \
        wsys_quality_now q on f.eid = q.eid left join wsys_equipment_info e on f.eid = e.eid "
        query = select_query + where_query
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return False


def his(eid_list, period):
    start = period[0]
    end = period[1]
    select_query = "select f.eid, e.name, f.obs_time, f.feature_info, q.quality_info "
    from_query = "from wsys_feature_his f left join wsys_quality_his q on f.eid = \
    q.eid left join wsys_equipment_info e on f.eid = e.eid "
    id_query = "where ("
    for x in eid_list:
        id_query += "f.eid = '"
        id_query += x
        id_query += "' or "
    id_query = id_query[:-3]
    id_query += ")"
    time_query = " and f.obs_time >=" + start + " and f.obs_time <=" + end

    conn = psycopg2.connect(database="postgres", user="postgres", password="1", host="localhost", port="6603")
    cur = conn.cursor()

    try:
        cur.execute(select_query + from_query + id_query + time_query)
        result = cur.fetchall()
        return result
    except Exception as e:
        print(e)
        return


def get_dic(parent_code):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select * from wsys_dict_code where parent_code = '" + parent_code + "'")
    except Exception as e:
        print(e)
        return False
    return cur.fetchall()


def show_dict():
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select code, name from wsys_dict_code")
    except Exception as e:
        print(e)
        return False

    return cur.fetchall()


def num_letter():
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select code, ex_value from wsys_dict_code where ex_value is not null")
    except Exception as e:
        print(e)
        return False

    return cur.fetchall()


def authority_check(username):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select role from wsys_user where user_name = '" + username + "'")
    except Exception as e:
        print(e)
        return False

    return cur.fetchone()[0]














