class Matrix(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, id_num, action_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.orientation = 0
        self.action_id = action_id
        self.action_status = None
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic
        self.display_off = ['00000000',
                            '00000000',
                            '00000000',
                            '00000000',
                            '00000000',
                            '00000000',
                            '00000000',
                            '00000000']

    def connected(self):
        self.is_connected = 1
        print("Matrix" + str(self.id) + " connected")
        
    def disconnected(self):
        self.is_connected = 0
        print("Marix" + str(self.id) + " disconnected")

    def set_display(self, rows, topic=None):   # rows is an 8 element list of 8 bits each as binary strings
        packet_size = 0x0b
        command_id = 0x52
        payload_size = 0x09
        module_id = self.id - 1
        row_bytes = []

        if topic is None:
            topic = self.default_topic

        # make sure the image is oriented the desired way
        if self.orientation == 90:
            rows = self.rotate_right(rows)
        if self.orientation == 180:
            rows = self.rotate_right(self.rotate_right(rows))
        if self.orientation == 270:
            rows = self.rotate_left(rows)

        for idx, row in enumerate(rows):
            row_bytes.append(int(hex(int(row, 2)), 16))

        if self.is_connected == 1:
            if self.protocol == "BLE":
                command = bytearray([packet_size, command_id, payload_size, row_bytes[0], row_bytes[1], row_bytes[2],
                                     row_bytes[3], row_bytes[4], row_bytes[5], row_bytes[6], row_bytes[7], module_id])
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, row_bytes[0], row_bytes[1], row_bytes[2],
                                                  row_bytes[3], row_bytes[4], row_bytes[5], row_bytes[6],
                                                  row_bytes[7], module_id])
                self.MQTT.publish(topic, command)
                return
        print(self.name + " is NOT Connected!")

    def write_command(self, command):
        if self.is_connected == 1:
            if self.protocol == "BLE":
                command = bytearray(command)
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                del command[0]
                command = bytearray(command)
                command = self.MQTT.get_mqtt_cmd(command)
                self.MQTT.publish(topic, command)
                return
        print(self.name + " is NOT Connected!")

    def display_text(self, text="Test", orientation = 0, repeats = 1, scroll_rate = 8,topic = None):
        length = len(text)
        if length > 28:
            print("Text must be 28 characters or less")
            return

        packet_size = length + 8
        command_id1 = 0xA7
        command_id2 = 0xA8
        payload_size = length + 6
        module_id = self.id - 1
        if topic is None:
            topic = self.default_topic

        if length < 11:
            command = [packet_size, command_id1, payload_size, self.action_id, module_id, orientation, repeats, scroll_rate, length]
            for char in text:
                command.append(int(ord(char)))
            write_command(command)
        else:
            command = [packet_size, command_id1, payload_size, self.action_id, module_id, orientation, repeats, scroll_rate, length]
            text1 = text[:11]
            for char in text1:
                command.append(int(ord(char)))
            command = bytearray(command)
            self.write_command(command)
            text2 = text[11:]
            command = [len(text2)+2, command_id2, len(text2)]
            for char in text2:
                command.append(int(ord(char)))
            self.write_command(command)

    def off(self):
        self.set_display(self.display_off)

    def timed_display(self, rows, duration, topic=None): # duration is in ms
        packet_size = 0x0e
        command_id = 0xA3
        payload_size = 0x0c
        module_id = self.id - 1
        row_bytes = []
        time_h = duration / 256
        time_l = duration % 256

        if topic is None:
            topic = self.default_topic

        # make sure the image is oriented the desired way
        if self.orientation == 90:
            rows = self.rotate_right(rows)
        if self.orientation == 180:
            rows = self.rotate_right(self.rotate_right(rows))
        if self.orientation == 270:
            rows = self.rotate_left(rows)

        for idx, row in enumerate(rows):
            row_bytes.append(int(hex(int(row, 2)), 16))

        if self.is_connected == 1:
            if self.protocol == "BLE":
                command = bytearray([packet_size, command_id, payload_size, self.action_id, module_id,
                                     row_bytes[0], row_bytes[1], row_bytes[2], row_bytes[3], row_bytes[4],
                                     row_bytes[5], row_bytes[6], row_bytes[7], time_h, time_l])
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, self.action_id, module_id,
                                                  row_bytes[0], row_bytes[1], row_bytes[2], row_bytes[3], row_bytes[4],
                                                  row_bytes[5], row_bytes[6], row_bytes[7], time_h, time_l])
                self.MQTT.publish(topic, command)
                return
        print(self.name + " is NOT Connected!")

    def list_to_bytes(self, rows):
        output = []
        for row in rows:
            byte = ''
            for bit in row:
                byte += bit
            output.append(byte)
        return output

    def rotate_right(self, rows):
        list_rows = []
        for r in rows:
            list_rows.append(list(r))
        new_rows = [['0' for i in range(8)] for j in range(8)]
        #  Apply Left Right Transformation
        for idx, row in enumerate(list_rows):
            for idy, bit in enumerate(row):
                new_rows[idy][7 - idx] = bit
        output = self.list_to_bytes(new_rows)
        return output

    def rotate_left(self, rows):
        list_rows = []
        for r in rows:
            list_rows.append(list(r))
        new_rows = [['0' for i in range(8)] for j in range(8)]
        #  Apply Left Turn Transformation
        for idx, row in enumerate(list_rows):
            for idy, bit in enumerate(row):
                new_rows[7 - idy][idx] = bit
        output = self.list_to_bytes(new_rows)
        return output

    def flip_y(self, rows):
        list_rows = []
        for r in rows:
            list_rows.append(list(r))
        new_rows = [['0' for i in range(8)] for j in range(8)]
        #  Apply Flip in Y axis Turn Transformation
        for idx, row in enumerate(list_rows):
            for idy, bit in enumerate(row):
                new_rows[7 - idx][idy] = bit
        output = self.list_to_bytes(new_rows)
        return output

    def flip_x(self, rows):
        list_rows = []
        for r in rows:
            list_rows.append(list(r))
        new_rows = [['0' for i in range(8)] for j in range(8)]
        #  Apply Flip in X axis Turn Transformation
        for idx, row in enumerate(list_rows):
            for idy, bit in enumerate(row):
                new_rows[idy][idx] = bit
        output = self.list_to_bytes(new_rows)
        return output

    def action_complete(self, id, cmd_status):
        self.action_status = cmd_status

    def check_action(self):
        value = self.action_status
        if self.action_status is None:
            return False
        self.action_status = None
        return True

