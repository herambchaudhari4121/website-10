from weatherSys import db_handling as db


class find_equip(object):
    def pre_order (self, service):

        if service[4] == 'E':
            return service
        else:
            if not service:
                return

        service_set = db.find_child(service[1])
        equipment_set = []

        for x in service_set:
            equipment_set.append(self.pre_order(x))

        return equipment_set



def equipment (user_id):

    service = db.user_find_service (user_id)
    equipment = find_equip()

    for x in service:

        equip_collections = equipment.pre_order(x)
    return equip_collections


