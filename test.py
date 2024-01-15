import can
import sys

interface = sys.argv[1]

#print(interface)

with can.Bus(interface = 'socketcan',channel = interface , receive_own_messages = True) as bus:
    while True:

        msg = bus.recv()
        if msg:
            print(msg)
