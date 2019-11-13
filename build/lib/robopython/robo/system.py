from binascii import hexlify

class System(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, action_id):
        self.is_connected = 1
        self.name = name
        self.chargeLevel = 0
        self.chargeStatus = 'Unknown'
        self.firmwareVersion = None
        self.robotSound = 0x00
        self.cheerSound = 0x01
        self.honkSound = 0x02
        self.catSound = 0x03
        self.alarmSound = 0x04
        self.dogSound = 0x05
        self.laserSound = 0x06
        self.dingSound = 0x07
        self.sounds = [self.robotSound, self.cheerSound, self.honkSound, self.catSound, self.alarmSound, self.dogSound,
                       self.laserSound, self.dingSound]
        self.action_id = action_id
        self.action_status = None
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic

    def connected(self):
        self.is_connected = 1
        
    def disconnected(self):
        self.is_connected = 0

    def get_battery_stats(self, topic=None):
        status_options = ['Unknown', 'Discharging', 'Charging', 'Full']
        packet_size = 0x02
        command_id = 0x10
        payload = 0x00

        if topic is None:
            topic = self.default_topic

        if self.protocol == "BLE":
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload]))
            charge_data = hexlify(self.BLE.read_from_robo())
            charge_data = [charge_data[i:i+2] for i in xrange(0, len(charge_data), 2)]
            if len(charge_data) == 4:
                self.chargeLevel = int(charge_data[-2], 16)
                self.chargeStatus = int(charge_data[-1], 16)
                if self.chargeStatus <= 3:
                    self.chargeStatus = status_options[self.chargeStatus]
            return [self.chargeLevel, self.chargeStatus]

        if self.protocol == "MQTT":
            command = self.MQTT.get_mqtt_cmd([command_id, payload])
            self.MQTT.publish(topic, command)
            charge_data = self.MQTT.message
            if charge_data is None:
                return
            charge_data = [charge_data[i:i+2] for i in xrange(0, len(charge_data), 2)]
            self.chargeLevel = int(charge_data[-2], 16)
            self.chargeStatus = int(charge_data[-1], 16)
            if self.chargeLevel > 100:
                self.chargeLevel = 100
            if self.chargeStatus <= 3:
                self.chargeStatus = status_options[self.chargeStatus]
            return [self.chargeLevel, self.chargeStatus]

    def get_firmware_version(self, topic=None):
        packet_size = 0x02
        command_id = 0x07
        payload = 0x00

        if topic is None:
            topic = self.default_topic

        if self.protocol == "BLE":
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload]))
            fw_data = hexlify(self.BLE.read_from_robo())
            fw_data = [fw_data[i:i+2] for i in xrange(0, len(fw_data), 2)]
            return fw_data
        if self.protocol == "MQTT":
            command = self.MQTT.get_mqtt_cmd([command_id, payload])
            self.MQTT.publish(topic, command)
            fw_data = self.MQTT.message
            if fw_data is None:
                return
            fw_data = [int(fw_data[i:i+2], 16) for i in xrange(0, len(fw_data), 2)]
            fw_data = fw_data[2:]
            FW_Version = ''.join(chr(i) for i in fw_data)   # turn ascii to string
            return FW_Version

    def get_sound_clips(self, topic=None):
        packet_size = 0x02
        command_id = 0x60
        payload = 0x00

        if topic is None:
            topic = self.default_topic

        if self.protocol == "BLE":
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload]))
            clip_data = hexlify(self.BLE.read_from_robo())
            clip_data = [clip_data[i:i+2] for i in xrange(0, len(clip_data), 2)]
            return clip_data
        if self.protocol == "MQTT":
            command = self.MQTT.get_mqtt_cmd([command_id, payload])
            self.MQTT.publish(topic, command)
            clips_data = self.MQTT.message
            if clips_data is None:
                return
            clips_data = [clips_data[i:i+2] for i in xrange(0, len(clips_data), 2)]
            return clips_data

    def play_sound(self, sound, topic=None):
        packet_size = 0x03
        command_id = 0x61
        payload_size = 0x01

        if topic is None:
            topic = self.default_topic

        if self.protocol == "BLE":
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload_size, sound]))
            return
        if self.protocol == "MQTT":
            command = self.MQTT.get_mqtt_cmd([command_id, payload_size, sound])
            self.MQTT.publish(topic, command)
            return

    def set_tune(self, tune, tempo, topic=None):
        packet_size = 0x04
        command_id = 0x92
        payload_size = 0x02

        if topic is None:
            topic = self.default_topic

        if self.protocol == "BLE":
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload_size, tune, tempo]))
            return
        if self.protocol == "MQTT":
            command = self.MQTT.get_mqtt_cmd([command_id, payload_size, tune, tempo])
            self.MQTT.publish(topic, command)
            return

    # tunes is a list of tuples (Note, Beat_Length) 4 bits each, must combine them into 1 byte to save space
    # TODO test with a single upload, then multiple and build a top level function that manages uploading a tune of any length
    def upload_custom_tune(self, tune, index, topic=None): 
        length = len(tune)
        MAX_TUNE_SIZE = 240

        if length > MAX_TUNE_SIZE:
            print("The length of this tune is larger than the limit of: " + str(MAX_TUNE_SIZE) + " notes")
            return

        packet_size = length+3
        command_id = 0x93
        payload_size = length+1

        if topic is None:
            topic = self.default_topic

        if self.protocol == "BLE":
            payload = [packet_size, command_id, payload_size, index]
            for i in range(0, length):
                payload.append(tune[i])
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray(payload))
            return
        if self.protocol == "MQTT":
            payload = [command_id, payload_size, index]
            for i in range(0, length):
                payload.append(tune[i])
            command = self.MQTT.get_mqtt_cmd(payload)
            self.MQTT.publish(topic, command)
            return

    def kill_tune(self):
        self.set_tune(0xf0, 0)

    def play_custom_tune(self, tempo):
        self.set_tune(0xff, tempo)

    def play_note(self, note, beat, tempo, topic=None):
        packet_size = 0x03
        command_id = 0x94
        payload_size = 0x02

        r = range(0,16)
        if beat not in r or note not in r:
            print("Beat and/or Note is out of range")
            return

        beat = 0x0f 
        note = (note << 4) + beat # combine note and beat data

        if topic is None:
            topic = self.default_topic

        if self.protocol == "BLE":
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload_size, note, tempo]))
            return
        if self.protocol == "MQTT":
            command = self.MQTT.get_mqtt_cmd([command_id, payload_size, note, tempo])
            self.MQTT.publish(topic, command)
            return

    def action_complete(self, id, cmd_status):
        self.action_status = cmd_status

    def check_action(self):
        value = self.action_status
        if self.action_status is None:
            return False
        self.action_status = None
        return True
