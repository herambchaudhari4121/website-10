import psycopg2


def initiate_db():
    # conn = psycopg2.connect(database="WeatherSys", user="zygd", password="zygd61270388", host="39.106.226.214", port="54321")
    # return conn.cursor()
    return


def single_result(data):
    return data[0][0]

def wsys_user_pwd (username,pwd):
    cur = initiate_db()

    cur.execute("select * from wsys_user where user_name = '" + username +"' and  password ='" + pwd + "' " )
    return cur.fetchall()





def user_find_service (user_id):
    cur = initiate_db()

    cur.execute("select service_code from wsys_service_user where user_id = '" + user_id +"'" )
    rows = cur.fetchall()

    service_set = []
    for x in rows:
        cur.execute("select * from wsys_service_struct where code = '" + x[0] + "'")

        service_set.append(cur.fetchall()[0])


    return service_set


def find_child (service_code):
    cur = initiate_db()
    cur.execute("select * from wsys_service_struct where parent_code = '" + service_code + "'")

    return cur.fetchall()











