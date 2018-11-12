from binascii import hexlify

class LineTracker(object):

    def __init__(self, name, ble, id_num, l_trigger_id, c_trigger_id, r_trigger_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.l_trigger_id = l_trigger_id
        self.c_trigger_id = c_trigger_id
        self.r_trigger_id = r_trigger_id
        self.BLE = ble

    def get_right_value(self):
        value = None
        return value

    def get_center_value(self):
        value = None
        return value

    def get_left_value(self):
        value = None
        return value

