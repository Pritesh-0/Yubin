
import sys
import struct

    
def build(can_id, pwm, ID,motor):

    data = pwm.to_bytes(4,'little') + ID.to_bytes(1,'little') + motor.to_bytes(1,'little')
    dlc = len(data)
    
    pd=''
    for i in range(6):
        pd+="{:02X}".format(data[i])
    #frame = 'T00000'+str(can_id)+str(dlc)+pd
    frame=bytes('T','utf-8')+bytes('00000'+str(can_id),'utf-8')+bytes(str(dlc),'utf-8')+bytes(pd,'utf-8')+bytes('\r\n','utf-8')
    return frame


def disect(frame):
    #frame = frame.decode()
    can_id ,dlc, data = frame[1:9], frame[9:10], frame[10:22]
    print('can_id: ',int(can_id.decode('utf-8')))
    print('dlc: ',dlc.decode('utf-8'))
    #print(data[4].decode('utf-8'))
    pwm=data[:8]
    print('pwm: ', int(''.join([x.decode('utf-8') for x in [pwm[6:],pwm[4:6],pwm[2:4],pwm[:2]]]),16))
    print('Id: ', int(data[8:10].decode('utf-8'),16))
    print('Motor_no: ',int(data[10:12].decode('utf-8'),16))

ids={
        'lattepanda':0x100,
        'gripper_arm':0x200,
        'bio_arm':0x300,
        'astro_assist':0x400,
        'fpv':0x500,
        }

if __name__ == '__main__':
        #msg = build(0x100,0102030405,10,11)
        f=b'T0000010066C1700001E05'
        #print(msg)
        disect(f)




