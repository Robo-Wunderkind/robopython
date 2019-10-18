import random


class RGB(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, id_num, action_id):
        self.is_connected = 1
        self.name = name
        self.id = id_num
        self.action_id = action_id
        self.action_status = None
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic
        self.R = 0
        self.G = 0
        self.B = 0

    def connected(self):
        self.is_connected = 1
        
    def disconnected(self):
        self.is_connected = 0

    def saturate(self, number):
        if number > 255:
            return 255
        if number < 0:
            return 0
        return number

    def set_rgb(self, red, green, blue, topic=None):
        red = self.saturate(red)
        green = self.saturate(green)
        blue = self.saturate(blue)

        packet_size = 0x07
        command_id = 0x53
        payload_size = 0x05
        on_off = 0x01
        module_id = self.id-1
        command = bytearray([packet_size, command_id, payload_size, module_id, on_off, red, green, blue])
        self.R = red
        self.G = green
        self.B = blue

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, module_id, on_off, red, green, blue])
                self.MQTT.publish(topic, command)
                return
        print(self.name + " is NOT Connected!")

    def blink_rgb(self, red, green, blue, num_blinks, period, topic=None):
        red = self.saturate(red)
        green = self.saturate(green)
        blue = self.saturate(blue)
        if period < 0 or period > 0xffff:
            print("Period must be positive number in ms and less than 65,535")
            return
        if num_blinks < 0 or num_blinks > 0xff:
            print("Blinks must be 0-255")
            return

        if topic is None:
            topic = self.default_topic

        packet_size = 0x0A
        command_id = 0xA2
        payload_size = 0x08
        module_id = self.id-1
        period_h = period/256
        period_l = period % 256
        command = bytearray([packet_size, command_id, payload_size, self.action_id, module_id, red, green, blue,
                             period_h, period_l, num_blinks])
        self.R = red
        self.G = green
        self.B = blue

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, self.action_id, module_id, red, green, blue,
                                                  period_h, period_l, num_blinks])
                self.MQTT.publish(topic, command)
                return
        print(self.name + " is NOT Connected!")

    def red(self):
        self.set_rgb(255, 0, 0)

    def green(self):
        self.set_rgb(0, 255, 0)

    def blue(self):
        self.set_rgb(0, 0, 255)

    def yellow(self):
        self.set_rgb(255, 255, 0)

    def orange(self):
        self.set_rgb(255, 128, 0)

    def white(self):
        self.set_rgb(255, 255, 255)

    def off(self):
        self.set_rgb(0, 0, 0)

    def random(self):
        self.set_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def timed_rgb(self, red, green, blue, time, topic=None):
        packet_size = 0x0A
        command_id = 0xA2
        payload_size = 0x08
        module_id = self.id-1
        time_h = time/256
        time_l = time % 256
        command = bytearray([packet_size, command_id, payload_size, self.action_id, module_id, red, green, blue,
                             time_h, time_l, 0x00])

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([packet_size, command_id, payload_size, self.action_id, module_id, red,
                                                  green, blue, time_h, time_l, 0x00])
                self.MQTT.publish(topic, command)
                return
        print(self.name + " is NOT Connected!")

    def action_complete(self, id, cmd_status):
        self.action_status = cmd_status

    def check_action(self):
        value = self.action_status
        if self.action_status is None:
            return
        self.action_status = None
        return value
