from binascii import hexlify


class Camera(object):

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
    def disconnected(self):
        self.is_connected = 0

    def start(self):
        pass

    def stop(self):
        pass

    def face_detect(self, face):
        pass

    def colour_detect(self, colour):
        pass

    def triggered(self, cmd_id, cmd_status):
        if self.trigger_id == cmd_id:
            self.trigger_status = cmd_status

    def check_trigger(self):
        value = self.trigger_status
        if value is None:
            return
        self.trigger_status = None
        return value
