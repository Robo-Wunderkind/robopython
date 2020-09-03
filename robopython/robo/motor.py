class Motor(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, id_num, action_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.wheel_diameter = 89
        self.action_id = action_id
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic
        self.action_status = None
        self.max_velocity = 300

    def connected(self):
        self.is_connected = 1
        print("Motor" + str(self.id) + " connected")
        
    def disconnected(self):
        self.is_connected = 0
        print("Motor" + str(self.id) + " disconnected")

    def set_pwm(self, pwm, topic=None):   # 0, 128, 255 = 0 --- 127 = 100% CW    129 = 100% CCW
        assert type(pwm) is int, "pwm must be an integer"
        if pwm < 0 or pwm > 255:
            print("PWM must be 0-255")
            return

        if topic is None:
            topic = self.default_topic

        packet_size = 0x04
        command_id = 0x50
        payload_size = 0x02
        module_id = self.id-1
        command = bytearray([packet_size, command_id, payload_size, module_id, pwm])

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, module_id, pwm])
                self.MQTT.publish(topic, str(command))
                return
        print(self.name + " is NOT Connected!")

    def angle(self, angle, topic=None):   # angle must be positive, direction 1 = CW direction = 0 = CCW
        assert type(angle) is int, "angle must be an integer"
        
        if topic is None:
            topic = self.default_topic

        packet_size = 0x07
        command_id = 0x5b
        payload_size = 0x05
        module_id = self.id-1
        direction = 1

        if angle < 0:
            direction = 0

        angleH = abs(angle)/256
        angleL = abs(angle)%256
        command = bytearray([packet_size, command_id, payload_size, module_id, self.action_id, angleH, angleL, direction])

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, module_id, self.action_id, angleH, angleL, direction])
                self.MQTT.publish(topic, str(command))
                return
        print(self.name + " is NOT Connected!")

    def set_speed_cw(self, speed):   # speed 0-100
        assert type(speed) is int, "speed must be an integer"
        if speed < 0 or speed > 100:
            print ("Speed must be 0 - 100")
        pwm = int((speed*127/100))
        self.set_pwm(pwm)

    def set_speed_ccw(self, speed):   # speed 0-100
        assert type(speed) is int, "speed must be an integer"
        if speed < 0 or speed > 100:
            print ("Speed must be 0 - 100")
            return
        pwm = int((speed*127/100))
        pwm = 256 - pwm
        self.set_pwm(pwm)

    def stop(self):
        self.set_pwm(0)

    def spin_distance(self, vel, distance, topic=None, wd=89):  # distance < 100cm and vel < 300mm/s
        assert type(wd) is int, "Wheel Diameter must be an integer in mm"
        assert type(distance) is int, "Distance must be an integer in cm"
        assert type(vel) is int, "Velocity must be an integer 0-100%"

        vel = (vel*self.max_velocity/100)

        if topic is None:
            topic = self.default_topic

        packet_size = 10
        command_id = 0xa0
        payload_size = 0x08
        module_id = self.id-1
        velocity_h = vel/256
        velocity_l = vel % 256
        wd_h = wd/256
        wd_l = wd % 256
        distance_h = distance / 256
        distance_l = distance % 256
        command = bytearray([packet_size, command_id, payload_size, self.action_id, module_id, velocity_h, velocity_l,
                             wd_h, wd_l, distance_h, distance_l])
        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd(
                    [command_id, payload_size, self.action_id, module_id, velocity_h, velocity_l, wd_h, wd_l,
                     distance_h, distance_l])
                self.MQTT.publish(topic, command)
                return
        print(self.name + " is NOT Connected!")

    def spin_velocity(self, vel):
        self.spin_distance(vel, 65000)

    def action_complete(self, id, cmd_status):
        self.action_status = cmd_status

    def check_action(self):
        value = self.action_status
        if self.action_status is None:
            return False
        self.action_status = None
        return True

