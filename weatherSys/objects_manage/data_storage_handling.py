import pandas as pd
from . import feature_handling as fh
from weatherSys import db_handling as db
import time
equipments = db.equipments()


def data_transfer(period, eid_list, column):
    result = db.feature_his(eid_list, column, period, '', '')
    data = result[0]
    features = {x:[] for x in column}
    for x in data:
        for index, y in enumerate(column):
            features[y].append(x[5+index])
    return features


def generate_file(username, useradmin, period, eid_list, column, file_type):
    try:
        data = data_transfer(period, eid_list, column)

        e_name = {x[0]:x[1] for x in equipments.equip_name(username,useradmin)}
        df = pd.DataFrame(data)
        prefix = '/usr/local/www/'
        title = time.strftime(','.join(e_name[x] for x in eid_list) + str(int(time.time())))


        if file_type == 'csv':
            df.to_csv(prefix + title + '.csv', index=False, sep=',')
        else:
            df.to_excel(prefix + title + '.xlsx', sheet_name="sheetname", index=False)

        return True
    except Exception as e:
        print(e)
        return False

