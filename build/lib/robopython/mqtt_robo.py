import paho.mqtt.client as mqtt
from binascii import hexlify
from past.builtins import xrange
import time
import socket


class MQTT(object):
    def __init__(self, client_name="RoboController", host_name="Robo_IoT", broker_address = "192.168.3.254"):
        self.broker = host_name
        self.broker_address = broker_address
        self.client = mqtt.Client(client_name)
        self.client.on_message = self.on_message  # attach function to callback
        self.MQTT_Connected = False
        self.message = "None"
        self.topic = None
        self.roboName = None
        self.build_cmd = '01'
        self.event_cmd = 'c0'
        self.QOS = 0 # 0-2
        self.robo_dict = {}
        self.client.loop_stop() # make sure we start fresh
        self.connect()

    def get_broker_address(self): # doesn't seem to always work
        address = None
        try:
            address = socket.gethostbyname(self.broker)
            print(address)
        except socket.gaierror:
            print("Could not find broker on this network: ", self.broker)
            return
        return address

    def get_mqtt_cmd(self, cmd):
        mqtt_command = ""
        for item in cmd: 
            if isinstance(item, str):
                mqtt_command += item
                continue
            byte = str(hex(item))[2:]
            if len(byte) == 1:              # if the number is just a single digit
                byte = '0' + byte
            mqtt_command += byte
        return mqtt_command

    def add_robo(self, robo_name, robo_inst):
        self.robo_dict[robo_name] = robo_inst
        print("Added Robo - " + robo_name)

    def remove_robo(self, robo_name, robo_inst):
        del self.robo_dict[robo_inst]
        print("Removed Robo - " + robo_name)

    def get_robo_name(self):
        name = None 
        indeces = [i for i, ltr in enumerate(self.topic) if ltr == '/']
        if len(indeces) == 2:
            name = self.topic[indeces[0]+1:indeces[1]]
            return name
        return None

    def on_message(self, client, userdata, message):
        self.message = str(message.payload)
        self.topic = str(message.topic)
        #print("message received " + self.message)
        #print("message topic = " + self.topic)
        #print("message qos = " + str(message.qos))
        #print("message retain flag = " + str(message.retain))
        if self.topic is not None:
            self.roboName = self.get_robo_name()
            if self.roboName in self.robo_dict:
                msg = [self.message[i:i + 2] for i in xrange(0, len(self.message), 2)]
                cmd = msg[0]
                robo = self.robo_dict[self.roboName]
                if cmd == self.build_cmd:
                    build_data = msg
                    print("Updating Build of: " + self.roboName)
                    robo.update_build(build_data)
                    return
                if cmd == self.event_cmd:
                    event_id = str(int(msg[2], 16))
                    result = int(msg[3], 16)
                    if event_id in robo.triggers:
                        robo.triggers[event_id].triggered(int(event_id), result)
                        return
                    elif event_id in robo.actions:
                        robo.actions[event_id].action_complete(int(event_id), result)
                        return
                    return

    def connect(self):
        if self.broker_address is None:
            print("Broker Not Found, Cannot Connect")
            return
        self.MQTT_Connected = True
        print("Connecting to MQTT")
        try:
            self.client.connect(self.broker_address, 1883, 30)  # connect to broker
        except BaseException:
            self.MQTT_Connected = False
            print("Failed to connect")
            return False
        self.client.loop_stop()  # stop the loop
        self.client.loop_start()  # start the loop
        #self.client.loop_forever()
        print("MQTT Connection Status - " + str(self.MQTT_Connected))
        return True

    def disconnect(self):
        if self.MQTT_Connected:
            self.client.loop_stop()
            self.client.disconnect()

    def publish(self, topic, data, retain = False):
        if self.MQTT_Connected:
            self.client.publish(topic, data, self.QOS, retain)

    def subscribe(self, topic):
        if self.MQTT_Connected:
            self.client.subscribe((topic, self.QOS))

    def unsubscribe(self, topic):
        if self.MQTT_Connected:
            self.client.unsubscribe(topic)
