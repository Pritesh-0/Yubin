import can
import sys
import struct

interface = sys.argv[1]

#print(interface)

#bus = can.Bus(interface = 'socketcan',channel = interface)
    
def build(can_id, data):
    dlc = len(data)

    frame = can.Message(
            arbitration_id = can_id, 
            is_extended_id = True,
            data = data,
            dlc = dlc,
            )
    return frame


def disect(frame):
    can_id,dlc,data = hex(frame.arbitration_id), frame.dlc, list(frame.data)
    print('can_id: ',can_id)
    print('dlc: ',dlc)
    print('pwm: ', data)

ids={
        'lattepanda':0x100,
        'gripper_arm':0x200,
        'bio_arm':0x300,
        'astro_assist':0x400,
        'fpv':0x500,
        }

with can.Bus(interface = 'socketcan',channel = interface, receive_own_messages = True) as bus:

    msg = build(0x300,[15,20,00,00,10,11])
    
    disect(msg)
    bus.send(msg)




