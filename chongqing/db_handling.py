import psycopg2
import re
from DBUtils.PooledDB import PooledDB
import json

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


def soil_map(username, obs_time):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        if username == 'admin':
            cur.execute("select * from (select e.*, st.status, st.opt_time, r.name, n.btryvltgsts1 from wsys_equipment_info e \
			   join wsys_service_equipment se on e.eid = se.eid \
			   join wsys_sensor_now n on e.eid = n.eid \
			   join wsys_service_user su on se.code = su.service_code \
			   join wsys_user u on u.id = su.user_id \
			   join wsys_service s on su.service_code = s.code \
			   join wsys_dict_range r on s.location_code = r.code \
			   join wsys_equipment_status st on e.eid = st.eid ) as t1 \
			   left join (select eid, obs_time, soil_volume, soil_moisture from wsys_feature_now where obs_time >= " + obs_time + ") as t2 \
			   on t1.eid = t2.eid") #可以去掉几个join
        else:
            cur.execute("select * from (select e.*, st.status, st.opt_time, r.name, n.btryvltgsts1 from wsys_equipment_info e \
			   join wsys_service_equipment se on e.eid = se.eid \
			   join wsys_sensor_now n on e.eid = n.eid \
			   join wsys_service_user su on se.code = su.service_code \
			   join wsys_user u on u.id = su.user_id \
			   join wsys_service s on su.service_code = s.code \
			   join wsys_dict_range r on s.location_code = r.code \
			   join wsys_equipment_status st on e.eid = st.eid \
			   where u.user_name = '" + username + "') as t1 \
			   left join (select eid, obs_time, soil_volume, soil_moisture from wsys_feature_now where obs_time >= " + obs_time + ") as t2 \
			   on t1.eid = t2.eid")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except Exception as e:
        conn.close()
        cur.close()
        print(e)

def soil_data_receive(username, obs_time):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        if username == 'admin':
            cur.execute("select count(t2.obs_time),count(t1.eid),t1.name from (select e.*,r.name from wsys_equipment_info e \
			   join wsys_service_equipment se on e.eid = se.eid join wsys_service_user su on se.code = su.service_code\
				join wsys_service s on se.code = s.code join wsys_user u on u.id = su.user_id\
			   join wsys_dict_range r on r.code = s.location_code) as t1\
                left join (select e.eid, f.obs_time, f.soil_volume, f.soil_moisture from wsys_equipment_info e \
                join wsys_feature_his f on  f.eid = e.eid where e.e_code = '0102' and f.obs_time >= " + obs_time + ") as t2\
                on t1.eid = t2.eid group by t1.name")
        else:
            cur.execute("select count(t2.obs_time),count(t1.eid),t1.name from (select e.*,r.name from wsys_equipment_info e \
			   join wsys_service_equipment se on e.eid = se.eid join wsys_service_user su on se.code = su.service_code\
				join wsys_service s on se.code = s.code join wsys_user u on u.id = su.user_id\
			   join wsys_dict_range r on r.code = s.location_code where u.user_name = '" + username + "') as t1\
                left join (select e.eid, f.obs_time, f.soil_volume, f.soil_moisture from wsys_equipment_info e \
                join wsys_feature_his f on  f.eid = e.eid where e.e_code = '0102' and f.obs_time >= " + obs_time + ") as t2\
                on t1.eid = t2.eid group by t1.name")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except Exception as e:
        conn.close()
        cur.close()
        print(e)

    return False


def report_rate(station_id, username, obs_time):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        if username == 'admin':
            cur.execute("select * from (select count(t2.obs_time), t1.eid from (select e.* from wsys_equipment_info e \
			   join wsys_service_equipment se on e.eid = se.eid join wsys_service_user su on se.code = su.service_code\
				join wsys_service s on se.code = s.code join wsys_user u on u.id = su.user_id) as t1\
                left join (select e.eid, f.obs_time, f.soil_volume, f.soil_moisture from wsys_equipment_info e \
                join wsys_feature_his f on  f.eid = e.eid where e.e_code = '0102' and f.obs_time >= " + obs_time + " and \
                f.obs_time < " + str(int(obs_time)+86400) + ") as t2\
                on t1.eid = t2.eid group by t1.eid) as t3\
				join (select e.*, st.status from wsys_equipment_info e join wsys_equipment_status st on e.eid = st.eid) as t4\
				on t3.eid = t4.eid")
        else:
            if not station_id:
                cur.execute("select * from (select count(t2.obs_time), t1.eid from (select e.* from wsys_equipment_info e \
                   join wsys_service_equipment se on e.eid = se.eid join wsys_service_user su on se.code = su.service_code\
                    join wsys_service s on se.code = s.code join wsys_user u on u.id = su.user_id\
                    where u.user_name = '" + username +"') as t1\
                    left join (select e.eid, f.obs_time, f.soil_volume, f.soil_moisture from wsys_equipment_info e \
                    join wsys_feature_his f on  f.eid = e.eid where e.e_code = '0102' and f.obs_time >= " + obs_time + " and \
                    f.obs_time < " + str(int(obs_time)+86400) + ") as t2\
                    on t1.eid = t2.eid group by t1.eid) as t3\
                    join (select e.*, st.status from wsys_equipment_info e join wsys_equipment_status st on e.eid = st.eid) as t4\
                    on t3.eid = t4.eid")
            else:
                cur.execute("select * from (select count(t2.obs_time), t1.eid from (select e.* from wsys_equipment_info e \
                                   join wsys_service_equipment se on e.eid = se.eid join wsys_service_user su on se.code = su.service_code\
                                    join wsys_service s on se.code = s.code join wsys_user u on u.id = su.user_id\
                                    where e.station_id = '" + station_id + "') as t1\
                                    left join (select e.eid, f.obs_time, f.soil_volume, f.soil_moisture from wsys_equipment_info e \
                                    join wsys_feature_his f on  f.eid = e.eid where e.e_code = '0102' and f.obs_time >= " + obs_time + " and \
                                    f.obs_time < " + str(int(obs_time) + 86400) + ") as t2\
                                    on t1.eid = t2.eid group by t1.eid) as t3\
                                    join (select e.*, st.status from wsys_equipment_info e join wsys_equipment_status st on e.eid = st.eid) as t4\
                                    on t3.eid = t4.eid")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except Exception as e:
        conn.close()
        cur.close()
        print(e)
        return False


def get_report(station_id, obs_time):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select f.obs_time from wsys_equipment_info e \
            join wsys_feature_his f on  f.eid = e.eid\
            where e.station_id = '" + station_id + "' and f.obs_time >=" +  obs_time + " and \
                f.obs_time < " + str(int(obs_time)+86400) + "order by f.obs_time")
        data = cur.fetchall()
        cur.close()
        conn.close()

        return data

    except Exception as e:
        conn.close()
        cur.close()
        print(e)
        return False


def district_station(username):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        if username == 'admin':
            cur.execute("select r.name, r.code, e.eid, e.station_id, e.station_name from wsys_equipment_info e \
            join wsys_service_equipment se on e.eid =se.eid join wsys_service_user su on se.code=su.service_code \
            join wsys_user u on su.user_id = u.id join wsys_service s on su.service_code = s.code \
            join wsys_dict_range r on r.code = s.location_code")
        else:
            cur.execute("select r.name, r.code, e.eid, e.station_id, e.station_name from wsys_equipment_info e \
            join wsys_service_equipment se on e.eid =se.eid join wsys_service_user su on se.code=su.service_code \
            join wsys_user u on su.user_id = u.id join wsys_service s on su.service_code = s.code \
            join wsys_dict_range r on r.code = s.location_code where user_name = '" + username + "'")

        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except Exception as e:
        conn.close()
        cur.close()
        print(e)
        return False


def chongqing_features(username, start, end, district, station_id):
    conn = pool.connection()
    cur = conn.cursor()
    try:

        if station_id:
            cur.execute("select * from (select e.*, st.status, st.opt_time, r.name, n.btryvltgsts1 from wsys_equipment_info e \
               join wsys_service_equipment se on e.eid = se.eid \
               join wsys_sensor_now n on e.eid = n.eid \
               join wsys_service_user su on se.code = su.service_code \
               join wsys_user u on u.id = su.user_id \
               join wsys_service s on su.service_code = s.code \
               join wsys_dict_range r on s.location_code = r.code \
               join wsys_equipment_status st on e.eid = st.eid \
               where e.station_id = '" + station_id + "') as t1 \
               left join (select eid, obs_time, soil_volume, soil_moisture from wsys_feature_his where obs_time >= "\
                + start + " and obs_time < " + end + ") as t2 on t1.eid = t2.eid")
        else:
            if district:
                cur.execute("select * from (select e.*, st.status, st.opt_time, r.name, n.btryvltgsts1 from wsys_equipment_info e \
                               join wsys_service_equipment se on e.eid = se.eid \
                               join wsys_sensor_now n on e.eid = n.eid \
                               join wsys_service_user su on se.code = su.service_code \
                               join wsys_user u on u.id = su.user_id \
                               join wsys_service s on su.service_code = s.code \
                               join wsys_dict_range r on s.location_code = r.code \
                               join wsys_equipment_status st on e.eid = st.eid \
                               where u.user_name = '" + username + "' and r.code = '" + district + "') as t1 \
                               left join (select eid, obs_time, soil_volume, soil_moisture from wsys_feature_his where obs_time >= " \
                            + start + " and obs_time < " + end + ") as t2 on t1.eid = t2.eid")
            else:
                cur.execute("select * from (select e.*, st.status, st.opt_time, r.name, n.btryvltgsts1 from wsys_equipment_info e \
                                               join wsys_service_equipment se on e.eid = se.eid \
                                               join wsys_sensor_now n on e.eid = n.eid \
                                               join wsys_service_user su on se.code = su.service_code \
                                               join wsys_user u on u.id = su.user_id \
                                               join wsys_service s on su.service_code = s.code \
                                               join wsys_dict_range r on s.location_code = r.code \
                                               join wsys_equipment_status st on e.eid = st.eid \
                                               where u.user_name = '" + username + "') as t1 \
                                               left join (select eid, obs_time, soil_volume, soil_moisture from wsys_feature_his where obs_time >= " \
                            + start + " and obs_time < " + end + ") as t2 on t1.eid = t2.eid")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except Exception as e:
        conn.close()
        cur.close()
        print(e)



class equipments:
    conn = pool.connection()
    cur = conn.cursor()

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

    def show_extr(self, eid_list):
        try:
            query = "select * from wsys_equipment_extr where p_code like '02%' or p_code = '010202'"
            if eid_list:
                query += " and ("
                for x in eid_list:
                    query += " eid = '" + x + "' or "
                query = query[:-4]
                query += ")"
            self.cur.execute(query)
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
                    print("select distinct e.* from wsys_equipment_info e \
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

    def add_extend(self, data):
        try:
            table = "wsys_equipment_extr"
            column = ["eid", "p_code", "p_value"]
            self.cur.execute(insert_query(data, table, column))
        except Exception as e:
            print(e)
            return 0
        return 1

    def update_extend(self, update_data):

        try:
            query = "UPDATE wsys_equipment_extr SET p_value = CASE id "
            for x in update_data:
                if update_data[x]:

                    query += " WHEN " + x + " THEN ARRAY " + "[" + "'" + "','".join(update_data[x]) + "'" + "] "
                else:
                    query += " WHEN " + x + " THEN ARRAY [''] "

            query += " END WHERE id IN (" + ','.join(update_data.keys()) + ")"
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


def kriging(username, timestamp):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select f.soil_volume, f.obs_time, e.station_name, e.longitude, e.latitude, u.user_name \
            from wsys_feature_his f\
            join wsys_equipment_info e on f.eid = e.eid\
            join wsys_service_equipment se on se.eid = e.eid\
            join wsys_service_user su on su.service_code = se.code\
            join wsys_user u on su.user_id = u.id\
            where u.user_name = '" + username + "' and f.obs_time = " + timestamp )

        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    except Exception as e:
        conn.close()
        cur.close()
        print(e)





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

def character_column(table):
    with open('weatherSys/cold_data/character.json', 'r', encoding='utf8')as fp:
        json_data = json.load(fp)

    return json_data[table]

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

def equip_location(username):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute("select e.eid, r.name from wsys_equipment_info e\
            join wsys_service_equipment se on e.eid = se.eid\
            join wsys_service s on se.code = s.code\
            join wsys_service_user su on su.service_code = s.code\
            join wsys_user u on su.user_id = u.id\
            join wsys_dict_range r on s.location_code = r.code\
            where u.user_name = '" + username + "'")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    except Exception as e:
        conn.close()
        cur.close()
        print(e)