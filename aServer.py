import asyncio
import sys
import json
import can
from canSR import build, disect

interface = sys.argv[1]
bus = can.Bus(interface = 'socketcan',channel = interface, receive_own_messages = True)
def sendCan(data):
    data = json.loads(data)
    pwm1,pwm2,pwm3,pwm4=data['A1'],data['A2'],data['A3'],data['A4']
    msg1=build(0x300,pwm1,10,10)
    bus.send(msg1)
    msg2=build(0x300,pwm2,10,11)
    bus.send(msg2)
    msg3=build(0x300,pwm3,10,12)
    bus.send(msg3)
    #msg4=build(0x300,pwm4,10,13)
    #bus.send(msg4)


async def handle_client(reader, writer):

    async def read():
        while True:
            #try:
                #async with asyncio.timeout(5):
                    #print('r')
                    data = await reader.read(100)
                    if not data:
                        break

                    message = data.decode()
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

