from weatherSys import db_handling as db
import logging

class current_data:
    def __init__(self):
        self.data_box = {}
        transfer = {'11':'干燥', '12':'潮湿','13':'积水','14':'雪','15':'冰', '16':'霜', '17':'有融雪剂','00':'状况未知','99':'其他'}
        for x in db.current_data():
            if x[1]:
                x[1]['obs_time'] = x[2]
                if 'rw_trs' in x[1]:
                    if x[1]['rw_trs']:

                        if x[1]['rw_trs'][:2] in transfer:
                            x[1]['rw_trs'] = transfer[x[1]['rw_trs'][:2]]
                    else:
                        x[1]['rw_trs'] = '--'
                else:
                    x[1]['rw_trs'] = '--'
                self.data_box[x[0]] = x[1]

            else:
                self.data_box[x[0]] = {'obs_time':x[2]}

    def new_data(self, eid, data):
        transfer = {'11': '干燥', '12': '潮湿', '13': '积水', '14': '雪', '15': '冰', '16': '霜', '17': '有融雪剂', '00': '状况未知',
                    '99': '其他'}
        if 'rw_trs' in data:
            if data['rw_trs']:
                if str(data['rw_trs'])[:2] in transfer:
                    data['rw_trs'] = transfer[str(data['rw_trs'])[:2]]
            else:
                data['rw_trs'] = '--'
        else:
            data['rw_trs'] = '--'


        self.data_box[eid] = data