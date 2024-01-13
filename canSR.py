import can
import sys
import struct



#print(interface)

#bus = can.Bus(interface = 'socketcan',channel = interface)
    
def build(can_id, pwm, ID,motor):

    data = pwm.to_bytes(4,'little') + ID.to_bytes(1,'little') + motor.to_bytes(1,'little')
    dlc = len(data)
    
    pd=''
    for i in range(6):
        pd+="{:02X}".format(data[i])
    frame=bytes('T','utf-8')+bytes('00000'+str(can_id),'utf-8')+bytes(str(dlc),'utf-8')+bytes(pd,'utf-8')+bytes('\r\n','utf-8')
    #frame = can.Message(
    #       arbitration_id = can_id, 
    #      is_extended_id = True,
    #       data = data,
    #      dlc = dlc,
    #      )
    return frame


def disect(frame):
    can_id,dlc,data = hex(frame.arbitration_id), frame.dlc, frame.data
    print('can_id: ',can_id)
    print('dlc: ',dlc)
    print('pwm: ', int.from_bytes(bytes(data[:4]),'big'))
    print('Id: ', data[4])
    print('Motor_no: ',data[5])

ids={
        'lattepanda':0x100,
        'gripper_arm':0x200,
        'bio_arm':0x300,
        'astro_assist':0x400,
        'fpv':0x500,
        }

if __name__ == '__main__':
    with can.Bus(interface = 'socketcan',channel = interface, receive_own_messages = True) as bus:
        msg = build(0x300,15200000,10,11)
    
        disect(msg)
        bus.send(msg)




