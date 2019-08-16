#!/usr/bin/env python3
# author snowyang

import serial
import threading
import queue
import time
import slip
import crc

HCI_DATA = 0x00
HCI_ACK = 0x01


class Hci():

    def __init__(self, on_event):
        self.slip = slip.Slip()
        self.send_seq = 0
        self.recv_seq = -1
        self.send_q = queue.Queue()
        self.recv_q = queue.Queue()
        self.on_event = on_event
        self.forceThreadExit = False

    def write(self, _data):
        self.send_q.put(_data)

    def read(self):
        return self.recv_q.get()

    def daemon(self):
        # it's a daemon thread, only it has the right to access comport.
        # user's operation is pushed into queue, poped by this thread
        # and is excuted one-by-one.
        while True:
            try:
                # do send
                if self.send_q.qsize() > 0:
                    self.output(self.send_q.get())
                # do recv
                self.yield_until(HCI_DATA, 10)
                if self.forceThreadExit == True:
                    break
            except serial.SerialException as e:
                self.slip.close()
                self.on_event("serial", e)
                break

    def open(self, comport):
        self.slip.open(comport)
        self.th = threading.Thread(target=self.daemon, daemon=True)
        self.th.start()

    def close(self):
        self.forceThreadExit = True
        self.th.join()
        self.forceThreadExit = False
        self.slip.close()

    def send_data(self, frame, retry):
        retry = 3
        while retry > 0:
            self.slip.write(frame)
            if self.yield_until(HCI_ACK, 100) == True:
                # got ack, break from loop
                self.on_event("sent", self.send_seq)
                return
            # no ack after timeout, retry
            self.on_event('timeout', (self.send_seq, retry))
            retry -= 1
        self.on_event("lost", self.send_seq)

    def output(self, _data):
        # packed _data to hci frame and send it
        frame = HCI_DATA.to_bytes(1, 'big') + \
            self.send_seq.to_bytes(1, 'big') + _data
        frame += crc.crc16(frame).to_bytes(2, 'big')
        self.send_data(frame, retry=3)
        self.send_seq = 0 if self.send_seq >= 0xFF else self.send_seq + 1

    def send_ack(self, seq):
        frame = HCI_ACK.to_bytes(1, 'big') + seq.to_bytes(1, 'big')
        frame += crc.crc16(frame).to_bytes(2, 'big')
        self.slip.write(frame)

    def yield_until(self, expect_type, timeout):
        while timeout > 0:
            # sleep 10ms
            time.sleep(0.01)
            timeout -= 10

            # try get a frame
            frame = self.slip.read()
            # no frame, continue
            if frame == b'':
                continue

            # got a frame
            # cut type, seq, data and crc from frame
            _type, _seq, _data, _crc = frame[0], frame[1], frame[2:-2], frame[-2:]
            # check crc
            crcval = int.from_bytes(_crc, 'big')
            crccal = crc.crc16(frame[:-2])
            # crc error, continue
            if crccal != crcval:
                self.on_event("crcerror", (_type, _seq, crcval, crccal))
                continue

            # dispatch frame
            if _type == HCI_DATA:
                # send ack
                self.send_ack(_seq)
                # drop duplicate data, continue
                if self.recv_seq == _seq:
                    continue
                # push data to queue, update recved sequence
                self.recv_q.put(_data)
                self.recv_seq = _seq
            else:
                # ack is not for last sent data, continue
                if _seq != self.send_seq:
                    self.on_event("ackoos", _seq)
                    continue

            # return true if we got a expect type
            if _type == expect_type:
                return True

        # return false if timeout
        return False


if __name__ == "__main__":

    def on_event(evt, e):
        print('event=%s, value=%s' % (evt, e))
    hci = Hci(on_event)

    # get comport list for user select
    portlist = hci.slip.portlist()
    if len(portlist) == 0:
        print('no comport, exit')
        exit(0)
    print("\ncomport list")
    for i, port in enumerate(portlist):
        print(" %d: %s" % (i, port))
    i = int(input('\nplease select a comport number: '))
    comport = portlist[i]
    print('comport "%s" is selected' % comport)

    hci.open(comport)

    hci.write(b'Hello world')

    while True:
        _data = hci.read()
        print('recv: %s' % _data)
        hci.write(_data)

    input('press any key to exit: \n')
