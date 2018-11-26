from binascii import hexlify

class Light(object):

    def __init__(self, name, ble, id_num, trigger_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.trigger_id = trigger_id
        self.trigger_status = None
        self.BLE = ble

    def get_light(self):                        # we need 2 bytes for this data to go up to 65,000+
        packet_size = 0x03
        command_id = 0x80
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])
		
        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            light = hexlify(self.BLE.read_from_robo())
            light = [light[i:i+2] for i in xrange(0, len(light), 2)]
            if len(light) != 5:
                return
            light_lvl = int(light[-2], 16)*256 + int(light[-3], 16)
            return light_lvl
        print(self.name + " is NOT Connected!")

    def set_trigger(self, value, comparator):        # comparator 0 = less than 1 = greater than
        packet_size = 0x06
        command_id = 0xB2
        payload_size = 0x04
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, self.trigger_id, module_id, comparator, value])

        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            # print "Set Light Trigger to: " + str(value) + " comparator is  " + str(comparator)
            return
        print (self.name + " is NOT Connected!")

    def triggered(self, cmd_id, cmd_status):
        if self.trigger_id == cmd_id:
            self.trigger_status = cmd_status

    def check_trigger(self):
        value = self.trigger_status
        if value is None:
            return
        self.trigger_status = None
        return value
