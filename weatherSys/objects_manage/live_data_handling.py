from weatherSys import db_handling as db



class current_data:
    def __init__(self):
        self.data_box = {[x[0]] : x[1] for x in db.current_data()}

    def new_data(self, eid, data):
        self.data_box[eid] = data


