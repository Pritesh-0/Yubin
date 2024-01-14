import asyncio
import sys
import json
import can
import serial
import pickle
import time
from canSR import build, disect

fpv=0
def sendCan(data): 
    data = pickle.loads(data)
    #print(data)
    pwm=list(map(int,[data["pwm1"],data["pwm2"],data["pwm3"],data["pwm4"]]))
    button=list(map(int,[data['b1'],data['b2'],data['b3'],data['b4'],data['b5']]))
    astro=[0,0]
    motors=[10,11,12,13]
    astro_motor=[25,26]
    
    if button[4]==1:
        global fpv
        fpvmsg = build(500,0,40,fpv%4)
        fpv+=1
        #print(fpvmsg)
        #sob.write(fpvmsg)

    for i in range(4):
        msg=build(can_id,pwm[i],10,motors[i])
        #print(msg)
        #sob.write(msg)
    
    if button[0]==1:
        astro[0]=2
    elif button[2]==1:
        astro[0]=1

    if button[1]==1:
        astro[1]=2
    elif button[3]==1:
        astro[1]=1
    for i in range(2):
        msg=build(can_id,astro[i],10,astro_motor[i])
        print(msg)
        #sob.write(msg)


async def handle_client(reader, writer):

    async def read():
        while True:
            #try:
                #async with asyncio.timeout(5):
                    #print('r')
                    data = await reader.read(100000)
                    if not data:
                        break
                    #message = pickle.loads(data)
                    #print(message)
                    #message = data.decode()
                    sendCan(data)
                    #print(f"Received: {message}")
                    sys.stdout.flush()
            #except TimeoutError:
                #print('timeout in read')

    async def write():
        while True:
            #try:
                #async with asyncio.timeout(5):
                    #print('w')
                    response = await asyncio.to_thread(input,"enter message: ")

                    writer.write(response.encode())
                    await writer.drain()
                    sys.stdout.flush()
            #except TimeoutError:
                #print('timeout in write')


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
    #bus = can.Bus(interface = 'socketcan',channel = interface, receive_own_messages = True)
    sob=serial.Serial(
        port='/dev/ttyACM'+str(interface),
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
        )
    sob.write(bytes('h\r\n','utf-8'))
    time.sleep(1)
    sob.write(bytes('S4\r\n','utf-8'))
    time.sleep(1)
    sob.write(bytes('O\r\n','utf-8'))
    
    asyncio.run(main())

