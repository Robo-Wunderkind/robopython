import platform
import time
from binascii import hexlify
from .pygatt.backends.bgapi.bgapi import BGAPIBackend


class BLED112(object):

    def __init__(self, name, com_port=None):
        self.read_uuid = 'aa000000-77f1-415f-9c9e-8a22a7f02242'       # C01
        self.read_uuid_flag = 'aa000003-77f1-415f-9c9e-8a22a7f02242'  # C04
        self.write_uuid = 'aa000002-77f1-415f-9c9e-8a22a7f02242'      # C03
        self.write_uuid_flag = 'aa000001-77f1-415f-9c9e-8a22a7f02242' # C02
        self.WriteOK = 0
        self.ReadDone = 0
        self.read_data = None
        self.com_port = com_port
        self.name = name
        self.rx = 0
        self.connection = None
        self.BLE_Connected = False
        self.os = platform.system()
        self.check_os()
        self.Devices = []
        self.adapter = self.set_adapter()
        self.start()
        if self.BLE_Connected:
            self.connect_ble()

    def set_adapter(self):
        if self.com_port is None:
            adapter = BGAPIBackend()
            return adapter
        adapter = BGAPIBackend(serial_port=self.com_port)
        return adapter


    def check_os(self):
        if self.os == 'Windows':
            print("Running on Windows, please ensure your BLED112 dongle is plugged in")
        if self.os == 'Linux':
            print("Running on Linux, please ensure your BLED112 dongle is plugged in")
        if self.os == 'Darwin':
            print("Running on Mac, please ensure your BLED112 dongle is plugged in")

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
            # count = 0               # added a counter to timeout after waiting
            while self.WriteOK == 0:
                pass

    def start(self):
        time.sleep(0.3)
        self.BLE_Connected = True
        try:
            self.adapter.start()
        except BaseException:
            self.BLE_Connected = False
            print("BLED112 Not Connected")

    def stop(self):
        self.adapter.stop()

    def scan(self):
        time.sleep(0.2)
        self.Devices = []
        byte = 0
        devices = self.adapter.scan()
        for idx, dev in enumerate(devices):
            name = dev['name']
            if name != ' ':
                filtered_name = ''
                for char in name:
                    try:
                        byte = int(hexlify(char.encode()), 16)
                    except UnicodeEncodeError:
                        byte = 0
                    if byte <= 32:
                        continue
                    filtered_name += char
                devices[idx]['name'] = filtered_name
        self.Devices = devices
        return self.Devices

    def handle_rx_flag(self, handle, value):
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        self.WriteOK = 1

    def subscribe(self, uuid, handle):
        if self.connection is not None:
            self.connection.subscribe(uuid, callback=handle)

    def connect_ble(self):
        self.scan()
        for device in self.Devices:
            if str(device['name']) == self.name:
                self.connection = self.adapter.connect(device['address'])
                print('Connected to ' + self.name + '!')
                self.subscribe(self.read_uuid_flag, self.handle_rx_flag)
                return
        raise Exception('Connection Failed - ' + self.name + ' does not exist')

    def disconnect_ble(self):
        pass

    def get_rssi(self):
        return self.connection.get_rssi()

    def get_characteristics(self):
        return self.connection.getCharacteristics()