import asyncio
import sys
import json
import can
from canSR import build, disect

cid={'idmo':0x200,'bio':0x300}
interface = sys.argv[1]
can_id = cid[sys.argv[2]]
#bus = can.Bus(interface = 'socketcan',channel = interface, receive_own_messages = True)
def sendCan(data): 
    data = json.loads(data)
    #print(data)
    pwm=list(map(int,[data["pwm1"],data["pwm2"],data["pwm3"],data["pwm4"]]))
    button=list(map(int,[data['b1'],data['b2'],data['b3'],data['b4'],data['b5']]))
    motors=[10,11,12,13]
    for i in range(4):
        msg=build(can_id,pwm[i],10,motors[i])
        print(msg)


async def handle_client(reader, writer):

    async def read():
        while True:
            #try:
                #async with asyncio.timeout(5):
                    #print('r')
                    data = await reader.read(1000)
                    if not data:
                        break
                    message = data.decode('utf-8')
                    sendCan(message)
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
    asyncio.run(main())

