from binascii import hexlify


class LT(object):

    def __init__(self, name, ble, id_num, l_trigger_id, c_trigger_id, r_trigger_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.l_trigger_id = l_trigger_id
        self.c_trigger_id = c_trigger_id
        self.r_trigger_id = r_trigger_id
        self.BLE = ble

    def get_right_value(self):
        value = get_values()[2]
        return value

    def get_center_value(self):
        value = get_values()[1]
        return value

    def get_left_value(self):
        value = get_values()[0]
        return value

    def get_values(self):
        packet_size = 0x03
        command_id = 0x86
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])
        right = 0
        left = 0
        center = 0  

        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            intensity = hexlify(self.BLE.read_from_robo())
            intensity = [intensity[i:i + 2] for i in xrange(0, len(intensity), 2)]
            print intensity
            if len(intensity) != 9:
                return
            left = int(intensity[3], 16) * 256 + int(intensity[2], 16)
            center = int(intensity[5], 16) * 256 + int(intensity[4], 16)
            right = int(intensity[7], 16) * 256 + int(intensity[6], 16)
            return [left, center, right]
        print(self.name + " is NOT Connected!")
