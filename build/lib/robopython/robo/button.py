from binascii import hexlify

class Button(object):

    def __init__(self, name, ble, id_num, trigger_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.trigger_id = trigger_id
        self.trigger_status = None
        self.BLE = ble

    def get_state(self):
        packet_size = 0x03
        command_id = 0x85
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])

        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            status = hexlify(self.BLE.read_from_robo())
            status = [status[i:i+2] for i in xrange(0, len(status), 2)]

            if len(status) != 4:
                return
            state = int(status[-2], 16)
            return state
        print (self.name + " is NOT Connected!")

    def set_trigger(self, condition):  # condition +ve number of clicks 0 is pressed -1 is released
        packet_size = 0x05
        command_id = 0xB1
        payload_size = 0x03
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, self.trigger_id, module_id, condition])

        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            # print "Set Button Trigger"
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
