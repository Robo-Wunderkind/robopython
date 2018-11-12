class Matrix(object):

    def __init__(self, name, ble, id_num, action_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self. orientation = 0
        self.action_id = action_id
        self.action_status = None
        self.BLE = ble
        self.display_off = ['00000000',
                            '00000000',
                            '00000000',
                            '00000000',
                            '00000000',
                            '00000000',
                            '00000000',
                            '00000000']

    def set_display(self, rows):   # rows is an 8 element list of 8 bits each as binary strings
        packet_size = 0x0b
        command_id = 0x52
        payload_size = 0x09
        module_id = self.id - 1
        row_bytes = []

        # make sure the image is oriented the desired way
        if self.orientation == 90:
            rows = self.rotate_right(rows)
        if self.orientation == 180:
            rows = self.rotate_right(self.rotate_right(rows))
        if self.orientation == 270:
            rows = self.rotate_left(rows)

        for idx, row in enumerate(rows):
            row_bytes.append(int(hex(int(row, 2)), 16))

        command = bytearray([packet_size, command_id, payload_size, row_bytes[0], row_bytes[1], row_bytes[2],
                             row_bytes[3], row_bytes[4], row_bytes[5], row_bytes[6], row_bytes[7], module_id])
        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            return
        print (self.name + " is NOT Connected!")

    def off(self):
        self.set_display(self.display_off)

    def timed_display(self, rows, duration):
        packet_size = 0x0e
        command_id = 0xA3
        payload_size = 0x0c
        module_id = self.id - 1
        row_bytes = []
        time_h = duration / 256
        time_l = duration % 256

        # make sure the image is oriented the desired way
        if self.orientation == 90:
            rows = self.rotate_right(rows)
        if self.orientation == 180:
            rows = self.rotate_right(self.rotate_right(rows))
        if self.orientation == 270:
            rows = self.rotate_left(rows)

        for idx, row in enumerate(rows):
            row_bytes.append(int(hex(int(row, 2)), 16))

        command = bytearray([packet_size, command_id, payload_size, self.action_id, module_id,
                             row_bytes[0], row_bytes[1], row_bytes[2], row_bytes[3], row_bytes[4],
                             row_bytes[5], row_bytes[6], row_bytes[7], time_h, time_l]
                            )
        if self.is_connected == 1:
            self.BLE.write_to_robo(self.BLE.write_uuid, command)
            return
        print (self.name + " is NOT Connected!")

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

    def action_complete(self, cmd_status):
        self.action_status = cmd_status

    def check_action(self):
        value = self.action_status
        if self.action_status is None:
            return
        self.action_status = None
        return value

