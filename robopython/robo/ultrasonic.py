import time
from binascii import hexlify
from past.builtins import xrange


class Ultrasonic(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, id_num, u_trigger_id, s_trigger_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.u_trigger_id = u_trigger_id
        self.s_trigger_id = s_trigger_id
        self.u_trigger_status = None
        self.s_trigger_status = None
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic

    def connected(self):
        self.is_connected = 1
        print("Ultrasonic" + str(self.id) + " connected")
        
    def disconnected(self):
        self.is_connected = 0
        print("Ultrasonic" + str(self.id) + " disconnected")

    def get_distance(self, topic=None):
        packet_size = 0x03
        command_id = 0x84
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])
        distance_cm = 0

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                distance = hexlify(self.BLE.read_from_robo())
                distance = [distance[i:i + 2] for i in xrange(0, len(distance), 2)]
                if len(distance) != 7:
                    return
                distance_cm = int(distance[2], 16) + int(distance[3], 16)*256
                return distance_cm
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, module_id])
                self.MQTT.message = "None"
                self.MQTT.publish(topic, command)
                while self.MQTT.message[0:2] != '84':
                  time.sleep(0.01)
                distance = self.MQTT.message
                distance = [distance[i:i + 2] for i in xrange(0, len(distance), 2)]
                if len(distance) != 7:
                    return
                distance_cm = int(distance[2], 16) + int(distance[3], 16)*256
                return distance_cm
        print(self.name + " is NOT Connected!")

    def get_sound(self, topic=None):
        packet_size = 0x03
        command_id = 0x81
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                sound = hexlify(self.BLE.read_from_robo())
                sound = [sound[i:i+2] for i in xrange(0, len(sound), 2)]
                if len(sound) != 4:
                    return
                sound_lvl = int(sound[-2], 16)
                return sound_lvl
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, module_id])
                self.MQTT.publish(topic, command)
                sound = self.MQTT.message
                if sound is None:
                    return 0
                sound = [sound[i:i + 2] for i in xrange(0, len(sound), 2)]
                sound = int(sound[2], 16)
                return sound
        print(self.name + " is NOT Connected!")

    def set_distance_trigger(self, value, comparator, topic=None):
        # comparator 0 = less than 1 = greater than
        packet_size = 0x06
        command_id = 0xB0
        payload_size = 0x04
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, self.u_trigger_id, module_id, comparator, value])

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                pass
        print(self.name + " is NOT Connected!")

    def set_sound_trigger(self, value, comparator, topic=None):
        packet_size = 0x06
        command_id = 0xB4
        payload_size = 0x04
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, self.s_trigger_id, module_id, comparator, value])

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            # print "Set Sound Trigger to: " + str(value) + " comparator is  " + str(comparator)
            return
        print(self.name + " is NOT Connected!")

    def check_sound_trigger(self):
        value = self.s_trigger_status
        if value is None:
            return False
        self.s_trigger_status = None
        return True

    def check_ultrasonic_trigger(self):
        value = self.u_trigger_status
        if value is None:
            return False
        self.u_trigger_status = None
        return True

    def triggered(self, cmd_id, cmd_status):
        if cmd_id == self.u_trigger_id:
            self.u_trigger_status = cmd_status
            return
        if cmd_id == self.s_trigger_id:
            self.s_trigger_status = cmd_status
