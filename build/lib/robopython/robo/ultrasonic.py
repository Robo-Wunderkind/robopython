from binascii import hexlify

class Ultrasonic(object):

    def __init__(self, name, ble, id_num, u_trigger_id, s_trigger_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.u_trigger_id = u_trigger_id
        self.s_trigger_id = s_trigger_id
        self.u_trigger_status = None
        self.s_trigger_status = None
        self.BLE = ble

    def get_distance(self):
        packet_size = 0x03
        command_id = 0x84
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])
        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            distance = hexlify(self.BLE.read_from_robo())
            distance = [distance[i:i + 2] for i in xrange(0, len(distance), 2)]
            print distance
            if len(distance) != 7:
                return
            distance_cm = int(distance[2], 16) + int(distance[3], 16)*256
            return distance_cm
        print (self.name + " is NOT Connected!")

    def get_sound_level(self):
        packet_size = 0x03
        command_id = 0x81
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])

        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            sound = hexlify(self.BLE.read_from_robo())
            sound = [sound[i:i+2] for i in xrange(0, len(sound), 2)]
            if len(sound) != 4:
                return
            sound_lvl = int(sound[-2], 16)
            return sound_lvl
        print (self.name + " is NOT Connected!")

    def set_distance_trigger(self, value, comparator):        # comparator 0 = less than 1 = greater than
        packet_size = 0x06
        command_id = 0xB0
        payload_size = 0x04
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, self.u_trigger_id, module_id, comparator, value])

        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            # print "Set Distance Trigger to: " + str(value) + " comparator is  " + str(comparator)
            return
        print (self.name + " is NOT Connected!")

    def set_sound_trigger(self, value, comparator):
        packet_size = 0x06
        command_id = 0xB4
        payload_size = 0x04
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, self.s_trigger_id, module_id, comparator, value])

        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            # print "Set Sound Trigger to: " + str(value) + " comparator is  " + str(comparator)
            return
        print (self.name + " is NOT Connected!")

    def check_sound_trigger(self):
        value = self.s_trigger_status
        if value is None:
            return
        self.s_trigger_status = None
        return value

    def check_ultrasonic_trigger(self):
        value = self.u_trigger_status
        if value is None:
            return
        self.u_trigger_status = None
        return value

    def triggered(self, cmd_id, cmd_status):
        if cmd_id == self.u_trigger_id:
            self.u_trigger_status = cmd_status
            return
        if cmd_id == self.s_trigger_id:
            self.s_trigger_status = cmd_status
