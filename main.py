import serial

import random

def get_random_hex_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color_hex = (r << 16) | (g << 8) | b
    return (color_hex >> 8) & 0xFF, color_hex & 0xFF

def createCommandBody(my_type: int, amount: int = None):
    # Added type into the request body(1st one byte)
    print(type(my_type))
    res = bytearray([my_type, ])
    print(res)

    if my_type == 1:
        #Vendista takes penny
        amount *= 10

        # Adding 4 bytes of the amount to the request
        byte1 = (amount >> 24) & 0xFF
        byte2 = (amount >> 16) & 0xFF
        byte3 = (amount >> 8) & 0xFF
        byte4 = amount & 0xFF

        res.append(byte4)
        res.append(byte3)
        res.append(byte2)
        res.append(byte1)
        # res.append(f"0x{byte1:02X}")

        res.append(0x06)
        res.append(0x43)
        import time

        # Adding 4 bytes of UNIX time to the request
        unix_time = int(time.time())
        print(unix_time)

        # Convert Unix time to 4 bytes in 0x00 format
        ubyte1 = (unix_time >> 24) & 0xFF
        ubyte2 = (unix_time >> 16) & 0xFF
        ubyte3 = (unix_time >> 8) & 0xFF
        ubyte4 = unix_time & 0xFF
        print(f"0x{byte1:02X} 0x{byte2:02X} 0x{byte3:02X} 0x{byte4:02X}")
        res.append(ubyte4)
        res.append(ubyte3)
        res.append(ubyte2)
        res.append(ubyte1)

        # Adding a 1 byte to use GSM channel
        res.append(0x01)
        return res

    elif my_type == 9:
        color = get_random_hex_color()
        res.append(color[0])
        res.append(color[1])
        return res




def createCommand(body, size):
    crcTable = [0] * 256

    def MakeCRC16Table():
        for s in range(256):
            r = s << 8
            for s1 in range(8):
                if r & (1 << 15):
                    r = (r << 1) ^ 0x8005
                else:
                    r = r << 1
            crcTable[s] = r

    def GetCRC16(buf, length):
        crc = 0xFFFF
        for i in range(length):
            crc = crcTable[((crc >> 8) ^ buf[i]) & 0xFF] ^ (crc << 8)
        crc ^= 0xFFFF
        return crc
    MakeCRC16Table()
    crc = GetCRC16(body, size)
    byte1 = (crc >> 8) & 0xFF
    byte2 = crc & 0xFF

    command = bytearray([size, byte2, byte1])
    command += body
    # command = b"".join([command, body])
    return command


def createTransactionSlave(inst_type, amount, body_len):


    port = '/dev/ttyUSB0'
    baud_rate = 115200
    data_bits = 8
    stop_bits = 1
    parity = serial.PARITY_NONE

    ser = serial.Serial(port, baud_rate, bytesize=data_bits,
                        stopbits=stop_bits, parity=parity)
    command = createCommand(createCommandBody(inst_type, amount), body_len)
    ser.write(command)
    ser.close()


if __name__ == '__main__':
    my_type = 9
    amount = 1
    body_len = 3
    #print(createCommand(createCommandBody(my_type), body_len))

    createTransactionSlave(my_type, amount, body_len)
