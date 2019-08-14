#!/usr/bin/env python3
# author snowyang

import serial
import serial.tools.list_ports

START       = b'\xC0'
END         = b'\xD0'
ESC         = b'\xDB'
START_ESC   = b'\xDB\xDC'
END_ESC     = b'\xDB\xDE'
ESC_ESC     = b'\xDB\xDD'

MIN_LEN = 4
MAX_LEN = 1028

class Slip():

    def __init__(self):
        self.serial = serial.Serial(baudrate=115200, timeout=0)
        self.recvbuf = b''
        self.i_st = -1

    def portlist(self):
        return [comport.device for comport in serial.tools.list_ports.comports()]

    def open(self, port):
        self.serial.port = port
        self.serial.open()

    def close(self):
        self.serial.close()

    # return one hci frame, otherwise b''.
    # non-blocking
    # shoule be called periodically
    def read(self):
        # recv bytes, put into buffer
        recvbytes = self.serial.read(MAX_LEN)
        self.recvbuf += recvbytes

        # no start, find it
        if self.i_st == -1:
            self.i_st = self.recvbuf.find(START)
            if self.i_st == -1:
                return b''

        # with start, find end
        i_ed = self.recvbuf.find(END)
        if i_ed == -1:
            return b''
        
        # cut hci frame from recv buffer
        hcibuf = self.recvbuf[self.i_st+1:i_ed]
        # example: | start | ... | start | ... | end |
        i_st_r = hcibuf.rfind(START)
        if i_st_r != -1:
            hcibuf = hcibuf[i_st_r+1:]

        # clear resources
        self.i_st = -1
        self.recvbuf = self.recvbuf[i_ed+1:]

        # invalid length, drop it
        n = len(hcibuf)
        if n < MIN_LEN or n > MAX_LEN:
            return b''
        
        frame = hcibuf.replace(START_ESC, START).replace(END_ESC, END).replace(ESC_ESC, ESC)
        # return hci frame
        return frame

    # wrap data with start and end, send it
    def write(self, frame):
        hcibuf = frame.replace(ESC, ESC_ESC).replace(START, START_ESC).replace(END, END_ESC)
        self.serial.write(START + hcibuf + END)

    
if __name__ == "__main__":

    # unit test
    import time

    slip = Slip()

    # get comport list for user select
    portlist = slip.portlist()
    if len(portlist) == 0:
        print('no comport, exit')
        exit(0)
    print("\ncomport list")
    for i, port in enumerate(portlist):
        print(" %d: %s"%(i, port))
    i = int(input('\nplease select a comport number: '))
    comport = portlist[i]
    print('comport "%s" is selected'%comport)
    slip.open(comport)

    # | START | ... | END |
    print('')
    rawbytes = START+b'HELLOWORLD'+END
    slip.serial.write(rawbytes)
    print('raw bytes: %s'%rawbytes)
    time.sleep(0.01)
    print('hci frame: %s'%slip.read())

    # | START | ... | END | START | ... | END |
    print('')
    rawbytes = START+b'HELLO'+END+START+b'WORLD'+END
    slip.serial.write(rawbytes)
    print("raw bytes: %s"%rawbytes)
    time.sleep(0.01)
    print('hci frame: %s'%slip.read())
    print('hci frame: %s'%slip.read())

    # | START | ... | START | ... | END |
    print('')
    rawbytes = START+b'HELLO'+ START+b'WORLD'+END
    slip.serial.write(rawbytes)
    print("raw bytes: %s"%rawbytes)
    time.sleep(0.01)
    print('hci frame: %s'%slip.read())

    # | START | ... 
    print('')
    rawbytes = START+b'HELLO'
    slip.serial.write(rawbytes)
    print("raw bytes: %s"%rawbytes)
    time.sleep(0.01)
    print('hci frame: %s'%slip.read())
    # ... | END |
    rawbytes = b'WORLD'+END
    slip.serial.write(rawbytes)
    print("raw bytes: %s"%rawbytes)
    time.sleep(0.01)
    print('hci frame: %s'%slip.read())

    slip.close()