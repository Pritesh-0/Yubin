import asyncio
import sys
import pygame
import time
import pickle
from canSR import disect

def conv(v):

    v=int(v*10000)
    vs=float(v-(10000))/float(20000)
    val = 1920000 + int(vs*800000)
    return val

def getValues(data):
    data=pickle.loads(data)
    dlc=data['dlc']
    pwm=data['pwm']
    sid=data['Id']
    mot_num=data['Motor_no']
    #print(data)
    print(mot_num,pwm)



def getPwm():
    pygame.event.get()
    joystick=joysticks[0]

    ax = [conv(joystick.get_axis(i)) for i in range(6)]
    btn = [joystick.get_button(i) for i in range(8)]
    pos = pickle.dumps({"axis" : ax, "btn" : btn})
    return pos

async def read(reader):
    while True:
        data = await reader.read(1000)
        if not data:
            break
        
        getValues(data)
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

