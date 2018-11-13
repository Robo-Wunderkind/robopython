import time
import platform
from pygatt.backends.bgapi.bgapi import BGAPIBackend
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
from robo.ir import IR


class BLED112(object):

    def __init__(self, com_port=None):
        self.read_uuid = 'aa000000-77f1-415f-9c9e-8a22a7f02242'
        self.read_uuid_flag = 'aa000003-77f1-415f-9c9e-8a22a7f02242'
        self.write_uuid = 'aa000002-77f1-415f-9c9e-8a22a7f02242'
        self.write_uuid_flag = 'aa000001-77f1-415f-9c9e-8a22a7f02242'
        self.WriteOK = 0
        self.ReadDone = 0
        self.read_data = None
        self.com_port = com_port
        self.rx = 0
        self.connection = None
        self.os = platform.system()
        self.check_os()
        self.Devices = []
        self.adapter = self.set_adapter()
        self.start()

    def set_adapter(self):		
        if self.com_port is None:
            adapter = BGAPIBackend()
            return adapter
        adapter = BGAPIBackend(serial_port = self.com_port)
        return adapter

    def check_os(self):
        if self.os == 'Windows':
            print ("Running on Windows, please ensure your BLED112 dongle is plugged in")
        if self.os == 'Linux':
            print ("Running on Linux, please ensure your BLED112 dongle is plugged in")
        if self.os == 'Darwin':
            print ("Running on Mac, please ensure your BLED112 dongle is plugged in")

    def read_from_robo(self):
        if self.connection is not None:
            read_data = self.connection.char_read(self.read_uuid)
            if self.ReadDone == 255:
                self.ReadDone = 0
            payload = bytearray([self.ReadDone])
            self.write_to_flag(payload)
            self.ReadDone += 1
            self.rx = 0
            return read_data

    def write_to_flag(self, data):
        if self.connection is not None:
            self.connection.char_write(self.write_uuid_flag, data)

    def write_to_robo(self, uuid, data):
        if self.connection is not None:
            self.connection.char_write(uuid, data)
            self.WriteOK = 0
            while self.WriteOK == 0:
                pass

    def start(self):
        time.sleep(0.3)
        self.adapter.start()

    def stop(self):
        self.adapter.stop()

    def scan(self):
        time.sleep(0.2)
        self.Devices = []
        devices = self.adapter.scan()
        for idx, dev in enumerate(devices):
            name = dev['name']
            if name != ' ':
                filtered_name = ''
                for char in name:
                    byte = int(hexlify(char), 16)
                    if byte <= 32:
                        continue
                    filtered_name += char
                devices[idx]['name'] = filtered_name
        self.Devices = devices
        return self.Devices
        # print self.Devices

    def handle_rx_flag(self, handle, value):
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        self.WriteOK = 1

    def subscribe(self, uuid, handle):
        if self.connection is not None:
            self.connection.subscribe(uuid, callback=handle)

    def connect_ble(self, name):
        self.scan()
        for device in self.Devices:
            if str(device['name']) == name:
                self.connection = self.adapter.connect(device['address'])
                print ('Connected to ' + name + '!')
                return
        print ('Connection Failed - ' + name + ' does not exist')

    def disconnect_ble(self):
        pass


class Robo(object):
    characters = {
        'A': ('00000000',
              '00111100',
              '01100110',
              '01100110',
              '01111110',
              '01100110',
              '01100110',
              '01100110'
              ),
        'B': ('00000000',
              '01111100',
              '01100110',
              '01100110',
              '01111100',
              '01100110',
              '01100110',
              '01111100'
              ),
        'C': ('00000000',
              '00111100',
              '01100110',
              '01100000',
              '01100000',
              '01100000',
              '01100110',
              '00111100'
              ),
        'D': ('00000000',
              '01111100',
              '01100110',
              '01100110',
              '01100110',
              '01100110',
              '01100110',
              '01111100'
              ),
        'E': ('00000000',
              '01111110',
              '01100000',
              '01100000',
              '01111100',
              '01100000',
              '01100000',
              '01111110'
              ),
        'F': ('00000000',
              '01111110',
              '01100000',
              '01100000',
              '01111100',
              '01100000',
              '01100000',
              '01100000'
              ),
        'G': ('00000000',
              '00111100',
              '01100110',
              '01100000',
              '01100000',
              '01101110',
              '01100110',
              '00111100'
              ),
        'H': ('00000000',
              '01100110',
              '01100110',
              '01100110',
              '01111110',
              '01100110',
              '01100110',
              '01100110'
              ),
        'I': ('00000000',
              '00111100',
              '00011000',
              '00011000',
              '00011000',
              '00011000',
              '00011000',
              '00111100'
              ),
        'J': ('00000000',
              '00011110',
              '00001100',
              '00001100',
              '00001100',
              '01101100',
              '01101100',
              '00111000'
              ),
        'K': ('00000000',
              '01100110',
              '01101100',
              '01111000',
              '01110000',
              '01111000',
              '01101100',
              '01100110'
              ),
        'L': ('00000000',
              '01100000',
              '01100000',
              '01100000',
              '01100000',
              '01100000',
              '01100000',
              '01111110'
              ),
        'M': ('00000000',
              '01100011',
              '01110111',
              '01111111',
              '01101011',
              '01100011',
              '01100011',
              '01100011'
              ),
        'N': ('00000000',
              '01100011',
              '01110011',
              '01111011',
              '01101111',
              '01100111',
              '01100011',
              '01100011'
              ),
        'O': ('00000000',
              '00111100',
              '01100110',
              '01100110',
              '01100110',
              '01100110',
              '01100110',
              '00111100'
              ),
        'P': ('00000000',
              '01111100',
              '01100110',
              '01100110',
              '01100110',
              '01111100',
              '01100000',
              '01100000'
              ),
        'Q': ('00000000',
              '00111100',
              '01100110',
              '01100110',
              '01100110',
              '01101110',
              '00111100',
              '00000110'
              ),
        'R': ('00000000',
              '01111100',
              '01100110',
              '01100110',
              '01111100',
              '01111000',
              '01101100',
              '01100110'
              ),
        'S': ('00000000',
              '00111100',
              '01100110',
              '01100000',
              '00111100',
              '00000110',
              '01100110',
              '00111100'
              ),
        'T': ('00000000',
              '01111110',
              '01011010',
              '00011000',
              '00011000',
              '00011000',
              '00011000',
              '00011000'
              ),
        'U': ('00000000',
              '01100110',
              '01100110',
              '01100110',
              '01100110',
              '01100110',
              '01100110',
              '00111110'
              ),
        'V': ('00000000',
              '01100110',
              '01100110',
              '01100110',
              '01100110',
              '01100110',
              '00111100',
              '00011000'
              ),
        'W': ('00000000',
              '01100011',
              '01100011',
              '01100011',
              '01101011',
              '01111111',
              '01110111',
              '01100011'
              ),
        'X': ('00000000',
              '01100011',
              '01100011',
              '00110110',
              '00011100',
              '00110110',
              '01100011',
              '01100011'
              ),
        'Y': ('00000000',
              '01100110',
              '01100110',
              '01100110',
              '00111100',
              '00011000',
              '00011000',
              '00011000'
              ),
        'Z': ('00000000',
              '01111110',
              '00000110',
              '00001100',
              '00011000',
              '00110000',
              '01100000',
              '01111110'
              ),
        'a': ('00000000',
              '00000000',
              '00000000',
              '00111100',
              '00000110',
              '00111110',
              '01100110',
              '00111110'
              ),
        'b': ('00000000',
              '01100000',
              '01100000',
              '01100000',
              '01111100',
              '01100110',
              '01100110',
              '01111100'
              ),
        'c': ('00000000',
              '00000000',
              '00000000',
              '00111100',
              '01100110',
              '01100000',
              '01100110',
              '00111100'
              ),
        'd': ('00000000',
              '00000110',
              '00000110',
              '00000110',
              '00111110',
              '01100110',
              '01100110',
              '00111110'
              ),
        'e': ('00000000',
              '00000000',
              '00000000',
              '00111100',
              '01100110',
              '01111110',
              '01100000',
              '00111100'
              ),
        'f': ('00000000',
              '00011100',
              '00110110',
              '00110000',
              '00110000',
              '01111100',
              '00110000',
              '00110000'
              ),
        'g': ('00000000',
              '00000000',
              '00111110',
              '01100110',
              '01100110',
              '00111110',
              '00000110',
              '00111100'
              ),
        'h': ('00000000',
              '01100000',
              '01100000',
              '01100000',
              '01111110',
              '01100110',
              '01100110',
              '01100110'
              ),
        'i': ('00000000',
              '00000000',
              '00011000',
              '00000000',
              '00011000',
              '00011000',
              '00011000',
              '00111100'
              ),
        'j': ('00000000',
              '00001100',
              '00000000',
              '00001100',
              '00001100',
              '01101100',
              '01101100',
              '00111000'
              ),
        'k': ('00000000',
              '01100000',
              '01100000',
              '01100110',
              '01101100',
              '01111000',
              '01101100',
              '01100110'
              ),
        'l': ('00000000',
              '00011000',
              '00011000',
              '00011000',
              '00011000',
              '00011000',
              '00011000',
              '00011000'
              ),
        'm': ('00000000',
              '00000000',
              '00000000',
              '01100011',
              '01110111',
              '01111111',
              '01101011',
              '01101011'
              ),
        'n': ('00000000',
              '00000000',
              '00000000',
              '01111100',
              '01111110',
              '01100110',
              '01100110',
              '01100110'
              ),
        'o': ('00000000',
              '00000000',
              '00000000',
              '00111100',
              '01100110',
              '01100110',
              '01100110',
              '00111100'
              ),
        'p': ('00000000',
              '00000000',
              '01111100',
              '01100110',
              '01100110',
              '01111100',
              '01100000',
              '01100000'
              ),
        'q': ('00000000',
              '00000000',
              '00111100',
              '01101100',
              '01101100',
              '00111100',
              '00001101',
              '00001111'
              ),
        'r': ('00000000',
              '00000000',
              '00000000',
              '01111100',
              '01100110',
              '01100110',
              '01100000',
              '01100000'
              ),
        's': ('00000000',
              '00000000',
              '00000000',
              '00111110',
              '01000000',
              '00111100',
              '00000010',
              '01111100'
              ),
        't': ('00000000',
              '00000000',
              '00011000',
              '00011000',
              '01111110',
              '00011000',
              '00011000',
              '00011000'
              ),
        'u': ('00000000',
              '00000000',
              '00000000',
              '01100110',
              '01100110',
              '01100110',
              '01100110',
              '00111110'
              ),
        'v': ('00000000',
              '00000000',
              '00000000',
              '01100110',
              '01100110',
              '01100110',
              '00111100',
              '00011000'
              ),
        'w': ('00000000',
              '00000000',
              '00000000',
              '01100011',
              '01101011',
              '01101011',
              '01101011',
              '00111110'
              ),
        'x': ('00000000',
              '00000000',
              '00000000',
              '01100110',
              '00111100',
              '00011000',
              '00111100',
              '01100110'
              ),
        'y': ('00000000',
              '00000000',
              '00000000',
              '01100110',
              '01100110',
              '00111110',
              '00000110',
              '00111100'
              ),
        'z': ('00000000',
              '00000000',
              '00000000',
              '00111100',
              '00001100',
              '00011000',
              '00110000',
              '00111100'
              ),
        '0': ('00000000',
              '00111100',
              '01100110',
              '01101110',
              '01110110',
              '01100110',
              '01100110',
              '00111100'
              ),
        '1': ('00000000',
              '00011000',
              '00111000',
              '01111000',
              '00011000',
              '00011000',
              '00011000',
              '01111110'
              ),
        '2': ('00000000',
              '00111100',
              '01100110',
              '00000110',
              '00001100',
              '00110000',
              '01100000',
              '01111110'
              ),
        '3': ('00000000',
              '00111100',
              '01100110',
              '00000110',
              '00011100',
              '00000110',
              '01100110',
              '00111100'
              ),
        '4': ('00000000',
              '00001100',
              '00011100',
              '00101100',
              '01001100',
              '01111110',
              '00000110',
              '00001100'
              ),
        '5': ('00000000',
              '01111110',
              '01100000',
              '01111100',
              '00000110',
              '00000110',
              '01100110',
              '00111100'
              ),
        '6': ('00000000',
              '00111100',
              '01100110',
              '01100000',
              '01111100',
              '01100110',
              '01100110',
              '00111100'
              ),
        '7': ('00000000',
              '01111110',
              '01100110',
              '00001100',
              '00001100',
              '00011000',
              '00011000',
              '00011000'
              ),
        '8': ('00000000',
              '00111100',
              '01100110',
              '01100110',
              '00111100',
              '01100110',
              '01100110',
              '00111100'
              ),
        '9': ('00000000',
              '00111100',
              '01100110',
              '01100110',
              '00111110',
              '00000110',
              '01100110',
              '00111100'
              ),
        ' ': ('00000000',
              '00000000',
              '00000000',
              '00000000',
              '00000000',
              '00000000',
              '00000000',
              '00000000'
              ),
        '?': ('00000000',
              '00111100',
              '01100110',
              '00000110',
              '00011100',
              '00011000',
              '00000000',
              '00011000'
              ),
        '!': ('00011000',
              '00011000',
              '00011000',
              '00011000',
              '00011000',
              '00000000',
              '00011000',
              '00011000'
              ),
        '+': ('00000000',
              '00000000',
              '00001000',
              '00001000',
              '00111110',
              '00001000',
              '00001000',
              '00000000'
              ),
        '-': ('00000000',
              '00000000',
              '00000000',
              '00000000',
              '00111100',
              '00000000',
              '00000000',
              '00000000'
              ),
        '=': ('00000000',
              '00000000',
              '00000000',
              '00111100',
              '00000000',
              '00111100',
              '00000000',
              '00000000'
              ),
        '/': ('00000000',
              '00000000',
              '00000110',
              '00001100',
              '00011000',
              '00110000',
              '01100000',
              '00000000'
              ),
        '%': ('00000000',
              '01100000',
              '01100110',
              '00001100',
              '00011000',
              '00110000',
              '01100110',
              '00000110'
              ),
        'up': ('00011000',
               '00111100',
               '11111111',
               '00111100',
               '00111100',
               '00111100',
               '00111100',
               '00111100'
               ),
        'down': ('00111100',
                 '00111100',
                 '00111100',
                 '00111100',
                 '11111111',
                 '01111110',
                 '00111100',
                 '00011000'
                 ),
        'right': ('00001000',
                  '00001100',
                  '11111110',
                  '11111111',
                  '11111111',
                  '11111110',
                  '00001100',
                  '00001000'
                  ),
        'left': ('00010000',
                 '00110000',
                 '01111111',
                 '11111111',
                 '11111111',
                 '01111111',
                 '00110000',
                 '00010000'
                 ),
        'smile': ('00000000',
                  '11000011',
                  '11000011',
                  '00000000',
                  '10000001',
                  '11000011',
                  '00111100',
                  '00000000'
                  ),
        'check_mark': ('00000000',
                       '00000001',
                       '00000011',
                       '00000110',
                       '00001100',
                       '11011000',
                       '01110000',
                       '00100000'
                       ),
        'x_mark': ('11000011',
                   '01000010',
                   '00100100',
                   '00011000',
                   '00011000',
                   '00100100',
                   '01000010',
                   '11000011'
                   )

    }
    characters = OrderedDict(sorted(characters.items(), key=lambda t: t[0]))

    def __init__(self, name, com_port=None):
        self.name = name
        self.BLE = BLED112(com_port)
        self.connect_ble()
        self.BLE.subscribe(self.BLE.read_uuid_flag, self.BLE.handle_rx_flag)
        self.BLE.subscribe(self.BLE.read_uuid, self.handle_rx_data)
        self.build = None
        self.low_battery = 0
        self.drive_status = None
        self.drive_id = 0xa6
        self.turn_status = None
        self.turn_id = 0xa7
        self.infinite = 65000
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
                                 [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]
                                 ]
        # Create max instances of all objects
        self.Motor1 = Motor('Motor1', self.BLE, 1, 1)
        self.Motor2 = Motor('Motor2', self.BLE, 2, 2)
        self.Motor3 = Motor('Motor3', self.BLE, 3, 3)
        self.Motor4 = Motor('Motor4', self.BLE, 4, 4)
        self.Motor5 = Motor('Motor5', self.BLE, 5, 5)
        self.Motor6 = Motor('Motor6', self.BLE, 6, 6)
        self.Motors = [self.Motor1, self.Motor2, self.Motor3, self.Motor4, self.Motor5, self.Motor6]

        self.Servo1 = Servo('Servo1', self.BLE, 1, 7)
        self.Servo2 = Servo('Servo2', self.BLE, 2, 8)
        self.Servo3 = Servo('Servo3', self.BLE, 3, 9)
        self.Servo4 = Servo('Servo4', self.BLE, 4, 10)
        self.Servo5 = Servo('Servo5', self.BLE, 5, 11)
        self.Servo6 = Servo('Servo6', self.BLE, 6, 12)

        self.RGB1 = RGB('RGB1', self.BLE, 1, 13)
        self.RGB2 = RGB('RGB2', self.BLE, 2, 14)
        self.RGB3 = RGB('RGB3', self.BLE, 3, 15)
        self.RGB4 = RGB('RGB4', self.BLE, 4, 16)
        self.RGB5 = RGB('RGB5', self.BLE, 5, 17)
        self.RGB6 = RGB('RGB6', self.BLE, 6, 18)
        self.RGB7 = RGB('RGB7', self.BLE, 7, 19)
        self.RGB8 = RGB('RGB8', self.BLE, 8, 20)
        self.RGBs = [self.RGB1, self.RGB2, self.RGB3, self.RGB4, self.RGB5, self.RGB6, self.RGB7, self.RGB8]

        self.Button1 = Button('Button1', self.BLE, 1, 21)
        self.Button2 = Button('Button2', self.BLE, 2, 22)
        self.Button3 = Button('Button3', self.BLE, 3, 23)
        self.Button4 = Button('Button4', self.BLE, 4, 24)

        self.Ultrasonic1 = Ultrasonic('Ultrasonic1', self.BLE, 1, 25, 26)
        self.Ultrasonic2 = Ultrasonic('Ultrasonic2', self.BLE, 2, 27, 28)
        self.Ultrasonic3 = Ultrasonic('Ultrasonic3', self.BLE, 3, 29, 30)
        self.Ultrasonic4 = Ultrasonic('Ultrasonic4', self.BLE, 4, 31, 32)

        self.Light1 = Light('Light1', self.BLE, 1, 33)
        self.Light2 = Light('Light2', self.BLE, 2, 34)
        self.Light3 = Light('Light3', self.BLE, 3, 35)
        self.Light4 = Light('Light4', self.BLE, 4, 36)

        self.Motion1 = Motion('Motion1', self.BLE, 1, 37)
        self.Motion2 = Motion('Motion2', self.BLE, 2, 38)
        self.Motion3 = Motion('Motion3', self.BLE, 3, 39)
        self.Motion4 = Motion('Motion4', self.BLE, 4, 40)

        self.Matrix1 = Matrix('Matrix1', self.BLE, 1, 41)
        self.Matrix2 = Matrix('Matrix2', self.BLE, 2, 42)
        self.Matrix3 = Matrix('Matrix3', self.BLE, 3, 43)
        self.Matrix4 = Matrix('Matrix4', self.BLE, 4, 44)
        self.Matrix5 = Matrix('Matrix5', self.BLE, 5, 45)
        self.Matrix6 = Matrix('Matrix6', self.BLE, 6, 46)
        self.Matrix7 = Matrix('Matrix7', self.BLE, 7, 47)
        self.Matrix8 = Matrix('Matrix8', self.BLE, 8, 48)
        self.Matrices = [self.Matrix1, self.Matrix2, self.Matrix3, self.Matrix4, self.Matrix5, self.Matrix6,
                         self.Matrix6, self.Matrix7, self.Matrix8]

        self.Meteo1 = Meteo('Meteo1', self.BLE, 1, 49)

        self.Camera1 = Camera('Camera1', self.BLE, 1, 50)

        self.IR1 = IR('IR1', self.BLE, 1, 51)

        self.System = System('System', self.BLE, 52)

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
                             self.Ultrasonic3, self.Ultrasonic2, self.Light4, self.Light3]
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
                        '52': self.System
                        }

        self.get_build()

    def connect_ble(self):
        self.BLE.connect_ble(self.name)

    def handle_rx_data(self, handle, value):
        data = hexlify(value)
        data = [data[i:i + 2] for i in xrange(0, len(data), 2)]
        read_data = data
        if read_data[0] not in self.interrupts:
            return

        if read_data[0] == 'c0':
            cmd_id = str(int(read_data[-2], 16))
            cmd_status = int(read_data[-1], 16)
            if cmd_id == str(self.drive_id):
                self.drive_complete(cmd_status)
                return
            if cmd_id == str(self.turn_id):
                self.turn_complete(cmd_status)
                return
            if cmd_id in self.triggers:
                self.triggers[cmd_id].triggered(int(cmd_id), cmd_status)
                return
            if cmd_id in self.actions:
                self.actions[cmd_id].action_complete(cmd_status)
                return
        if read_data[0] == '01':
            self.update_build(read_data)
        if read_data[0] == '11':
            self.low_battery = 1

    def get_rssi(self):
        return self.BLE.connection.get_rssi()

    def get_characteristics(self):
        return self.BLE.connection.getCharacteristics()

    def update_build(self, build_data):
        self.build = []
        if build_data is None:
            return
        if len(build_data) == 8:
            build_data = build_data[2:]
            for idx, byte in enumerate(build_data):
                byte = bin(int(byte, 16))[2:].zfill(8)
                for idy, bit in enumerate(byte):
                    self.currentBuildBits[idx][idy] = bit
                    if bit == '1':
                        self.build.append(self.build_map[idx][idy].name)
                        self.build_map[idx][idy].is_connected = 1
                    if bit == '0':
                        self.build_map[idx][idy].is_connected = 0
        # print self.build
        return self.build

    def get_build(self):
        self.build = []
        packet_size = 0x02
        payload_size = 0x01
        command_id = 0x01
        self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, payload_size, command_id]))
        build = hexlify(self.BLE.read_from_robo())							 	        	    # byte array of the build
        if len(build) == 8:  												# if we have a valid build configuration
            build = build[2:]
            for idx, byte in enumerate(build):
                byte = bin(int(byte, 16))[2:].zfill(8)       				# converting from hex to binary string
                for idy, bit in enumerate(byte):
                    self.currentBuildBits[idx][idy] = bit
                    if bit == '1':
                        self.build.append(self.build_map[idx][idy].name)
                        self.build_map[idx][idy].is_connected = 1
                    if bit == '0':
                        self.build_map[idx][idy].is_connected = 0
        return self.build

    def change_ble_name(self, name):
        if len(name) > 16:
            print ("Name must be less than 16 characters")

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
        self.BLE.write_to_robo(self.BLE.write_uuid, command)

    def set_drive(self, motor_cmds, vel, distance, action_id, wd=0x59):
        # distance < 100cm and vel < 100 %
        packet_size = 0x0b
        command_id = 0xa6
        payload_size = 0x09
        wd_h = wd / 256
        wd_l = wd % 256
        directions = 0
        motors = 0

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

        command = bytearray([packet_size, command_id, payload_size, action_id, motors, directions,
                             vel_h, vel_l, wd_h, wd_l, distance_h, distance_l])
        self.BLE.write_to_robo(self.BLE.write_uuid, command)

    def turn(self, vel, angle, direction, wait=1, motors=(1, 2), wd=89, turning_radius=91):
        if len(motors) != 2:
            print ("Turning is only valid for 2 motors at this time")
            return
        if direction != 0 and direction != 1:
            print ('Direction must be either 1 or 0')
            return
        distance = int((angle/360.00)*((turning_radius*2*3.14159)/10))
        motor_cmds = [[1, direction], [2, direction]]
        self.set_drive(motor_cmds, vel, distance, self.turn_id, wd)
        if angle >= self.infinite:
            return
        if wait == 1:
            while not self.check_turn_action():
                time.sleep(0.1)
            return True

    def drive(self, vel, distance, direction, wait=1, motors=(1, 2), wd=89):
        motor_cmds = None
        if len(motors) != 2:
            print ("Drive is only valid for 2 motors at this time, use se_drive for custom drive commands")
            return
        if direction != 0 and direction != 1:
            print ('Direction must be either 1 or 0')
            return
        if direction == 1:
            motor_cmds = [[1, 1], [2, 0]]
        if direction == 0:
            motor_cmds = [[1, 0], [2, 1]]
        self.set_drive(motor_cmds, vel, distance, self.drive_id, wd)
        if distance >= self.infinite:
            return
        if wait == 1:
            while not self.check_drive_action():
                time.sleep(0.1)
            return True

    def drive_complete(self, cmd_status):
        self.drive_status = cmd_status

    def check_drive_action(self):
        value = self.drive_status
        if value is None:
            return
        self.drive_status = None
        return value

    def turn_complete(self, cmd_status):
        self.turn_status = cmd_status

    def check_turn_action(self):
        value = self.turn_status
        if value is None:
            return
        self.turn_status = None
        return value

    def stop(self):
        for motor in self.Motors:
            if motor.is_connected:
                motor.set_pwm(0)

    def stop_all(self):
        packet_size = 0x04
        command_id = 0x30
        payload_size = 0x02
        off = 0x00
        command = bytearray([packet_size, command_id, payload_size, off])
        self.BLE.write_to_robo(self.BLE.write_uuid, command)
        for rgb in self.RGBs:
            if rgb.is_connected:
                rgb.off()
        for matrix in self.Matrices:
            if matrix.is_connected:
                matrix.off()

    # text is a string to be displayed, matrices are the matrix objects to be used
    def display_text(self, text, matrices):
        blank = [['0' for i in range(8)] for j in range(8)]
        window = blank
        buff = blank  # 8x8
        # Taking text from string to 2D Array that the Matrix can understand
        for char in text:
            if char in self.characters:
                for idx, row in enumerate(self.characters[char]):
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

    def delay(self, delay_time):
        time.sleep(delay_time)

    def sound(self, sound):
        if sound not in self.System.sounds:
            print("Sound index does not exist")
            return
        self.System.play_sound(sound)

    def battery_level(self):
        return self.System.get_battery_stats()

    def firmware(self):
        return self.System.get_firmware_version()


if __name__ == '__main__':
    BLE_Name = "RW_a"
    Robo = Robo(BLE_Name)
    while True:
        pass
        Robo.delay(0.3)