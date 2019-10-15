from binascii import hexlify


class IMU(object):

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
        
    def disconnected(self):
        self.is_connected = 0

    def get_accelerations(self, topic=None):                        # we need 2 bytes for this data to go up to 65,000+
        packet_size = 0x03
        command_id = 0x90
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 0:
            if self.protocol == "BLE":
                return

            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, module_id])
                self.MQTT.publish(topic, command)
                accelerations = self.MQTT.message
                if accelerations is None:
                    return
                accelerations = [accelerations[i:i + 2] for i in xrange(0, len(accelerations), 2)] 
                print accelerations
                return accelerations
                '''
                if len(light) != 5:
                    return
                light_lvl = int(light[3], 16) * 256 + int(light[2], 16)
                return light_lvl
                '''
        print(self.name + " is NOT Connected!")

    def set_trigger(self, value, comparator, topic=None):        # comparator 0 = less than 1 = greater than
        packet_size = 0x06
        command_id = 0xB2
        payload_size = 0x04
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, self.trigger_id, module_id, comparator, value])

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
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
