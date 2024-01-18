import asyncio
import sys
import serial
import pickle
import time
from canSR import build, disect

fpv=0
can_toggle=1

pv=[1520000]*4
fpvp = 0

def getSensor():
    ch=sob.read()
    if ch==b'T':
        frame=sob.read(22)
        fd=disect(frame)
        fd = pickle.dumps(fd)
        return fd
    else:
        return b''


def sendCan(data): 
    global can_toggle
    global fpv
    global fpvp
    data = pickle.loads(data)
    pwm=data["axis"]
    button=data["btn"]
    hat=data["hat"]
    px,py=hat[0],hat[1]
    joint=[pwm[1],pwm[4]]
    astro=[0,0]
    motors=[10,11,15,16]
    astro_motor=[25,26]
    ypr_motor=[20,21]

    if button[6]==1:
        sob.write(bytes('C\r\n','utf-8'))
        can_toggle=0
        print("Stop")
    if button[7]==1:
        sob.write(bytes('O\r\n','utf-8'))
        can_toggle=1
        print("Start")

    if can_toggle==1:
        if button[4]==1:
            if fpvp == 0:
                fpvp=1
                fpvmsg = build(500,0,40,fpv%4)
                fpv+=1
                print(fpvmsg)
                sob.write(fpvmsg)
            elif fpvp == 1:
                fpvp=0
            time.sleep(0.5)

        for i in range(2):
            if joint[i]!=pv[i]:
                msg=build(can_id,joint[i],10,motors[i])
                print(msg)
                sob.write(msg)
                #time.sleep(0.2)
    
        if button[0]==1:
            astro[0]=2
        elif button[2]==1:
            astro[0]=1

        if button[1]==1:
            astro[1]=2
        elif button[3]==1:
            astro[1]=1
        for i in range(2):
            if astro[i]!=0:
                msg=build(400,astro[i],10,astro_motor[i])
                print(msg)
                sob.write(msg)
                #time.sleep(0.2)

        if can_id==200:
            if px==1:
                msg=build(can_id,1,10,20)
                print(msg)
                sob.write(msg)
            if px==-1:
                msg=build(can_id,2,10,20)
                print(msg)
                sob.write(msg)
            if py==1:
                msg=build(can_id,1,10,21)
                print(msg)
                sob.write(msg)
            if py==-1:
                msg=build(can_id,2,10,21)
                print(msg)
                sob.write(msg)



async def handle_client(reader, writer):

    async def read():
        while True:
            data = await reader.read(100000)
            if not data:
                break
            sendCan(data)
            sys.stdout.flush()

    async def write():
        while True:
            response = await asyncio.to_thread(getSensor)
            writer.write(response)
            await writer.drain()
            sys.stdout.flush()

    try:
        task_read = asyncio.create_task(read())
        task_write = asyncio.create_task(write())
       
    
        await asyncio.gather(task_read, task_write)
    finally:
        writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888
    )

    addr = server.sockets[0].getsockname()

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    cid={'idmo':200,'bio':300}
    interface = sys.argv[1]
    can_id = cid[sys.argv[2]]
    sob=serial.Serial(
        port='/dev/ttyACM'+str(interface),
        #port= '/dev/pts/5',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
        )
    #sob.write(bytes('h\r\n','utf-8'))
    #time.sleep(1)
    sob.write(bytes('S7\r\n','utf-8'))
    time.sleep(1)
    sob.write(bytes('O\r\n','utf-8'))
    
    asyncio.run(main())

