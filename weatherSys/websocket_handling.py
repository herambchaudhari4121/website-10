from dwebsocket.decorators import accept_websocket, require_websocket

class client:
    def __init__(self):
        self.pool = {}
        print('new client')


    def new_websocket(self, req):
        found = False
        k = 0
        if self.pool:
            for x in range(sorted(self.pool.keys())[-1] + 1):
                if x != sorted(self.pool.keys())[x]:
                    self.pool[x] = req.websocket
                    k = x
                    found = True

            if not found:
                self.pool[sorted(self.pool.keys())[-1] + 1] = req.websocket
                k = sorted(self.pool.keys())[-1]

        else:
            self.pool[0] = req.websocket
        print('p', self.pool)

        return k



    def show_socket(self, key):
        print(self.pool[key])



    def push_socket(self, key, data):
        print('p_s', self.pool[key])
        self.pool[key].send(data.encode('utf-8'))


    def close_websocket(self, key):
        # if self.pool[key].close():
        print('p_c', self.pool)
        self.pool[key].close()
        self.pool.pop(key)
        print(self.pool)


class user_portal_handling:
    portal = {}
    def select_equip(self,  key, eid):

        if eid in self.portal:
            self.portal[eid].append(key)
        else:
            self.portal[eid] = [key]

        # self.portal[user_id] = [{key: ''}]

    # def close_connection(self, user_id, key):
    #     self.portal[user_id].pop(key)
    #     if not self.portal[user_id]:
    #         self.portal.pop(user_id)
    #
    # def select_equip(self, user_id, key, eid):
    #     self.portal[user_id][key] = eid

    def remove_connection(self, key):
        eid = ''
        for x in self.portal.items():
            if key in x[1]:
                x[1].remove(key)
            if not x[1]:
                eid = x[0]
                # self.portal.pop(x[0])
        print(self.portal)
        if eid in self.portal:
            if not self.portal[eid]:
                self.portal.pop(eid)