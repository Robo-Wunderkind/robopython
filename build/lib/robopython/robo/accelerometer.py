from binascii import hexlify
from past.builtins import xrange

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
        print("Accelerometer" + str(self.id) + " connected")
        
    def disconnected(self):
        self.is_connected = 0
        print("Acceleromter" + str(self.id) + " disconnected")

    def convert_bytes_to_acc_value(self, high_byte, low_byte):
        if int(high_byte, 16) >= 0x80:
            return float(((int(high_byte, 16)*256 + int(low_byte, 16)) - 65535 - 1))/100.0
        return float((int(high_byte, 16)*256 + int(low_byte, 16)))/100.0

    def convert_bytes_to_gyro_value(self, high_byte, low_byte):
        if int(high_byte, 16) >= 0x80:
            return float(((int(high_byte, 16)*256 + int(low_byte, 16)) - 65535 - 1))/10.0
        return float((int(high_byte, 16)*256 + int(low_byte, 16)))/10.0

    def get_values(self, topic=None):                       
        command_id = 0x89
        payload_size = 0x01
        packet_size = 0x03
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])
        sensor_values = {}

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                values = hexlify(self.BLE.read_from_robo())
                values = [values[i:i + 2] for i in xrange(0, len(values), 2)]
                if len(values) != 14: 
                    return
                sensor_values["acc_x"]  = self.convert_bytes_to_acc_value(values[2],values[3])
                sensor_values["acc_y"]  = self.convert_bytes_to_acc_value(values[4],values[5])
                sensor_values["acc_z"]  = self.convert_bytes_to_acc_value(values[6],values[7])
                sensor_values["gyro_x"] = self.convert_bytes_to_gyro_value(values[8],values[9])
                sensor_values["gyro_y"] = self.convert_bytes_to_gyro_value(values[10],values[11])
                sensor_values["gyro_z"] = self.convert_bytes_to_gyro_value(values[12],values[13])
                return sensor_values

            if self.protocol == "MQTT":
                return
        else:
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
