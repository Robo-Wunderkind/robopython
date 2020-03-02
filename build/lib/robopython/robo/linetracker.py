from binascii import hexlify


class LT(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, id_num, action_id, l_trigger_id, c_trigger_id, r_trigger_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.l_trigger_id = l_trigger_id
        self.c_trigger_id = c_trigger_id
        self.r_trigger_id = r_trigger_id
        self.action_id = action_id
        self.action_status = None
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic
        self.center = 0
        self.left = 0
        self.right = 0
        self.center_status = 0
        self.right_status = 0
        self.left_status = 0


    def connected(self):
        self.is_connected = 1
        print("LineTracker" + str(self.id) + " connected")
        
    def disconnected(self):
        self.is_connected = 0
        print("LineTracker" + str(self.id) + " disconnected")

    def get_right_value(self):
        self.get_values()
        value = self.right
        return value

    def get_center_value(self):
        self.get_values()
        value = self.center
        return value

    def get_left_value(self):
        self.get_values()
        value = self.left
        return value

    def get_sensor_values(self):
        self.get_values()
        return [self.left, self.center, self.right]

    def get_values(self):
        packet_size = 0x03
        command_id = 0x86
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])
        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                data = hexlify(self.BLE.read_from_robo())
                data = [data[i:i + 2] for i in xrange(0, len(data), 2)]
                if len(data) != 12:
                    return
                right = int(data[3], 16) * 256 + int(data[2], 16)
                center = int(data[5], 16) * 256 + int(data[4], 16)
                left = int(data[7], 16) * 256 + int(data[6], 16)
                if right > 10000 or left > 10000 or center > 10000:
                    return
                self.left = left
                self.right = right
                self.center = center
                index = int(data[8], 16)
                return
            if self.protocol == "MQTT":
                pass
        print(self.name + " is NOT Connected!")

    def calibrate(self):
        packet_size = 0x03
        command_id = 0x87
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])

        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            return
        print(self.name + " is NOT Connected!")

    def track(self, direction, speed, wd = 89, motors = 3):
        if speed > 100:
            print("Speed must be 0-100%")
            return

        packet_size = 0x09
        command_id = 0xa9
        payload_size = 0x07
        module_id = self.id - 1

        if self.is_connected == 1:
            if self.protocol == "BLE": 
                command = [packet_size, command_id, payload_size, self.action_id, module_id,
                             motors, direction, speed, 9, 25]
                self.BLE.write_to_robo(self.BLE.write_uuid, bytearray(command))
                return
            if self.protocol == "MQTT":
                command = [command_id, payload_size, self.action_id, module_id,
                             motors, direction, speed, 9, 25]
                command = self.MQTT.get_mqtt_cmd(command)
                self.MQTT.publish(self.default_topic, command)
                print command
                return
        print(self.name + " is NOT Connected!")

    def action_complete(self, id, cmd_status):
        self.action_status = cmd_status
        print("Line Tracking Done!")

    def check_action(self):
        value = self.action_status
        if self.action_status is None:
            return False
        self.action_status = None
        return True
