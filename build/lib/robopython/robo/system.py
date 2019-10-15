from binascii import hexlify

class System(object):

    def __init__(self, name, ble, action_id):
        self.is_connected = 0
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

    def get_battery_stats(self):
        status_options = ['Unknown', 'Discharging', 'Charging', 'Full']
        packet_size = 0x02
        command_id = 0x10
        payload = 0x00

        self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload]))
        charge_data = hexlify(self.BLE.read_from_robo())
        charge_data = [charge_data[i:i+2] for i in xrange(0, len(charge_data), 2)]

        if len(charge_data) == 4:
            self.chargeLevel = int(charge_data[-2], 16)
            s = int(charge_data[-1], 16)
            if s <= 3:
                self.chargeStatus = status_options[s]

        return [self.chargeLevel, self.chargeStatus]

    def get_firmware_version(self):
        packet_size = 0x02
        command_id = 0x07
        payload = 0x00

        self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload]))
        fw_data = hexlify(self.BLE.read_from_robo())
        fw_data = [fw_data[i:i+2] for i in xrange(0, len(fw_data), 2)]
        return fw_data

    def get_sound_clips(self):
        packet_size = 0x02
        command_id = 0x60
        payload = 0x00

        self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload]))
        clip_data = hexlify(self.BLE.read_from_robo())
        clip_data = [clip_data[i:i+2] for i in xrange(0, len(clip_data), 2)]
        return clip_data

    def play_sound(self, sound):
        packet_size = 0x03
        command_id = 0x61
        payload_size = 0x01
        self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload_size, sound]))

    def action_complete(self, cmd_status):
        self.action_status = cmd_status

    def check_action(self):
        value = self.action_status
        if self.action_status is None:
            return
        self.action_status = None
        return value
