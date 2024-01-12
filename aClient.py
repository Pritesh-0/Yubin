import asyncio
import sys
import pygame
import json
import time
from serialControl import conv


pygame.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

def getPwm():
    pygame.event.get()
    joystick=joysticks[0]
    b1,b2,b3,b4 = joystick.get_axis(0),joystick.get_axis(1),joystick.get_axis(3), joystick.get_axis(4)

    pos = json.dumps({"A1" : conv(b1), "A2" : conv(b2), "A3" : conv(b3), "A4":conv(b4)})
    print(pos)
    return pos

async def read(reader):
    while True:
        #try:
            #async with asyncio.timeout(5):
                #print('r')
                data = await reader.read(100)
                if not data:
                    break

                message = data.decode()
                print(f"Received: {message}")
                sys.stdout.flush()
        #except TimeoutError:
            #print('timeout in read')

async def write(writer):
    while True:
        #try:
            #async with asyncio.timeout(5):
                #print('w')
                message = await asyncio.to_thread(getPwm)


                writer.write(message.encode())
                await writer.drain()
                sys.stdout.flush()
                time.sleep(0.2)
        #except TimeoutError:
            #print('timeout in write')
        
        #await asyncio.sleep(1)

async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    try:
        task_read = asyncio.create_task(read(reader))
        task_write = asyncio.create_task(write(writer))

        await asyncio.gather(task_read, task_write)
    finally:
        writer.close()
        await writer.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())

