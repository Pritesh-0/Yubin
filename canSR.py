import can
import sys
import struct

    
def build(can_id, pwm, ID,motor):

    data = pwm.to_bytes(4,'little') + ID.to_bytes(1,'little') + motor.to_bytes(1,'little')
    dlc = len(data)
    
    pd=''
    for i in range(6):
        pd+="{:02X}".format(data[i])
    frame=bytes('T','utf-8')+bytes('00000'+str(can_id),'utf-8')+bytes(str(dlc),'utf-8')+bytes(pd,'utf-8')+bytes('\r\n','utf-8')
    return frame


def disect(frame):
    #frame = frame.decode()
    can_id ,dlc, data = frame[1:9], frame[9:10], frame[10:22]
    print('can_id: ',can_id)
    print('dlc: ',dlc)
    print('pwm: ', int.from_bytes(bytes(data[:4]),'little'))
    print('Id: ', data[4])
    print('Motor_no: ',data[5])

ids={
        'lattepanda':0x100,
        'gripper_arm':0x200,
        'bio_arm':0x300,
        'astro_assist':0x400,
        'fpv':0x500,
        }

#if __name__ == '__main__':
        #msg = build(0x100,0102030405,10,11)
        #print(msg)
        #disect(msg)




