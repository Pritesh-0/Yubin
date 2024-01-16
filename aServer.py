import asyncio
import sys
import serial
import pickle
import time
from canSR import build, disect
from DFr import slcan

fpv=0
can_toggle=1
def sendCan(data): 
    global can_toggle
    data = pickle.loads(data)
    #print(data)
    pwm=list(map(int,[data["pwm1"],data["pwm2"],data["pwm3"],data["pwm4"]]))
    button=list(map(int,[data['b1'],data['b2'],data['b3'],data['b4'],data['b5']]))
    stop,start=int(data["stop"]),int(data["start"])
    astro=[0,0]
    motors=[10,11,15,16]
    astro_motor=[25,26]

    if stop ==1:
        df.stop()
        can_toggle=0
        print("Stop")
    if start==1:
        df.start()
        can_toggle=1
        print("Start")

    if can_toggle==1:
        if button[4]==1:
            global fpv
            fpvmsg = build(500,0,40,fpv%4)
            fpv+=1
            #print(fpvmsg)
            df.write(fpvmsg)

        for i in range(4):
            msg=build(can_id,pwm[i],10,motors[i])
            #print(msg)
            df.write(msg)
    
        if button[0]==1:
            astro[0]=2
        elif button[2]==1:
            astro[0]=1

        if button[1]==1:
            astro[1]=2
        elif button[3]==1:
            astro[1]=1
        for i in range(2):
            msg=build(400,astro[i],10,astro_motor[i])
            df.write(msg)
        
    print(df.write_buff)
    #time.sleep(1)

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
            response = await asyncio.to_thread(input)
            writer.write(response.encode())
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
    
    df=slcan(interface,10)
    
    asyncio.run(main())

