import asyncio
import sys
import pygame
import time
import pickle

def conv(v):

    v=int(v*10000)
    vs=float(v-(10000))/float(20000)
    val = 1920000 + int(vs*800000)
    return str(val)

def getPwm():
    pygame.event.get()
    joystick=joysticks[0]

    a1,a2,a3,a4 = joystick.get_axis(0),joystick.get_axis(1),joystick.get_axis(3), joystick.get_axis(4)
    b1,b2,b3,b4,b5 = joystick.get_button(0), joystick.get_button(1), joystick.get_button(2), joystick.get_button(3), joystick.get_button(4)
    
    stop,start=joystick.get_button(6), joystick.get_button(7)
    pos = pickle.dumps({"pwm1" : conv(a1), "pwm2" : conv(a2), "pwm3" : conv(a3), "pwm4" : conv(a4), "b1" : str(b1), "b2":str(b2),"b3":str(b3),"b4":str(b4),"b5":str(b5),"stop":str(stop), "start":str(start)})
    #print(pos)
    return pos

async def read(reader):
    while True:
        data = await reader.read(1000)
        if not data:
            break

        message = data.decode()
        #print(f"Received: {message}")
        sys.stdout.flush()

async def write(writer):
    while True:
        message = await asyncio.to_thread(getPwm)
        writer.write(message)
        await writer.drain()
        sys.stdout.flush()
        time.sleep(0.02)


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
    pygame.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    asyncio.run(main())

