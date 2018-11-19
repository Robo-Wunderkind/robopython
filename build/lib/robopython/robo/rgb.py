import random

class RGB(object):

    def __init__(self, name, ble, id_num, action_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.action_id = action_id
        self.action_status = None
        self.BLE = ble

    def set_rgb(self, red, green, blue):
        if red > 255 or green > 255 or blue > 255 or red < 0 or green < 0 or blue < 0:
            print ("All colours must be an integer between 0 and 255")
            return
        packet_size = 0x07
        command_id = 0x53
        payload_size = 0x05
        on_off = 0x01
        module_id = self.id-1
        command = bytearray([packet_size, command_id, payload_size, module_id, on_off, red, green, blue])
        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            return
        print self.name + " is NOT Connected!"

    def blink_rgb(self, red, green, blue, num_blinks, period):
        if period < 0 or period > 0xffff:
            print ("Period must be positive number in ms and less than 65,535")
            return
        if num_blinks < 0 or num_blinks > 0xff:
            print ("Blinks must be 0-255")
            return
        packet_size = 0x0A
        command_id = 0xA2
        payload_size = 0x08
        module_id = self.id-1
        period_h = period/256
        period_l = period % 256
        command = bytearray([packet_size, command_id, payload_size, self.action_id, module_id, red, green, blue,
                             period_h, period_l, num_blinks])
        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            return
        print (self.name + " is NOT Connected!")

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
        self.set_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))

    def timed_rgb(self, red, green, blue, time):
        packet_size = 0x0A
        command_id = 0xA2
        payload_size = 0x08
        module_id = self.id-1
        time_h = time/256
        time_l = time % 256
        command = bytearray([packet_size, command_id, payload_size, self.action_id, module_id, red, green, blue,
                             time_h, time_l, 0x00])
        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            return
        print (self.name + " is NOT Connected!")

    def action_complete(self, cmd_status):
        self.action_status = cmd_status

    def check_action(self):
        value = self.action_status
        if self.action_status is None:
            return
        self.action_status = None
        return value
