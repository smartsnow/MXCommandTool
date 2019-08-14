#!/usr/bin/env python3
# author snowyang

import time
import threading
import hci

if __name__ == "__main__":

    def on_event(evt, val):
        if evt == 'resume':
            print('[Event][Comport resumed] port=%d'%val)
        elif evt == 'close':
            print('[Error][Comport closed] reason=%d'%val)
        elif evt == 'lost':
            print('[Error][Sent data failed] seq=%d'%val)
        elif evt == 'timeout':
            print('[Warning][Send data timeout] seq=%d, retry=%d'%(val[0], val[1]))
        elif evt == 'crcerror':
            print('[Warning][Frame CRC error] type=%d, seq=%d, crc=%d, crccal=%d'%(val[0], val[1], val[2], val[3]))
        elif evt == 'ackoos':
            print('[Warning][ACK Out Of Sequence] seq=%d'%val)

    hci = hci.Hci(on_event)

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

    def send_thread():
        while True:
            data = input()
            hci.write(data.encode())
    send_th = threading.Thread(target=send_thread, daemon=True)
    send_th.start()

    def recv_thread():
        while True:
            data = hci.read()
            print('[Data]',data.decode())
    recv_th = threading.Thread(target=recv_thread, daemon=True)
    recv_th.start()

    print('\nyou can input data at any time\n')

    while True:
        time.sleep(10)