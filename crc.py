#!/usr/bin/env python3
# author snowyang

def crc16(data):
    wcrc = 0
    for i in data:
        c = i
        for _ in range(8):
            treat = c & 0x80
            c <<= 1
            bcrc = (wcrc >> 8) & 0x80
            wcrc <<= 1
            wcrc = wcrc & 0xffff
            if (treat != bcrc):
                wcrc ^= 0x1021
    return wcrc


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], 'rb') as f:
        print('0x%x' % (crc16(f.read())))
