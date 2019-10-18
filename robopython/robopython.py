import time
import platform
from ble_robo import BLED112
from mqtt_robo import MQTT
from binascii import hexlify
from collections import OrderedDict
from robo.motor import Motor
from robo.servo import Servo
from robo.rgb import RGB
from robo.matrix import Matrix
from robo.ultrasonic import Ultrasonic
from robo.motion import Motion
from robo.light import Light
from robo.button import Button
from robo.meteo import Meteo
from robo.camera import Camera
from robo.system import System
from robo.accelerometer import IMU
from robo.ir import IR
from robo.linetracker import LT
from matrix_characters import characters



class Robo(object):

    characters = OrderedDict(sorted(characters.items(), key=lambda t: t[0]))

    def __init__(self, name, mqtt=None, com_port=None):
        self.name = "RW_" + name
        self.MQTT = mqtt
        self.build = None
        self.low_battery = 0
        self.drive_status = None
        self.drive_id = 0xa6
        self.turn_status = None
        self.turn_id  = 0xa7
        self.infinite = 65000
        self.protocol = None
        self.idle = True
        self.default_topic = "robo/" + name + "/" + "receive"
        self.receive_topic = "robo/" + name + "/" + "transmit"

        self.BLE = BLED112(self.name, com_port)
        if self.BLE.BLE_Connected and self.MQTT is None:
            self.BLE.subscribe(self.BLE.read_uuid, self.handle_rx_data)
            self.protocol = "BLE"

        if self.MQTT is not None:
            self.protocol = "MQTT"
            mqtt.subscribe(self.receive_topic)
            mqtt.add_robo(self.name, self)
            
        if self.protocol is None:
            raise Exception('BLE Nor MQTT is Selected, Exiting')

        self.interrupts = ['c0', '11', '01']
        self.maxModules = {
                            'Motor': 6,
                            'Servo': 6,
                            'RGB': 8,
                            'Button': 4,
                            'Matrix': 8,
                            'Ultrasonic': 4,
                            'Light': 4,
                            'Motion': 4
                          }
        self.currentBuildBits = [[0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0]
                                 ]

        # Create max instances of all objects
        self.Motor1 = Motor('Motor1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 1)
        self.Motor2 = Motor('Motor2', self.BLE, self.MQTT, self.protocol, self.default_topic, 2, 2)
        self.Motor3 = Motor('Motor3', self.BLE, self.MQTT, self.protocol, self.default_topic, 3, 3)
        self.Motor4 = Motor('Motor4', self.BLE, self.MQTT, self.protocol, self.default_topic, 4, 4)
        self.Motor5 = Motor('Motor5', self.BLE, self.MQTT, self.protocol, self.default_topic, 5, 5)
        self.Motor6 = Motor('Motor6', self.BLE, self.MQTT, self.protocol, self.default_topic, 6, 6)
        self.Motors = [self.Motor1, self.Motor2, self.Motor3, self.Motor4, self.Motor5, self.Motor6]

        self.Servo1 = Servo('Servo1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 7)
        self.Servo2 = Servo('Servo2', self.BLE, self.MQTT, self.protocol, self.default_topic, 2, 8)
        self.Servo3 = Servo('Servo3', self.BLE, self.MQTT, self.protocol, self.default_topic, 3, 9)
        self.Servo4 = Servo('Servo4', self.BLE, self.MQTT, self.protocol, self.default_topic, 4, 10)
        self.Servo5 = Servo('Servo5', self.BLE, self.MQTT, self.protocol, self.default_topic, 5, 11)
        self.Servo6 = Servo('Servo6', self.BLE, self.MQTT, self.protocol, self.default_topic, 6, 12)

        self.RGB1 = RGB('RGB1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 13)
        self.RGB2 = RGB('RGB2', self.BLE, self.MQTT, self.protocol, self.default_topic, 2, 14)
        self.RGB3 = RGB('RGB3', self.BLE, self.MQTT, self.protocol, self.default_topic, 3, 15)
        self.RGB4 = RGB('RGB4', self.BLE, self.MQTT, self.protocol, self.default_topic, 4, 16)
        self.RGB5 = RGB('RGB5', self.BLE, self.MQTT, self.protocol, self.default_topic, 5, 17)
        self.RGB6 = RGB('RGB6', self.BLE, self.MQTT, self.protocol, self.default_topic, 6, 18)
        self.RGB7 = RGB('RGB7', self.BLE, self.MQTT, self.protocol, self.default_topic, 7, 19)
        self.RGB8 = RGB('RGB8', self.BLE, self.MQTT, self.protocol, self.default_topic, 8, 20)
        self.RGBs = [self.RGB1, self.RGB2, self.RGB3, self.RGB4, self.RGB5, self.RGB6, self.RGB7, self.RGB8]

        self.Button1 = Button('Button1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 21)
        self.Button2 = Button('Button2', self.BLE, self.MQTT, self.protocol, self.default_topic, 2, 22)
        self.Button3 = Button('Button3', self.BLE, self.MQTT, self.protocol, self.default_topic, 3, 23)
        self.Button4 = Button('Button4', self.BLE, self.MQTT, self.protocol, self.default_topic, 4, 24)

        self.Ultrasonic1 = Ultrasonic('Ultrasonic1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 25, 26)
        self.Ultrasonic2 = Ultrasonic('Ultrasonic2', self.BLE, self.MQTT, self.protocol, self.default_topic, 2, 27, 28)
        self.Ultrasonic3 = Ultrasonic('Ultrasonic3', self.BLE, self.MQTT, self.protocol, self.default_topic, 3, 29, 30)
        self.Ultrasonic4 = Ultrasonic('Ultrasonic4', self.BLE, self.MQTT, self.protocol, self.default_topic, 4, 31, 32)

        self.Light1 = Light('Light1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 33)
        self.Light2 = Light('Light2', self.BLE, self.MQTT, self.protocol, self.default_topic, 2, 34)
        self.Light3 = Light('Light3', self.BLE, self.MQTT, self.protocol, self.default_topic, 3, 35)
        self.Light4 = Light('Light4', self.BLE, self.MQTT, self.protocol, self.default_topic, 4, 36)

        self.Motion1 = Motion('Motion1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 37)
        self.Motion2 = Motion('Motion2', self.BLE, self.MQTT, self.protocol, self.default_topic, 2, 38)
        self.Motion3 = Motion('Motion3', self.BLE, self.MQTT, self.protocol, self.default_topic, 3, 39)
        self.Motion4 = Motion('Motion4', self.BLE, self.MQTT, self.protocol, self.default_topic, 4, 40)

        self.Matrix1 = Matrix('Matrix1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 41)
        self.Matrix2 = Matrix('Matrix2', self.BLE, self.MQTT, self.protocol, self.default_topic, 2, 42)
        self.Matrix3 = Matrix('Matrix3', self.BLE, self.MQTT, self.protocol, self.default_topic, 3, 43)
        self.Matrix4 = Matrix('Matrix4', self.BLE, self.MQTT, self.protocol, self.default_topic, 4, 44)
        self.Matrix5 = Matrix('Matrix5', self.BLE, self.MQTT, self.protocol, self.default_topic, 5, 45)
        self.Matrix6 = Matrix('Matrix6', self.BLE, self.MQTT, self.protocol, self.default_topic, 6, 46)
        self.Matrix7 = Matrix('Matrix7', self.BLE, self.MQTT, self.protocol, self.default_topic, 7, 47)
        self.Matrix8 = Matrix('Matrix8', self.BLE, self.MQTT, self.protocol, self.default_topic, 8, 48)
        self.Matrices = [self.Matrix1, self.Matrix2, self.Matrix3, self.Matrix4, self.Matrix5, self.Matrix6,
                         self.Matrix6, self.Matrix7, self.Matrix8]

        self.Meteo1 = Meteo('Meteo1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 49)

        self.Camera1 = Camera('Camera1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 50)

        self.IR1 = IR('IR1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 51)

        self.System = System('System', self.BLE, self.MQTT, self.protocol, self.default_topic, 52)

        self.LT1 = LT('LT1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 53, 54, 55)
        self.LT2 = LT('LT2', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 56, 57, 58)
        self.LT3 = LT('LT3', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 59, 60, 61)
        self.LT4 = LT('LT4', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 62, 63, 64)
        self.IMU1 = IMU('IMU1', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 65)
        self.IMU2 = IMU('IMU2', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 66)
        self.IMU3 = IMU('IMU3', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 67)
        self.IMU4 = IMU('IMU4', self.BLE, self.MQTT, self.protocol, self.default_topic, 1, 68)

        self.build_map = [
                            [self.RGB2, self.RGB1, self.Servo2, self.Servo1, self.Motor4,
                             self.Motor3, self.Motor2, self.Motor1],
                            [self.System, self.Meteo1, self.Light1, self.Button2,
                             self.Button1, self.Camera1, self.IR1, self.Matrix1],
                            [self.Servo6, self.Servo5,  self.Servo4, self.Servo3,
                             self.Motor6, self.Motor5, self.Motion1, self.Ultrasonic1],
                            [self.Matrix3, self.Matrix2, self.RGB8, self.RGB7, self.RGB6,
                             self.RGB5, self.RGB4, self.RGB3],
                            [self.Light2, self.Button4, self.Button3, self.Matrix8,
                             self.Matrix7, self.Matrix6, self.Matrix5, self.Matrix4],
                            [self.Motion4, self.Motion3, self.Motion2, self.Ultrasonic4,
                             self.Ultrasonic3, self.Ultrasonic2, self.Light4, self.Light3],
                            [self.IMU4, self.IMU3, self.IMU2, self.IMU1,
                             self.LT4, self.LT3, self.LT2, self.LT1]
                        ]
        self.triggers = {'21': self.Button1, '22': self.Button2, '23': self.Button3, '24': self.Button4,
                         '25': self.Ultrasonic1, '26': self.Ultrasonic1, '27': self.Ultrasonic2, '28': self.Ultrasonic2,
                         '29': self.Ultrasonic3, '30': self.Ultrasonic3, '31': self.Ultrasonic4, '32': self.Ultrasonic4,
                         '33': self.Light1, '34': self.Light2, '35': self.Light3, '36': self.Light4, '37': self.Motion1,
                         '38': self.Motion2, '39': self.Motion3, '40': self.Motion4, '49': self.Meteo1,
                         '50': self.Camera1, '51': self.IR1
                         }
        self.actions = {'1': self.Motor1, '2': self.Motor2, '3': self.Motor3, '4': self.Motor4, '5': self.Motor5,
                        '6': self.Motor6, '7': self.Servo1, '8': self.Servo2, '9': self.Servo3, '10': self.Servo4,
                        '11': self.Servo5, '12': self.Servo6, '13': self.RGB1, '14': self.RGB2, '15': self.RGB3,
                        '16': self.RGB4, '17': self.RGB5, '18': self.RGB6, '19': self.RGB7, '20': self.RGB8,
                        '41': self.Matrix1, '42': self.Matrix2, '43': self.Matrix3, '44': self.Matrix4,
                        '45': self.Matrix5, '46': self.Matrix6, '47': self.Matrix7, '48': self.Matrix8,
                        '52': self.System, '166': self, '167': self # drive and turn ids
                        }

        self.get_build()
        time.sleep(0.5)

    def reset_build_map(self):
        for byte in self.build_map:
            for module in byte:
                pass
                #module.disconnected()

    def handle_rx_data(self, handle, value):
        data = hexlify(value)
        data = [data[i:i + 2] for i in xrange(0, len(data), 2)]
        read_data = data

        if read_data[0] not in self.interrupts:
            return

        if read_data[0] == '01':
            print(read_data)
            self.update_build(read_data)
            return
        if read_data[0] == '11':
            self.low_battery = 1
            return

        if read_data[0] == 'c0':
            cmd_id = str(int(read_data[-2], 16))
            cmd_status = int(read_data[-1], 16)
            if cmd_id in self.triggers:
                cmd_id = int(cmd_id)
                self.triggers[cmd_id].triggered(cmd_id, cmd_status)
                return
            if cmd_id in self.actions:
                cmd_id = int(cmd_id)
		if cmd_id == 166 or 167:
			self.action_complete(cmd_id, cmd_status)
			return
		else:
			self.actions[cmd_id].action_complete(cmd_id, cmd_status) #takes the instance of module that has its action completed 
																#and signals that the action is done
                return

    def update_build(self, build_data):
        self.build = []
        self.reset_build_map()
        print("Build to start is: ", self.build)
        if build_data is None:
            return
        build_data = build_data[2:]
        for idx, byte in enumerate(build_data):
            byte = bin(int(byte, 16))[2:].zfill(8)  # converting from hex to binary string
            for idy, bit in enumerate(byte):
                self.currentBuildBits[idx][idy] = bit
                if bit == '1':
                    name = self.build_map[idx][idy].name
                    if name not in self.build:
                        self.build.append(name)
                        #self.build_map[idx][idy].connected()
        print(self.build)
        return self.build

    def get_build(self):
        self.build = []
        self.reset_build_map()
        if self.protocol is not None:
            packet_size = 0x02
            payload_size = 0x01
            command_id = 0x01
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, payload_size, command_id]))
                build = hexlify(self.BLE.read_from_robo())  # byte array of the build
                if len(build) == 8 or len(build) == 9:
                    build = build[2:]
                    for idx, byte in enumerate(build):
                        byte = bin(int(byte, 16))[2:].zfill(8)  # converting from hex to binary string
                        for idy, bit in enumerate(byte):
                            self.currentBuildBits[idx][idy] = bit
                            if bit == '1':
                                name = self.build_map[idx][idy].name
                                if name not in self.build:
                                    self.build.append(name)
                                    #self.build_map[idx][idy].connected()
                print(self.build)
                return self.build

            if self.protocol == "MQTT":
                print("Build to start is: ", self.build)
                command = self.MQTT.get_mqtt_cmd([payload_size, command_id])
                self.MQTT.publish(self.default_topic, command)
                build = self.MQTT.message
                if build is None:
                    return
                build = [build[i:i + 2] for i in xrange(0, len(build), 2)]
                if build[0] != '01':
                    return
                build = build[2:]
                print build
                for idx, byte in enumerate(build):
                    byte = bin(int(byte, 16))[2:].zfill(8)  # converting from hex to binary string
                    for idy, bit in enumerate(byte):
                        self.currentBuildBits[idx][idy] = bit
                        if bit == '1':
                            name = self.build_map[idx][idy].name
                            if name not in self.build:
                                self.build.append(name)
                                #self.build_map[idx][idy].connected()
                print(self.build)
                return self.build

    def change_ble_name(self, name):
        if len(name) > 16:
            print("Name must be less than 16 characters")

        packet_size = len(name) + 2
        command_id = 0x06
        payload_size = len(name)
        name = map(bin, bytearray(name))
        name_bytes = []

        for byte in name:
            name_bytes.append(int(byte, 2))
        command = bytearray([packet_size, command_id, payload_size])
        for byte in name_bytes:
            command.append(byte)
        if self.protocol == "BLE":
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
        if self.protocol == "MQTT":
            pass

    def set_drive(self, motor_cmds, vel, distance, action_id, topic=None, wd=0x59):
        # distance < 100cm and vel < 100 %
        packet_size = 0x0b
        command_id = 0xa6
        payload_size = 0x09
        wd_h = wd / 256
        wd_l = wd % 256
        directions = 0
        motors = 0

        if topic is None:
            topic = self.default_topic

        assert type(vel) is int, "Velocity must be 0-100%"
        assert type(distance) is int, "Distance must be an integer of cm"
        assert type(motor_cmds) is list, "Motors must be given as a list of motor numbers + direction " \
                                         "e.g [[1, 0],[3, 1]] "
        for cmd in motor_cmds:
            index = cmd[0]-1
            if self.Motors[index].is_connected != 1:
                print ('Motor' + str(index) + ' is not connected')
                return

        distance_h = distance / 256
        distance_l = distance % 256
        for cmd in motor_cmds:
            motors += 2**(cmd[0]-1)
            directions += (2**(cmd[0]-1))*cmd[1]
        
        if vel < 0:
            vel = 0
        if vel > self.Motor1.max_velocity:
            vel = self.Motor1.max_velocity

        vel_h = vel / 256
        vel_l = vel % 256

        if vel > 0 and distance > 0:
            self.idle = False

        command = bytearray([packet_size, command_id, payload_size, action_id, motors, directions,
                             vel_h, vel_l, wd_h, wd_l, distance_h, distance_l])
        if self.protocol == "BLE":
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            return
        if self.protocol == "MQTT":
            command = self.MQTT.get_mqtt_cmd([command_id, payload_size, action_id, motors, directions,
                                              vel_h, vel_l, wd_h, wd_l, distance_h, distance_l])
            self.MQTT.publish(topic, command)

    def turn(self, vel, angle, direction, topic=None, wait=0, motors=(1, 2), wd=89, turning_radius=91):
        if len(motors) != 2:
            print("Turning is only valid for 2 motors at this time")
            return
        if direction != 0 and direction != 1:
            print('Direction must be either 1 or 0')
            return
        distance = int((angle/360.00)*((turning_radius*2*3.14159)/10))
        motor_cmds = [[1, direction], [2, direction]]
        self.set_drive(motor_cmds, vel, distance, self.turn_id, topic, wd)
        if angle >= self.infinite:
            return
        if wait == 1:
            while not self.idle():
                time.sleep(0.1)
            return True

    def turn_inf(self, vel, direction):
        self.turn(vel, 65000, direction, 0)

    def drive_inf(self, vel, direction):
        self.drive(vel, 65000, direction, None, 0)

    def drive(self, vel, distance, direction, topic=None, wait=0, motors=(1, 2), wd=89):
        motor_cmds = None
        if len(motors) != 2:
            print("Drive is only valid for 2 motors at this time, use set_drive for custom drive commands")
            return
        if direction != 0 and direction != 1:
            print('Direction must be either 1 or 0')
            return
        if direction == 1:
            motor_cmds = [[1, 1], [2, 0]]
        if direction == 0:
            motor_cmds = [[1, 0], [2, 1]]
        self.set_drive(motor_cmds, vel, distance, self.drive_id, topic, wd)
        if distance >= self.infinite:
            return
        if wait == 1:
            while not self.idle():
                time.sleep(0.1)
            return True

    def action_complete(self, id, cmd_status):
        #print "Action completed: ", id
        self.idle = True

    def stop(self):
        for motor in self.Motors:
            if motor.is_connected:
                motor.set_pwm(0)

    def stop_all(self, topic=None):
        packet_size = 0x04
        command_id = 0x30
        payload_size = 0x02
        off = 0x00
        command = bytearray([packet_size, command_id, payload_size, off])

        if topic is None:
            topic = self.default_topic

        if self.protocol == "BLE":
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
        if self.protocol == "MQTT":
            command = self.MQTT.get_mqtt_command([command_id, payload_size, off])
            self.MQTT.publish(topic, command)

        for rgb in self.RGBs:
            if rgb.is_connected:
                rgb.off()
        for matrix in self.Matrices:
            if matrix.is_connected:
                matrix.off()

    # text is a string to be displayed, matrices are the matrix objects to be used
    def display_text(self, text, matrices, speed):
        blank = [['0' for i in range(8)] for j in range(8)]
        window = blank
        buff = blank  # 8x8
        # Taking text from string to 2D Array that the Matrix can understand
        for char in text:
            if char in characters:
                for idx, row in enumerate(characters[char]):
                    buff[idx] += row
        buff = tuple(buff)
        # Partitioning the buffer into a window of 8*8 to be used on the display at this moment
        length = len(buff[0])
        for i in range(8, length):
            for m in range(0, len(matrices)):
                window = blank
                if (i + 8*m) > length:
                    continue
                for index in range(0, 8):
                    window[index] = buff[index][((i - 8)+8*m):(i+8*m)]
                window = matrices[m].list_to_bytes(window)
                matrices[m].set_display(window)
                time.sleep(speed)

    def delay(self, delay_time):
        time.sleep(delay_time)

    def sound(self, sound):
        if sound not in self.System.sounds:
            print("Sound index does not exist")
            return
        self.System.play_sound(sound)

    def play_tune(self, tune):
        self.System.set_tune(tune)

    def play_custom_tune(self, tempo):
        self.System.play_custom_tune(tempo)

    def upload_tune(self, tune, tempo):

        max_payload = 16
        index = 0
        tune_chunk = []
        print(tune)
        for idx, note in enumerate(tune):
            beat = note[1] 
            byte = (note[0] << 4) + beat # combine note and beat data
            tune_chunk.append(byte)
        print(tune_chunk)
        if len(tune_chunk) != 0:
            self.System.upload_custom_tune(tune_chunk, index)
        self.play_custom_tune(tempo)

    def play_note(self, note, beat = 0x0f, tempo = 0):
        self.System.play_note(note, beat, tempo)

    def stop_tune(self):
        self.System.kill_tune()

    def battery_level(self):
        return self.System.get_battery_stats()

    def firmware(self):
        return self.System.get_firmware_version()

    def disconnect_ble(self):
        self.BLE.stop()

