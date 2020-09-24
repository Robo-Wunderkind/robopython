from binascii import hexlify
from past.builtins import xrange

class Colour(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, id_num, trigger_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.trigger_id = trigger_id
        self.trigger_status = None
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic

    def connected(self):
        self.is_connected = 1
        print("COLOUR" + str(self.id) + " connected")
        
    def disconnected(self):
        self.is_connected = 0
        print("COLOUR" + str(self.id) + " disconnected")

    def get_colour_values(self, topic = None):
        packet_size = 0x03
        command_id = 0x74
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])

        if topic is None:
            topic = self.default_topic

        colours = [0,0,0,0]

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                colour_data = hexlify(self.BLE.read_from_robo())
                colour_data = [colour_data[i:i+2] for i in xrange(0, len(colour_data), 2)]
                '''
                if len(colour_data) != 5:
                    return
                '''
                colours[0] = int(colour_data[2], 16)*256 + int(colour_data[3], 16)
                colours[1] = int(colour_data[4], 16)*256 + int(colour_data[5], 16)
                colours[2] = int(colour_data[6], 16)*256 + int(colour_data[7], 16)
                colours[3] = int(colour_data[8], 16)*256 + int(colour_data[9], 16)
                return colours

            if self.protocol == "MQTT":
                pass
        print(self.name + " is NOT Connected!")

    def get_proximity(self, topic = None):
        packet_size = 0x03
        command_id = 0x75
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                proximity = hexlify(self.BLE.read_from_robo())
                proximity = [proximity[i:i+2] for i in xrange(0, len(proximity), 2)]
                return int(proximity[2], 16)

            if self.protocol == "MQTT":
                pass
        print(self.name + " is NOT Connected!")

    def get_colour(self, topic = None):
        packet_size = 0x03
        command_id = 0x77
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                colour = hexlify(self.BLE.read_from_robo())
                colour = [colour[i:i+2] for i in xrange(0, len(colour), 2)]
                return int(colour[2], 16)

            if self.protocol == "MQTT":
                pass
        print(self.name + " is NOT Connected!")

    def triggered(self, cmd_id, cmd_status):
        if self.trigger_id == cmd_id:
            self.trigger_status = cmd_status

    def check_trigger(self):
        value = self.trigger_status
        if value is None:
            return
        self.trigger_status = None
        return value
